using Microsoft.VisualStudio.TestTools.UnitTesting;
using CliApp1;

namespace CliApp1.Tests;

[TestClass]
public sealed class MathUtilsTests
{
    [TestMethod]
    public void Fib_ReturnsCorrectValue()
    {
        // Act
        var result = MathUtils.Fib(5);

        // Assert
        Assert.AreEqual(5, result);
    }
}
