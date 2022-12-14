#include "Python.h"

#if (PY_MAJOR_VERSION == 3) && (PY_MINOR_VERSION < 9)
// The function Py_SET_SIZE is defined starting with python 3.9.
void Py_SET_SIZE(PyVarObject *o, Py_ssize_t size){
    Py_SIZE(o) = size;
}
#endif
