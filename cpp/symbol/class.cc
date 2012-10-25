// No difference between static member funcs and member funcs as symbols.

// No symbol for default constructor & destructors.
class DefaultConstructor {
public:
  int value;
};

class ClassDecl {
public:
  // "U"
  ClassDecl();
  // "U"
  ~ClassDecl();
  // "U"
  void Run();
  static void StaticRun();

  int value;
};

class InlineDef {
public:
  // "W" : Week symbol (See man nm)
  InlineDef() {}
  // "W"
  ~InlineDef() {}
  // "W"
  void Run() {}
  // "W"
  static void StaticRun() {}

  int value;
};

class DeclAndDef {
public:
  // "T"
  DeclAndDef();
  // "T"
  ~DeclAndDef();
  // "T"
  void Run();
  // "T"
  static void StaticRun();

  int value;
};

DeclAndDef::DeclAndDef() {}

DeclAndDef::~DeclAndDef() {}

void DeclAndDef::Run() {}

void DeclAndDef::StaticRun() {}

void use_symbols() {
  DefaultConstructor default_constructor;
  default_constructor.value = 10;
  DefaultConstructor copied = default_constructor;

  ClassDecl decl;
  // decl.Run() introduces not only U ClassDecl::Run() but also
  // U _Unwind_Resume and U __gxx_personality_v0. What are these?
  decl.Run();
  InlineDef idef;
  idef.Run();
  DeclAndDef decdef;
  decdef.Run();

  // Access to value does not introduce any symbols.
  decl.value = 10;
  idef.value = 20;
  decdef.value = 30;

  // ClassDecl::StaticRun also introduces _Unwind_Resume and
  // __gxx_personality_v0.
  ClassDecl::StaticRun();
  InlineDef::StaticRun();
  DeclAndDef::StaticRun();
}
