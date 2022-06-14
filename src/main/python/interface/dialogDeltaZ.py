from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *
import os
from pyLong.dictionaries import *

from scipy.interpolate import interp1d

import numpy as np
import pandas as pd


class DialogDeltaZ(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent

        self.setWindowTitle("Profiles comparison")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/comparison.png')))

        mainlayout = QVBoxLayout()

        group = QGroupBox("Parameters")
        layout = QGridLayout()

        label = QLabel("Profile n°1 :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.profiles1 = QComboBox()
        for zprofile, sprofile in self.pyLong.project.profiles:
            self.profiles1.addItem(zprofile.title)
        layout.addWidget(self.profiles1, 0, 1)

        label = QLabel("Profile n°2 :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.profiles2 = QComboBox()
        for zprofile, sprofile in self.pyLong.project.profiles:
            self.profiles2.addItem(zprofile.title)
        layout.addWidget(self.profiles2, 1, 1)

        self.interpolate = QCheckBox("Interpolation :")
        self.interpolate.setChecked(False)
        layout.addWidget(self.interpolate, 2, 0)

        self.step = QDoubleSpinBox()
        self.step.setFixedWidth(70)
        self.step.setSuffix(" m")
        self.step.setLocale(QLocale('English'))
        self.step.setRange(0.1, 999.9)
        self.step.setDecimals(1)
        self.step.setSingleStep(1)
        self.step.setValue(10)
        layout.addWidget(self.step, 2, 1)

        label = QLabel("Output file :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.path = QLineEdit()
        layout.addWidget(self.path, 3, 1)

        browse = QPushButton("...")
        browse.setAutoDefault(False)
        browse.setFixedWidth(20)
        browse.clicked.connect(self.browse)
        layout.addWidget(browse, 3, 2)

        group.setLayout(layout)
        mainlayout.addWidget(group)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainlayout.addWidget(buttonBox)

        self.setLayout(mainlayout)

    def browse(self):
        path = QFileDialog.getSaveFileName(caption="Profiles comparison",
                                           filter="text file (*.txt)")[0]
        if path == "":
            return 0
        else:
            fileName = QFileInfo(path).fileName()
            fileRepertory = QFileInfo(path).absolutePath()
            fileName = fileName.split(".")[0]

            fileName += ".txt"
            path = fileRepertory + "/" + fileName

            self.path.setText(path)

    def validate(self):
        i = self.profiles1.currentIndex()
        j = self.profiles2.currentIndex()

        if i != -1 and j != -1:
            zprofile1, sprofile1 = self.pyLong.project.profiles[i]
            x1 = list(zprofile1.x)

            zprofile2, sprofile2 = self.pyLong.project.profiles[j]
            x2 = list(zprofile2.x)

            xmin = max(min(x1), min(x2))
            xmax = min(max(x1), max(x2))

            if (xmin in x1) and (xmin in x2):
                pass
            elif (xmin in x1) and (not xmin in x2):
                x2.append(xmin)
                x2.sort()
            elif (not xmin in x1) and (xmin in x2):
                x1.append(xmin)
                x1.sort()

            if (xmax in x1) and (xmax in x2):
                pass
            elif (xmax in x1) and (not xmax in x2):
                x2.append(xmax)
                x2.sort()
            elif (not xmax in x1) and (xmax in x2):
                x1.append(xmax)
                x1.sort()

            i = x1.index(xmin)
            j = x1.index(xmax)
            x1 = x1[i:j+1]

            i = x2.index(xmin)
            j = x2.index(xmax)
            x2 = x2[i:j+1]

            x = x1 + x2
            x.sort()
            x = list(np.unique(x))

            z1 = []
            z2 = []

            for i in range(len(x)):
                z1.append(zprofile1.interpolate(x[i]))
                z2.append(zprofile2.interpolate(x[i]))

            x = np.array(x)
            z1 = np.array(z1)
            z2 = np.array(z2)

            if not self.interpolate.isChecked():
                xz = np.array([x, z1 - z2]).T
                xz = pd.DataFrame(xz)
            else:
                f = interp1d(x, z1 - z2)

                new_x = np.arange(x[0], x[-1], self.step.value())
                new_x = list(new_x)
                new_x.append(x[-1])
                new_x = np.array(new_x)
                new_z = f(new_x)

                xz = np.array([new_x, new_z]).T
                xz = pd.DataFrame(xz)

            try:
                xz.to_csv(self.path.text(),
                          sep="\t",
                          float_format="%.3f",
                          decimal=".",
                          index=False,
                          header=['X', 'Dz'])
                self.accept()
            except:
                alert = QMessageBox(self)
                alert.setText("Processing failed.")
                alert.setIcon(QMessageBox.Warning)
                alert.exec_()

        else:
            alert = QMessageBox(self)
            alert.setText("No profiles available.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()







