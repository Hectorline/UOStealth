# -*- coding: utf-8 -*-

import ctypes
import importlib.machinery
import os
import sys

import py_stealth

TOP_LEVEL_NAME = os.path.splitext(os.path.basename(sys.argv[1]))[0]
METHODS = {key: vars(py_stealth)[key] for key in vars(py_stealth).keys()
           if not key.startswith('_') and key not in vars(ctypes).keys()}


class Finder(importlib.machinery.PathFinder):
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        spec = super().find_spec(fullname, path, target)
        if spec:
            spec.loader = Loader(spec.loader.name, spec.loader.path)
        return spec


class Loader(importlib.machinery.SourceFileLoader):
    def exec_module(self, module):
        code = self.get_code(module.__name__)
        if code is None:
            raise ImportError('cannot load module {} when get_code() '
                              'returns None'.format(module.__name__))
        vars(module).update(METHODS)
        if module.__name__ == TOP_LEVEL_NAME:
            module.__name__ = '__main__'
        exec(code, module.__dict__)
