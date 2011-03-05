// var FOLDER_NAME = 'chrome_extension_gdoc_oauth_test';
var FOLDER_NAME = 'folder0';

var FILE_NAME = 'example.json';

var CONTENT = 'Hello World!?';

var bgpage = chrome.extension.getBackgroundPage();

var message = function(text) {
  document.getElementById('message').innerHTML = text;
};

var partial = function(fn, var_args) {
  var args = Array.prototype.slice.call(arguments, 1);
  return function() {
    // Prepend the bound arguments to the current arguments.                                                                                                       
    var newArgs = Array.prototype.slice.call(arguments);
    newArgs.unshift.apply(newArgs, args);
    return fn.apply(this, newArgs);
  }
};

var deleteResource(resource_id) {
  var feed = bgpage.DOCLIST_FEED + resource_id.replace(':', '%3A');
  var req = {
    'method': 'DELETE',
    'headers': {
      'GData-Version': '3.0',
      'Host': 'docs.google.com',
      'If-Match': '*',
    },
    'parameters': {
      'delete': 'true'
    }
  };
  bgpage.oauth.sendSignedRequest(feed,
                                 processDeleteResource, req);
};

var processDeleteResource = function(response, xhr) {
  if (xhr.status == 200) {
    message('A resource is deleted.');
  } else {
    message('Failed to delete resource.');
  }
};

var uploadTextFile = function(callback, content, folder_id) {
  message('uploadTextFile');
  var feed = bgpage.DOCLIST_FEED;  
  if (folder_id) {
    feed += folder_id.replace(':', '%3A') + '/contents';
  }
  var req = {
    'method': 'POST',
    'headers': {
      'GData-Version': '3.0',
      'Host': 'docs.google.com',
      'Content-Type': 'text/plain',
      'Slug': FILE_NAME
    },
    'parameters': {
      'alt': 'json',
      'title': FILE_NAME,
    },
    'body': content
  };
  bgpage.oauth.sendSignedRequest(feed,
                                 partial(processUploadTextFile, callback), req);
};

var processUploadTextFile = function(callback, response, xhr) {
  if (xhr.status == 201) {
    message('A file is uploaded successfully.');
    callback();
  } else {
    message('Failed to upload a file.');
  }
};

var findFile = function(callback, folder_id) {
  var req = {
    'headers': {'GData-Version': '3.0'},
    'parameters': {
      'alt': 'json',
      'title': FILE_NAME,
    }
  };
  var feed = bgpage.DOCLIST_FEED;
  if (folder_id) {
    feed += folder_id.replace(':', '%3A') + '/contents';
  }
  bgpage.oauth.sendSignedRequest(feed,
                                 partial(processFindFile, callback), req);
};

var processFindFile = function(callback, response, xhr) {
  message(response);
  var data = JSON.parse(response);
};

var findFolder = function(callback) {
  message('findFolder');
  var req = {
    'headers': {'GData-Version': '3.0'},
    'parameters': {
      'alt': 'json',
      'title': FOLDER_NAME,
      'showfolders': 'true' // It seems like I can remove this flag.
    }
  };
  bgpage.oauth.sendSignedRequest(bgpage.DOCLIST_FEED + '-/folder',
                                 partial(processFindFolder, callback), req);
};

var processFindFolder = function(callback, response, xhr) {
  message('processFindFolder');
  if (xhr.status == 401) {
    bgpage.oauth.clearTokens();
    findFolder();
    return;
  }
  message('processFindFolder 2');
  var data = JSON.parse(response);
  // data.feed.entry is undefined when no folder is found.
  if (data.feed.entry && data.feed.entry.length > 0) {
    callback(data.feed.entry[0]);
  } else {
    callback(null);
  }
};

var showFolderInfo = function(folder) {
  if (!folder) {
    message('No folder. Creating...');
    createFolder(partial(findFolder, showFolderInfo));
    return;
  } else {
    message('The folder already exists: id = ' + folder.gd$resourceId.$t);
    var folder_id = folder.gd$resourceId.$t;
    uploadTextFile(function() {
        findFile(function() {}, folder_id);
      }, 'Hello world!' + new Date(), folder_id);
  }
};

var onCreate = function() {
  message('Authorizing...');
  bgpage.oauth.authorize(partial(findFolder, showFolderInfo));
};

var createFolder = function(callback) {
  var body =
  '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
  + '<entry xmlns="http://www.w3.org/2005/Atom">'
  + '<category scheme="http://schemas.google.com/g/2005#kind"'
  + ' term="http://schemas.google.com/docs/2007#folder"/>'
  + '<title>' + FOLDER_NAME + '</title>'
  + '</entry>';
  var length = String(body.length);
  var req = {
    'method': 'POST',
    'headers': {'Host': 'docs.google.com',
                'GData-Version': '3.0',
                // 'Content-Length': length,
                'Content-Type': 'application/atom+xml'},
    'parameters': {'alt': 'json'},
    'body': body
  };
  message('Sending a request to create a folder...');
  bgpage.oauth.sendSignedRequest(bgpage.DOCLIST_FEED,
                                 partial(handleCreateFolder, callback), req);
};

var handleCreateFolder = function(callback, response, xhr) {
  message('handleCreateFolder:' + xhr.status);
  if (xhr.status == 401) {
    // Authentication error.
    message('Access token might be revoked.');
    bgpage.oauth.clearTokens();
    onCreate();
    return;
  }
  if (xhr.status == 201) {
    callback();
  }
};

var onDelete = function() {
  message('delete');
};
