from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionaries import *
from pyLong.zProfile import *
from pyLong.sProfile import *
from pyLong.verticalAnnotation import *


class DialogAdjustAnnotations(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Adjust vertical annotations")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/adjustVerticalAnnotation.png')))
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()

        self.zConstant = QRadioButton("Same altitude")
        self.zConstant.setChecked(True)
        layout.addWidget(self.zConstant, 0, 0)

        self.altitude = QDoubleSpinBox()
        self.altitude.setFixedWidth(90)
        self.altitude.setSuffix(" m")
        self.altitude.setLocale(QLocale('English'))
        self.altitude.setSingleStep(10)
        self.altitude.setRange(-99999.999, 99999.999)
        self.altitude.setDecimals(3)
        layout.addWidget(self.altitude, 0, 1)

        self.adjust = QRadioButton("Adjust")
        layout.addWidget(self.adjust, 1, 0)

        self.profiles = QComboBox()

        for zprofile, sprofile in self.pyLong.project.profiles:
            self.profiles.addItem(zprofile.title)
        layout.addWidget(self.profiles, 1, 1)

        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)

        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

    def validate(self):
        self.apply()
        self.accept()

    def apply(self):
        indexes = []
        for item in self.pyLong.annotationsList.list.selectedIndexes():
            indexes.append(item.row())

        indexes.sort()
        indexes.reverse()

        j = self.pyLong.annotationsList.groups.currentIndex()

        if len(indexes) == 1:
            i = indexes[0]

            annotation = self.pyLong.project.groups[j].annotations[i]

            if type(annotation) == VerticalAnnotation:
                if self.zConstant.isChecked():
                    annotation.position['z coordinate'] = self.altitude.value()
                    annotation.update()

                else:
                    k = self.profiles.currentIndex()
                    if k != -1:
                        zprofile, sprofile = self.pyLong.project.profiles[k]
                        try:
                            annotation.position['z coordinate'] = zprofile.interpolate(annotation.position['x coordinate'])
                            annotation.update()
                        except:
                            pass

                self.pyLong.canvas.draw()

        else:
            for i in indexes:
                annotation = self.pyLong.project.groups[j].annotations[i]

                if type(annotation) == VerticalAnnotation:
                    if self.zConstant.isChecked():
                        annotation.position['z coordinate'] = self.altitude.value()
                        annotation.update()

                    else:
                        k = self.profiles.currentIndex()
                        if k != -1:
                            zprofile, sprofile = self.pyLong.project.profiles[k]
                            try:
                                annotation.position['z coordinate'] = zprofile.interpolate(annotation.position['x coordinate'])
                                annotation.update()
                            except:
                                pass

            self.pyLong.canvas.draw()
