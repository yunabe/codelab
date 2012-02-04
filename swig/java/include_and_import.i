// By this %import,
// SWIG understands how ::yunabe::MyClass should be mapped.
// But SWIG does not output wrapper codes for MyClass.
// (If this is %include, SWIG outputs the wrapper codes because
// %includes expands "basic.i" in this SWIG file.
%import "basic.i"

%{
#include "include_and_import.h"
%}

// The return value of createMyClass must be released by caller.
// http://www.swig.org/Doc1.3/Customization.html#ownership
// NEWOBJECT macro is defined in basic.i and become available here by %import!
NEWOBJECT(yunabe::createMyClass)

// Expand "include_and_import.h" here.
%include "include_and_import.h"
