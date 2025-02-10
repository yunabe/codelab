using CliApp1;
using MyLibrary;

// See https://aka.ms/new-console-template for more information
var name = args.Length > 0 ? args[0] : "World";
Console.WriteLine(Greeter.Greet(name));

var n = 40;
Console.WriteLine($"Fib({n}) = {MathUtils.Fib(n)}");
