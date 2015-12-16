class HelloWorld {
  constructor(name) {
    this.name = name || 'World';
  }
}

exports.helloWorld = function(name) {
  var hello = new HelloWorld(name);
  return 'Hello ' + hello.name + '!';
};
