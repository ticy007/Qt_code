from PyQt5.uic import loadUi
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtWidgets import*

class passwordWindow(QDialog):
    def __init__(self):        
        QWidget.__init__(self)
        loadUi("passwordSetting2.ui",self)
        self.setWindowTitle("设置密码")