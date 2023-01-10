// See https://aka.ms/new-console-template for more information

using cil_compiler;
using System.Reflection;
using System.Reflection.Emit;

void Main(string[] args)
{
    // Parse command line arguments
    string inputFile = null;
    string outputFile = null;
    for (int i = 0; i < args.Length; i++)
    {
        if (args[i] == "-input" && i + 1 < args.Length)
        {
            inputFile = args[i + 1];
        }
        else if (args[i] == "-output" && i + 1 < args.Length)
        {
            outputFile = args[i + 1];
        }
    }
    if (inputFile == null || outputFile == null)
    {
        Console.Error.WriteLine("Usage: MyCompiler -input <input_file> -output <output_file>");
        return;
    }
    // Read input file
    string input;
    using (var reader = new StreamReader(inputFile))
    {
        input = reader.ReadToEnd();
    }
    // Lex and parse input
    var lexer = new Lexer(input);
    var parser = new Parser(lexer);
    var ast = parser.Program();
    // Generate CIL instructions
    var assemblyName = Path.GetFileNameWithoutExtension(outputFile);
    var assemblyBuilder = AssemblyBuilder.DefineDynamicAssembly(new AssemblyName(assemblyName), AssemblyBuilderAccess.Save);
    var moduleBuilder = assemblyBuilder.DefineDynamicModule(assemblyName, outputFile);
    var typeBuilder = moduleBuilder.DefineType("Program");
    var methodBuilder = typeBuilder.DefineMethod("Main", MethodAttributes.Public | MethodAttributes.Static, typeof(void), new Type[0]);
    var generator = new InstructionGenerator(typeBuilder, methodBuilder);
    generator.Generate(ast);
    typeBuilder.CreateType();
    assemblyBuilder.SetEntryPoint(methodBuilder);
    assemblyBuilder.Save(outputFile);
}

Main(args);