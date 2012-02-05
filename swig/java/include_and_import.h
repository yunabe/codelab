// SWIG ignores #include by default.
#include "basic.h"

namespace yunabe {

// SWIG can understand MyClass is ::yunabe::MyClass (by %import in
// include_and_import.i) though there is no forward declaration
// (#include "basic.h" is ignored) of MyClass in this file.
MyClass* createMyClass(int x);

}  // namespace yunabe
