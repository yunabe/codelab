%module(directors="1") ues_time

%feature("director") Subtractor;

%{
// auto_pyobj is corresponding to SwigVar_PyObject.
#include "auto_pyobj.h"
#include "time.h"
#include "use_time.h"
%}

// See http://docs.python.org/c-api/
%define TIME_CPP2PY(cppvar, pyvar)
{
  int hour = cppvar.hour();
  int minute = cppvar.minute();
  int second = cppvar.second();
  auto_pyobj time_type(PyImport_ImportModule("time_type"));
  pyvar = PyObject_CallMethod(time_type.get(), "Time", "(iii)",
                              hour, minute, second);
}
%enddef

%define TIME_PY2CPP(pyvar, cppvar)
{
  auto_pyobj hour_obj(PyObject_GetAttrString(pyvar, "hour"));
  int hour = PyInt_AsLong(hour_obj.get());
  auto_pyobj minute_obj(PyObject_GetAttrString(pyvar, "minute"));
  int minute = PyInt_AsLong(minute_obj.get());
  auto_pyobj second_obj(PyObject_GetAttrString(pyvar, "second"));
  int second = PyInt_AsLong(second_obj.get());
  cppvar = yunabe::Time(hour, minute, second);
}
%enddef

%typemap(out) yunabe::Time TIME_CPP2PY($1, $result)

%typemap(in) yunabe::Time TIME_PY2CPP($input, $1)

// Notice formats of args are different from Java case :{
%typemap(directorin) yunabe::Time TIME_CPP2PY($1_name, $input)
%typemap(directorout) yunabe::Time TIME_PY2CPP($input, $result)

namespace yunabe {

yunabe::Time sumTimeAsValue(yunabe::Time x, yunabe::Time y);

class Subtractor {
 public:
  virtual ~Subtractor();
  virtual yunabe::Time subtract(yunabe::Time x, yunabe::Time y);
};

yunabe::Time subtractTime(yunabe::Time x, yunabe::Time y);
void registerSubtractor(Subtractor *subtractor);

}  // namespace yunabe
