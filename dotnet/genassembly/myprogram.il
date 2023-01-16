
//  .NET IL Disassembler.  Version 8.0.0-dev



// Metadata version: v4.0.30319
.assembly extern System.Runtime
{
  .ver 6:0:0:0
}
.assembly extern System.Console
{
  .ver 6:0:0:0
}
.assembly myprogram
{
  .ver 1:0:0:0
}
.module myprogram.dll
// MVID: {0236c71f-4055-4740-b9e9-3dd644e2443c}
.imagebase 0x00400000
.file alignment 0x00000200
.stackreserve 0x00100000
.subsystem 0x0003       // WINDOWS_CUI
.corflags 0x00000001    //  ILONLY
// Image base: 0x00007F32A10F1000


// =============== CLASS MEMBERS DECLARATION ===================

.class public auto ansi beforefieldinit ConsoleApplication.Program
       extends [System.Runtime]System.Object
{
  .method public hidebysig static void  Main() cil managed
  {
    .entrypoint
    // Code size       71 (0x47)
    .maxstack  8
    IL_0000:  call       void ConsoleApplication.Program::SayHello()
    IL_0005:  ldstr      "IntSum({0}, {1}) = {2}"
    IL_000a:  ldc.i4.7
    IL_000b:  box        [System.Runtime]System.Int32
    IL_0010:  ldc.i4.8
    IL_0011:  box        [System.Runtime]System.Int32
    IL_0016:  ldc.i4.7
    IL_0017:  ldc.i4.8
    IL_0018:  call       int32 ConsoleApplication.Program::IntSum(int32,
                                                                  int32)
    IL_001d:  box        [System.Runtime]System.Int32
    IL_0022:  call       void [System.Console]System.Console::WriteLine(string,
                                                                        object,
                                                                        object,
                                                                        object)
    IL_0027:  ldstr      "NaiveFib({0}) = {1}"
    IL_002c:  ldc.i4.s   40
    IL_002e:  conv.i8
    IL_002f:  box        [System.Runtime]System.Int64
    IL_0034:  ldc.i4.s   40
    IL_0036:  call       int64 ConsoleApplication.Program::NaiveFib(int64)
    IL_003b:  conv.i8
    IL_003c:  box        [System.Runtime]System.Int64
    IL_0041:  call       void [System.Console]System.Console::WriteLine(string,
                                                                        object,
                                                                        object)
    IL_0046:  ret
  } // end of method Program::Main

  .method public hidebysig static void  SayHello() cil managed
  {
    // Code size       11 (0xb)
    .maxstack  8
    IL_0000:  call       string ConsoleApplication.Program::GetHello()
    IL_0005:  call       void [System.Console]System.Console::WriteLine(string)
    IL_000a:  ret
  } // end of method Program::SayHello

  .method public hidebysig static string 
          GetHello() cil managed
  {
    // Code size       6 (0x6)
    .maxstack  8
    IL_0000:  ldstr      "Hello, world from GetHello!"
    IL_0005:  ret
  } // end of method Program::GetHello

  .method public hidebysig static int32  IntSum(int32 A_0,
                                                int32 A_1) cil managed
  {
    // Code size       4 (0x4)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  ldarg.1
    IL_0002:  add
    IL_0003:  ret
  } // end of method Program::IntSum

  .method public hidebysig static int64  NaiveFib(int64 A_0) cil managed
  {
    // Code size       27 (0x1b)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  ldc.i4.1
    IL_0002:  conv.i8
    IL_0003:  bgt.s      IL_0007

    IL_0005:  ldarg.0
    IL_0006:  ret

    IL_0007:  ldarg.0
    IL_0008:  ldc.i4.1
    IL_0009:  conv.i8
    IL_000a:  sub
    IL_000b:  call       int64 ConsoleApplication.Program::NaiveFib(int64)
    IL_0010:  ldarg.0
    IL_0011:  ldc.i4.2
    IL_0012:  conv.i8
    IL_0013:  sub
    IL_0014:  call       int64 ConsoleApplication.Program::NaiveFib(int64)
    IL_0019:  add
    IL_001a:  ret
  } // end of method Program::NaiveFib

  .method public hidebysig specialname rtspecialname 
          instance void  .ctor() cil managed
  {
    // Code size       7 (0x7)
    .maxstack  8
    IL_0000:  ldarg.0
    IL_0001:  call       instance void [System.Runtime]System.Object::.ctor()
    IL_0006:  ret
  } // end of method Program::.ctor

} // end of class ConsoleApplication.Program


// =============================================================

// *********** DISASSEMBLY COMPLETE ***********************
