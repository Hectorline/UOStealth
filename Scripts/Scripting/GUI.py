import atexit
from ctypes import *
from ctypes.wintypes import *
import configparser
import os
import sys
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

import py_stealth.py_stealth as py_stealth

CONFIG_FILE = 'py-hotkeys.ini'

MODS = {0x10: 'Shift', 0xA0: 'LShift', 0xA1: 'RShift', 0x11: 'Ctrl',
        0xA2: 'LCtrl', 0xA3: 'RCtrl', 0x12: 'Alt', 0xA4: 'LAlt', 0xA5: 'RAlt'}

KEYS = {0x1B: 'Esc', 0x70: 'F1', 0x71: 'F2', 0x72: 'F3', 0x73: 'F4',
        0x74: 'F5', 0x75: 'F6', 0x76: 'F7', 0x77: 'F8', 0x78: 'F9',
        0x79: 'F10', 0x7A: 'F11', 0x7B: 'F12', 0x13: 'PrintScreen',
        0x91: 'ScrollLock', 0x2C: 'Pause', 0x2D: 'Insert', 0x24: 'Home',
        0x21: 'PageUp', 0x2E: 'Delete', 0x23: 'End', 0x22: 'PageDown',
        0x08: 'Backspace', 0x09: 'Tab', 0x14: 'CapsLock', 0x0D: 'Return',
        0x20: 'Space', 0x25: 'Left', 0x26: 'Up', 0x27: 'Right', 0x28: 'Down',
        0xC0: '`', 0x31: '1', 0x32: '2', 0x33: '3', 0x34: '4', 0x35: '5',
        0x36: '6', 0x37: '7', 0x38: '8', 0x39: '9', 0x30: '0', 0xBD: '-',
        0xBB: '=', 0x51: 'Q', 0x57: 'W', 0x45: 'E', 0x52: 'R', 0x54: 'T',
        0x59: 'Y', 0x55: 'U', 0x49: 'I', 0x4F: 'O', 0x50: 'P', 0xDB: '[',
        0xDD: ']', 0x41: 'A', 0x53: 'S', 0x44: 'D', 0x46: 'F', 0x47: 'G',
        0x48: 'H', 0x4A: 'J', 0x4B: 'K', 0x4C: 'L', 0xBA: ';', 0xDE: "'",
        0xDC: '\\', 0x5A: 'Z', 0x58: 'X', 0x43: 'C', 0x56: 'V', 0x42: 'B',
        0x4E: 'N', 0x4D: 'M', 0xBC: ',', 0xBE: '.', 0xBF: '/', 0x90: 'NumLock',
        0x61: 'Num1', 0x62: 'Num2', 0x63: 'Num3', 0x64: 'Num4', 0x65: 'Num5',
        0x66: 'Num6', 0x67: 'Num7', 0x68: 'Num8', 0x69: 'Num9', 0x6B: 'Num+',
        0x60: 'Num0', 0x6E: 'Num.', 0x6D: 'Num-', 0x6A: 'Num*', 0x6F: 'Num/'}

HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 1
SWP_NOSIZE = 2

WH_KEYBOARD_LL = 13
WM_KEYUP = 0x101
WM_SYSKEYUP = 0x105
WM_KEYDOWN = 0x100
WM_SYSKEYDOWN = 0x104

LRESULT = LPARAM
LPWSTR = c_wchar_p
LPCWSTR = c_wchar_p

HOOKPROC = WINFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)
WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)

enum_windows_proc = WNDENUMPROC
low_level_keyboard_proc = HOOKPROC

CallNextHookEx = windll.user32.CallNextHookEx
CallNextHookEx.restype = LRESULT
CallNextHookEx.argtypes = (HHOOK,  # _In_ idHook
                           INT,  # _In_ nCode
                           WPARAM,  # _In_ wParam
                           LPARAM)  # _In_ lParam

DispatchMessage = windll.user32.DispatchMessageW
DispatchMessage.restype = LRESULT
DispatchMessage.argtypes = (LPMSG,)  # _In_ lpmsg

EnumWindows = windll.user32.EnumWindows
EnumWindows.restype = BOOL
EnumWindows.argtypes = (WNDENUMPROC,  # _In_ lpEnumFunc
                        LPARAM)  # _In_ lParam

GetClassName = windll.user32.GetClassNameW
GetClassName.restype = c_int
GetClassName.argtypes = (HWND,  # _In_ HWND
                         LPWSTR,  # _Out_ lpClassName
                         INT)  # _In_ nMaxCount

GetCurrentProcessId = windll.kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD

GetForegroundWindow = windll.user32.GetForegroundWindow
GetForegroundWindow.restype = HWND

GetLastError = windll.kernel32.GetLastError
GetLastError.restype = DWORD

