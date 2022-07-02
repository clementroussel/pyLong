from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import pandas as pd
import numpy as np
import shapefile

from pyLong.dictionaries import separators, delimiters
from pyLong.zProfile import zProfile
from pyLong.sProfile import sProfile
from pyLong.verticalAnnotation import VerticalAnnotation


class DialogAddShapeProfile(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Add a shape profile")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/addShapeProfile.png')))
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Path :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.path = QLineEdit()
        layout.addWidget(self.path, 0, 1)
        
        browse = QPushButton("...")
        browse.setFixedWidth(20)
        browse.clicked.connect(self.browse)
        layout.addWidget(browse, 0, 2)
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.title = QLineEdit()
        self.title.setText("profile n°{}".format(zProfile.counter + 1))
        layout.addWidget(self.title, 1, 1)
    
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        layout = QHBoxLayout()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.importProfile)

        layout.addWidget(buttonBox)
        mainLayout.addLayout(layout)
        
        self.setLayout(mainLayout)

    def updateAxis(self):
        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]

        self.pyLong.canvas.ax_z.set_xlim((self.layout.xAxisProperties['min'] - self.layout.xAxisProperties['left shift'],
                                          self.layout.xAxisProperties['max'] + self.layout.xAxisProperties['right shift']))

        self.pyLong.canvas.ax_z.set_xticks(np.linspace(self.layout.xAxisProperties['min'],
                                                       self.layout.xAxisProperties['max'],
                                                       self.layout.xAxisProperties['intervals'] + 1))

        for ax in self.pyLong.canvas.subplots:
            ax.set_xlim((self.layout.xAxisProperties['min'] - self.layout.xAxisProperties['left shift'],
                         self.layout.xAxisProperties['max'] + self.layout.xAxisProperties['right shift']))

            ax.set_xticks(np.linspace(self.layout.xAxisProperties['min'],
                                      self.layout.xAxisProperties['max'],
                                      self.layout.xAxisProperties['intervals'] + 1))

        self.pyLong.canvas.ax_z.set_ylim((self.layout.zAxisProperties['min'] - self.layout.zAxisProperties['lower shift'],
                                          self.layout.zAxisProperties['max'] + self.layout.zAxisProperties['upper shift']))

        self.pyLong.canvas.ax_z.set_yticks(np.linspace(self.layout.zAxisProperties['min'],
                                                       self.layout.zAxisProperties['max'],
                                                       self.layout.zAxisProperties['intervals'] + 1))

        self.pyLong.canvas.draw()
        
    def browse(self):
        path = QFileDialog.getOpenFileName(caption="Add a shape profile",
                                           filter="shape file (*.shp)")[0]
        self.path.setText(path)

    def importProfile(self):
        try:
            sf = shapefile.Reader(self.path.text())
            shapes = sf.shapes()

            if len(shapes) == 0 or shapes[0].shapeType != 13:
                alert = QMessageBox(self)
                alert.setText("Import failed.")
                alert.exec_()
                return 0
            else:
                shape = shapes[0]
                dist = [0]
                for i, (x,y) in enumerate(shape.points):
                    if i != 0:
                        d = ((x - shape.points[i-1][0])**2 + (y - shape.points[i-1][1])**2)**0.5
                        dist.append(d + dist[i-1])

                xz = np.array([dist, shape.z]).T

            if np.shape(xz[:,0])[0] < 2:
                alert = QMessageBox(self)
                alert.setText("Import failed : Profile must contain at least 2 points.")
                alert.exec_()
                return 0

            else:
                zprofile = zProfile()

                zprofile.title = self.title.text()
                zprofile.x = xz[:,0]
                zprofile.z = xz[:,1]

                zprofile.sort(mode=self.pyLong.project.settings.profileDirection)
                zprofile.update()

                sprofile = sProfile()
                sprofile.updateData(zprofile.x, zprofile.z)
                sprofile.update()

                self.pyLong.project.profiles.append((zprofile, sprofile))
                self.pyLong.profilesList.update()
                self.pyLong.canvas.ax_z.add_line(zprofile.line)
                self.pyLong.canvas.ax_z.add_line(sprofile.trickLine)
                self.pyLong.canvas.updateLegends()

                if len(self.pyLong.project.profiles) == 1:
                    i = self.pyLong.layoutsList.currentIndex()
                    self.layout = self.pyLong.project.layouts[i]

                    self.layout.xAxisProperties['min'] = np.min(zprofile.x)
                    self.layout.xAxisProperties['max'] = np.max(zprofile.x)

                    self.layout.zAxisProperties['min'] = np.min(zprofile.z)
                    self.layout.zAxisProperties['max'] = np.max(zprofile.z)

                    self.updateAxis()

                self.accept()

        except:
            alert = QMessageBox(self)
            alert.setText("Import failed.")
            alert.exec_()
