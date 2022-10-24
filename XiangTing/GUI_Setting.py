from PyQt5.uic import loadUi
from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtWidgets import*
import sys; sys.path.append('../../../API'); import API_FILE

class settingWindow(QDialog):
    def __init__(self, mainwindow):        
        QWidget.__init__(self)
        self.mainwindow = mainwindow
        loadUi("setting.ui",self)
        self.setWindowTitle("设置系统参数")
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton.clicked.connect(self.saveData)        
        self.loadSettings()

    def loadSettings(self):
        self.mainwindow.settingData = API_FILE.JSONRead("setting.JSON")
        self.textEdit_9.setText(self.mainwindow.settingData["PLCPort"])
        self.textEdit.setText(self.mainwindow.settingData["address"])
        self.textEdit_8.setText(self.mainwindow.settingData["IPAddress"])
        self.comboBox.setCurrentText(self.mainwindow.settingData["DetecterType"])
        self.comboBox_2.setCurrentText(self.mainwindow.settingData["MCAType"])
        self.comboBox_3.setCurrentText(str(self.mainwindow.settingData["ChannelNum"]))
        self.textEdit_2.setText(str(self.mainwindow.settingData["HighVoltage"])),
        self.textEdit_3.setText(str(self.mainwindow.settingData["gain"])), 
        self.textEdit_4.setText(API_FILE.dict2String(self.mainwindow.settingData["Lib"])), 
        self.textEdit_6.setText(self.mainwindow.settingData['prominence']),
        self.textEdit_5.setText(self.mainwindow.settingData['Background']),
        self.textEdit_7.setText(self.mainwindow.settingData['Uncertainty']),  
        self.plainTextEdit_2.setPlainText(self.mainwindow.settingData['calibChannel']),
        self.plainTextEdit.setPlainText(self.mainwindow.settingData['calibEnergy']),
        self.plainTextEdit_3.setPlainText(self.mainwindow.settingData['calibCPS']),
        self.plainTextEdit_4.setPlainText(self.mainwindow.settingData['calibDoserate']) 
        self.plainTextEdit_5.setPlainText(self.mainwindow.settingData['selectedRadionuclides'])

    def saveData(self):        
        setting = {
                    "PLCPort": self.textEdit_9.toPlainText(),
                    "address": self.textEdit.toPlainText(),
                    "IPAddress": self.textEdit_8.toPlainText(),
                    "DetecterType": self.comboBox.currentText(),
                    "MCAType": self.comboBox_2.currentText(),
                    "ChannelNum": self.comboBox_3.currentText(),
                    "HighVoltage": self.textEdit_2.toPlainText(),
                    "gain": self.textEdit_3.toPlainText(), 
                    "Lib": API_FILE.string2Dict(self.textEdit_4.toPlainText()),
                    'prominence':self.textEdit_6.toPlainText(),
                    'Background':self.textEdit_5.toPlainText(),
                    'Uncertainty':self.textEdit_7.toPlainText(),  
                    'calibChannel':self.plainTextEdit_2.toPlainText(),
                    'calibEnergy':self.plainTextEdit.toPlainText(),
                    'calibCPS':self.plainTextEdit_3.toPlainText(),
                    'calibDoserate':self.plainTextEdit_4.toPlainText(),
                    'selectedRadionuclides' : self.plainTextEdit_5.toPlainText()
                }
        API_FILE.JSONWrite("setting.json", setting)
        self.mainwindow.settingData = API_FILE.JSONRead("setting.JSON")
        self.mainwindow.settingsWindow.hide()

    def close(self):
        self.mainwindow.settingsWindow.hide()