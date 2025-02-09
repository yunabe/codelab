using Microsoft.VisualStudio.TestTools.UnitTesting;
using MyLibrary;

namespace MyLibrary.Tests;

[TestClass]
public class GreeterTests
{
    [TestMethod]
    public void Greet_ReturnsCorrectGreeting()
    {
        // Arrange
        var name = "World";
        var expectedGreeting = "Hello, World";

        // Act
        var result = Greeter.Greet(name);

        // Assert
        Assert.AreEqual(expectedGreeting, result);
    }
}
