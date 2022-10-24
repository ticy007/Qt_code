from PyQt5.QtCore import  QThread
# import debugpy
from datetime import datetime
import socket
import sys; sys.path.append('../../../API'); import API_System, API_Math, API_PyQt5
from GUI_Func import analysisSpectrum

class UpdateGUI(QThread):
    def __init__(self, plotCanvas, setting, selectedRadionuclides, parent):
        super(UpdateGUI, self).__init__()
        self.plotCanvas = plotCanvas
        self.setting = setting
        self.selectedRadionuclides = selectedRadionuclides
        self.startSample = False
        self.parent = parent
    def run(self):
        # debugpy.debug_this_thread()
        try:
            while True:
                self.sleep(1)
                if self.startSample:
                    text = analysisSpectrum((datetime.now()-self.parent.startSampleTime).total_seconds()+1, self.parent, self.plotCanvas, self.parent.channelData[self.parent.comboBox.currentText()])
                    self.parent.listWidget_2.addItem(text)
                    self.plotCanvas.canvas.axes.clear()
                    API_PyQt5.matplotlibPyqt5PlotLine(self.plotCanvas.canvas, range(1024), self.parent.channelData[self.parent.comboBox.currentText()],2,'.','None','blue' )
                    self.plotCanvas.canvas.draw() 
        except Exception as e:
            print(e)

class UpdateTime(QThread):
    def __init__(self, timeLabel, dateSetting, timeSetting):
        super(UpdateTime, self).__init__()        
        self.timeLabel = timeLabel
        self.dateSetting = dateSetting
        self.timeSetting = timeSetting
    def run(self):
        # debugpy.debug_this_thread()
        while True:
            self.sleep(1)
            current_time, today =API_System.getCurrentTime()
            self.timeLabel.setText(today + " "  + current_time)
            self.dateSetting.setText(today)
            self.timeSetting.setText(current_time)            
            
class UpdateDataJieChuang(QThread):
    def __init__(self, setting, parent):
        super(UpdateDataJieChuang, self).__init__()
        self.startSample =False
        self.setting = setting
        self.parent = parent

    def run(self):
        # debugpy.debug_this_thread()
        try:
            self.sleep(1)
            ipAddress = self.setting["IPAddress"].split(":")
            self.echoClient =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.echoClient.connect((ipAddress[0], int(ipAddress[1])))
            while True:
                self.sleep(1)
                if self.startSample:
                    channelData= []  
                    self.echoClient.send(API_Math.ByteArrayToHexString("FA FC 01 80 00 04 00 00 10 00 95 FB", ""))
                    text = self.echoClient.recv(10960); text =text.hex(); text =text[12:-4];#print(len(text)) 
                    if len(text) ==8192:
                        for j in range(0, len(text),8):
                            channelData.append(int("0x" +text[j:j+8], 16))
                        self.parent.channelData["伽马谱"] =channelData
        except Exception as e:
            print(e); print("Probe")

class UpdateDataXuanJie(QThread):
    def __init__(self, setting, parent, port):
        super(UpdateDataXuanJie, self).__init__()
        self.startSample =False
        self.setting = setting
        self.parent = parent
        self.serverPort =port

    def run(self): 
        try: 
            # debugpy.debug_this_thread()
            self.echoClient =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.echoClient.connect((socket.gethostname(), self.serverPort))        
            while True:
                self.sleep(1)  
                if self.startSample:
                    text= self.echoClient.recv(9216+7+9);
                    text=text.decode();text=text.replace('DataEnd','');text=text.replace('DataStart','');text=text.replace('start','');text = text.split('X')
                    if len(text)==1025:
                        for i in range(1024):
                            self.parent.channelData[str(self.serverPort)][i] = int(text[i])
        except Exception as e:
            print(e ); print("probe")

class UpdatePLC(QThread):
    def __init__(self, setting, parent, port):
        super(UpdatePLC, self).__init__()
        self.startSample =False
        self.setting = setting
        self.parent = parent
        self.serverPort =port
        self.message = ""

    def run(self): 
        try:  
            # debugpy.debug_this_thread()
            self.echoClient =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.echoClient.connect((socket.gethostname(), self.serverPort))        
            while True:
                self.sleep(1) 
                if self.startSample:
                    self.channelData= []  
                    self.echoClient.send(self.message.encode())
                    self.startSample = False
        except Exception as e:
            print(e ) ; print("PLC")