from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import pandas as pd
import numpy as np

from pyLong.dictionaries import separators, delimiters
from pyLong.zProfile import zProfile
from pyLong.sProfile import sProfile
from pyLong.verticalAnnotation import VerticalAnnotation


class DialogAddProfile(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Add a new profile")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/addProfile.png')))

        tabWidget = QTabWidget()
        textTab = QWidget()
        shpTab = QWidget()
        dbfTab = QWidget()

        tabWidget.addTab(textTab, "txt file")
        tabWidget.addTab(shpTab, "shape file")
        tabWidget.addTab(dbfTab, "database file")
        
        mainLayout = QVBoxLayout()
        
        # group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Delimiter :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.delimiter = QComboBox()
        self.delimiter.insertItems(0, list(delimiters.keys()))
        self.delimiter.setCurrentText("tabulation")
        layout.addWidget(self.delimiter, 0, 1)
        
        label = QLabel("Decimal separator :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.separator = QComboBox()
        self.separator.insertItems(0, list(separators.keys()))
        self.separator.setCurrentText("point")
        layout.addWidget(self.separator, 1, 1)
        
        self.profileOnly = QRadioButton("Import profile only")
        self.profileOnly.setChecked(True)
        layout.addWidget(self.profileOnly, 2, 0, 1, 2)

        self.annotationsWithProfile = QRadioButton("Import profile with annotations")
        layout.addWidget(self.annotationsWithProfile, 3, 0, 1, 2)

        self.annotationsOnly = QRadioButton("Import annotations only")
        layout.addWidget(self.annotationsOnly, 4, 0, 1, 2)
        
        label = QLabel("Path :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.path = QLineEdit()
        layout.addWidget(self.path, 5, 1)
        
        browse = QPushButton("...")
        browse.setFixedWidth(20)
        browse.clicked.connect(self.browse)
        layout.addWidget(browse, 5, 2)
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 6, 0)
        
        self.title = QLineEdit()
        self.title.setText("profile n°{}".format(zProfile.counter + 1))
        layout.addWidget(self.title, 6, 1)
    
        # group.setLayout(layout)
        # mainLayout.addWidget(group)
        textTab.setLayout(layout)

        mainLayout.addWidget(tabWidget)
        
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
        path = QFileDialog.getOpenFileName(caption="Add a new profile",
                                           filter="text file (*.txt)")[0]
        self.path.setText(path)

    def importProfile(self):
        try:
            profile = pd.read_csv(self.path.text(),
                                  delimiter=delimiters[self.delimiter.currentText()],
                                  decimal=separators[self.separator.currentText()],
                                  skiprows=0,
                                  encoding='utf-8').values

            xz = np.array(profile[:,:2].astype('float'))

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

                if zprofile.z[0] == xz[0, 1]:
                    sorted = False
                else:
                    sorted = True

                sprofile = sProfile()
                sprofile.updateData(zprofile.x, zprofile.z)
                sprofile.update()

                if self.profileOnly.isChecked() or self.annotationsWithProfile.isChecked():
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

            if self.annotationsOnly.isChecked() or self.annotationsWithProfile.isChecked():
                try:
                    annotations = list(profile[:, 2])
                    for i, label in enumerate(annotations):
                        if label is not np.nan and str(label) != 'nan':
                            annotation = VerticalAnnotation()
                            annotation.label = str(label)
                            annotation.title = str(label)

                            if not sorted:
                                annotation.position['x coordinate'] = xz[i, 0]
                            else:
                                n = len(annotations)
                                annotation.position['x coordinate'] = zprofile.x[n-1-i]

                            annotation.position['z coordinate'] = xz[i, 1]
                            annotation.update()

                            j = self.pyLong.annotationsList.groups.currentIndex()
                            self.pyLong.project.groups[j].annotations.append(annotation)

                            self.pyLong.canvas.ax_z.add_artist(annotation.annotation)

                    self.pyLong.annotationsList.updateList()
                    self.pyLong.canvas.draw()
                    self.accept()

                except:
                    alert = QMessageBox(self)
                    alert.setText("Annotations import failed.")
                    alert.exec_()

            else:
                self.accept()

        except:
            alert = QMessageBox(self)
            alert.setText("Import failed.")
            alert.exec_()
