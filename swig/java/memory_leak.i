%module(directors="1") modulename
%feature("director") Runner;

%{
#include "memory_leak.h"
%}

%typemap(javain,
         pre="$javainput.swigReleaseOwnership();")
   Runner* runner "$javaclassname.getCPtr($javainput)"

%include "memory_leak.h"
