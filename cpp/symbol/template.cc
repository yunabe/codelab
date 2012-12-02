
template <typename Type>
class Template {
public:
  static void RunDecl();
  static void RunInline() {}
  static void RunDef();

  static int value;
};

template <typename Type> int Template<Type>::value;
template <typename Type> void Template<Type>::RunDef() {}

void use_symbols() {
  // "U": Same as normal class.
  Template<int>::RunDecl();
  // "W": Same as normal class.
  Template<int>::RunInline();

  // "W": With template, non-inlined method is "W" too.
  // So, it is okay to define non-inlined method in ".h" file and the definition
  // are created in multiple object files for "template".
  Template<int>::RunDef();
  // u Template<int>::value
  // static member of template class is "u" (unique global symbol) rather than
  // "B" for normal class. So, there is only one instance of a static member
  // in process even if the symbol are defined in multiple object files.
  Template<int>::value = 10;
}
