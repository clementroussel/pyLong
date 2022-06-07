from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.dictionaries import *

from interface.colorsComboBox import *


class DialogVerticalAnnotation(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setModal(False)
        
        self.pyLong = parent
        
        i = self.pyLong.annotationsList.groups.currentIndex()
        j = self.pyLong.annotationsList.list.currentRow()
        self.annotation = self.pyLong.project.groups[i].annotations[j]
        
        self.setWindowTitle("Vertical annotation")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/verticalAnnotation.png')))
    
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
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Position")
        layout = QGridLayout()
        
        point = QPushButton()
        point.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        point.setIconSize(QSize(12,12))
        point.setMaximumWidth(25)
        point.setAutoDefault(False)
        point.clicked.connect(self.point)
        layout.addWidget(point, 0, 0)
        
        label = QLabel("Profile :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.profiles = QComboBox()
        
        for zprofile, sprofile in self.pyLong.project.profiles:
            self.profiles.addItem(zprofile.title)
    
        layout.addWidget(self.profiles, 0, 2)
        
        label = QLabel("X coordinate :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.x = QDoubleSpinBox()
        self.x.setMaximumWidth(90)
        self.x.setSuffix(" m")
        self.x.setLocale(QLocale('English'))
        self.x.setRange(-99999.999, 99999.999)
        self.x.setDecimals(3)
        self.x.setSingleStep(0.1)
        self.x.setValue(self.annotation.position['x coordinate'])
        self.x.valueChanged.connect(self.update)
        layout.addWidget(self.x, 1, 1)
        
        xInterpolation = QPushButton("x, z = f(x)")
        xInterpolation.setAutoDefault(False)
        xInterpolation.clicked.connect(self.xSolver)
        layout.addWidget(xInterpolation, 1, 2)

        label = QLabel("Z coordinate :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.z = QDoubleSpinBox()
        self.z.setMaximumWidth(90)
        self.z.setSuffix(" m")
        self.z.setLocale(QLocale('English'))
        self.z.setRange(-99999.999, 99999.999)
        self.z.setDecimals(3)
        self.z.setSingleStep(0.1)
        self.z.setValue(self.annotation.position['z coordinate'])
        self.z.valueChanged.connect(self.update)
        layout.addWidget(self.z, 2, 1)

        zInterpolation = QPushButton("z = f(x)")
        zInterpolation.setAutoDefault(False)
        zInterpolation.clicked.connect(self.zInterpolation)
        layout.addWidget(zInterpolation, 2, 2)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Arrow")
        layout = QGridLayout()
        
        label = QLabel("Arrow style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.arrowStyle = QComboBox()
        self.arrowStyle.addItem("-")
        self.arrowStyle.addItem("->")
        self.arrowStyle.addItem("-|>")
        self.arrowStyle.addItem("<-")
        self.arrowStyle.addItem("<->")
        self.arrowStyle.addItem("<|-")
        self.arrowStyle.addItem("<|-|>")
        self.arrowStyle.setCurrentText(self.annotation.arrowProperties['arrow style'])
        self.arrowStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.arrowStyle, 0, 1)
        
        label = QLabel("Line style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.lineStyle = QComboBox()
        self.lineStyle.insertItems(0, list(lineStyles.keys()))
        self.lineStyle.setCurrentText(self.annotation.arrowProperties['line style'])
        self.lineStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineStyle, 1, 1)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.thickness = QDoubleSpinBox()
        self.thickness.setMaximumWidth(50)
        self.thickness.setLocale(QLocale('English'))
        self.thickness.setRange(0, 99.9)
        self.thickness.setDecimals(1)
        self.thickness.setSingleStep(0.1)
        self.thickness.setValue(self.annotation.arrowProperties['thickness'])
        self.thickness.valueChanged.connect(self.update)
        layout.addWidget(self.thickness, 2, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.arrowColor = ColorsComboBox(self.pyLong.appctxt)
        self.arrowColor.setCurrentText(self.annotation.arrowProperties['color'])
        self.arrowColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.arrowColor, 3, 1)
        
        label = QLabel("Length :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.length = QDoubleSpinBox()
        self.length.setMaximumWidth(70)
        self.length.setLocale(QLocale('English'))
        self.length.setSuffix(" m")
        self.length.setRange(0, 9999.9)
        self.length.setDecimals(1)
        self.length.setSingleStep(0.1)
        self.length.setValue(self.annotation.arrowProperties['length'])
        self.length.valueChanged.connect(self.update)
        layout.addWidget(self.length, 4, 1)
        
        label = QLabel("Vertical shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.verticalShift = QDoubleSpinBox()
        self.verticalShift.setMaximumWidth(70)
        self.verticalShift.setLocale(QLocale('English'))
        self.verticalShift.setSuffix(" m")
        self.verticalShift.setRange(0, 9999.9)
        self.verticalShift.setDecimals(1)
        self.verticalShift.setSingleStep(0.1)
        self.verticalShift.setValue(self.annotation.arrowProperties['vertical shift'])
        self.verticalShift.valueChanged.connect(self.update)
        layout.addWidget(self.verticalShift, 5, 1)
        
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
        self.opacity.setRange(0, 1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.annotation.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 0, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.order = QSpinBox()
        self.order.setMaximumWidth(45)
        self.order.setLocale(QLocale('English'))
        self.order.setRange(1, 99)
        self.order.setSingleStep(1)
        self.order.setValue(self.annotation.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 1, 1)
        
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
        self.annotation.position['x coordinate'] = self.x.value()
        self.annotation.position['z coordinate'] = self.z.value()
        self.annotation.arrowProperties['arrow style'] = self.arrowStyle.currentText()
        self.annotation.arrowProperties['line style'] = self.lineStyle.currentText()
        self.annotation.arrowProperties['thickness'] = self.thickness.value()
        self.annotation.arrowProperties['color'] = self.arrowColor.currentText()
        self.annotation.arrowProperties['length'] = self.length.value()
        self.annotation.arrowProperties['vertical shift'] = self.verticalShift.value()
        self.annotation.opacity = self.opacity.value()
        self.annotation.order = self.order.value()
        
        self.annotation.update()
        
        self.pyLong.canvas.draw()
        
    def xSolver(self):
        z = self.z.value()
        x = self.x.value()
        
        if self.profiles.currentIndex() != -1:
            i = self.profiles.currentIndex()
            zprofile, sprofile = self.pyLong.project.profiles[i]
        else:
            alert = QMessageBox(self)
            alert.setText("No profile available.")
            alert.exec_()
            return 0

        if z >= np.min(zprofile.z) and z <= np.max(zprofile.z):
            try:
                x = zprofile.solve(z, x)
                self.x.setValue(x)
            except:
                pass
        else:
            alert = QMessageBox(self)
            alert.setText("Z coordinate out of range.")
            alert.exec_()

        self.update()                          
        
    def zInterpolation(self):
        x = self.x.value()
        
        if self.profiles.currentIndex() != -1:
            i = self.profiles.currentIndex()
            zprofile, sprofile = self.pyLong.project.profiles[i]
        else:
            alert = QMessageBox(self)
            alert.setText("No profile available.")
            alert.exec_()
            return 0
        
        if x >= np.min(zprofile.x) and x <= np.max(zprofile.x):
            z = zprofile.interpolate(x)
            self.z.setValue(z)
        else:
            alert = QMessageBox(self)
            alert.setText("X coordinate out of range.")
            alert.exec_()
            
        self.update()
        
    def point(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclick)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclick(self, event):
        try:
            self.x.setValue(event.xdata)
            self.z.setValue(event.ydata)
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
