from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *
import os
from pyLong.dictionaries import *

import numpy as np
import pandas as pd


class DialogMezap(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.calculationsList.list.currentRow()
        self.mezap = self.pyLong.project.calculations[i]
        
        self.setWindowTitle("Energy line (MEZAP)")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rock.png')))
    
        tableWidget = QTabWidget()
        parametersTab = QWidget()

        tableWidget.addTab(parametersTab, "Parameters")
        
        # parameters tab
        layout = QGridLayout()
        
        label = QLabel("Profile :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.profiles = QComboBox()
        
        for zprofile, sprofile in self.pyLong.project.profiles:
            self.profiles.addItem(zprofile.title)

        try:
            self.profiles.setCurrentText(self.mezap.parameters['zprofile'].title)
        except:
            pass

        layout.addWidget(self.profiles, 0, 1, 1, 2)
        
        label = QLabel("X")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1)      

        label = QLabel("Z")
        label.setAlignment(Qt.AlignCenter)
        label.setVisible(False)
        layout.addWidget(label, 1, 2)
        
        label = QLabel("Start :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.xStart = QDoubleSpinBox()
        self.xStart.setFixedWidth(90)
        self.xStart.setSuffix(" m")
        self.xStart.setLocale(QLocale('English'))
        self.xStart.setSingleStep(1)
        self.xStart.setRange(0, 99999.999)
        self.xStart.setDecimals(3)
        self.xStart.setValue(self.mezap.parameters['x start'])
        layout.addWidget(self.xStart, 2, 1)        

        self.zStart = QDoubleSpinBox()
        self.zStart.setFixedWidth(90)
        self.zStart.setSuffix(" m")
        self.zStart.setLocale(QLocale('English'))
        self.zStart.setSingleStep(1)
        self.zStart.setRange(0, 99999.999)
        self.zStart.setDecimals(3)
        self.zStart.setReadOnly(True)
        self.zStart.setValue(self.mezap.parameters['z start'])
        self.zStart.setVisible(False)
        layout.addWidget(self.zStart, 2, 2)
        
        label = QLabel("Report :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        sublayout = QHBoxLayout()
        
        self.reportPath = QLineEdit()
        self.reportPath.setText(self.mezap.reportPath)
        sublayout.addWidget(self.reportPath)
        
        browserReportPath = QPushButton("...")
        browserReportPath.setFixedWidth(20)
        browserReportPath.clicked.connect(self.browseReportPath)
        browserReportPath.setAutoDefault(False)
        sublayout.addWidget(browserReportPath)

        layout.addLayout(sublayout, 3, 1, 1, 2)

        self.exportValues = QCheckBox("Export angles and normalized areas.")
        self.exportValues.setChecked(self.mezap.exportValues)

        layout.addWidget(self.exportValues, 4, 0, 1, 3)

        label = QLabel("Path :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)

        sublayout = QHBoxLayout()

        self.exportValuesPath = QLineEdit()
        self.exportValuesPath.setText(self.mezap.exportValuesPath)
        sublayout.addWidget(self.exportValuesPath)

        browserValuesPath = QPushButton("...")
        browserValuesPath.setFixedWidth(20)
        browserValuesPath.clicked.connect(self.browseValuesPath)
        browserValuesPath.setAutoDefault(False)
        sublayout.addWidget(browserValuesPath)

        layout.addLayout(sublayout, 5, 1, 1, 2)
        
        parametersTab.setLayout(layout)

        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.title = QLineEdit()
        self.title.setText(self.mezap.title)
        self.title.textChanged.connect(self.updateTitle)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        layout = QGridLayout()
        
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.title, 0, 1)
        
        layout.addWidget(tableWidget, 1, 0, 1, 2)
        
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)

    def browseReportPath(self):
        path = QFileDialog.getSaveFileName(caption="Report",
                                           filter="pdf file (*.pdf)")[0]
        if path == "":
            return 0
        else:
            fileName = QFileInfo(path).fileName()
            repertory = QFileInfo(path).absolutePath()
            fileName = fileName.split(".")[0]

            fileName += ".pdf"
            path = repertory + "/" + fileName

            self.reportPath.setText(path)

    def browseValuesPath(self):
        path = QFileDialog.getSaveFileName(caption="Angles and normalized areas",
                                             filter="text file (*.txt)")[0]
        if chemin == "":
            return 0
        else:
            fileName = QFileInfo(path).fileName()
            repertory = QFileInfo(path).absolutePath()
            fileName = fileName.split(".")[0]

            fileName += ".txt"
            path = repertory + "/" + fileName

            self.exportValuesPath.setText(path)

    def updateTitle(self):
        self.mezap.title = self.title.text()
        self.pyLong.calculationsList.update()

    def validate(self):
        self.apply()
        self.accept()

    def apply(self):
        self.mezap.title = self.title.text()
        self.mezap.reportPath = self.reportPath.text()

        self.mezap.parameters['zprofile'] = self.pyLong.project.profiles[self.profiles.currentIndex()][0]
        self.mezap.parameters['sprofile'] = self.pyLong.project.profiles[self.profiles.currentIndex()][1]
        self.mezap.parameters['x start'] = self.xStart.value()

        self.mezap.exportValues = self.exportValues.isChecked()
        self.mezap.exportValuesPath = self.exportValuesPath.text()

        self.mezap.calculate()

        if self.mezap.success:
            try:
                if self.exportValues.isChecked():
                    data = np.array([self.mezap.x, self.mezap.angles, self.mezap.normalizedAreas]).T
                    data = pd.DataFrame(data)
                    data.to_csv(self.exportValuesPath.text(),
                                sep="\t",
                                float_format="%.3f",
                                decimal=".",
                                index=False,
                                header=['X', 'Angle', 'Area'])

                self.mezap.x = []
                self.mezap.angles = []
                self.mezap.normalizedAreas = []

                # os.startfile(self.mezap.reportPath)
            except:
                pass
        else:
            alert = QMessageBox(self)
            alert.setText("Processing failed.")
            alert.exec_()