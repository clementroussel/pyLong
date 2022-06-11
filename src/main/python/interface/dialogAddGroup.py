from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.group import *


class DialogAddGroup(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Add a group")
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("New group")
        layout = QGridLayout()
        
        label = QLabel("title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.title = QLineEdit()
        self.title.setText("group {}".format(Group.counter + 1))
        layout.addWidget(self.title, 0, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonBox)
        
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
            
    def validate(self):
        group = Group()
        group.title = self.title.text()
            
        self.pyLong.project.groups.append(group)

        self.pyLong.annotationsList.updateGroups()
        self.pyLong.annotationsList.groups.setCurrentIndex(self.pyLong.annotationsList.groups.count() - 1)

        self.accept()
