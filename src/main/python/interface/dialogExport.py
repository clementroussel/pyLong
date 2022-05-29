from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionaries import *


class DialogExport(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        i = self.pyLong.profilesList.list.currentRow()
        
        self.setWindowTitle("Export <{}>".format(self.pyLong.profilesList.list.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/export.png')))
        
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
    
        label = QLabel("Number of decimal places :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)    
        
        self.decimal = QSpinBox()
        self.decimal.setFixedWidth(40)
        self.decimal.setRange(0,99)
        self.decimal.setValue(3)
        layout.addWidget(self.decimal, 2, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        mainLayout.addWidget(buttonBox)        
        self.setLayout(mainLayout)
        
    def validate(self):
        try:
            i = self.pyLong.profilesList.list.currentRow()
            zprofile, sprofile = self.pyLong.project.profiles[i]
            
            path = QFileDialog.getSaveFileName(caption="Export",
                                               filter="text file (*.txt)")[0]
            
            if path == "":
                return 0

            else:
                fileName = QFileInfo(path).fileName()
                fileFolder = QFileInfo(path).absolutePath()
                fileName = fileName.split(".")[0]
                fileName += ".txt"
                path = fileFolder + "/" + fileName

                delimiter = delimiters[self.delimiter.currentText()]
                formatting = "%.{}f".format(self.decimal.value())
                separator = separators[self.separator.currentText()]
                
                zprofile.export(path, delimiter, formatting, separator)

            self.accept()
            
        except:
            alert = QMessageBox(self)
            alert.setText("Processing failed. Sorry.")
            alert.exec_()
            pass
