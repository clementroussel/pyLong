from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.dictionaries import *

from interface.colorsComboBox import *


class DialogInterval(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        self.setModal(False)
        
        self.pyLong = parent

        i = self.pyLong.annotationsList.groups.currentIndex()
        j = self.pyLong.annotationsList.list.currentRow()
        self.annotation = self.pyLong.project.groups[i].annotations[j]
        
        self.setWindowTitle("Interval")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/interval.png')))
        
        mainLayout = QGridLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.title = QLineEdit()
        self.title.setText(self.annotation.title)
        self.title.textChanged.connect(self.updateTitle)
        layout.addWidget(self.title)  
        
        mainLayout.addLayout(layout, 0, 0, 1, 2)
        
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
        
        self.size = QDoubleSpinBox()
        self.size.setMaximumWidth(50)
        self.size.setLocale(QLocale('English'))
        self.size.setRange(0, 99.9)
        self.size.setDecimals(1)
        self.size.setSingleStep(0.1)
        self.size.setValue(self.annotation.labelProperties['size'])
        self.size.valueChanged.connect(self.update)
        layout.addWidget(self.size, 1, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.textColor = ColorsComboBox(self.pyLong.appctxt)
        self.textColor.setCurrentText(self.annotation.labelProperties['color'])
        self.textColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.textColor, 2, 1)
        
        sublayout = QHBoxLayout()
        
        label = QLabel("Z :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label)
        
        self.zText = QDoubleSpinBox()
        self.zText.setMaximumWidth(90)
        self.zText.setSuffix(" m")
        self.zText.setLocale(QLocale('English'))
        self.zText.setRange(0, 99999.999)
        self.zText.setDecimals(3)
        self.zText.setSingleStep(0.1)
        self.zText.setValue(self.annotation.labelProperties['z coordinate'])
        self.zText.valueChanged.connect(self.update)
        sublayout.addWidget(self.zText)
        
        pointZ = QPushButton()
        pointZ.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        pointZ.setIconSize(QSize(12,12))
        pointZ.setMaximumWidth(25)
        pointZ.setAutoDefault(False)
        pointZ.clicked.connect(self.pointZ)
        sublayout.addWidget(pointZ)
        
        layout.addLayout(sublayout, 3, 0, 1, 3)
        
        group.setLayout(layout)
        mainLayout.addWidget(group, 1, 0)
        
        group = QGroupBox("Frame")
        layout = QGridLayout()
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.frameStyle = QComboBox()
        self.frameStyle.insertItems(0,list(lineStyles.keys()))
        self.frameStyle.setCurrentText(self.annotation.frameProperties['style'])
        self.frameStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.frameStyle, 0, 1)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.frameThickness = QDoubleSpinBox()
        self.frameThickness.setMaximumWidth(50)
        self.frameThickness.setLocale(QLocale('English'))
        self.frameThickness.setRange(0, 99.9)
        self.frameThickness.setDecimals(1)
        self.frameThickness.setSingleStep(0.1)
        self.frameThickness.setValue(self.annotation.frameProperties['thickness'])
        self.frameThickness.valueChanged.connect(self.update)
        layout.addWidget(self.frameThickness, 1, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.frameColor = ColorsComboBox(self.pyLong.appctxt)
        self.frameColor.setCurrentText(self.annotation.frameProperties['color'])
        self.frameColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.frameColor, 2, 1)
        
        layout.addWidget(QWidget(), 3, 0)
        
        group.setLayout(layout)
        mainLayout.addWidget(group, 1, 1)
        
        group = QGroupBox("Start")
        layout = QGridLayout()
        
        pointStart = QPushButton()
        pointStart.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        pointStart.setIconSize(QSize(12,12))
        pointStart.setMaximumWidth(25)
        pointStart.setAutoDefault(False)
        pointStart.clicked.connect(self.pointStart)
        layout.addWidget(pointStart, 0, 0)
        
        label = QLabel("Profile :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.startProfiles = QComboBox()
        
        for zprofile, sprofile in self.pyLong.project.profiles:
            self.startProfiles.addItem(zprofile.title)
            
        layout.addWidget(self.startProfiles, 0, 2)
        
        label = QLabel("X :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.xStart = QDoubleSpinBox()
        self.xStart.setMaximumWidth(90)
        self.xStart.setSuffix(" m")
        self.xStart.setLocale(QLocale('English'))
        self.xStart.setRange(0, 99999.999)
        self.xStart.setDecimals(3)
        self.xStart.setSingleStep(0.1)
        self.xStart.setValue(self.annotation.limits['x start'])
        self.xStart.valueChanged.connect(self.update)
        layout.addWidget(self.xStart, 1, 1)
        
        xStartInterpolation = QPushButton("x, z = f(x)")
        xStartInterpolation.setAutoDefault(False)
        xStartInterpolation.clicked.connect(lambda : self.xSolver('start'))
        layout.addWidget(xStartInterpolation, 1, 2)
        
        label = QLabel("Z :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.zStart = QDoubleSpinBox()
        self.zStart.setMaximumWidth(90)
        self.zStart.setSuffix(" m")
        self.zStart.setLocale(QLocale('English'))
        self.zStart.setRange(0, 99999.999)
        self.zStart.setDecimals(3)
        self.zStart.setSingleStep(0.1)
        self.zStart.setValue(self.annotation.limits['z start'])
        self.zStart.valueChanged.connect(self.update)
        layout.addWidget(self.zStart, 2, 1)
        
        zStartInterpolation = QPushButton("z = f(x)")
        zStartInterpolation.setAutoDefault(False)
        zStartInterpolation.clicked.connect(lambda : self.zInterpolation('start'))
        layout.addWidget(zStartInterpolation, 2, 2)
        
        group.setLayout(layout)
        mainLayout.addWidget(group, 2, 0)
        
        group = QGroupBox("End")
        layout = QGridLayout()
        
        pointEnd = QPushButton()
        pointEnd.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        pointEnd.setIconSize(QSize(12,12))
        pointEnd.setMaximumWidth(25)
        pointEnd.setAutoDefault(False)
        pointEnd.clicked.connect(self.pointEnd)
        layout.addWidget(pointEnd, 0, 0)
        
        label = QLabel("Profile :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.endProfiles = QComboBox()

        for zprofile, sprofile in self.pyLong.project.profiles:
            self.endProfiles.addItem(zprofile.title)
            
        layout.addWidget(self.endProfiles, 0, 2)
        
        label = QLabel("X :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.xEnd = QDoubleSpinBox()
        self.xEnd.setMaximumWidth(90)
        self.xEnd.setSuffix(" m")
        self.xEnd.setLocale(QLocale('English'))
        self.xEnd.setRange(0, 99999.999)
        self.xEnd.setDecimals(3)
        self.xEnd.setSingleStep(0.1)
        self.xEnd.setValue(self.annotation.limits['x end'])
        self.xEnd.valueChanged.connect(self.update)
        layout.addWidget(self.xEnd, 1, 1)
        
        xEndInterpolation = QPushButton("x, z = f(x)")
        xEndInterpolation.setAutoDefault(False)
        xEndInterpolation.clicked.connect(lambda : self.xSolver('end'))
        layout.addWidget(xEndInterpolation, 1, 2)

        label = QLabel("Z :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.zEnd = QDoubleSpinBox()
        self.zEnd.setMaximumWidth(90)
        self.zEnd.setSuffix(" m")
        self.zEnd.setLocale(QLocale('English'))
        self.zEnd.setRange(0, 99999.999)
        self.zEnd.setDecimals(3)
        self.zEnd.setSingleStep(0.1)
        self.zEnd.setValue(self.annotation.limits['z end'])
        self.zEnd.valueChanged.connect(self.update)
        layout.addWidget(self.zEnd, 2, 1)
        
        zEndInterpolation = QPushButton("z = f(x)")
        zEndInterpolation.setAutoDefault(False)
        zEndInterpolation.clicked.connect(lambda : self.zInterpolation('end'))
        layout.addWidget(zEndInterpolation, 2, 2)
        
        group.setLayout(layout)
        mainLayout.addWidget(group, 2, 1)
        
        group = QGroupBox("Lines")
        layout = QGridLayout()
        
        label = QLabel("Lower altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0) 
        
        self.lowerZ = QDoubleSpinBox()
        self.lowerZ.setMaximumWidth(90)
        self.lowerZ.setSuffix(" m")
        self.lowerZ.setLocale(QLocale('English'))
        self.lowerZ.setRange(-9999, 99999.999)
        self.lowerZ.setDecimals(3)
        self.lowerZ.setSingleStep(0.1)
        self.lowerZ.setValue(self.annotation.limits['z low'])
        self.lowerZ.valueChanged.connect(self.update)
        layout.addWidget(self.lowerZ, 0, 1)
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.lineStyle = QComboBox()
        self.lineStyle.insertItems(0, list(lineStyles.keys()))
        self.lineStyle.setCurrentText(self.annotation.limitsProperties['style'])
        self.lineStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineStyle, 1, 1)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.lineThickness = QDoubleSpinBox()
        self.lineThickness.setMaximumWidth(50)
        self.lineThickness.setLocale(QLocale('English'))
        self.lineThickness.setRange(0, 99.9)
        self.lineThickness.setDecimals(1)
        self.lineThickness.setSingleStep(0.1)
        self.lineThickness.setValue(self.annotation.limitsProperties['thickness'])
        self.lineThickness.valueChanged.connect(self.update)
        layout.addWidget(self.lineThickness, 2, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.lineColor = ColorsComboBox(self.pyLong.appctxt)
        self.lineColor.setCurrentText(self.annotation.limitsProperties['color'])
        self.lineColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineColor, 3, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group, 3, 0)
        
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
        layout.addWidget(label, 0, 2)
        
        self.order = QSpinBox()
        self.order.setMaximumWidth(45)
        self.order.setLocale(QLocale('English'))
        self.order.setRange(1, 99)
        self.order.setSingleStep(1)
        self.order.setValue(self.annotation.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 0, 3)
        
        group.setLayout(layout)
        mainLayout.addWidget(group, 4, 0)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
    
        mainLayout.addWidget(buttonBox, 5, 0, 1, 2)
        
        self.setLayout(mainLayout)
        
    def xSolver(self, where):
        if where == 'start':
            
            if self.startProfiles.currentIndex() != -1:
                i = self.startProfiles.currentIndex()
                zprofile, sprofile = self.pyLong.project.profiles[i]
            else:
                alert = QMessageBox(self)
                alert.setText("No profile available.")
                alert.exec_()
                return 0
            
            x = self.xStart.value()
            z = self.zStart.value()
            if z >= np.min(zprofile.z) and z <= np.max(zprofile.z):
                try:
                    x = zprofile.solve(z, x)
                    self.xStart.setValue(x)
                except:
                    pass
            else:
                alert = QMessageBox(self)
                alert.setText("Z coordinate out of range.")
                alert.exec_()
                 
        else:
            
            if self.endProfiles.currentIndex() != -1:
                i = self.endProfiles.currentIndex()
                zprofile, sprofile = self.pyLong.project.profiles[i]
            else:
                alert = QMessageBox(self)
                alert.setText("No profile available.")
                alert.exec_()
                return 0
            
            x = self.xEnd.value()
            z = self.zEnd.value()
            if x >= np.min(zprofile.z) and z <= np.max(zprofile.z):
                try:
                    x = zprofile.solve(z, x)
                    self.xEnd.setValue(x)
                except:
                    pass
            else:
                alert = QMessageBox(self)
                alert.setText("Z coordinate out of range.")
                alert.exec_()  
                
        self.update()
        
    def zInterpolation(self, where):
        if where == 'start':
            if self.startProfiles.currentIndex() != -1:
                i = self.startProfiles.currentIndex()
                zprofile, sprofile = self.pyLong.project.profiles[i]
            else:
                alert = QMessageBox(self)
                alert.setText("No profile available.")
                alert.exec_()
                return 0
            
            x = self.xStart.value()
            if x >= np.min(zprofile.x) and x <= np.max(zprofile.x):
                z = zprofile.interpolate(x)
                self.zStart.setValue(z)
            else:
                alert = QMessageBox(self)
                alert.setText("X coordinate out of range.")
                alert.exec_()
                 
        else:
            if self.endProfiles.currentIndex() != -1:
                i = self.endProfiles.currentIndex()
                zprofile, sprofile = self.pyLong.project.profiles[i]
            else:
                alert = QMessageBox(self)
                alert.setText("No profile available.")
                alert.ex
            
            x = self.xEnd.value()
            if x >= np.min(zprofile.x) and x <= np.max(zprofile.x):
                z = zprofile.interpolate(x)
                self.zEnd.setValue(z)
            else:
                alert = QMessageBox(self)
                alert.setText("X coordinate out of range.")
                alert.exec_()  
                
        self.update()
        
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
        self.annotation.labelProperties['z coordinate'] = self.zText.value()
        self.annotation.labelProperties['size'] = self.size.value()
        self.annotation.labelProperties['color'] = self.textColor.currentText()
        
        self.annotation.frameProperties['style'] = self.frameStyle.currentText()
        self.annotation.frameProperties['thickness'] = self.frameThickness.value()
        self.annotation.frameProperties['color'] = self.frameColor.currentText()
        
        self.annotation.limits['x start'] = self.xStart.value()
        self.annotation.limits['z start'] = self.zStart.value()
        
        self.annotation.limits['x end'] = self.xEnd.value()
        self.annotation.limits['z end'] = self.zEnd.value()
        
        self.annotation.limits['z low'] = self.lowerZ.value()
        
        self.annotation.limitsProperties['style'] = self.lineStyle.currentText()
        self.annotation.limitsProperties['color'] = self.lineColor.currentText()
        self.annotation.limitsProperties['thickness'] = self.lineThickness.value()
        
        self.annotation.opacity = self.opacity.value()
        self.annotation.order = self.order.value()
        
        self.annotation.update()
        
        self.pyLong.canvas.draw()
        
    def pointZ(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickZ)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickZ(self, event):
        try:
            self.zText.setValue(event.ydata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.update()
        
    def pointStart(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickStart)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickStart(self, event):
        try:
            self.xStart.setValue(event.xdata)
            self.zStart.setValue(event.ydata)
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
            self.zEnd.setValue(event.ydata)
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
