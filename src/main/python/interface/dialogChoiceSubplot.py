from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.subplot import *


class DialogChoixSubplot(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.pyLong = parent.pyLong

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]

        self.setWindowTitle("Subplot choice")

        mainLayout = QVBoxLayout()

        group = QGroupBox("Available subplots")
        layout = QVBoxLayout()

        self.subplotsList = QListWidget()
        self.subplotsList.doubleClicked.connect(self.validate)
        list = []
        for i in range(self.parent.subplotsList.count()):
            list.append(self.parent.subplotsList.item(i).text())
        for subplots in self.pyLong.project.subplots:
            if subplots not in list:
                self.subplotsList.addItem(subplots)

        layout.addWidget(self.subplotsList)

        group.setLayout(layout)

        mainLayout.addWidget(group)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def validate(self):
        try:
            i = self.subplotsList.currentIndex()
            if i == -1:
                pass
            else:
                subplot = Subplot()
                subplot.id = self.subplotsList.currentItem().text()

                self.layout.subplots.append(subplot)

                self.accept()
        except:
            self.accept()
