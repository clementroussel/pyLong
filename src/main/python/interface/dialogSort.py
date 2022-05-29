from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionaries import *


class DialogSort(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
 
        mainLayout = QVBoxLayout()
        
        i = self.pyLong.profilesList.list.currentRow()
        self.setWindowTitle("Sort <{}>".format(self.pyLong.profilesList.list.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/sort.png')))
        
        self.zprofile, self.sprofile = self.pyLong.project.profiles[i]
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Direction :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.direction = QComboBox()
        self.direction.addItem("ascending")
        self.direction.addItem("descending")
        self.direction.currentTextChanged.connect(self.preview)
        layout.addWidget(self.direction, 0, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

        self.pyLong.project.preview.visible = True
        self.pyLong.project.preview.x = self.zprofile.x
        self.pyLong.project.preview.z = self.zprofile.z
        self.pyLong.project.preview.update()
        
        self.pyLong.canvas.draw()
        
        self.preview()
        
    def preview(self):
        if self.direction.currentText() == "ascending":
            self.pyLong.project.preview.sort(mode="ascending")
            
        else:
            self.pyLong.project.preview.sort(mode="descending")

        self.pyLong.project.preview.update()
        
        self.pyLong.canvas.draw()
        
    def validate(self):
        if self.direction.currentText() == "ascending":
            self.zprofile.sort(mode="ascending")
        else:
            self.zprofile.sort(mode="descending")
            
        self.sprofile.updateData(self.zprofile.x, self.zprofile.z)
        
        self.zprofile.update()
        self.sprofile.update()

        if self.sprofile.annotationsVisible:
            self.pyLong.canvas.updateFigure()
        
        self.accept()
