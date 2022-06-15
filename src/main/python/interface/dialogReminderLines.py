from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.reminderLine import *

from interface.dialogConfigReminderLine import *

from pyLong.dictionaries import *


class DialogReminderLines(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]

        self.setMinimumWidth(225)
        self.setWindowTitle("Reminder lines manager")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/reminderLinesManager.png')))
        
        mainLayout = QVBoxLayout()
        
        self.list = QListWidget()
        self.list.doubleClicked.connect(self.properties)
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.itemChanged.connect(self.activate)
        for line in self.pyLong.project.reminderLines:
            item = QListWidgetItem()
            item.setText("X = {} m".format(line.x))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if line.active:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list.addItem(item)

        mainLayout.addWidget(self.list)

        layout = QHBoxLayout()

        moveUp = QPushButton()
        moveUp.setAutoDefault(False)
        moveUp.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/moveUp.png')))
        moveUp.setFixedSize(QSize(25, 25))
        moveUp.clicked.connect(self.moveUp)
        layout.addWidget(moveUp)

        moveDown = QPushButton()
        moveDown.setAutoDefault(False)
        moveDown.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/moveDown.png')))
        moveDown.setFixedSize(QSize(25, 25))
        moveDown.clicked.connect(self.moveDown)
        layout.addWidget(moveDown)

        layout.addWidget(QLabel())

        properties = QPushButton()
        properties.setAutoDefault(False)
        properties.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/config.png')))
        properties.setFixedSize(QSize(25, 25))
        properties.clicked.connect(self.properties)
        layout.addWidget(properties)

        layout.addWidget(QLabel())

        add = QPushButton("+")
        add.setAutoDefault(False)
        add.setFixedSize(QSize(25, 25))
        add.clicked.connect(self.add)
        layout.addWidget(add)

        delete = QPushButton("-")
        delete.setAutoDefault(False)
        delete.setFixedSize(QSize(25, 25))
        delete.clicked.connect(self.delete)
        layout.addWidget(delete)

        mainLayout.addLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)

        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def activate(self):
        for i in range(self.list.count()):
            line = self.pyLong.project.reminderLines[i]
            if self.list.item(i).checkState() == Qt.Checked:
                line.active = True
            else:
                line.active = False

    def validate(self):
        self.apply()
        self.accept()

    def apply(self):
        self.pyLong.canvas.updateFigure()

    def moveUp(self):
        self.pyLong.project.reminderLines.sort()
        self.update()

    def moveDown(self):
        self.pyLong.project.reminderLines.sort(reverse=True)
        self.update()

    def properties(self):
        if self.selection():
            DialogConfigReminderLine(parent=self).exec_()

    def selection(self):
        n = self.list.count()
        selections = []

        for i in range(n):
            selections.append(self.list.item(i).isSelected())

        return n > 0 and True in selections

    def delete(self):
        if self.selection():
            indexes = []
            for item in self.list.selectedIndexes():
                indexes.append(item.row())

            indexes.sort()
            indexes.reverse()

            if len(indexes) == 1:
                i = indexes[0]

                self.pyLong.project.reminderLines.pop(i)
                self.update()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

            else:
                for i in indexes:
                    self.pyLong.project.reminderLines.pop(i)

                self.update()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

        else:
            pass

    def add(self):
        line = ReminderLine()
        line.subplots = list(self.pyLong.project.subplots)
        self.pyLong.project.reminderLines.append(line)
        self.update()

    def update(self):
        self.list.clear()
        for line in self.pyLong.project.reminderLines:
            item = QListWidgetItem()
            item.setText("X = {} m".format(line.x))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if line.active:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list.addItem(item)
