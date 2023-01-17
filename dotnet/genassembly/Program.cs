// See https://aka.ms/new-console-template for more information

using System.Reflection;
using System.Reflection.Metadata;
using System.Reflection.Metadata.Ecma335;
using System.Reflection.PortableExecutable;

// https://learn.microsoft.com/ja-jp/dotnet/api/system.reflection.metadata.ecma335.metadatabuilder?view=net-7.0
//
// TODO(yunabe): Understand how to use StoreLocal and LoadLocal.

MethodDefinitionHandle DefineConstructor(
    TypeReferenceHandle systemObjectTypeRef, MetadataBuilder metadata, BlobBuilder codeBuilder, MethodBodyStreamEncoder methodBodyStream) {

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

    // Emit IL for Program::.ctor
    InstructionEncoder il = new InstructionEncoder(codeBuilder);

    // ldarg.0
    il.LoadArgument(0); 

    // call instance void [mscorlib]System.Object::.ctor()
    il.Call(objectCtorMemberRef);

    // ret
    il.OpCode(ILOpCode.Ret);

    int ctorBodyOffset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    // Create method definition for Program::.ctor
    // Note: It seems like we can omit .ctor (and mark the class static?) if we want.
    return metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.HideBySig | MethodAttributes.SpecialName | MethodAttributes.RTSpecialName,
        MethodImplAttributes.IL,
        metadata.GetOrAddString(".ctor"),
        parameterlessCtorBlobIndex,
        ctorBodyOffset,
        parameterList: default(ParameterHandle));
}

// An example of a static method without parameters or the return value.
MethodDefinitionHandle DefineSayHello(
    ModuleDefinitionHandle moduleDef,
    AssemblyReferenceHandle sysConsoleAssemblyRef, MetadataBuilder metadata, BlobBuilder codeBuilder,  MethodBodyStreamEncoder methodBodyStream) {
    TypeReferenceHandle systemConsoleTypeRefHandle = metadata.AddTypeReference(
        sysConsoleAssemblyRef,
        metadata.GetOrAddString("System"),
        metadata.GetOrAddString("Console"));

    // Get reference to Console.WriteLine(string) method.
    var consoleWriteLineSignature = new BlobBuilder();

    // Create signature for "void Main()" method.
    new BlobEncoder(consoleWriteLineSignature).
        MethodSignature().
        Parameters(1,
            returnType => returnType.Void(),
            parameters => parameters.AddParameter().Type().String());

    MemberReferenceHandle consoleWriteLineMemberRef = metadata.AddMemberReference(
        systemConsoleTypeRefHandle,
        metadata.GetOrAddString("WriteLine"),
        metadata.GetOrAddBlob(consoleWriteLineSignature));

    TypeReferenceHandle programTypeRefHandle = metadata.AddTypeReference(
        moduleDef,
        metadata.GetOrAddString("ConsoleApplication"),
        metadata.GetOrAddString("Program"));

    // Get reference to Console.WriteLine(string) method.
    var getHellobSignature = new BlobBuilder();

    // Create signature for "void SayHello()" method.
    new BlobEncoder(getHellobSignature).
        MethodSignature().
        Parameters(0,
            returnType => returnType.Type().String(),
            parameters => {});

    MemberReferenceHandle getHelloMemberRef = metadata.AddMemberReference(
        programTypeRefHandle,
        metadata.GetOrAddString("GetHello"),
        metadata.GetOrAddBlob(getHellobSignature));


    // Emit IL for Program::Main
    var flowBuilder = new ControlFlowBuilder();
    InstructionEncoder il = new InstructionEncoder(codeBuilder, flowBuilder);

    // Load a message by calling GetHello.
    il.Call(getHelloMemberRef);

    // call void [mscorlib]System.Console::WriteLine(string)
    il.Call(consoleWriteLineMemberRef);

    // ret
    il.OpCode(ILOpCode.Ret);

    int offset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    BlobBuilder signature = new BlobBuilder();
    new BlobEncoder(signature).
        MethodSignature().
        Parameters(0, returnType => returnType.Void(), parameters => { });

    // Create method definition for Program::Main
    return metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
        MethodImplAttributes.IL,
        metadata.GetOrAddString("SayHello"),
        metadata.GetOrAddBlob(signature),
        offset,
        parameterList: default(ParameterHandle));
 }

 // An example of a static method without parameters or the return value.
