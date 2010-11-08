#ifndef YUNABE_PRACTICE_PYTHON_C_AUTO_PYOBJ_H_
#define YUNABE_PRACTICE_PYTHON_C_AUTO_PYOBJ_H_

class auto_pyobj {
public:
  auto_pyobj() : obj_(NULL) { };

  explicit auto_pyobj(PyObject* obj) : obj_(obj) { };

  auto_pyobj(auto_pyobj& o) : obj_(o.release()) { };
  
  auto_pyobj& operator= (auto_pyobj& o) {
    reset(o.release());
    return *this;
  };

  ~auto_pyobj() { Py_XDECREF(obj_); };

  PyObject* get() { return obj_; };

  void reset(PyObject* obj) {
    Py_XDECREF(obj_);
    obj_ = obj;
  };

  PyObject* release() {
    PyObject* obj = obj_;
    obj_ = NULL;
    return obj;
  };

private:
  PyObject* obj_;
};

#endif  // YUNABE_PRACTICE_PYTHON_C_AUTO_PYOBJ_H_
