%module(directors="1") modulename

%feature("director") DirectorRoot;

%{
#include "director.h"  
%}

namespace yunabe {

class NoDirectorRoot {
 public:
  NoDirectorRoot();
  virtual ~NoDirectorRoot();

  virtual void PrintName() const;
  static void CallPrintName(const NoDirectorRoot& root);
};

class DirectorRoot {
 public:
  DirectorRoot();
  virtual ~DirectorRoot();

  virtual void PrintName() const;
  static void CallPrintName(const DirectorRoot& root);
};

}  // namespace yunabe
