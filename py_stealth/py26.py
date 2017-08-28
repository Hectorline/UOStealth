
import ctypes
import imp
import os
import sys

import py_stealth


TOP_LEVEL_NAME = os.path.basename(sys.argv[1]).rpartition('.')[0]
SUFFIXES = imp.get_suffixes()

# py_stealth names without ctypes
methods = {}
for key in vars(py_stealth).keys():
    if key not in vars(ctypes).keys():
        methods[key] = vars(py_stealth)[key]


class Finder(object):
    @staticmethod
    def find_module(fullname, path=None):
        module = fullname.rpartition('.')[2]
        f, pathname, info = imp.find_module(module, path)
        if info[2] not in (imp.PY_SOURCE, imp.PY_COMPILED, imp.PKG_DIRECTORY):
            return None  # not packet, .py, .pyw, .pyc
        if info[2] == imp.PKG_DIRECTORY:  # package
            try:
                f, pathname, info = imp.find_module('__init__', [pathname])
            except ImportError:
                return None
        return Loader(fullname, f, pathname)


class Loader(object):
    def __init__(self, name, f, path):
        self.name = name
        self.f = f
        self.path = path

    def load_module(self, fullname):
        module = sys.modules.setdefault(fullname, imp.new_module(fullname))
        module.__loader__ = self
        module.__file__ = self.path
        module.__package__ = module.__name__
        if os.path.basename(self.path).rpartition('.')[0] == '__init__':
            module.__path__ = [os.path.dirname(self.path)]
        else:
            module.__package__ = module.__package__.rpartition('.')[0]
        code = compile(self.f.read(), self.path, 'exec')
        self.f.close()
        # injects
        vars(module).update(methods)  # methods
        if module.__name__ == TOP_LEVEL_NAME:
            module.__name__ = '__main__'
        exec(code, module.__dict__)
        return module
