#!/usr/bin/env python
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def build_plugmap(window):
    retval = {}
    for c in range(65, 26+65):
        control = getattr(window, f"plug{chr(c)}")
        fromValue = control.property("fromValue")
        retval[control.property("fromValue")] = control
    return retval
    
def window():
    app = QApplication(sys.argv)
    window = uic.loadUi("./Enigma.ui")
    window.dial_1.setValue(10)
    build_plugmap(window)
    window.show()
    sys.exit(app.exec_())

window()