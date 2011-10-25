#include <cstdio>
#include <string>
#include "ppapi/cpp/instance.h"
#include "ppapi/cpp/module.h"
#include "ppapi/cpp/var.h"

int fib(int n);

/// The Instance class.  One of these exists for each instance of your NaCl
/// module on the web page.
class NaiveFibInstance : public pp::Instance {
 public:
  explicit NaiveFibInstance(PP_Instance instance) : pp::Instance(instance) {}

  virtual ~NaiveFibInstance() {}

  virtual void HandleMessage(const pp::Var& var_message) {
    int result = -1;
    if (var_message.is_number()) {
      int n = var_message.AsInt();
      result = fib(n);
    }
    pp::Var reply(result);
    PostMessage(reply);
  }
};

/// The Module class.  The browser calls the CreateInstance() method to create
/// an instance of your NaCl module on the web page.
class NaiveFibModule : public pp::Module {
 public:
  NaiveFibModule() : pp::Module() {}
  virtual ~NaiveFibModule() {}

  virtual pp::Instance* CreateInstance(PP_Instance instance) {
    return new NaiveFibInstance(instance);
  }
};

namespace pp {
/// Factory function called by the browser when the module is first loaded.
/// The browser keeps a singleton of this module.
Module* CreateModule() {
  return new NaiveFibModule();
}
}  // namespace pp