GetMessage = windll.user32.GetMessageW
GetMessage.restype = BOOL
GetMessage.argtypes = (LPMSG,  # _Out_ lpMsg
                       HWND,  # _In_opt_ hWnd
                       UINT,  # _In_ wMsgFilterMin
                       UINT)  # _In_ wMsgFilterMax

GetModuleHandle = windll.kernel32.GetModuleHandleW
GetModuleHandle.restype = HMODULE
GetModuleHandle.argtypes = (LPCWSTR,)  # _In_opt_ lpModuleName

GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = DWORD
GetWindowThreadProcessId.argtypes = (HWND,  # _In_ hWnd
                                     LPDWORD)  # _Out_opt_ lpdwProcessId

IsWindowVisible = windll.user32.IsWindowVisible
IsWindowVisible.restype = BOOL
IsWindowVisible.argtypes = (HWND,)  # _In_ hWnd

MessageBox = windll.user32.MessageBoxW
MessageBox.restype = INT
MessageBox.argtypes = (HWND,  # _In_opt_ hWnd
                       LPCWSTR,  # _In_opt_ lpText
                       LPCWSTR,  # _In_opt_ lpCaption
                       UINT)  # _In_ uType

SetWindowsHookEx = windll.user32.SetWindowsHookExW
SetWindowsHookEx.restype = HHOOK
SetWindowsHookEx.argtpes = (c_int,  # _In_ idHook
                            HOOKPROC,  # _In_ lpfn
                            HINSTANCE,  # _In_ hMod
                            DWORD)  # _In_ dwThreadId

SetWindowPos = windll.user32.SetWindowPos
SetWindowPos.restype = BOOL
SetWindowPos.argtypes = (HWND,  # _In_ hWnd
                         HWND,  # _In_opt hWndInsertAfter
                         INT,  # _In_ X
                         INT,  # _In_ Y
                         INT,  # _In_ cx
                         INT,  # _In_ cy
                         UINT)  # _In_ uFlags

TranslateMessage = windll.user32.TranslateMessage
TranslateMessage.restype = BOOL
TranslateMessage.argtypes = (LPMSG,)  # _In_ lpMsg

UnhookWindowsHookEx = windll.user32.UnhookWindowsHookEx
UnhookWindowsHookEx.restype = BOOL
UnhookWindowsHookEx.argtypes = (HHOOK,)  # _In_ hhk


class KBDLLHOOK(Structure):
    _fields_ = [('vkCode', c_ulong),
                ('scanCode', c_ulong),
                ('flags', c_ulong),
                ('time', c_ulong),
                ('dwExtraInfo', c_ulong)]


class ScriptThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = None

    def run(self):
        py_stealth.StartStealthSocketInstance(sys.executable.encode())
        self.method()
        py_stealth.CorrectDisconnection()


