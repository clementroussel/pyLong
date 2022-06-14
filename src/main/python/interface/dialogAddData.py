from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionaries import *

from pyLong.otherData import *

class DialogAddData(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]
        
        self.setWindowTitle("Add data")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/addData.png')))
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Parameters")
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
        layout.addWidget(self.separator, 1, 1)
        
        label = QLabel("Path :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.path = QLineEdit()
        layout.addWidget(self.path, 2, 1)
        
        browse = QPushButton("...")
        browse.setFixedWidth(20)
        browse.clicked.connect(self.browse)
        layout.addWidget(browse, 2, 2)
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.title = QLineEdit()
        self.title.setText("data n°{}".format(OtherData.counter + 1))
        layout.addWidget(self.title, 3, 1)

        label = QLabel("Subplot :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.subplots = QComboBox()
        self.subplots.addItems(self.pyLong.project.subplots)
        layout.addWidget(self.subplots, 4, 1)
    
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        layout = QHBoxLayout()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)

        layout.addWidget(buttonBox)
        mainLayout.addLayout(layout)
        
        self.setLayout(mainLayout)
        
    def browse(self):
        path = QFileDialog.getOpenFileName(caption="Add data",
                                           filter="text file (*.txt)")[0]
        self.path.setText(path)

    def validate(self):
        if self.path.text() == "":
            alert = QMessageBox(self)
            alert.setText("Missing parameter : path")
            alert.exec_()
            return 0

        elif self.subplots.currentIndex() == -1:
            alerte = QMessageBox(self)
            alerte.setText("No subplot available.")
            alerte.exec_()
            return 0

        else:
            try:
                data = pd.read_csv(self.path.text(),
                                   delimiter=delimiters[self.delimiter.currentText()],
                                   decimal=separators[self.separator.currentText()],
                                   skiprows=0,
                                   encoding='utf-8').values

                xy = np.array(data[:, :2].astype('float'))

                if np.shape(xy[:, 0])[0] < 2:
                    alert = QMessageBox(self)
                    alert.setText("Import failed : Data must contain at least 2 points.")
                    alert.exec_()
                    return 0
                
                else:
                    data = OtherData()

                    data.title = self.title.text()
                    data.x = xy[:, 0]
                    data.y = xy[:, 1]
                    data.subplot = self.subplots.currentText()
                    
                    data.update()
                    self.pyLong.project.otherData.append(data)
                    self.pyLong.otherDataList.update()

                    try:
                        i = [subplot.id for subplot in self.layout.subplots].index(data.subplot)

                    except:
                        i = -1

                    if i != -1:
                        self.pyLong.canvas.subplots[i].add_line(data.line)
                        self.pyLong.canvas.updateLegends()

                    self.accept()

            except:
                alert = QMessageBox(self)
                alert.setText("Import failed.")
                alert.exec_()
