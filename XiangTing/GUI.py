from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
import sys; sys.path.append('../../../API'); import API_System, API_FILE, API_PyQt5, API_Math, API_Radiation
from GUI_Setting import settingWindow; from GUI_Passwd import passwordWindow
from GUI_Update import UpdateDataJieChuang, UpdateTime, UpdateGUI, UpdateDataXuanJie, UpdatePLC
import GUI_Func
import numpy as np

class SpectrumMeter(QMainWindow):    
    def __init__(self):        
        QMainWindow.__init__(self)
        
        #region global variables       
        self.settingData = API_FILE.JSONRead("setting.JSON")
        loadUi("GUI_VLLW.ui",self) 
        if self.settingData["PLCPort"] != "8888": 
            self.dockWidget_2.hide()
        
        self.showServerWindow = True
        self.selectedRadionuclides = []; self.serverPortList=[]; self.startSampleTime = ""; self.SampleTime = ""
        #endregion
        
        #region GUI Function
        self.settingsWindow = settingWindow(self)     
        self.passwordWindow = passwordWindow()      

        self.label_1 = QLabel("")
        self.statusbar.addPermanentWidget(self.label_1, 1)

        self.setWindowTitle("核素识别窗口")
        if self.settingData["PLCPort"] == "8888": 
            self.dockWidget_2.setWindowTitle("蒙卡计算与模型显示窗口") 
        self.listWidget_2.addItem("核素识别与活度计算：") 
        self.listWidget.addItem("操作提示：")  

        self.pushButton.clicked.connect(self.changePassword)
        self.pushButton_2.clicked.connect(self.changeSettings)

        self.toolButton.clicked.connect(self.startSample)
        self.toolButton_2.clicked.connect(self.stopSample)
        self.toolButton_3.clicked.connect(self.restartServer)
        self.toolButton_5.clicked.connect(self.clearCanvas)
        self.toolButton_9.clicked.connect(self.saveFileDialog)
        self.toolButton_7.clicked.connect(self.openFileNamesDialog)
        self.toolButton_8.clicked.connect(self.showOrHideServerDialog)

        if self.settingData["PLCPort"] == "8888":
            self.toolButton_4.clicked.connect(self.conveyorMoveForward)
            self.toolButton_12.clicked.connect(self.conveyorMoveBackward)
            self.toolButton_13.clicked.connect(self.conveyorSpeed)
            self.toolButton_6.clicked.connect(self.conveyorStop)
            self.toolButton_11.clicked.connect(self.MonteCarlosimulation)
            self.toolButton_14.clicked.connect(self.ModelMoveForward)
            self.toolButton_15.clicked.connect(self.ModelMoveBackward)
            self.toolButton_16.clicked.connect(self.SaveSpectrumInOnce)
            self.toolButton_10.clicked.connect(self.calculateActivity)
        if self.settingData["PLCPort"] == "8888":
            self.toolButton_4.installEventFilter(self)
            self.toolButton_13.installEventFilter(self)
            self.toolButton_12.installEventFilter(self)
            self.toolButton_6.installEventFilter(self)
            self.toolButton_11.installEventFilter(self)
            self.toolButton_14.installEventFilter(self)
            self.toolButton_15.installEventFilter(self)
            self.toolButton_16.installEventFilter(self)
            self.toolButton_10.installEventFilter(self)

        self.toolButton.installEventFilter(self)
        self.toolButton_2.installEventFilter(self)
        self.toolButton_3.installEventFilter(self)
        self.toolButton_5.installEventFilter(self)
        self.toolButton_9.installEventFilter(self)
        self.toolButton_7.installEventFilter(self)
        self.toolButton_8.installEventFilter(self)

        self.checkboxList =[self.checkBox_1,self.checkBox_2,self.checkBox_3,self.checkBox_4,
                            self.checkBox_5,self.checkBox_6,self.checkBox_7,self.checkBox_8,
                            self.checkBox_9,self.checkBox_10,self.checkBox_11,self.checkBox_12,
                            self.checkBox_13,self.checkBox_14,self.checkBox_15,self.checkBox_16,
                            self.checkBox_17,self.checkBox_18,self.checkBox_19,self.checkBox_20,
                            self.checkBox_21,self.checkBox_22,self.checkBox_23,self.checkBox_24,
                            self.checkBox_25,self.checkBox_26,self.checkBox_27,self.checkBox_28]        

        self.checkBox_1.stateChanged.connect(lambda:self.updateTable(self.checkBox_1))
        self.checkBox_2.stateChanged.connect(lambda:self.updateTable(self.checkBox_2))
        self.checkBox_3.stateChanged.connect(lambda:self.updateTable(self.checkBox_3))
        self.checkBox_4.stateChanged.connect(lambda:self.updateTable(self.checkBox_4))
        self.checkBox_5.stateChanged.connect(lambda:self.updateTable(self.checkBox_5))
        self.checkBox_6.stateChanged.connect(lambda:self.updateTable(self.checkBox_6))
        self.checkBox_7.stateChanged.connect(lambda:self.updateTable(self.checkBox_7))
        self.checkBox_8.stateChanged.connect(lambda:self.updateTable(self.checkBox_8))
        self.checkBox_9.stateChanged.connect(lambda:self.updateTable(self.checkBox_9))
        self.checkBox_10.stateChanged.connect(lambda:self.updateTable(self.checkBox_10))
        self.checkBox_11.stateChanged.connect(lambda:self.updateTable(self.checkBox_11))
        self.checkBox_12.stateChanged.connect(lambda:self.updateTable(self.checkBox_12))
        self.checkBox_13.stateChanged.connect(lambda:self.updateTable(self.checkBox_13))
        self.checkBox_14.stateChanged.connect(lambda:self.updateTable(self.checkBox_14))
        self.checkBox_15.stateChanged.connect(lambda:self.updateTable(self.checkBox_15))
        self.checkBox_16.stateChanged.connect(lambda:self.updateTable(self.checkBox_16))
        self.checkBox_17.stateChanged.connect(lambda:self.updateTable(self.checkBox_17))
        self.checkBox_18.stateChanged.connect(lambda:self.updateTable(self.checkBox_18))
        self.checkBox_19.stateChanged.connect(lambda:self.updateTable(self.checkBox_19))
        self.checkBox_20.stateChanged.connect(lambda:self.updateTable(self.checkBox_20))
        self.checkBox_21.stateChanged.connect(lambda:self.updateTable(self.checkBox_21))
        self.checkBox_22.stateChanged.connect(lambda:self.updateTable(self.checkBox_22))
        self.checkBox_23.stateChanged.connect(lambda:self.updateTable(self.checkBox_23))
        self.checkBox_24.stateChanged.connect(lambda:self.updateTable(self.checkBox_24))
        self.checkBox_25.stateChanged.connect(lambda:self.updateTable(self.checkBox_25))
        self.checkBox_26.stateChanged.connect(lambda:self.updateTable(self.checkBox_26))
        self.checkBox_27.stateChanged.connect(lambda:self.updateTable(self.checkBox_27))
        self.checkBox_28.stateChanged.connect(lambda:self.updateTable(self.checkBox_28))
        #endregion
        self.startCommunicationWithServer()        

    def startCommunicationWithServer(self):
        GUI_Func.updateSelectedRadionuclides(self.settingData, self.checkboxList, self.tableWidget, self.selectedRadionuclides)

        self.UpdateTimeWorker = UpdateTime(self.label_23, self.label_14, self.label_16)
        self.UpdateTimeWorker.start()
        self.UpdateMatplotlibWorker = UpdateGUI(self.widget, self.settingData, self.selectedRadionuclides, self)
        self.UpdateMatplotlibWorker.start()

        self.comboBox.clear()

        self.channelData={}; self.getDataWorker ={}
        if self.settingData["MCAType"] == "北京捷创核仪":
            for key in ["伽马谱","中子谱"]:
                self.comboBox.addItem(key); self.channelData[key] = np.zeros(1024); 
                self.getDataWorker[key] =UpdateDataJieChuang(self.settingData, self)
                self.getDataWorker["伽马谱"].start()          
        else: 
            # API_System.runExe(os.path.join(os.getcwd()+ '\\Debug\\SocketClient.exe'))           
            serverPortList = self.settingData["address"].split(",");self.channelData={};index =0; self.getDataWorker ={}
            for port in serverPortList:
                self.comboBox.addItem(port); self.channelData[port] = np.zeros(1024); self.serverPortList.append(int(port))
                self.getDataWorker[port]=UpdateDataXuanJie(self.settingData, self, int(port))
                self.getDataWorker[str(port)].start()

        if self.settingData["PLCPort"] =="8888":
            self.getDataWorker["8888"]=UpdatePLC(self.settingData, self, 8888)
            self.getDataWorker["8888"].start()

    def conveyorMoveForward(self):
        self.getDataWorker["8888"].message ="MoveForwad";self.getDataWorker["8888"].startSample = True 

    def conveyorMoveBackward(self):        
        self.getDataWorker["8888"].message ="MoveBackward";self.getDataWorker["8888"].startSample = True 

    def conveyorSpeed(self):
        self.getDataWorker["8888"].message =f"Speed:{str(self.spinBox.value())}"
        self.getDataWorker["8888"].startSample = True

    def conveyorStop(self):
        self.getDataWorker["8888"].message ="Stop";self.getDataWorker["8888"].startSample = True

    def MonteCarlosimulation(self):
        startPoint = self.textEdit.toPlainText().split(',')
        path =API_Radiation.MonteCarloRadiationTransport(11, 1,{'x': float(startPoint[0]), 'y': float(startPoint[1]), "z": float(startPoint[2])})
        pointList = API_Radiation.pointDict2PointList(path)
        line_actor = API_PyQt5.vtkDrawLine(pointList)
        API_PyQt5.VTKAddActor(line_actor, self.widget_2.ren, self.widget_2.iren)

    def ModelMoveForward(self):
        API_PyQt5.VTKMoveActor(self.widget_2.stl_actor, self.widget_2.iren, self.spinBox_4.value(), 0, 0 )
        API_PyQt5.VTKSetActorColor(self.widget_2.stl_actor, self.widget_2.iren, np.random.rand(), np.random.rand(),np.random.rand() )

    def ModelMoveBackward(self):
        pass

    def SaveSpectrumInOnce(self):
        for i in range(len(self.serverPortList)):
            API_FILE.SPEWrite(f"/VLLW_Data/{(self.spinBox_5.value()-1)*8+1}.Spe",
             self.channelData[{str(self.serverPortList[i])}], 
             self.SampleTime, datetime.datetime.now())
        self.listWidget.addItem(f"第{self.spinBox_5.value()}步采集的数据保存成功")

    def calculateActivity(self):
        pass

    def showOrHideServerDialog(self):
        try:
            if self.showServerWindow:
                self.worker.clientsocket.send("Hide".encode())
                self.listWidget.addItem(API_System.getCurrentTime()[0] + " :服务器窗口已隐藏...")
                self.showServerWindow = False 
            else:
                self.worker.clientsocket.send("Show".encode())
                self.listWidget.addItem(API_System.getCurrentTime()[0] + " :服务器窗口已显示...")
                self.showServerWindow =True 
        except Exception as e:
            QMessageBox.about(self, "提示信息", "请先与服务器建立连接") 

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
            channelData, sampleTime = API_FILE.SPERead(files[0])
            API_PyQt5.matplotlibPyqt5Clear(self.widget.canvas)          
            GUI_Func.analysisSpectrum(sampleTime, self, self.widget, channelData)
            API_PyQt5.matplotlibPyqt5PlotLine(self.widget.canvas, range(1024), channelData,2,'.','None','blue' )
            API_PyQt5.matplotlibPyqt5Axis(self.widget.canvas, xlim=[0,1024], logy='log')
            self.widget.canvas.draw()
            self.listWidget.addItem("打开文件"+files[0])

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            API_FILE.SPEWrite(fileName, self.channelData[self.comboBox.currentText()], self.SampleTime, datetime.now())
            self.listWidget.addItem("保存数据成功")

    def eventFilter(self, object, event): 
        if event.type() == QtCore.QEvent.HoverMove:
            self.label_1.setText(object.statusTip())
            return True
        return False    

    def updateTable(self, checkBox):
        if checkBox.isChecked():            
            rowPosition = self.tableWidget.rowCount()
            self.selectedRadionuclides.append(checkBox.text())
            data = self.settingData['Lib'][checkBox.text()]
            data = GUI_Func.dataInsertTable(self.settingData, data, checkBox)
            API_PyQt5.tableItemInsert(self.tableWidget, rowPosition, data)        
        else:
            self.selectedRadionuclides.remove(checkBox.text()) 
            API_PyQt5.tableItemRemove(self.tableWidget, checkBox.text())

    def openServer(self):
        pass
    
    #region JieChuang comunication Protocol
    # command
    # yangsong: start
    # shen:
    # b'\xfa\xfc\x00\x05\x00\x04\x00\x00\x00\x00\x01\xfb'
    # 示例:FA FC 00 40 00 04 00 00 01 FF D6 FB(设定高压值（V）=512/1024*1100)V；
    # set HV: b'\xFA\xFC\x00\x40\x00\x04\x00\x00\x01\xFF\xD6\xFB'
    # read HV: FA FC 00 41 00 04 00 00 00 00 45 FB
    # FA FC 00 42 00 04 00 00 00 00 46 FB(关闭高压)；                                  
    # FA FC 00 42 00 04 00 00 00 01 47 FB(打开 高压)；   
    # stop sample: b'\xFA\xFC\x00\x82\x00\x04\x00\x00\x00\x00\x86\xFB'
    # start sample: b'\xFA\xFC\x00\x82\x00\x04\x00\x00\x00\x01\x87\xFB' 
    # 0~4096 channel data: b'\xFA\xFC\x01\x80\x00\x04\x00\x00\x40\x00\x84\xFB'
    # hex(0x00 ^ 0x82 ^0x00 ^0x04 ^0x00  ^0x00  ^0x00  ^0x01) 2~9按位异或运算
    #endregion
    def startSample(self):
        try:
            self.startSampleTime = datetime.now()
            if self.settingData["MCAType"] =='北京捷创核仪':
                hv = hex(int(int(self.settingData["HighVoltage"])*1024/1100))[2:]
                if len(hv) <4:
                    hv1 = "0" + hv[:1]
                    hv2 = hv[1:]
                inputByteArray = "FA FC 00 40 00 04 00 00 02 E8 AE FB"; inputByteArray =inputByteArray.split(' '); inputByteArray[-4]=hv1; inputByteArray[-3]=hv2;  
                
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString(inputByteArray, "check")) # set HV
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString("FA FC 00 42 00 04 00 01 00 00 47 FB", "")) # open HV
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString("FA FC 00 61 00 04 00 00 00 01 64 FB", "")) # read HV
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString("FA FC 00 80 00 04 00 00 00 00 84 FB", "")) #clear data
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString("FA FC 00 82 00 04 00 00 00 01 87 FB", "")) # start sample
                self.getDataWorker["伽马谱"].startSample = True
            if self.settingData["MCAType"] =='山西轩杰智创科技': 
                for port in self.serverPortList: 
                    self.getDataWorker[str(port)].echoClient.send("SettingProbe".encode())                   
                    self.getDataWorker[str(port)].echoClient.send("start".encode())
                    self.getDataWorker[str(port)].startSample = True
            self.UpdateMatplotlibWorker.startSample = True
            self.listWidget.addItem(API_System.getCurrentTime()[0] + " :数据采集已开启...")             
        except Exception as e:
            print(e)
            QMessageBox.about(self, "提示信息", "数据采集失败")

    def stopSample(self):
        try:
            if self.settingData["MCAType"] =='北京捷创核仪':
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString("FA FC 00 80 00 04 00 00 00 00 84 FB", "")) #clear data
                self.getDataWorker["伽马谱"].echoClient.send(b"\xFA\xFC\x00\x82\x00\x04\x00\x00\x00\x00\x86\xFB") # stop sample
                self.getDataWorker["伽马谱"].echoClient.send(API_Math.ByteArrayToHexString("FA FC 00 42 00 04 00 00 00 00 46 FB", "")) #close HV
                self.getDataWorker["伽马谱"].startSample =False
            if self.settingData["MCAType"] =='山西轩杰智创科技':
                for port in self.serverPortList: 
                    self.getDataWorker[str(port)].echoClient.send("stop".encode())
                    self.getDataWorker[str(port)].startSample = False
            self.UpdateMatplotlibWorker.startSample = False
            self.listWidget.addItem(API_System.getCurrentTime()[0] + " :数据采集已停止...") 
            self.SampleTime = (datetime.now()-self.startSampleTime).total_seconds()+1
            GUI_Func.analysisSpectrum(self.SampleTime, self, self.widget, self.channelData[self.comboBox.currentText()])
        except Exception as e:
            QMessageBox.about(self, "提示信息", "停止数据采集失败")

    def restartServer(self):        
        try:
            self.startUpdate()
            self.listWidget.addItem(API_System.getCurrentTime()[0] + " :传感器已开启...") 
        except Exception as e:
            QMessageBox.about(self, "提示信息", "传感器连接失败")

    def clearCanvas(self):
        self.widget.canvas.axes.clear(); self.widget.canvas.draw()

    def changePassword(self):
        self.passwordWindow.show()

    def changeSettings(self):        
        self.settingsWindow.show()


if __name__ == "__main__":
    app = QApplication([])
    window = SpectrumMeter(); window.show()
    app.exec_()