#include <stdio.h>

#include "director.h"

namespace yunabe {
  
DirectorRoot::DirectorRoot() {}

DirectorRoot::~DirectorRoot() {}

void DirectorRoot::PrintName() const {
  printf("I'm DirectorRoot in C++.\n");
}

// static
void DirectorRoot::CallPrintName(const DirectorRoot& root) {
  root.PrintName();
}

NoDirectorRoot::NoDirectorRoot() {}

NoDirectorRoot::~NoDirectorRoot() {}

void NoDirectorRoot::PrintName() const {
  printf("I'm NoDirectorRoot in C++.\n");
}

// static
void NoDirectorRoot::CallPrintName(const NoDirectorRoot& root) {
  root.PrintName();
}


}  // namespace yunabe
