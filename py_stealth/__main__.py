# -*- coding: utf-8 -*-

import ctypes
import os
import sys
import traceback

import py_stealth


class StealthOutput(object):
    softspace = 0
    encoding = None

    def write(self, text):
        py_stealth.AddToSystemJournal(text)

    def flush(self):
        pass


def main():
    # check argv
    try:
        self, script, port = sys.argv
    except ValueError:
        error = 'sys.argv must be like: pythonw.exe -B path_to_script port'
        ctypes.windll.user32.MessageBoxA(0, bytes(error), bytes('Error'), 0)
        exit()
    # connect to stealth
    directory, filename = os.path.split(script)
    if directory not in sys.path:
        sys.path.append(directory)
    py_stealth.StartStealthSocketInstance(bytes(filename, encoding='utf8'))
    # change output to stealth system journal
    output = StealthOutput()
    sys.stdout = output
    sys.stderr = output
    # modify import system
    if sys.version_info < (3, 4):  # 2.6 2.7 3.0 3.1 3.2 3.3
        import py26 as importer
    elif sys.version_info > (3, 3):  # 3.4 3.5 3.6
        import py34 as importer
    sys.meta_path.insert(0, importer.Finder())
    # import script
    try:
        __import__(filename.rpartition('.')[0])
    except Exception:
        trace = traceback.format_exc()
        exceptions = ['\\py_stealth\\',
                      'exec(code, module.__dict__)',
                      "__import__(filename.rpartition('.')[0])"]
        for line in trace.splitlines():
            if [1 for x in exceptions if x in line]:
                continue
            output.write(line)
    finally:
        py_stealth.CorrectDisconnection()


if __name__ == '__main__':
    main()
