// See https://aka.ms/new-console-template for more information

using cil_compiler;
using System.Reflection;
using System.Reflection.Metadata.Ecma335;

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
    var builder = new MetadataBuilder();
    var moduleBuilder = builder.AddModule(assemblyName, default);
    var typeBuilder = moduleBuilder.AddType("Program");
    var methodBuilder = typeBuilder.AddMethod("Main", MethodAttributes.Public | MethodAttributes.Static, default, new Type[0]);
    var generator = new InstructionGenerator(typeBuilder, methodBuilder);
    generator.Generate(ast);
    moduleBuilder.SetEntryPoint(methodBuilder);
    // Save assembly to file
    using (var stream = File.Create(outputFile))
    {
        builder.Save(stream);
    }
}

Main(args);