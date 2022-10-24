import copy
import sys; sys.path.append('../../../API'); import API_Radiation, API_PyQt5
import numpy as np
from PyQt5 import QtCore

def analysisSpectrum(deltaTime, mainwindow, plot, channelData):
    try:        
        uncertain, peaks, width, nucliesExist, cps, doseRate = API_Radiation.radionuclidesExisted(mainwindow.settingData, deltaTime, channelData, mainwindow.selectedRadionuclides)
        
        doseRate = "{:.2f}".format(doseRate)
        cps = "{:.2f}".format(cps)
        
        for key in nucliesExist:
            for index in range(len(nucliesExist[key]['channel'])):
                j = nucliesExist[key]['channel'][index]
                plot.canvas.axes.plot(peaks[j], channelData[peaks[j]], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="green")
                color=np.random.rand(3,)
                plot.canvas.axes.plot([peaks[j]-width[j], peaks[j]-width[j]], [0, channelData[peaks[j]-int(width[j])]], linestyle='dashed', color=color )
                plot.canvas.axes.plot([peaks[j]+width[j], peaks[j]+width[j]], [0, channelData[peaks[j]-int(width[j])]], linestyle='dashed', color=color )
                API_PyQt5.matplotlibPyqt5AddCanvasText(peaks[j], channelData[peaks[j]], key, plot.canvas, 10)
                
        plot.canvas.draw()

        for i in range(len(uncertain)):
            uncertain[i] = "{:.2f}".format(uncertain[i])
            width[i] = "{:.2f}".format(width[i])
        nuclidesInfo="" 
        for key in nucliesExist:
            for i in range(len(nucliesExist[key]['channel'])):
                nucliesExist[key]['channel'][i] = peaks[nucliesExist[key]['channel'][i]]
            nuclidesInfo += key +f"存在{nucliesExist[key]['num']}个峰，峰的位置在道址{nucliesExist[key]['channel']}\n，峰的面积为{nucliesExist[key]['PearArea']}" + "\n" 

        text = "峰位置: \n" + str(peaks) + \
                "\n\n峰不确定度:\n"+ str(uncertain)+ \
                "\n\n峰宽度:\n" + str(width) +\
                "\n\n核素识别结果: \n"+ nuclidesInfo +\
                "\nCPS: \n"+ str(cps) +\
                "\n\n剂量率: \n"+ str(doseRate) +" uSv/hr"
        mainwindow.listWidget_2.clear()        
        mainwindow.listWidget_2.addItem(text)            
    except Exception as e:
        print(e)

def dataInsertTable(settingData, data, checkBox):
    dataItem = []; dicItem = settingData['Lib'][checkBox.text()]; dicName={"nuclides": checkBox.text()} 
    if type(data['halfLife']) != list:
        dicName.update(dicItem); dataItem.append(dicName)
    else:        
        for i in range(len(data['halfLife'])):
            for key in data:
                dicName[key] = dicItem[key][i]
            dataItem.append(copy.deepcopy(dicName))
    return dataItem

def updateSelectedRadionuclides(settingData, checkboxList, tableWidget, selectedRadionuclides):
    selected =settingData['selectedRadionuclides'].split(",")
    for selectedRadionuclide in selected:
        for checkBox in checkboxList:
            if selectedRadionuclide==checkBox.text():          
                data = settingData['Lib'][checkBox.text()]
                data = dataInsertTable(settingData, data, checkBox)
                checkBox.setCheckState(QtCore.Qt.Checked)

def plotParticlePath(parent):    
    origin = [0.0, 0.0, 0.0]
    p0 = [100.0, 100.0, 0.0]
    p1 = [0.0, 100.0, 100.0]
    p2 =[1.0, 100.0, 1.0]
    p3 =[1.0, 200.0, 1.0]

    points =[ p0, p1,p2,p3, origin ]
    parent.widget_2.addLine(points)
    # API_PyQt5.VTKRemoveActor( self.widget_2.LineActor,self.widget_2.ren, self.widget_2.iren)   

def loadEfficiencyMatrix():
    pass
