from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np
from pyparsing import line_end

from pyLong.dictionaries import *

from interface.colorsComboBox import *


class DialogLinearAnnotation(QDialog):
    def __init__(self, parent) :
        super().__init__(parent=parent)
        
        self.setModal(False)
        
        self.pyLong = parent
        
        i = self.pyLong.annotationsList.groups.currentIndex()
        j = self.pyLong.annotationsList.list.currentRow()
        self.annotation = self.pyLong.project.groups[i].annotations[j]
        
        self.setWindowTitle("Linear annotation")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/linearAnnotation.png')))
 
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.title = QLineEdit()
        self.title.setText(self.annotation.title)
        self.title.textChanged.connect(self.updateTitle)
        layout.addWidget(self.title)  
        
        mainLayout.addLayout(layout)
        
        group = QGroupBox("Text")
        layout = QGridLayout()
        
        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.label = QLineEdit()
        self.label.setMaxLength(50)
        self.label.setText(self.annotation.label)
        self.label.textEdited.connect(self.update)
        layout.addWidget(self.label, 0, 1)
        
        label = QLabel("Size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.textSize = QDoubleSpinBox()
        self.textSize.setMaximumWidth(50)
        self.textSize.setLocale(QLocale('English'))
        self.textSize.setRange(0, 99.9)
        self.textSize.setDecimals(1)
        self.textSize.setSingleStep(0.1)
        self.textSize.setValue(self.annotation.labelProperties['size'])
        self.textSize.valueChanged.connect(self.update)
        layout.addWidget(self.textSize, 1, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.textColor = ColorsComboBox(self.pyLong.appctxt)
        self.textColor.setCurrentText(self.annotation.labelProperties['color'])
        self.textColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.textColor, 2, 1)
        
        label = QLabel("Vertical shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3 ,0)
        
        self.verticalShift = QDoubleSpinBox()
        self.verticalShift.setMaximumWidth(65)
        self.verticalShift.setLocale(QLocale('English'))
        self.verticalShift.setSuffix(" m")
        self.verticalShift.setRange(-9999, 9999)
        self.verticalShift.setDecimals(1)
        self.verticalShift.setSingleStep(0.1)
        self.verticalShift.setValue(self.annotation.labelProperties['vertical shift'])
        self.verticalShift.valueChanged.connect(self.update)
        layout.addWidget(self.verticalShift, 3, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Limits")
        layout = QGridLayout()
        
        label = QLabel("X start :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.xStart = QDoubleSpinBox()
        self.xStart.setMaximumWidth(90)
        self.xStart.setSuffix(" m")
        self.xStart.setLocale(QLocale('English'))
        self.xStart.setRange(-99999.999, 99999.999)
        self.xStart.setDecimals(3)
        self.xStart.setSingleStep(0.1)
        self.xStart.setValue(self.annotation.arrowProperties['x start'])
        self.xStart.valueChanged.connect(self.update)
        layout.addWidget(self.xStart, 0, 1)
        
        pointStart = QPushButton()
        pointStart.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        pointStart.setIconSize(QSize(12,12))
        pointStart.setMaximumWidth(25)
        pointStart.setAutoDefault(False)
        pointStart.clicked.connect(self.pointStart)
        layout.addWidget(pointStart, 0, 2)

        label = QLabel("X end :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.xEnd = QDoubleSpinBox()
        self.xEnd.setMaximumWidth(90)
        self.xEnd.setSuffix(" m")
        self.xEnd.setLocale(QLocale('English'))
        self.xEnd.setRange(-99999.999, 99999.999)
        self.xEnd.setDecimals(3)
        self.xEnd.setSingleStep(0.1)
        self.xEnd.setValue(self.annotation.arrowProperties['x end'])
        self.xEnd.valueChanged.connect(self.update)
        layout.addWidget(self.xEnd, 1, 1)
        
        pointEnd = QPushButton()
        pointEnd.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        pointEnd.setIconSize(QSize(12,12))
        pointEnd.setMaximumWidth(25)
        pointEnd.setAutoDefault(False)
        pointEnd.clicked.connect(self.pointEnd)
        layout.addWidget(pointEnd, 1, 2)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Arrow")
        layout = QGridLayout()
        
        sublayout = QHBoxLayout()
        
        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label)
        
        self.zArrow = QDoubleSpinBox()
        self.zArrow.setMaximumWidth(90)
        self.zArrow.setSuffix(" m")
        self.zArrow.setLocale(QLocale('English'))
        self.zArrow.setRange(-99999.999, 99999.999)
        self.zArrow.setDecimals(3)
        self.zArrow.setSingleStep(0.1)
        self.zArrow.setValue(self.annotation.arrowProperties['z coordinate'])
        self.zArrow.valueChanged.connect(self.update)
        sublayout.addWidget(self.zArrow)
        
        pointZ = QPushButton()
        pointZ.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        pointZ.setIconSize(QSize(12,12))
        pointZ.setMaximumWidth(25)
        pointZ.setAutoDefault(False)
        pointZ.clicked.connect(self.pointZ)
        sublayout.addWidget(pointZ)
        
        layout.addLayout(sublayout, 0, 0, 1, 2)
        
        label = QLabel("Arrow style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.arrowStyle = QComboBox()
        self.arrowStyle.addItem("-")
        self.arrowStyle.addItem("<->")
        self.arrowStyle.addItem("<|-|>")
        self.arrowStyle.setCurrentText(self.annotation.arrowProperties['arrow style'])
        self.arrowStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.arrowStyle, 1, 1)
        
        label = QLabel("Line style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.lineStyle = QComboBox()
        self.lineStyle.insertItems(0, list(lineStyles.keys()))
        self.lineStyle.setCurrentText(self.annotation.arrowProperties['line style'])
        self.lineStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineStyle, 2, 1)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.thickness = QDoubleSpinBox()
        self.thickness.setMaximumWidth(50)
        self.thickness.setLocale(QLocale('English'))
        self.thickness.setRange(0, 99.9)
        self.thickness.setDecimals(1)
        self.thickness.setSingleStep(0.1)
        self.thickness.setValue(self.annotation.arrowProperties['thickness'])
        self.thickness.valueChanged.connect(self.update)
        layout.addWidget(self.thickness, 3, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.arrowColor = ColorsComboBox(self.pyLong.appctxt)
        self.arrowColor.setCurrentText(self.annotation.arrowProperties['color'])
        self.arrowColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.arrowColor, 4, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Opacity and order")
        layout = QGridLayout()
        
        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.opacity = QDoubleSpinBox()
        self.opacity.setMaximumWidth(45)
        self.opacity.setLocale(QLocale('English'))
        self.opacity.setRange(0,1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.annotation.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 0, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 2)
        
        self.order = QSpinBox()
        self.order.setMaximumWidth(45)
        self.order.setLocale(QLocale('English'))
        self.order.setRange(1,99)
        self.order.setSingleStep(1)
        self.order.setValue(self.annotation.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 0, 3)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        
    def validate(self):
        self.pyLong.checkNavigationTools()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.update()
        self.accept()

    def updateTitle(self):
        self.annotation.title = self.title.text()
        self.pyLong.annotationsList.updateList()
        
    def update(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass

        self.annotation.label = self.label.text()
        self.annotation.labelProperties['size'] = self.textSize.value()
        self.annotation.labelProperties['color'] = self.textColor.currentText()
        self.annotation.labelProperties['vertical shift'] = self.verticalShift.value()
        
        self.annotation.arrowProperties['x start'] = self.xStart.value()
        self.annotation.arrowProperties['x end'] = self.xEnd.value()
        self.annotation.arrowProperties['z coordinate'] = self.zArrow.value()
        self.annotation.arrowProperties['arrow style'] = self.arrowStyle.currentText()
        self.annotation.arrowProperties['line style'] = self.lineStyle.currentText()
        self.annotation.arrowProperties['color'] = self.arrowColor.currentText()
        self.annotation.arrowProperties['thickness'] = self.thickness.value()
        
        self.annotation.opacity = self.opacity.value()
        self.annotation.order = self.order.value()
        
        self.annotation.update()

        self.pyLong.canvas.draw()
        
    def pointStart(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickStart)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickStart(self, event):
        try:
            self.xStart.setValue(event.xdata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.update()
        
    def pointEnd(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickEnd)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickEnd(self, event):
        try:
            self.xEnd.setValue(event.xdata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.update()
        
    def pointZ(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickAltitude)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickAltitude(self, event):
        try:
            self.zArrow.setValue(event.ydata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.update()
        
    def closeEvent(self, event):
        self.pyLong.checkNavigationTools()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
    def reject(self):
        self.pyLong.checkNavigationTools()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        self.accept()
