namespace cs_codelab;
class Program
{
    static void PlayWithBasicValues()
    {
        // You cannot omit ";".
        int a = 12;
        double b = 3.4;
        Console.WriteLine(a + b);
        a += 1;
        Console.WriteLine(a + b);

        // This is invalid. const is compile-time constant.
        // const int c = a * 2;
        //
        // C# does not support a final local variable in Java?
        // https://stackoverflow.com/questions/1327544/what-is-the-equivalent-of-javas-final-in-c#comment1161857_1327549

        {
            // This is invalid.
            // double a = 34;
            //
            // C# does not allow hiding a reference with a new variable in the
            // inner scope.
        }

        // C# 3.0
        var name = "world";
        Console.WriteLine(string.Format("Hello, {0}!", name));
        // This is int!
        var vint = 2;
        // This is double!
        var vdb = 2.0;
        // v/vint = 0, 1/vdb = 0.5.
        // C# converts int to double implicitly, unlike Go.
        Console.WriteLine(string.Format("1/vint = {0}, 1/vdb = {1}", 1 / vint, 1 / vdb));
    }

    static void PlayWithControlFlow()
    {
        int a = 10;
        // () is mandatory, {} is optional.
        if (a * 3.4 < 1000)
        {
            Console.WriteLine("a * 3.4 < 1000");
        }
        else
        {
            Console.WriteLine("a * 3.4 >= 1000");
        }

        switch (a)
        {
            case 1:
                Console.WriteLine("a = 1");
                break;
            case 10:
            case 2:
                Console.WriteLine("a = 10 or 2");
                break;
            // C# does not support fallthrough.
            // case 3:
            //    Console.WriteLine("a = 3");
            default:
                break;
        }

        while (a > 0)
        {
            Console.WriteLine("a in while = {0}", a);
            a -= 2;
        }
        for (; a < 5; a++)
        {
            Console.WriteLine("a in for = {0}", a);
        }
    }

    static void PlayWithArrays()
    {
        Console.WriteLine("### PlayWithArrays ###");
        // Zero initialized.
        int[] ar = new int[5];
        for (int i = 0; i < ar.Length; ++i)
        {
            ar[i] = i * i;
        }
        Console.WriteLine("ar = [{0}]", string.Join(", ", ar));
        ar = new int[] { 1, 2, 3, 4, 5 };
        Console.WriteLine("ar = [{0}]", string.Join(", ", ar));

        // C# 8.0
        var sub = ar[1..^1];  // omits the first and the last element
        Console.WriteLine("sub = [{0}]", string.Join(", ", sub));
        // sub is a copy, the assignment to sub does not affect ar.
        sub[1] = 0;
        Console.WriteLine("ar = [{0}], sub = [{1}]", string.Join(", ", ar), string.Join(", ", sub));

        var bb = ^0;
        int cc = -1;
        Console.WriteLine("bb  = {0}, cc = {1}", bb, cc);
    }

    static void Main(string[] args)
    {
        PlayWithBasicValues();
        PlayWithControlFlow();
        PlayWithArrays();
    }
}
