from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionaries import *
from interface.checkableComboBox import *


class DialogConfigReminderLine(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.pyLong = parent.pyLong
        
        i = self.parent.list.currentRow()
        self.line = self.pyLong.project.reminderLines[i]
        
        self.setWindowTitle("Properties")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/config.png')))
        
        mainLayout = QVBoxLayout()

        layout = QGridLayout()
    
        label = QLabel("X :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.x = QDoubleSpinBox()
        self.x.setFixedWidth(90)
        self.x.setSuffix(" m")
        self.x.setLocale(QLocale('English'))
        self.x.setRange(0, 99999.999)
        self.x.setSingleStep(0.1)
        self.x.setDecimals(3)
        self.x.setValue(self.line.x)
        layout.addWidget(self.x, 0, 1)

        self.mainSubplot = QCheckBox("Draw in the main plot too")
        self.mainSubplot.setChecked(self.line.mainSubplot)
        self.mainSubplot.stateChanged.connect(self.updateInterface)
        layout.addWidget(self.mainSubplot, 1, 0, 1, 2)

        label = QLabel("Z :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.z = QDoubleSpinBox()
        self.z.setFixedWidth(90)
        self.z.setSuffix(" m")
        self.z.setLocale(QLocale('English'))
        self.z.setRange(0, 99999.999)
        self.z.setSingleStep(0.1)
        self.z.setDecimals(3)
        self.z.setValue(self.line.z)
        layout.addWidget(self.z, 2, 1)

        mainLayout.addLayout(layout)

        group = QGroupBox("Subplots")
        sublayout = QVBoxLayout()

        self.list = QListWidget()
        for subplot in self.pyLong.project.subplots:
            item = QListWidgetItem()
            item.setText(subplot)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if subplot in self.line.subplots:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list.addItem(item)

        sublayout.addWidget(self.list)
        group.setLayout(sublayout)


        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        mainLayout.addWidget(buttonBox)        
        self.setLayout(mainLayout)

    def validate(self):
        self.line.x = self.x.value()
        self.line.mainSubplot = self.mainSubplot.isChecked()
        self.line.z = self.z.value()
        self.line.subplots.clear()

        for i in range(self.list.count()):
            if self.list.item(i).checkState() == Qt.Checked:
                self.line.subplots.append(self.list.item(i).text())

        self.parent.update()
        self.accept()

    def updateInterface(self, value):
        self.z.setEnabled(value)
