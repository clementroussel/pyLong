from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.dialogAddSubplot import *


class DialogManageSubplots(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.pyLong = parent

        self.setWindowTitle("Subplots manager")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/subplotsManager.png')))

        mainLayout = QVBoxLayout()

        group = QGroupBox("Available subplots")
        layout = QVBoxLayout()

        self.subplotsList = QListWidget()
        for subplots in self.pyLong.project.subplots:
            self.subplotsList.addItem(subplots)

        layout.addWidget(self.subplotsList)

        sublayout = QHBoxLayout()

        sublayout.addWidget(QLabel())

        addSubplot = QPushButton("+")
        addSubplot.setAutoDefault(False)
        addSubplot.setFixedSize(QSize(25, 25))
        addSubplot.clicked.connect(self.addSubplot)
        sublayout.addWidget(addSubplot)

        deleteSubplot = QPushButton("-")
        deleteSubplot.setAutoDefault(False)
        deleteSubplot.setFixedSize(QSize(25, 25))
        deleteSubplot.clicked.connect(self.deleteSubplot)
        sublayout.addWidget(deleteSubplot)

        layout.addLayout(sublayout)

        group.setLayout(layout)

        mainLayout.addWidget(group)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def deleteSubplot(self):
        i = self.subplotsList.currentRow()
        subplot = self.pyLong.project.subplots[i]

        l = []
        for layout in self.pyLong.project.layouts:
            l += [subplot.id for subplot in layout.subplots]

        l += [data.subplot for data in self.pyLong.project.otherData]

        for line in self.pyLong.project.reminderLines:
            l += [subplot for subplot in line.subplots]

        if subplot not in l:
            self.pyLong.project.subplots.remove(subplot)
        else:
            alert = QMessageBox(self)
            alert.setText("Subplot {} is used and cannot be deleted.".format(subplot))
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

        self.updateList()

    def addSubplot(self):
        DialogAddSubplot(parent=self).exec_()
        self.updateList()

    def updateList(self):
        self.subplotsList.clear()
        for subplots in self.pyLong.project.subplots:
            self.subplotsList.addItem(subplots)
