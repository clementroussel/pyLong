from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogManageGroups(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Groups manager")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/groupsManager.png')))
        
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        sublayout = QVBoxLayout()
        
        self.leftGroupsList = QComboBox()
        for group in self.pyLong.project.groups:
            self.leftGroupsList.addItem(group.title)
        self.leftGroupsList.currentIndexChanged.connect(self.updateInterface)
        
        self.leftAnnotationsList = QListWidget()
        self.leftAnnotationsList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        sublayout.addWidget(self.leftGroupsList)
        sublayout.addWidget(self.leftAnnotationsList)
        
        layout.addLayout(sublayout)
        
        sublayout = QVBoxLayout()

        moveToRight = QPushButton()
        moveToRight.setAutoDefault(False)
        moveToRight.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/right.png')))
        moveToRight.clicked.connect(self.moveToRight)

        moveToLeft = QPushButton()
        moveToLeft.setAutoDefault(False)
        moveToLeft.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/left.png')))
        moveToLeft.clicked.connect(self.moveToLeft)

        sublayout.addWidget(moveToRight)
        sublayout.addWidget(moveToLeft)
        
        layout.addLayout(sublayout)
        
        sublayout = QVBoxLayout()
        
        self.rightGroupsList = QComboBox()
        for group in self.pyLong.project.groups:
            self.rightGroupsList.addItem(group.title)
        self.rightGroupsList.currentIndexChanged.connect(self.updateInterface)
        
        self.rightAnnotationsList = QListWidget()
        self.rightAnnotationsList.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        sublayout.addWidget(self.rightGroupsList)
        sublayout.addWidget(self.rightAnnotationsList)
        
        layout.addLayout(sublayout)        

        mainLayout.addLayout(layout)
        
        self.setLayout(mainLayout)

        self.updateInterface()

    def updateInterface(self):
        self.leftAnnotationsList.clear()
        self.rightAnnotationsList.clear()

        i = self.leftGroupsList.currentIndex()
        for annotation in self.pyLong.project.groups[i].annotations :
            self.leftAnnotationsList.addItem(annotation.title)

        j = self.rightGroupsList.currentIndex()
        for annotation in self.pyLong.project.groups[j].annotations :
            self.rightAnnotationsList.addItem(annotation.title)

    def moveToRight(self):
        i = self.leftGroupsList.currentIndex()
        j = self.rightGroupsList.currentIndex()

        indexes = []
        for item in self.leftAnnotationsList.selectedIndexes():
            indexes.append(item.row())

        indexes.sort()
        indexes.reverse()

        for k in indexes:
            annotation = self.pyLong.project.groups[i].annotations[k]
            self.pyLong.project.groups[j].annotations.append(annotation)
            self.pyLong.project.groups[i].annotations.pop(k)

        self.updateInterface()

    def moveToLeft(self):
        i = self.leftGroupsList.currentIndex()
        j = self.rightGroupsList.currentIndex()

        indexes = []
        for item in self.rightAnnotationsList.selectedIndexes():
            indexes.append(item.row())

        indexes.sort()
        indexes.reverse()

        for k in indexes:
            annotation = self.pyLong.project.groups[j].annotations[k]
            self.pyLong.project.groups[i].annotations.append(annotation)
            self.pyLong.project.groups[j].annotations.pop(k)

        self.updateInterface()
