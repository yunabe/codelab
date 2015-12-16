var hello = require('../src/hello.js');

describe("Our data array", function() {
    it("has four items", function() {
        expect('Hello Test!').toBe(hello.helloWorld('Test'));
    });
});
