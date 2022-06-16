from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *

from pyLong.dictionaries import *


class DialogDataOptions(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
        
        i = self.pyLong.otherDataList.list.currentRow()
        self.data = self.pyLong.project.otherData[i]

        mainLayout = QVBoxLayout()

        self.setWindowTitle("Style <{}> ".format(self.data.title))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/style.png')))

        layout = QHBoxLayout()

        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)

        self.title = QLineEdit()
        self.title.setText(self.data.title)
        self.title.textChanged.connect(self.updateTitle)
        layout.addWidget(self.title)

        mainLayout.addLayout(layout)

        layout = QHBoxLayout()

        label = QLabel("Subplot : {}".format(self.data.subplot))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)

        layout.addWidget(QLabel())

        mainLayout.addLayout(layout)

        layout = QGridLayout()
        
        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.label = QLineEdit()
        self.label.setText(self.data.label)
        self.label.textChanged.connect(self.updateLabel)
        layout.addWidget(self.label, 1, 1)
        
        label = QLabel("Line style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.lineStyle = QComboBox()
        self.lineStyle.insertItems(0, list(lineStyles.keys()))
        self.lineStyle.setCurrentText(self.data.lineProperties['style'])
        self.lineStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineStyle, 2, 1)
        
        label = QLabel("Line color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 3, 0)
        
        self.lineColor = ColorsComboBox(self.pyLong.appctxt)
        self.lineColor.setCurrentText(self.data.lineProperties['color'])
        self.lineColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineColor, 3, 1)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 4, 0)
        
        self.thickness = QDoubleSpinBox()
        self.thickness.setMaximumWidth(50)
        self.thickness.setLocale(QLocale('English'))
        self.thickness.setRange(0, 99.9)
        self.thickness.setDecimals(1)
        self.thickness.setSingleStep(0.1)
        self.thickness.setValue(self.data.lineProperties['thickness'])
        self.thickness.valueChanged.connect(self.update)
        layout.addWidget(self.thickness, 4, 1)

        label = QLabel("Marker style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 5, 0)
        
        self.markerStyle = QComboBox()
        self.markerStyle.insertItems(0, list(markerStyles.keys()))
        self.markerStyle.setCurrentText(self.data.markerProperties['style'])
        self.markerStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.markerStyle, 5, 1)
        
        label = QLabel("Marker color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 6, 0)
        
        self.markerColor = ColorsComboBox(self.pyLong.appctxt)
        self.markerColor.setCurrentText(self.data.markerProperties['color'])
        self.markerColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.markerColor, 6, 1)
        
        label = QLabel("Marker size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 7, 0)
        
        self.markerSize = QDoubleSpinBox()
        self.markerSize.setMaximumWidth(50)
        self.markerSize.setLocale(QLocale('English'))
        self.markerSize.setRange(0, 99.9)
        self.markerSize.setSingleStep(0.1)
        self.markerSize.setDecimals(1)
        self.markerSize.setValue(self.data.markerProperties['size'])
        self.markerSize.valueChanged.connect(self.update)
        layout.addWidget(self.markerSize, 7, 1)
        
        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 8, 0)
        
        self.opacity = QDoubleSpinBox()
        self.opacity.setFixedWidth(45)
        self.opacity.setLocale(QLocale('English'))
        self.opacity.setRange(0, 1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.data.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 8, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 9, 0)
        
        self.order = QSpinBox()
        self.order.setFixedWidth(45)
        self.order.setRange(0, 99)
        self.order.setValue(self.data.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 9, 1)

        mainLayout.addLayout(layout)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def updateTitle(self, value):
        self.data.title = value
        self.setWindowTitle("Style <{}>".format(value))
        self.pyLong.otherDataList.update()

    def updateLabel(self):
        self.data.label = self.label.text()
        self.data.update()

        self.pyLong.canvas.updateLegends()

    def update(self):
        self.data.label = self.label.text()
        self.data.lineProperties['style'] = self.lineStyle.currentText()
        self.data.lineProperties['color'] = self.lineColor.currentText()
        self.data.lineProperties['thickness'] = self.thickness.value()
        self.data.markerProperties['style'] = self.markerStyle.currentText()
        self.data.markerProperties['color'] = self.markerColor.currentText()
        self.data.markerProperties['size'] = self.markerSize.value()
        self.data.opacity = self.opacity.value()
        self.data.order = self.order.value()

        self.data.update()
        self.pyLong.canvas.draw()