MethodDefinitionHandle DefineGetHello(
    MetadataBuilder metadata, BlobBuilder codeBuilder,  MethodBodyStreamEncoder methodBodyStream) {
    // Emit IL for Program::Main
    InstructionEncoder il = new InstructionEncoder(codeBuilder);

    // ldstr "hello"
    il.LoadString(metadata.GetOrAddUserString("Hello, world from GetHello!"));

    // ret
    il.OpCode(ILOpCode.Ret);

    int offset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    BlobBuilder signature = new BlobBuilder();
    new BlobEncoder(signature).
        MethodSignature().
        Parameters(0, returnType => returnType.Type().String(), parameters => { });

    // Create method definition for Program::Main
    return metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
        MethodImplAttributes.IL,
        metadata.GetOrAddString("GetHello"),
        metadata.GetOrAddBlob(signature),
        offset,
        parameterList: default(ParameterHandle));
 }

// An example of a static method without parameters or the return value.
MethodDefinitionHandle DefineIntSum(
    MetadataBuilder metadata, BlobBuilder codeBuilder,  MethodBodyStreamEncoder methodBodyStream) {
    // Emit IL for Program::Main
    InstructionEncoder il = new InstructionEncoder(codeBuilder);

    il.LoadArgument(0);
    il.LoadArgument(1);
    il.OpCode(ILOpCode.Add);
    il.OpCode(ILOpCode.Ret);

    int offset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    BlobBuilder signature = new BlobBuilder();
    new BlobEncoder(signature).
        MethodSignature().
        Parameters(2, returnType => returnType.Type().Int32(), parameters => {
            parameters.AddParameter().Type().Int32();
            parameters.AddParameter().Type().Int32();
        });

    // TODO(yunabe): Name parameters by metadata.AddParameter and parameterList param.
    // Create method definition for Program::Main
    return metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
        MethodImplAttributes.IL,
        metadata.GetOrAddString("IntSum"),
        metadata.GetOrAddBlob(signature),
        offset,
        parameterList: default(ParameterHandle));
 }

// An example of a recursion call
//
// long NaiveFib(long n) {
//    if (n <= 1) {
//      return n;
//    }
//    return NaiveFib(n - 1) + NaiveFib(n - 2);
// }
MethodDefinitionHandle DefineNaiveFib(
    ModuleDefinitionHandle moduleDef,
    MetadataBuilder metadata, BlobBuilder codeBuilder,  MethodBodyStreamEncoder methodBodyStream) {
    // Create reference for "long NaiveFib(long)" method.
    TypeReferenceHandle programTypeRefHandle = metadata.AddTypeReference(
        moduleDef,
        metadata.GetOrAddString("ConsoleApplication"),
        metadata.GetOrAddString("Program"));
    var fibSignature = new BlobBuilder();
    new BlobEncoder(fibSignature).
        MethodSignature().
        Parameters(1,
            returnType => returnType.Type().Int64(),
            parameters => {
                parameters.AddParameter().Type().Int64();
            });
    MemberReferenceHandle fibMemberRef = metadata.AddMemberReference(
        programTypeRefHandle,
        metadata.GetOrAddString("NaiveFib"),
        metadata.GetOrAddBlob(fibSignature));

    // Emit IL for NaiveFib
    var flowBuilder = new ControlFlowBuilder();
    InstructionEncoder il = new InstructionEncoder(codeBuilder, flowBuilder);
    il.LoadArgument(0);
    il.LoadConstantI4(1);
    il.OpCode(ILOpCode.Conv_i8);
    var elseLabel = il.DefineLabel();
    il.Branch(ILOpCode.Bgt_s, elseLabel);

    il.LoadArgument(0);
    il.OpCode(ILOpCode.Ret);

    il.MarkLabel(elseLabel);
    il.LoadArgument(0);
    il.LoadConstantI4(1);
    il.OpCode(ILOpCode.Conv_i8);
    il.OpCode(ILOpCode.Sub);
    il.Call(fibMemberRef);

    il.LoadArgument(0);
    il.LoadConstantI4(2);
    il.OpCode(ILOpCode.Conv_i8);
    il.OpCode(ILOpCode.Sub);
    il.Call(fibMemberRef);

    il.OpCode(ILOpCode.Add);
    il.OpCode(ILOpCode.Ret);

    int offset = methodBodyStream.AddMethodBody(il);
    codeBuilder.Clear();

    return metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
        MethodImplAttributes.IL,
        metadata.GetOrAddString("NaiveFib"),
        metadata.GetOrAddBlob(fibSignature),
        offset,
        parameterList: default(ParameterHandle));
 }

