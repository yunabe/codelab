// See https://aka.ms/new-console-template for more information

using System.Reflection;
using System.Reflection.Metadata;
using System.Reflection.Metadata.Ecma335;
using System.Reflection.PortableExecutable;

// https://learn.microsoft.com/ja-jp/dotnet/api/system.reflection.metadata.ecma335.metadatabuilder?view=net-7.0

MethodDefinitionHandle EmitHelloWorld(MetadataBuilder metadata, BlobBuilder ilBuilder)
{
    Guid mvid = Guid.NewGuid();
    // Create module and assembly for a console application.
    metadata.AddModule(
        0,
        metadata.GetOrAddString("myprogram.dll"),
        metadata.GetOrAddGuid(mvid),
        default(GuidHandle),
        default(GuidHandle));

    metadata.AddAssembly(
        metadata.GetOrAddString("myprogram"),
        version: new Version(1, 0, 0, 0),
        culture: default(StringHandle),
        publicKey: default(BlobHandle),
        flags: 0,
        hashAlgorithm: AssemblyHashAlgorithm.None);

    // Create references to System.Object and System.Console types.
    AssemblyReferenceHandle sysRuntimeAssemblyRef = metadata.AddAssemblyReference(
        name: metadata.GetOrAddString("System.Runtime"),
        version: new Version(6, 0, 0, 0),
        culture: default(StringHandle),
        publicKeyOrToken: default(BlobHandle),
        flags: default(AssemblyFlags),
        hashValue: default(BlobHandle));
    AssemblyReferenceHandle sysConsoleAssemblyRef = metadata.AddAssemblyReference(
        name: metadata.GetOrAddString("System.Console"),
        version: new Version(6, 0, 0, 0),
        culture: default(StringHandle),
        publicKeyOrToken: default(BlobHandle),
        flags: default(AssemblyFlags),
        hashValue: default(BlobHandle));

    TypeReferenceHandle systemObjectTypeRef = metadata.AddTypeReference(
        sysRuntimeAssemblyRef,
        metadata.GetOrAddString("System"),
        metadata.GetOrAddString("Object"));

    TypeReferenceHandle systemConsoleTypeRefHandle = metadata.AddTypeReference(
        sysConsoleAssemblyRef,
        metadata.GetOrAddString("System"),
        metadata.GetOrAddString("Console"));

    // Get reference to Console.WriteLine(string) method.
    var consoleWriteLineSignature = new BlobBuilder();

    new BlobEncoder(consoleWriteLineSignature).
        MethodSignature().
        Parameters(1,
            returnType => returnType.Void(),
            parameters => parameters.AddParameter().Type().String());

    MemberReferenceHandle consoleWriteLineMemberRef = metadata.AddMemberReference(
        systemConsoleTypeRefHandle,
        metadata.GetOrAddString("WriteLine"),
        metadata.GetOrAddBlob(consoleWriteLineSignature));

    // Get reference to Object's constructor.
    var parameterlessCtorSignature = new BlobBuilder();

    new BlobEncoder(parameterlessCtorSignature).
        MethodSignature(isInstanceMethod: true).
        Parameters(0, returnType => returnType.Void(), parameters => { });

    BlobHandle parameterlessCtorBlobIndex = metadata.GetOrAddBlob(parameterlessCtorSignature);

    MemberReferenceHandle objectCtorMemberRef = metadata.AddMemberReference(
        systemObjectTypeRef,
        metadata.GetOrAddString(".ctor"),
        parameterlessCtorBlobIndex);

    // Create signature for "void Main()" method.
    var mainSignature = new BlobBuilder();

    new BlobEncoder(mainSignature).
        MethodSignature().
        Parameters(0, returnType => returnType.Void(), parameters => { });

    var methodBodyStream = new MethodBodyStreamEncoder(ilBuilder);

    var codeBuilder = new BlobBuilder();
    InstructionEncoder il;
    
    // Emit IL for Program::.ctor
    il = new InstructionEncoder(codeBuilder);

    // ldarg.0
    il.LoadArgument(0); 

    // call instance void [mscorlib]System.Object::.ctor()
    il.Call(objectCtorMemberRef);

    // ret
    il.OpCode(ILOpCode.Ret);

    int ctorBodyOffset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    // Emit IL for Program::Main
    var flowBuilder = new ControlFlowBuilder();
    il = new InstructionEncoder(codeBuilder, flowBuilder);

    // ldstr "hello"
    il.LoadString(metadata.GetOrAddUserString("Hello, world!"));

    // call void [mscorlib]System.Console::WriteLine(string)
    il.Call(consoleWriteLineMemberRef);

    // ret
    il.OpCode(ILOpCode.Ret);

    int mainBodyOffset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    // Create method definition for Program::Main
    MethodDefinitionHandle mainMethodDef = metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
        MethodImplAttributes.IL,
        metadata.GetOrAddString("Main"),
        metadata.GetOrAddBlob(mainSignature),
        mainBodyOffset,
        parameterList: default(ParameterHandle));

    // Create method definition for Program::.ctor
    // Note: It seems like we can omit .ctor (and mark the class static?) if we want.
    MethodDefinitionHandle ctorDef = metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.HideBySig | MethodAttributes.SpecialName | MethodAttributes.RTSpecialName,
        MethodImplAttributes.IL,
        metadata.GetOrAddString(".ctor"),
        parameterlessCtorBlobIndex,
        ctorBodyOffset,
        parameterList: default(ParameterHandle));

    // Create type definition for the special <Module> type that holds global functions
    // TODO(yunabe): Understand why this is necessary.
    // This defines an empty <Module> type (begin: mainMethodDef, end: mainMethodDef).
    // Probably, <Module> must be defined in a DLL though I did not find such a rule in ECMA-335 spec.
    metadata.AddTypeDefinition(
        default(TypeAttributes),
        default(StringHandle),
        metadata.GetOrAddString("<Module>"),
        baseType: default(EntityHandle),
        fieldList: MetadataTokens.FieldDefinitionHandle(1),
        methodList: mainMethodDef);

    // Create type definition for ConsoleApplication.Program
    metadata.AddTypeDefinition(
        TypeAttributes.Class | TypeAttributes.Public | TypeAttributes.AutoLayout | TypeAttributes.BeforeFieldInit,
        metadata.GetOrAddString("ConsoleApplication"),
        metadata.GetOrAddString("Program"),
        baseType: systemObjectTypeRef,
        fieldList: MetadataTokens.FieldDefinitionHandle(1),
        methodList: mainMethodDef);
    return mainMethodDef;
}

