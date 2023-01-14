
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
// MVID: {2d32f6e0-2a00-446c-970f-99c615a1c299}
.imagebase 0x00400000
.file alignment 0x00000200
.stackreserve 0x00100000
.subsystem 0x0003       // WINDOWS_CUI
.corflags 0x00000001    //  ILONLY
// Image base: 0x00007F72A6EC1000


// =============== CLASS MEMBERS DECLARATION ===================

.class public auto ansi beforefieldinit ConsoleApplication.Program
       extends [System.Runtime]System.Object
{
  .method public hidebysig static void  Main() cil managed
  {
    .entrypoint
    // Code size       28 (0x1c)
    .maxstack  8
    IL_0000:  call       void ConsoleApplication.Program::SayHello()
    IL_0005:  ldstr      "IntSum(7, 8) = "
    IL_000a:  call       void [System.Console]System.Console::Write(string)
    IL_000f:  ldc.i4.7
    IL_0010:  ldc.i4.8
    IL_0011:  call       int32 ConsoleApplication.Program::IntSum(int32,
                                                                  int32)
    IL_0016:  call       void [System.Console]System.Console::WriteLine(int32)
    IL_001b:  ret
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
