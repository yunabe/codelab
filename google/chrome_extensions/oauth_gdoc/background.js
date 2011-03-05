var DOCLIST_SCOPE = 'https://docs.google.com/feeds';
var DOCLIST_FEED = DOCLIST_SCOPE + '/default/private/full/';

var request = {
  'request_url': 'https://www.google.com/accounts/OAuthGetRequestToken',
  'authorize_url': 'https://www.google.com/accounts/OAuthAuthorizeToken',
  'access_url': 'https://www.google.com/accounts/OAuthGetAccessToken',
  'consumer_key': 'anonymous',
  'consumer_secret': 'anonymous',
  'scope': DOCLIST_SCOPE,
  'app_name': 'Chrome Extension Sample - Accessing Google Docs with OAuth'
};

var oauth = ChromeExOAuth.initBackgroundPage(request);

var processDocListResults = function(response, xhr) {
  if (xhr.status != 200) {
    alert('xhr.status != 200 (' + xhr.status + ')');
    return;
  }

  var data = JSON.parse(response);
  alert(data.feed.entry.length);
};

var loadDocList = function() {
  alert('Ready to fetch private data ...');
  var req = {
    'headers': {'GData-Version': '3.0'},
    'parameters': {
      'alt': 'json',
      'showfolders': 'true'
    }
  };
  oauth.sendSignedRequest(DOCLIST_FEED, processDocListResults, req);  
};

var createFolder = function() {
  var name = prompt('Folder name');
  var body =
  '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
  + '<entry xmlns="http://www.w3.org/2005/Atom">'
  + '<category scheme="http://schemas.google.com/g/2005#kind"'
  + ' term="http://schemas.google.com/docs/2007#folder"/>'
  + '<title>' + name + '</title>'
  + '</entry>';
  var length = String(body.length);
  alert(length);
  var req = {
    'method': 'POST',
    'headers': {'Host': 'docs.google.com',
                'GData-Version': '3.0',
                // 'Content-Length': length,
                'Content-Type': 'application/atom+xml'},
    'parameters': {'alt': 'json'},
    'body': body
  };
  oauth.sendSignedRequest(DOCLIST_FEED, handleCreateFolder, req);
};

var handleCreateFolder = function() {
};

// oauth.authorize(loadDocList);
// oauth.authorize(createFolder);
