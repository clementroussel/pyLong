from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.group import *

from pyLong.text import Text
from pyLong.verticalAnnotation import VerticalAnnotation
from pyLong.linearAnnotation import LinearAnnotation
from pyLong.interval import Interval
from pyLong.rectangle import Rectangle

class DialogDeleteGroups(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Delete groups")
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Delete groups :")
        layout = QVBoxLayout()
        
        self.groupsList = QListWidget()
        for g in self.pyLong.project.groups[1:]:
            item = QListWidgetItem()
            item.setText(g.title)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.groupsList.addItem(item)
        
        layout.addWidget(self.groupsList)
        group.setLayout(layout)
        
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonBox)
        
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
        
    def validate(self):
        n = self.pyLong.annotationsList.groups.count()
        n -= 1
        for i in range(n-1, -1, -1):
            if self.groupsList.item(i).checkState() == Qt.Checked:
                for annotation in self.pyLong.project.groups[i+1].annotations:
                    if type(annotation) == Text:
                        annotation.text.remove()

                    elif type(annotation) == VerticalAnnotation:
                        annotation.annotation.remove()

                    elif type(annotation) == LinearAnnotation:
                        annotation.annotation.remove()
                        annotation.text.remove()

                    elif type(annotation) == Interval:
                        annotation.text.remove()
                        annotation.startLine.remove()
                        annotation.endLine.remove()

                    elif type(annotation) == Rectangle:
                        annotation.rectangle.remove()

                    
                self.pyLong.project.groups[i+1].annotations.clear()                
                self.pyLong.project.groups.pop(i+1)
                self.pyLong.annotationsList.groups.removeItem(i+1)
                self.pyLong.canvas.updateLegends()
        self.accept()