from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.layout import *


class DialogDeleteLayouts(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Delete layouts")
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Delete layouts :")
        layout = QVBoxLayout()
        
        self.layoutsList = QListWidget()
        for l in self.pyLong.project.layouts[1:]:
            item = QListWidgetItem()
            item.setText(l.title)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.layoutsList.addItem(item)
        
        layout.addWidget(self.layoutsList)
        group.setLayout(layout)
        
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonBox)
        
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
        
    def validate(self):
        n = self.pyLong.layoutsList.count()
        n -= 1
        for i in range(n-1, -1, -1):
            if self.layoutsList.item(i).checkState() == Qt.Checked:
                self.pyLong.project.layouts.pop(i+1)
                self.pyLong.layoutsList.removeItem(i+1)
        self.accept()
