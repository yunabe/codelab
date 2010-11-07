class auto_pyobj {
public:
  auto_pyobj() : obj_(NULL) { };

  explicit auto_pyobj(PyObject* obj) : obj_(obj) { };

  auto_pyobj(auto_pyobj& o) : obj_(o.get()) {
    o.obj_ = NULL;
  };

  ~auto_pyobj() { Py_XDECREF(obj_); }

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