void WritePEImage(
    Stream peStream,
    MetadataBuilder metadataBuilder,
    BlobBuilder ilBuilder,
    MethodDefinitionHandle entryPointHandle
    )
{
    // Create executable with the managed metadata from the specified MetadataBuilder.
    var peHeaderBuilder = new PEHeaderBuilder(
        imageCharacteristics: Characteristics.ExecutableImage
        );

    var peBuilder = new ManagedPEBuilder(
        peHeaderBuilder,
        new MetadataRootBuilder(metadataBuilder),
        ilBuilder,
        entryPoint: entryPointHandle,
        flags: CorFlags.ILOnly);

    // Write executable into the specified stream.
    var peBlob = new BlobBuilder();
    BlobContentId contentId = peBuilder.Serialize(peBlob);
    peBlob.WriteContentTo(peStream);
}

void BuildHelloWorldApp()
{
    using var peStream = new FileStream(
        "myprogram.dll", FileMode.OpenOrCreate, FileAccess.ReadWrite
        );
    
    var ilBuilder = new BlobBuilder();
    var metadataBuilder = new MetadataBuilder();

    MethodDefinitionHandle entryPoint = EmitHelloWorld(metadataBuilder, ilBuilder);
    WritePEImage(peStream, metadataBuilder, ilBuilder, entryPoint);
}

BuildHelloWorldApp();
