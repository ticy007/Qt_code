from PyQt5 import QtWidgets
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtkmodules.all as vtk
from vtkmodules.vtkCommonColor import vtkNamedColors
import sys
sys.path.append('../../../API')
import API_PyQt5

class vtkWidget(QtWidgets.QWidget):
 
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent) 
        self.frame = QtWidgets.QFrame() 
        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        self.setLayout(self.vl)

        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        assembly = vtk.vtkAssembly()
        filenames = [r'G:\Project\Model\Blender\04.模型文件\探头盒子整体版.stl']
        for filename in filenames:            
            self.stl_actor =API_PyQt5.vtkLoadStl(filename, 0 ,0, 0)
            assembly.AddPart(self.stl_actor)
        
        self.ren.AddActor(assembly) 
        colors = vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d("White"))
        self.ren.ResetCamera()
        self.iren.Initialize()

    def addLine(self, points):
        self.LineActor = API_PyQt5.vtkDrawLine(points)
        self.ren.AddActor(self.LineActor)
        self.iren.GetRenderWindow().Render() 
        
        