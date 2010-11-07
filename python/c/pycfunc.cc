#include <Python.h>
#include <string>

#include "auto_pyobj.h"

using std::string;

// Simple function.
static PyObject* pyc_sum(PyObject *self, PyObject *args) {
  int x, y;
  if (!PyArg_ParseTuple(args, "ii", &x, &y)) {
    return NULL;
  }
  return Py_BuildValue("i", x + y);
}

// How to handle strings.
static PyObject* pyc_concat(PyObject *self, PyObject *args) {
  const char* x;
  const char* y;
  if (!PyArg_ParseTuple(args, "ss", &x, &y)) {
    return NULL;
  }
  string result(x);
  result += y;
  // Content of result.c_str() is copied to a new PyObject.
  // So, we can release it in string's destructor.
  return Py_BuildValue("s", result.c_str());
}

const char* kDivideKeywords[] = {"numerator", "denominator", NULL};

// Arguments with keywords.
static PyObject* pyc_divide(PyObject* self, PyObject* args, PyObject *keywds) {
  int numerator, denominator;
  // Why the last arg is not "const" char**?
  if (!PyArg_ParseTupleAndKeywords(args, keywds, "ii", (char**)kDivideKeywords,
                                   &numerator, &denominator)) {
    return NULL;
  }
  return Py_BuildValue("i", numerator / denominator);
}

static PyObject* pyc_list2tuple(PyObject* self, PyObject* args) {
  // See Include/listobject.h and tupleobject.h in Python source to learn
  // list and tuple Python API.
  PyObject* list;
  if (!PyArg_ParseTuple(args, "O", &list)) {
    return NULL;
  }
  if (!PyList_Check(list)) {
    PyErr_SetString(PyExc_TypeError, "parameter must be list");
    return NULL;
  }
  Py_ssize_t size = PyList_Size(list);
  PyObject* tuple = PyTuple_New(size);
  for (Py_ssize_t i = 0; i < size; ++i) {
    PyTuple_SetItem(tuple, i, PyList_GetItem(list, i));
  }
  return tuple;
}

// Iterator, function call, complicated reference count.
static PyObject* pyc_reduce(PyObject* self, PyObject* args) {
  // As reference counts of objects in arguments are automatically managed by
  // args, we don't need to take care of them even if func() removes all of
  // other references to func or seq.
  PyObject* func;
  PyObject* seq;
  if (!PyArg_ParseTuple(args, "OO", &func, &seq)) {
    return NULL;
  }
  if (!PyCallable_Check(func)) {
    PyErr_SetString(PyExc_TypeError, "parameter must be callable");
    return NULL;
  }
  auto_pyobj it(PyObject_GetIter(seq));
  if (!it.get()) {
    return NULL;
  }
  auto_pyobj result;
  while (true) {
    auto_pyobj item(PyIter_Next(it.get()));
    if (!item.get()) {
      break;
    }
    if (result.get() == NULL) {
      result = item;
      continue;
    }
    // Do we need this? -> We need this.
    Py_INCREF(result.get());
    Py_INCREF(item.get());
    auto_pyobj func_args(Py_BuildValue("(OO)", result.get(), item.get()));
    if (func_args.get() == NULL) {
      return NULL;
    }
    result.reset(PyEval_CallObject(func, func_args.get()));
  }
  if (PyErr_Occurred()) {
    // An error occurred in PyIter_Next.
    return NULL;
  }
  if (result.get() == NULL) {
    PyErr_SetString(PyExc_TypeError,
                    "pyc.reduce() of empty sequence with no initial value");
    return NULL;
  }
  return result.release();
}

static PyMethodDef PycMethods[] = {
  {"sum", pyc_sum, METH_VARARGS,
   "Returns sum of 2 integers."},
  {"concat", pyc_concat, METH_VARARGS,
   "Concatinates 2 strings."},
  {"divide", (PyCFunction)pyc_divide, METH_VARARGS | METH_KEYWORDS,
   "Concatinates 2 strings."},
  {"reduce", pyc_reduce, METH_VARARGS,
   "Apply a function of two arguments "
   "cumulatively to the items of a sequence."},
  {"list2tuple", pyc_list2tuple, METH_VARARGS,
   "Convert list to tuple."},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

// The name of initialization function must be "init + module name.
PyMODINIT_FUNC
initpycfunc(void) {
  Py_InitModule3("pycfunc", PycMethods,
                 "Learning how to define Python functions using C/C++.");
}
