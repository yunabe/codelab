// g++ -c -o virtual.o virtual.cc && nm virtual.o --demangle

class Virtual {
public:
  // No symbol is introduced for virtual method.
  // If it's not virtual, "U" symbol is exported.
  virtual void Run();
};

class Constructor {
public:
  // "T" ("U" if definition is inlined.)
  Constructor();
  virtual void Run();
};

// This introduces "U vtable for Constructor".
Constructor::Constructor() {}

class VirtualDef {
public:
  VirtualDef();
  // "T"
  virtual void Run();
};

// This introduces
//   V typeinfo for VirtualDef
//   V typeinfo name for VirtualDef
//   V vtable for VirtualDef
// Note: V is a weak object.
void VirtualDef::Run() {}

class VirtualDefSecond {
public:
  virtual ~VirtualDefSecond();
  // "T"
  virtual void Run();
};

// This does not introduces symbols of vtable and typeinfo because this is
// not the first virtual member.
void VirtualDefSecond::Run() {}

class ConstructorWithAllInlined {
public:
  ConstructorWithAllInlined();

  virtual void Run() {}
};

// When all virtual fuctiona are inlined, a constructor introduces
// definition os vtables and typeinfo symbols.
ConstructorWithAllInlined::ConstructorWithAllInlined() {}

class InlineConstructor {
public:
  // The symbols of vtable and typeinfo are introduced even if the constructor
  // is inlined. This means multiple objects files can have definitions of
  // the vtable. But only one definition is used in prodcess because
  // symbols are "V" (a weak object).
  InlineConstructor() {}

  virtual void Run() {}
};

void use_symbols() {
  Virtual* vir = 0;
  vir->Run();

  Constructor constructor;
  InlineConstructor inline_const;
}
