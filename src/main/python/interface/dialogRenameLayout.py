from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogRenameLayout(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Rename layout")
        
        i = self.pyLong.layoutsList.currentIndex()
        self.currentLayout = self.pyLong.project.layouts[i]
        
        mainLayout = QGridLayout()
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        mainLayout.addWidget(label, 0, 0)      
        
        self.title = QLineEdit()
        self.title.setText(self.currentLayout.title)
        mainLayout.addWidget(self.title, 0, 1)        
                
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        mainLayout.addWidget(buttonBox, 1, 0, 1, 2)

        self.setLayout(mainLayout)
        
    def validate(self):
        i = self.pyLong.layoutsList.currentIndex()
        self.currentLayout.title = self.title.text()
        self.pyLong.layoutsList.setItemText(i, self.title.text())
        self.accept()
