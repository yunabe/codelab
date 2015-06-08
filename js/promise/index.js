
var getUser = function(name, callback) {
  user = null;
  if (name == 'alice') {
    user = {
      name: 'alice',
      id: 0
    }
  }
  setTimeout(function() {
    callback(user);
  }, 0);
};

var getUserCompany = function(user, callback) {
  company = null;
  if (user.id == 0) {
    company = {
      id: 0,
      name: 'Apple'
    };
  }
  setTimeout(function() {
    callback(company);
  }, 0);
};

var promiseGetUser = function(name) {
  return new Promise(function(resolve, reject) {
    getUser(name, function(user) {
      if (user == null) {
	reject("User Not Found");
      } else {
	resolve(user);
      }
    });
  });
};


var promiseGetUserCompany = function(user) {
  return new Promise(function(resolve, reject) {
    getUserCompany(user, function(company) {
      if (company == null) {
	reject("Company Not Found");
      } else {
	resolve(company);
      }
    });
  });
};

var main = function() {
  promiseGetUser('alice')
      .then(promiseGetUserCompany)
      .then(function(company) {
	console.log('Alice company:', company.name);
	});
};

main();
