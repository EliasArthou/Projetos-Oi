from __future__ import print_function
import ctypes

MB_ABORTRETRYIGNORE = 2
MB_CANCELTRYCONTINUE = 6
MB_HELP = 0x4000
MB_OK = 0
MB_OKCANCEL = 1
MB_RETRYCANCEL = 5
MB_YESNO = 4
MB_YESNOCANCEL = 3

MB_ICONEXCLAMATION = MB_ICONWARNING = 0x30
MB_ICONINFORMATION = MB_ICONASTERISK = 0x40
MB_ICONQUESTION = 0x20
MB_ICONSTOP = MB_ICONERROR = MB_ICONHAND = 0x10

MB_DEFBUTTON1 = 0
MB_DEFBUTTON2 = 0x100
MB_DEFBUTTON3 = 0x200
MB_DEFBUTTON4 = 0x300

MB_APPLMODAL = 0
MB_SYSTEMMODAL = 0x1000
MB_TASKMODAL = 0x2000

MB_DEFAULT_DESKTOP_ONLY = 0x20000
MB_RIGHT = 0x80000
MB_RTLREADING = 0x100000

MB_SETFOREGROUND = 0x10000
MB_TOPMOST = 0x40000
MB_SERVICE_NOTIFICATION = 0x200000

IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDRETRY = 4
IDIGNORE = 5
IDYES = 6
IDNO = 7
IDTRYAGAIN = 10
IDCONTINUE = 11


def msgbox(text, style, title):
    return ctypes.windll.user32.MessageBoxW(None, text, title, style)


def criarinputbox(titulo, mensagem, substituircaracter=''):
    import tkinter as tk
    from tkinter import simpledialog

    ROOT = tk.Tk()

    ROOT.withdraw()
    # the input dialog
    USER_INP = simpledialog.askstring(title=titulo, prompt=mensagem, show=substituircaracter)
    if USER_INP is None:
        USER_INP = 0

    return USER_INP