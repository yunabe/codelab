// By this %import,
// SWIG understands how ::yunabe::MyClass should be mapped.
// But SWIG does not output wrapper codes for MyClass.
// (If this is %include, SWIG outputs the wrapper codes because
// %includes expands "basic.i" in this SWIG file.
%import "basic.i"

%{
#include "include_and_import.h"
%}

// Expand "include_and_import.h" here.
%include "include_and_import.h"