class Application:
    def __init__(self):
        self.Shift = threading.Event()
        self.Ctrl = threading.Event()
        self.Alt = threading.Event()
        self.LShift = threading.Event()
        self.LCtrl = threading.Event()
        self.LAlt = threading.Event()
        self.RShift = threading.Event()
        self.RCtrl = threading.Event()
        self.RAlt = threading.Event()
        # storage for launched threads : list
        self.threads = []
        # binds
        self.binds = {}  # {(key codes): method}
        self.switch_bind = None  # [shift, ctrl, alt, key]
        # hooks
        self.launch_manager()
        # other
        self.hwnd = None
        self.vk_codes = None  # temporary storage
        self.module = None
        # widgets
        # root
        self.root = tk.Tk()
        self.root.geometry('400x200')
        self.root.title('Python hot keys for Stealth')
        self.root.resizable(0, 0)
        # widgets
        # choose file sector
        file_label = ttk.LabelFrame(self.root, text='Choose script file')
        file_label.pack(fill=tk.X, ipadx=3, padx=1)
        # path_to_file entry
        self.path_entry = ttk.Entry(file_label)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=3)
        # browse button
        button = ttk.Button(file_label, text='Browse', command=self.filedialog)
        button.pack(side=tk.RIGHT, pady=3)
        # hot keys sector
        hk_label = ttk.LabelFrame(self.root, text='Bind your hot keys')
        hk_label.pack(fill=tk.BOTH, ipadx=3, ipady=1, padx=1)
        # listbox with binds
        self.listbox = tk.Listbox(hk_label)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # scrollbar for listbox
        scrollbar = ttk.Scrollbar(hk_label, command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar)
        # buttons sector
        frame = ttk.Frame(hk_label)
        frame.pack(side=tk.RIGHT, fill=tk.Y)
        # entry for hot key selecting
        self.hk_entry = ttk.Entry(frame, justify=tk.CENTER)
        self.hk_entry.grid(row=1, column=1, columnspan=2, pady=1)
        self.hk_entry.insert(0, 'Button')
        self.hk_entry.bind('<Key>', self.get_vk_codes)
        # entry for command
        self.cmd_entry = ttk.Entry(frame, justify=tk.CENTER)
        self.cmd_entry.grid(row=2, column=1, columnspan=2, pady=1)
        self.cmd_entry.insert(0, 'Command')
        # add button
        button = ttk.Button(frame, text='Add', command=self.add_hotkey)
        button.grid(row=3, column=1, padx=1)
        # clear button
        button = ttk.Button(frame, text='Clear', command=self.clear_hotkey)
        button.grid(row=3, column=2, padx=1)
        # on/off key bind entry
        self.switch_entry = ttk.Entry(frame, justify=tk.CENTER)
        self.switch_entry.grid(row=4, column=1, columnspan=2, pady=1)
        self.switch_entry.insert(0, 'On/Off Button')
        self.switch_entry.bind('<Key>', self.get_vk_codes)
        # on top checkbox
        self.var_ontop = tk.BooleanVar()
        self.ontop = ttk.Checkbutton(frame, text='OnTop',
                                     command=self.on_top_switch,
                                     variable=self.var_ontop)
        self.ontop.grid(row=5, column=1, pady=2)
        # on/off checkbox
        self.var_switch = tk.BooleanVar()
        switcher = ttk.Checkbutton(frame, text='On/Off',
                                   command=self.on_off_switch,
                                   variable=self.var_switch)
        switcher.grid(row=5, column=2, pady=2)
        # config
        self.config = self.load_config()  # .ini

    def add_cfg(self, section, option, value):
        self.config[section][option] = str(value)
        with open(CONFIG_FILE, 'w') as file:
            self.config.write(file)

    def add_hotkey(self, codes=None, method=None, from_cfg=False):
        if self.module is None:
            return MessageBox(0, 'Choose script file first!', 'Error', 0)
        if self.vk_codes is None and not from_cfg:
            return MessageBox(0, 'Need to specify keyboard button', 'Error', 0)
        method = method or self.cmd_entry.get()
        if not hasattr(self.module, method):
            error = 'Can not find "' + method + '" in ' + self.module.__name__
            return MessageBox(0, error, 'Error', 0)
        if not callable(getattr(self.module, method)):
            error = 'Selected object must be callable.'
            return MessageBox(0, error, 'Error', 0)
        if self.vk_codes in self.binds:
            error = 'Selected button is already bound.'
            return MessageBox(0, error, 'Error', 0)
        codes = codes or self.vk_codes
        self.binds[codes] = getattr(self.module, method)
        vk_codes = ('{} ' * len(codes)).format(*codes)
        # save to .ini
        if not from_cfg:
            self.add_cfg('binds', vk_codes, method)
        # save vk codes to listbox
        self.vk_codes = None
        names = self.get_vk_codes_names(codes)
        line = vk_codes + '| ' + names + ' => ' + method
        self.listbox.insert(0, line)
        self.set_entry(self.hk_entry, 'Button')

    def clear_hotkey(self):
        try:
            index = self.listbox.curselection()[0]
        except IndexError:
            return
        codes = self.listbox.get(index).split('|')[0]
        self.listbox.delete(index)
        del self.binds[tuple([int(x) for x in codes.split()])]
        del self.config['binds'][codes.strip()]
        with open('py-hotkeys.ini', 'w') as file:
            self.config.write(file)

    def filedialog(self):
        path = filedialog.askopenfilename()
        self.load_module(path)

    def get_vk_codes(self, event):
        if event.keycode in (16, 17, 18):  # MODS
            pass
        elif event.type == '2':  # key pressed
            codes = [k for k, v in MODS.items() if getattr(self, v).is_set()]
            codes.sort()  # 1st shift, 2nd ctrl, 3rd alt
            codes.append(event.keycode)
            if event.widget is self.hk_entry:
                self.vk_codes = tuple(codes)
            elif event.widget is self.switch_entry:
                self.switch_bind = codes
                value = ('{} ' * len(codes)).format(*codes)
                self.add_cfg('main', 'on\off bind', value)
            self.set_entry(event.widget, self.get_vk_codes_names(codes))
        return 'break'  # block widget bindings

    @staticmethod
    def get_vk_codes_names(codes):
        res = ''
        for code in codes:
            res += ' ' if res else ''  # separator
            res += MODS[code] if code in MODS else ''
            res += KEYS[code] if code in KEYS else ''
        return res

    def launch_manager(self):
        @low_level_keyboard_proc
        def hook_handler(code, wparam, lparam):
            vkc = KBDLLHOOK.from_address(lparam).vkCode
            # MODS
            if vkc in MODS:  # if code in MODS.keys()
                event = getattr(self, MODS[vkc])
                if wparam == WM_KEYDOWN or wparam == WM_SYSKEYDOWN:  # pressed
                    event.set()
                elif wparam == WM_KEYUP or wparam == WM_SYSKEYUP:  # released
                    event.clear()
                else:
                    error = 'Unknown hook type "{}"'.format(wparam)
                    MessageBox(0, error, 'Error', 0)
                    exit()
            # keys
            elif wparam == WM_KEYDOWN or wparam == WM_SYSKEYDOWN:  # no mods
                if vkc not in KEYS:  # debug
                    error = 'Unknown key code {}'.format(hex(vkc))
                    MessageBox(0, error, 'Error', 0)
                    return CallNextHookEx(0, code, wparam, lparam)
                buffer = create_unicode_buffer('', 255)
                GetClassName(GetForegroundWindow(), buffer, 255)
                if buffer.value == 'Ultima Online':
                    items = MODS.items()
                    codes = [k for k, v in items if getattr(self, v).is_set()]
                    codes.sort()  # 1st shift, 2nd ctrl, 3rd alt
                    codes.append(vkc)
                    if codes == self.switch_bind:
                        self.var_switch.set(0 if self.var_switch.get() else 1)
                        self.on_off_switch()
                    if self.var_switch.get():
                        try:
                            method = self.binds[tuple(codes)]
                        except KeyError:
                            pass
                        else:
                            thread = ScriptThread(daemon=True)
                            thread.method = method
                            thread.start()
                            self.threads.append(thread)
                        for thread in self.threads.copy():
                            if not thread.is_alive():
                                thread.join()
                                del self.threads[self.threads.index(thread)]

            return CallNextHookEx(0, code, wparam, lparam)

        def register():
            hook_id = SetWindowsHookEx(WH_KEYBOARD_LL, hook_handler,
                                       GetModuleHandle(None), 0)
            if not hook_id:
                MessageBox(0, 'Can not register hook.', 'Error', 0)
                exit()
            atexit.register(UnhookWindowsHookEx, hook_id)

            msg = MSG()
            while True:
                GetMessage(msg, None, 0, 0)
                TranslateMessage(msg)
                DispatchMessage(msg)

        t = threading.Thread(target=register, daemon=True)
        t.start()

    def load_config(self):
        cfg = configparser.ConfigParser()
        cfg.add_section('main')
        cfg.add_section('binds')
        for path in sys.path:
            full = os.path.join(path, CONFIG_FILE)
            if os.path.exists(full):
                break
        if cfg.read(full):
            try:  # on/off switcher bind
                codes = cfg['main']['on\off bind']
                codes = [int(x) for x in codes.split()]
                self.switch_bind = codes
                self.switch_entry.delete(0, tk.END)
                self.switch_entry.insert(0, self.get_vk_codes_names(codes))
            except KeyError:
                pass
            try:  # on\off switcher
                val = cfg.getboolean('main', 'on\off')
                self.var_switch.set(val)
            except configparser.NoOptionError:
                pass
            try:  # load script
                path = cfg['main']['module']
                self.load_module(path, True)
            except KeyError:
                return cfg
            for codes in cfg['binds']:
                self.add_hotkey(codes=tuple([int(x) for x in codes.split()]),
                                method=cfg['binds'][codes], from_cfg=True)
        return cfg

    def load_module(self, path=None, from_cfg=False):
        path = path or self.path_entry.get()
        if os.path.exists(path):
            directory = os.path.dirname(path)
            filename = os.path.basename(path)
            if directory not in sys.path:
                sys.path.append(directory)
            self.module = __import__(filename.rpartition('.')[0])
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, filename + ' loaded successfully')
        if not from_cfg:
            self.add_cfg('main', 'module', path)

    def on_top_switch(self):
        @enum_windows_proc
        def enum_windows_handler(hwnd, lparam):
            buffer = c_ulong()
            GetWindowThreadProcessId(hwnd, byref(buffer))
            if pid == buffer.value:
                if IsWindowVisible(hwnd):
                    self.hwnd = hwnd
                    return 0
            return 1

        if self.hwnd is None:
            # get self hwnd
            pid = GetCurrentProcessId()
            EnumWindows(enum_windows_handler, 0)
        # magic
        val = self.var_ontop.get()
        SetWindowPos(self.hwnd, HWND_TOPMOST if val else HWND_NOTOPMOST,
                     0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

    def on_off_switch(self, from_cfg=False):
        val = self.var_switch.get()
        if not from_cfg:
            self.add_cfg('main', 'on\off', val)

    @staticmethod
    def set_entry(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, str(text))


if __name__ == '__main__':
    app = Application()
    app.root.mainloop()
