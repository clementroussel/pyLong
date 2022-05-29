from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionaries import *
from pyLong.zProfile import *
from pyLong.sProfile import *


class DialogFilter(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        mainLayout = QVBoxLayout()
        
        i = self.pyLong.profilesList.list.currentRow()
        self.setWindowTitle("Filter <{}>".format(self.pyLong.profilesList.list.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/filter.png')))
        
        self.zprofile, self.sprofile = self.pyLong.project.profiles[i]
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Filter :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.filters = QComboBox()
        self.filters.addItems(["Lowess", "Butterworth", "Savitsky-Golay"])
        self.filters.currentTextChanged.connect(self.updateFilterParameters)
        layout.addWidget(self.filters, 0, 1)
        
        self.parameter1Name = QLabel()
        self.parameter1Name.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.parameter1Name, 1, 0)
        
        self.parameter1 = QDoubleSpinBox()
        self.parameter1.setLocale(QLocale('English'))
        self.parameter1.setVisible(False)
        self.parameter1.valueChanged.connect(self.controlParameters)
        self.parameter1.valueChanged.connect(self.preview)
        layout.addWidget(self.parameter1, 1, 1)
    
        self.parameter2Name = QLabel()
        self.parameter2Name.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.parameter2Name, 2, 0)
        
        self.parameter2 = QDoubleSpinBox()
        self.parameter2.setLocale(QLocale('English'))
        self.parameter2.setVisible(False)
        self.parameter2.valueChanged.connect(self.controlParameters)
        self.parameter2.valueChanged.connect(self.preview)
        layout.addWidget(self.parameter2, 2, 1)
        
        label = QLabel("Output profile title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.title = QLineEdit()
        self.title.setText("profile n°{}".format(zProfile.counter + 1))
        layout.addWidget(self.title, 3, 1) 

        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)
        
        self.updateFilterParameters()

        self.pyLong.project.preview.visible = True
        self.pyLong.project.preview.x = self.zprofile.x
        self.pyLong.project.preview.z = self.zprofile.z
        self.pyLong.project.preview.update()
            
        self.pyLong.canvas.draw()
        
        self.preview()
        
    def preview(self):
        if self.filters.currentText() == "Lowess":
            try:
                x, z = self.zprofile.lowess(self.parameter1.value(), self.parameter2.value())
                
                self.pyLong.project.preview.x = x
                self.pyLong.project.preview.z = z
                self.pyLong.project.preview.update()
                
                self.pyLong.canvas.draw()
            
            except:
                pass
            
        elif self.filters.currentText() == "Butterworth":
            try:
                x, z = self.zprofile.butterworth(self.parameter1.value(), self.parameter2.value())
                
                self.pyLong.project.preview.x = x
                self.pyLong.project.preview.z = z
                self.pyLong.project.preview.update()
                
                self.pyLong.canvas.draw()
            
            except:
                pass
            
        else:
            try:
                x, z = self.zprofile.savitsky_golay(self.parameter1.value(), self.parameter2.value())
                
                self.pyLong.project.preview.x = x
                self.pyLong.project.preview.z = z
                self.pyLong.project.preview.update()
                
                self.pyLong.canvas.draw()
                
            except:
                pass
            
    def validate(self):
        if self.filters.currentText() == "Lowess":
            try:
                x, z = self.zprofile.lowess(self.parameter1.value(), self.parameter2.value()) 
                
                zprofile = zProfile()
                sprofile = sProfile()
                
                zprofile.title = self.title.text()
                zprofile.x = x
                zprofile.z = z
                zprofile.update()
                
                sprofile.updateData(x, z)
                sprofile.update()
                
                self.pyLong.project.profiles.append((zprofile, sprofile))
                self.pyLong.profilesList.update()

                self.pyLong.canvas.ax_z.add_line(zprofile.line)
            
                self.accept()
                
            except:
                alert = QMessageBox(self)
                alert.setText("Processing failed. Sorry.")
                alert.exec_()
            
        elif self.filters.currentText() == "Butterworth":
            try:
                x, z = self.zprofile.butterworth(self.parameter1.value(), self.parameter2.value())
                
                zprofile = zProfile()
                sprofile = sProfile()
                
                zprofile.title = self.title.text()
                zprofile.x = x
                zprofile.z = z
                zprofile.update()
                
                sprofile.updateData(x, z)
                sprofile.update()
                
                self.pyLong.project.profiles.append((zprofile, sprofile))
                self.pyLong.profilesList.update()

                self.pyLong.canvas.ax_z.add_line(zprofile.line)
            
                self.accept()
                
            except:
                alert = QMessageBox(self)
                alert.setText("Processing failed. Sorry.")
                alert.exec_()
        
        else:
            try:
                x, z = self.zprofile.savitsky_golay(self.parameter1.value(), self.parameter2.value())
                
                zprofile = zProfile()
                sprofile = sProfile()
                
                zprofile.title = self.title.text()
                zprofile.x = x
                zprofile.z = z
                zprofile.update()
                
                sprofile.updateData(x, z)
                sprofile.update()
                
                self.pyLong.project.profiles.append((zprofile, sprofile))
                self.pyLong.profilesList.update()

                self.pyLong.canvas.ax_z.add_line(zprofile.line)
            
                self.accept()
                
            except:
                alert = QMessageBox(self)
                alert.setText("Processing failed. Sorry.")
                alert.exec_()
        
    def controlParameters(self):
        if self.filters.currentText() == "Savitsky-Golay":
            if int(self.parameter1.value()) >= int(self.parameter2.value()):
                self.parameter1.setValue(self.parameter2.value() - 1)
        
    def updateFilterParameters(self):
        if self.filters.currentText() == "Lowess":
            self.parameter1Name.setText("Window size :")
            self.parameter1Name.setVisible(True)
            self.parameter1.setDecimals(0)
            self.parameter1.setSingleStep(1)
            self.parameter1.setRange(1, 99999)
            self.parameter1.setValue(1)
            self.parameter1.setVisible(True)
            self.parameter2Name.setText("Parameter :")
            self.parameter2Name.setVisible(True)
            self.parameter2.setDecimals(4)
            self.parameter2.setSingleStep(0.0001)
            self.parameter2.setRange(0.0001, 1)
            self.parameter2.setValue(0.0001)
            self.parameter2.setVisible(True)
            
        elif self.filters.currentText() == "Butterworth":
            self.parameter1Name.setText("Filter order :")
            self.parameter1Name.setVisible(True)
            self.parameter1.setDecimals(0)
            self.parameter1.setSingleStep(1)
            self.parameter1.setRange(1, 99)
            self.parameter1.setVisible(True)
            self.parameter1.setValue(1)
            self.parameter2Name.setText("Critical frequency :")
            self.parameter2Name.setVisible(True)
            self.parameter2.setDecimals(3)
            self.parameter2.setSingleStep(0.001)
            self.parameter2.setRange(0.001, 0.999)
            self.parameter2.setValue(0.5)
            self.parameter2.setVisible(True)
            
        else:
            self.parameter1Name.setText("Polynomial order :")
            self.parameter1Name.setVisible(True)
            self.parameter1.setDecimals(0)
            self.parameter1.setSingleStep(1)
            self.parameter1.setRange(0, 99)
            self.parameter1.setVisible(True)
            self.parameter1.setValue(0)
            self.parameter2Name.setText("Window size :")
            self.parameter2Name.setVisible(True)
            self.parameter2.setDecimals(0)
            self.parameter2.setSingleStep(2)
            self.parameter2.setRange(1, 99999)
            self.parameter2.setVisible(True)
            self.parameter2.setValue(1)
            
        self.preview()