MethodDefinitionHandle DefineMainMethod(
    ModuleDefinitionHandle moduleDef,
    AssemblyReferenceHandle sysConsoleAssemblyRef, AssemblyReferenceHandle sysRuntimeAssemblyRef,
    MetadataBuilder metadata, BlobBuilder codeBuilder,  MethodBodyStreamEncoder methodBodyStream) {
    TypeReferenceHandle programTypeRefHandle = metadata.AddTypeReference(
        moduleDef,
        metadata.GetOrAddString("ConsoleApplication"),
        metadata.GetOrAddString("Program"));

    // Emit IL for Program::Main
    var flowBuilder = new ControlFlowBuilder();
    InstructionEncoder il = new InstructionEncoder(codeBuilder, flowBuilder);

    /////////////////////////////////////////////////////////
    // Call a method without a return value or parameters. //
    /////////////////////////////////////////////////////////
    var sayHelloSignature = new BlobBuilder();
    new BlobEncoder(sayHelloSignature).
        MethodSignature().
        Parameters(0,
            returnType => returnType.Void(),
            parameters => {});
    MemberReferenceHandle sayHelloMemberRef = metadata.AddMemberReference(
        programTypeRefHandle,
        metadata.GetOrAddString("SayHello"),
        metadata.GetOrAddBlob(sayHelloSignature));
    il.Call(sayHelloMemberRef);

    ////////////////////
    // Call IntSum() ///
    ////////////////////
    // This is an example of how to call functions with paramters and
    // how to Box primitive values.

    // Prepare [System.Runtime]System.Int32 for boxing.
    TypeReferenceHandle int32TypeRefHandle = metadata.AddTypeReference(
        sysRuntimeAssemblyRef,
        metadata.GetOrAddString("System"),
        metadata.GetOrAddString("Int32"));

    TypeReferenceHandle systemConsoleTypeRefHandle = metadata.AddTypeReference(
        sysConsoleAssemblyRef,
        metadata.GetOrAddString("System"),
        metadata.GetOrAddString("Console"));
    var consoleWriteLineSignature = new BlobBuilder();
    new BlobEncoder(consoleWriteLineSignature).
        MethodSignature().
        Parameters(4,
            returnType => returnType.Void(),
            parameters => {
                parameters.AddParameter().Type().String();
                parameters.AddParameter().Type().Object();
                parameters.AddParameter().Type().Object();
                parameters.AddParameter().Type().Object();
            });    
    MemberReferenceHandle consoleWriteLineMemberRef = metadata.AddMemberReference(
        systemConsoleTypeRefHandle,
        metadata.GetOrAddString("WriteLine"),
        metadata.GetOrAddBlob(consoleWriteLineSignature));

    il.LoadString(metadata.GetOrAddUserString("IntSum({0}, {1}) = {2}"));
    int intSumArg0 = 7, intSumArg1 = 8;

    // Load int32 constants and box them.
    il.LoadConstantI4(intSumArg0);
    il.OpCode(ILOpCode.Box);
    il.Token(int32TypeRefHandle);
    il.LoadConstantI4(intSumArg1);
    il.OpCode(ILOpCode.Box);
    il.Token(int32TypeRefHandle);

    // Create signature for "void SayHello()" method.
    var intSumSignature = new BlobBuilder();
    new BlobEncoder(intSumSignature).
        MethodSignature().
        Parameters(2,
            returnType => returnType.Type().Int32(),
            parameters => {
                parameters.AddParameter().Type().Int32();
                parameters.AddParameter().Type().Int32();
            });
    MemberReferenceHandle intSumMemberRef = metadata.AddMemberReference(
        programTypeRefHandle,
        metadata.GetOrAddString("IntSum"),
        metadata.GetOrAddBlob(intSumSignature));

    il.LoadConstantI4(intSumArg0);
    il.LoadConstantI4(intSumArg1);
    il.Call(intSumMemberRef);
    // Box the output
    il.OpCode(ILOpCode.Box);
    il.Token(int32TypeRefHandle);

    il.Call(consoleWriteLineMemberRef);

    // Call NaiveFib
    TypeReferenceHandle int64TypeRefHandle = metadata.AddTypeReference(
        sysRuntimeAssemblyRef,
        metadata.GetOrAddString("System"),
        metadata.GetOrAddString("Int64"));
    var fibSignature = new BlobBuilder();
    new BlobEncoder(fibSignature).
        MethodSignature().
        Parameters(1,
            returnType => returnType.Type().Int64(),
            parameters => {
                parameters.AddParameter().Type().Int64();
            });
    MemberReferenceHandle fibMemberRef = metadata.AddMemberReference(
        programTypeRefHandle,
        metadata.GetOrAddString("NaiveFib"),
        metadata.GetOrAddBlob(fibSignature));
    var consoleWriteLine2Signature = new BlobBuilder();
    new BlobEncoder(consoleWriteLine2Signature).
        MethodSignature().
        Parameters(3,
            returnType => returnType.Void(),
            parameters => {
                parameters.AddParameter().Type().String();
                parameters.AddParameter().Type().Object();
                parameters.AddParameter().Type().Object();
            });    
    MemberReferenceHandle consoleWriteLine2MemberRef = metadata.AddMemberReference(
        systemConsoleTypeRefHandle,
        metadata.GetOrAddString("WriteLine"),
        metadata.GetOrAddBlob(consoleWriteLine2Signature));

    int fibArg = 40;
    il.LoadString(metadata.GetOrAddUserString("NaiveFib({0}) = {1}"));
    il.LoadConstantI4(fibArg);
    il.OpCode(ILOpCode.Conv_i8);
    il.StoreLocal(0);
    il.LoadLocal(0);
    il.OpCode(ILOpCode.Box);
    il.Token(int64TypeRefHandle);

    il.LoadLocal(0);
    il.Call(fibMemberRef);
    il.OpCode(ILOpCode.Conv_i8);
    il.OpCode(ILOpCode.Box);
    il.Token(int64TypeRefHandle);

    il.Call(consoleWriteLine2MemberRef);

    // ret
    il.OpCode(ILOpCode.Ret);

    // We need to define local variables to use StoreLocal/LoadLocal.
    // Ref:
    // https://github.com/dotnet/roslyn/blob/3b3124564a963dae015846ecb481859da8416138/src/Compilers/Core/Portable/PEWriter/MetadataWriter.cs#L2990
    var localVarSig = new BlobBuilder();
    new BlobEncoder(localVarSig).LocalVariableSignature(1).AddVariable().Type().Int64();
    StandaloneSignatureHandle localVarSigHandle = metadata.AddStandaloneSignature(metadata.GetOrAddBlob(localVarSig));

    int offset = methodBodyStream.AddMethodBody(il, localVariablesSignature: localVarSigHandle);
    codeBuilder.Clear();

    BlobBuilder signature = new BlobBuilder();
    new BlobEncoder(signature).
        MethodSignature().
        Parameters(0, returnType => returnType.Void(), parameters => { });

    // Create method definition for Program::Main
    return metadata.AddMethodDefinition(
        MethodAttributes.Public | MethodAttributes.Static | MethodAttributes.HideBySig,
        MethodImplAttributes.IL,
        metadata.GetOrAddString("Main"),
        metadata.GetOrAddBlob(signature),
        offset,
        parameterList: default(ParameterHandle));
}

MethodDefinitionHandle EmitHelloWorld(MetadataBuilder metadata, BlobBuilder ilBuilder)
{
    Guid mvid = Guid.NewGuid();
    // Create module and assembly for a console application.
    ModuleDefinitionHandle moduleDef = metadata.AddModule(
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

    var methodBodyStream = new MethodBodyStreamEncoder(ilBuilder);
    var codeBuilder = new BlobBuilder();
    MethodDefinitionHandle mainMethodDef = DefineMainMethod(moduleDef, sysConsoleAssemblyRef, sysRuntimeAssemblyRef, metadata, codeBuilder,  methodBodyStream);
    DefineSayHello(moduleDef, sysConsoleAssemblyRef, metadata, codeBuilder,  methodBodyStream);
    DefineGetHello(metadata, codeBuilder,  methodBodyStream);
    DefineIntSum(metadata, codeBuilder, methodBodyStream);
    DefineNaiveFib(moduleDef, metadata, codeBuilder, methodBodyStream);
    MethodDefinitionHandle ctorDef = DefineConstructor(systemObjectTypeRef, metadata, codeBuilder,  methodBodyStream);

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
