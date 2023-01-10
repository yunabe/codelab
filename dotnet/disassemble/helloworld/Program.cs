namespace helloworld;
class Program
{
    private static long NaiveFib(long n) {
        if (n <= 1) {
            return n;
        }
        return NaiveFib(n - 1) + NaiveFib(n - 2);
    }
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
        long n = 40;
        Console.WriteLine("NaiveFib({0}) = {1}", n, NaiveFib(n));
    }
}
