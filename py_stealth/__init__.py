# -*- coding: utf-8 -*-

import ctypes

from . import py_stealth


# py_stealth names without ctypes
methods = {}
for key in vars(py_stealth).keys():
    if key not in vars(ctypes).keys():
        methods[key] = vars(py_stealth)[key]
print(methods)
vars().update(methods)


__all__ = [name for name in methods.keys()]




