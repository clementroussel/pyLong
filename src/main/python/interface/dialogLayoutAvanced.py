from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.dialogChoiceSubplot import *
from interface.dialogLayoutSubplot import *


class DialogLayoutAdvanced(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.pyLong = parent

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]

        self.setWindowTitle("Advanced layout {} properties".format(self.layout.title))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/advancedLayout.png')))
        
        mainLayout = QVBoxLayout()

        layout = QGridLayout()

        label = QLabel("Subdivisions :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.subdivisions = QSpinBox()
        self.subdivisions.setFixedWidth(40)
        self.subdivisions.setRange(1, 99)
        self.subdivisions.setValue(self.layout.subdivisions)
        self.subdivisions.valueChanged.connect(self.update)
        layout.addWidget(self.subdivisions, 0, 1)

        label = QLabel("Spacing :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.spacing = QDoubleSpinBox()
        self.spacing.setFixedWidth(55)
        self.spacing.setLocale(QLocale('English'))
        self.spacing.setRange(0, 1)
        self.spacing.setSingleStep(0.05)
        self.spacing.setDecimals(3)
        self.spacing.setValue(self.layout.hspace)
        self.spacing.valueChanged.connect(self.updateSpacing)
        layout.addWidget(self.spacing, 1, 1)

        mainLayout.addLayout(layout)

        group = QGroupBox("Subplots inserted")
        layout = QVBoxLayout()

        self.subplotsList = QListWidget()
        self.subplotsList.doubleClicked.connect(self.subplotProperties)
        for subplot in self.layout.subplots:
            self.subplotsList.addItem("{}".format(subplot.id))

        layout.addWidget(self.subplotsList)

        sublayout = QHBoxLayout()

        moveUp = QPushButton()
        moveUp.setAutoDefault(False)
        moveUp.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/moveUp.png')))
        moveUp.setFixedSize(QSize(25, 25))
        moveUp.clicked.connect(self.moveUp)
        sublayout.addWidget(moveUp)

        moveDown = QPushButton()
        moveDown.setAutoDefault(False)
        moveDown.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/moveDown.png')))
        moveDown.setFixedSize(QSize(25, 25))
        moveDown.clicked.connect(self.moveDown)
        sublayout.addWidget(moveDown)

        sublayout.addWidget(QLabel())

        properties = QPushButton()
        properties.setAutoDefault(False)
        properties.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/layout.png')))
        properties.setFixedSize(QSize(25, 25))
        properties.clicked.connect(self.subplotProperties)
        sublayout.addWidget(properties)

        sublayout.addWidget(QLabel())

        addSubplot = QPushButton("+")
        addSubplot.setAutoDefault(False)
        addSubplot.setFixedSize(QSize(25, 25))
        addSubplot.clicked.connect(self.addSubplot)
        sublayout.addWidget(addSubplot)

        removeSubplot = QPushButton("-")
        removeSubplot.setAutoDefault(False)
        removeSubplot.setFixedSize(QSize(25, 25))
        removeSubplot.clicked.connect(self.removeSubplot)
        sublayout.addWidget(removeSubplot)

        layout.addLayout(sublayout)

        group.setLayout(layout)

        mainLayout.addWidget(group)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

        self.checkSubdivisions()

    def moveUp(self):
        n = self.subplotsList.count()
        selections = []

        for i in range(n):
            selections.append(self.subplotsList.item(i).isSelected())

        i = self.subplotsList.currentRow()
        if True in selections and i > 0:
            self.layout.subplots[i-1], self.layout.subplots[i] = self.layout.subplots[i], self.layout.subplots[i-1]

            self.updateSubplotsList()
            self.subplotsList.setCurrentRow(i-1)
            self.pyLong.canvas.updateFigure()

    def moveDown(self):
        n = self.subplotsList.count()
        selections = []

        for i in range(n):
            selections.append(self.subplotsList.item(i).isSelected())

        i = self.subplotsList.currentRow()
        if True in selections and i < n-1:
            self.layout.subplots[i + 1], self.layout.subplots[i] = self.layout.subplots[i], self.layout.subplots[i + 1]

            self.updateSubplotsList()
            self.subplotsList.setCurrentRow(i + 1)
            self.pyLong.canvas.updateFigure()

    def subplotProperties(self):
        n = self.subplotsList.count()
        selections = []

        for i in range(n):
            selections.append(self.subplotsList.item(i).isSelected())

        if True in selections:
            DialogLayoutSubplot(parent=self).exec_()

    def addSubplot(self):
        n = 0
        for subplot in self.layout.subplots:
            n += subplot.subdivisions
        if self.subdivisions.value() > n+1:
            DialogChoixSubplot(parent=self).exec_()
            self.updateSubplotsList()
            self.checkSubdivisions()
            self.update()
        else:
            alert = QMessageBox(self)
            alert.setText("Increase the number of subdivisions to add a new subplot.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def updateSubplotsList(self):
        self.subplotsList.clear()
        for subplot in self.layout.subplots:
            self.subplotsList.addItem("{}".format(subplot.id))

    def update(self):
        self.layout.subdivisions = self.subdivisions.value()
        self.pyLong.canvas.updateFigure()

    def checkSubdivisions(self):
        n = 0
        for subplot in self.layout.subplots:
            n += subplot.subdivisions

        self.subdivisions.setMinimum(n+1)

    def updateSpacing(self):
        self.layout.hspace = self.spacing.value()

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)

        self.pyLong.canvas.draw()

    def removeSubplot(self):
        i = self.subplotsList.currentRow()
        if i != -1:
            self.layout.subplots.pop(i)
        self.updateSubplotsList()
        self.checkSubdivisions()
        self.update()
