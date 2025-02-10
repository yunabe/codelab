using MathNet.Numerics.Statistics;

namespace MyLibrary
{
    public static class StatisticsUtils
    {
        public static double ComputeStandardDeviation(List<float> values)
        {
            return Statistics.StandardDeviation(values.Select(v => (double)v));
        }
    }
}