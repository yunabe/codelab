using Microsoft.VisualStudio.TestTools.UnitTesting;
using MyLibrary;
using System.Collections.Generic;

namespace MyLibrary.Tests
{
    [TestClass]
    public class StatisticsUtilsTests
    {
        [TestMethod]
        public void ComputeStandardDeviation_ReturnsCorrectValue()
        {
            // Arrange
            var values = new List<float> { 1.0f, 2.0f, 3.0f, 4.0f, 5.0f };

            // Act
            var result = StatisticsUtils.ComputeStandardDeviation(values);

            // Assert
            Assert.AreEqual(1.5811, result, 0.0001);
        }
    }
}