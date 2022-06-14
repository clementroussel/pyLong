from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *

from pyLong.dictionaries import *


class DialogEnergyLine(QDialog):

    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.calculationsList.list.currentRow()
        self.energyLine = self.pyLong.project.calculations[i]
        
        self.setWindowTitle("Enery line")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rock.png')))
    
        tableWidget = QTabWidget()
        parametersTab = QWidget()
        styleTab = QWidget() 

        tableWidget.addTab(parametersTab, "Parameters")
        tableWidget.addTab(styleTab, "Style")  
        
        # parameters tab
        layout = QGridLayout()
        
        label = QLabel("Profile :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.profiles = QComboBox()
        
        for zprofile, sprofile in self.pyLong.project.profiles:
            self.profiles.addItem(zprofile.title)
        layout.addWidget(self.profiles, 0, 1, 1, 2)
        
        try:
            self.profiles.setCurrentIndex(self.energyLine.parameters['zprofile'])
        except:
            self.profiles.setCurrentIndex(0)
        
        label = QLabel("Method :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0) 
        
        self.methods = QComboBox()
        self.methods.addItems(["start + end", "start + angle", "end + angle"])
        self.methods.setCurrentText(self.energyLine.parameters['method'])
        self.methods.currentTextChanged.connect(self.updateInterface)
        layout.addWidget(self.methods, 1, 1, 1, 2)
        
        label = QLabel("X")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 2, 1)      

        label = QLabel("Z")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 2, 2)
        
        label = QLabel("Start :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        label = QLabel("End :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.xStart = QDoubleSpinBox()
        self.xStart.setFixedWidth(90)
        self.xStart.setSuffix(" m")
        self.xStart.setLocale(QLocale('English'))
        self.xStart.setSingleStep(1)
        self.xStart.setRange(0, 99999.999)
        self.xStart.setDecimals(3)
        self.xStart.setValue(self.energyLine.parameters['x start'])
        layout.addWidget(self.xStart, 3, 1)        

        self.zStart = QDoubleSpinBox()
        self.zStart.setFixedWidth(90)
        self.zStart.setSuffix(" m")
        self.zStart.setLocale(QLocale('English'))
        self.zStart.setSingleStep(1)
        self.zStart.setRange(0, 99999.999)
        self.zStart.setDecimals(3)
        self.zStart.setValue(self.energyLine.parameters['z start'])
        self.zStart.setReadOnly(True)
        layout.addWidget(self.zStart, 3, 2)

        self.xEnd = QDoubleSpinBox()
        self.xEnd.setFixedWidth(90)
        self.xEnd.setSuffix(" m")
        self.xEnd.setLocale(QLocale('English'))
        self.xEnd.setSingleStep(1)
        self.xEnd.setRange(0, 99999.999)
        self.xEnd.setDecimals(3)
        self.xEnd.setValue(self.energyLine.parameters['x end'])
        layout.addWidget(self.xEnd, 4, 1)        

        self.zEnd = QDoubleSpinBox()
        self.zEnd.setFixedWidth(90)
        self.zEnd.setSuffix(" m")
        self.zEnd.setLocale(QLocale('English'))
        self.zEnd.setSingleStep(1)
        self.zEnd.setRange(0, 99999.999)
        self.zEnd.setDecimals(3)
        self.zEnd.setReadOnly(True)
        self.zEnd.setValue(self.energyLine.parameters['z end'])
        layout.addWidget(self.zEnd, 4, 2)
        
        label = QLabel("Angle :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.angle = QDoubleSpinBox()
        self.angle.setSuffix(" deg")
        self.angle.setLocale(QLocale('English'))
        self.angle.setRange(0, 89.99)
        self.angle.setDecimals(6)
        self.angle.setSingleStep(1)
        self.angle.setValue(self.energyLine.parameters['angle'])
        layout.addWidget(self.angle, 5, 1, 1, 2)
        
        parametersTab.setLayout(layout)
        
        # style tab
        layout = QGridLayout()
        
        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.label = QLineEdit()
        self.label.setText(self.energyLine.label)
        self.label.textEdited.connect(self.updateLegend)
        layout.addWidget(self.label, 0, 1)
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.style = QComboBox()
        self.style.insertItems(0, list(lineStyles.keys()))
        self.style.setCurrentText(self.energyLine.lineProperties['style'])
        self.style.currentTextChanged.connect(self.update)
        layout.addWidget(self.style, 1, 1, 1, 2)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 2, 0)
        
        self.color = ColorsComboBox(self.pyLong.appctxt)
        self.color.setCurrentText(self.energyLine.lineProperties['color'])
        self.color.currentTextChanged.connect(self.update)
        layout.addWidget(self.color, 2, 1, 1, 2)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 3, 0)
        
        self.thickness = QDoubleSpinBox()
        self.thickness.setFixedWidth(50)
        self.thickness.setLocale(QLocale('English'))
        self.thickness.setRange(0, 99.9)
        self.thickness.setDecimals(1)
        self.thickness.setSingleStep(0.1)
        self.thickness.setValue(self.energyLine.lineProperties['thickness'])
        self.thickness.valueChanged.connect(self.update)
        layout.addWidget(self.thickness, 3, 1, 1, 2)
        
        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 4, 0)
        
        self.opacity = QDoubleSpinBox()
        self.opacity.setFixedWidth(50)
        self.opacity.setLocale(QLocale('English'))
        self.opacity.setRange(0, 1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.energyLine.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 4, 1, 1, 2)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 5, 0)
        
        self.order = QSpinBox()
        self.order.setFixedWidth(50)
        self.order.setRange(1, 99)
        self.order.setValue(self.energyLine.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 5, 1, 1, 2)
        
        styleTab.setLayout(layout)

        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.title = QLineEdit()
        self.title.setText(self.energyLine.title)
        self.title.textChanged.connect(self.updateTitle)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        layout = QGridLayout()
        
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.title, 0, 1)
        
        layout.addWidget(tableWidget, 1, 0, 1, 2)
        
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)      

        self.updateInterface()
    
    def validate(self):
        self.apply()
        self.accept()

    def update(self):
        self.energyLine.lineProperties['style'] = self.style.currentText()
        self.energyLine.lineProperties['color'] = self.color.currentText()
        self.energyLine.lineProperties['thickness'] = self.thickness.value()
        self.energyLine.opacity = self.opacity.value()
        self.energyLine.order = self.order.value()

        self.energyLine.update()
        self.pyLong.canvas.draw()

    def updateLegend(self):
        self.energyLine.label = self.label.text()
        self.energyLine.update()

        self.pyLong.canvas.updateLegends()

    def updateTitle(self):
        self.energyLine.title = self.title.text()
        self.pyLong.calculationsList.update()
    
    def apply(self):
        self.energyLine.parameters['zprofile'] = self.pyLong.project.profiles[self.profiles.currentIndex()][0]
        self.energyLine.parameters['sprofile'] = self.pyLong.project.profiles[self.profiles.currentIndex()][1]
        self.energyLine.parameters['method'] = self.methods.currentText()
        self.energyLine.parameters['x start'] = self.xStart.value()
        self.energyLine.parameters['x end'] = self.xEnd.value()
        self.energyLine.parameters['angle'] = self.angle.value()
        
        try:
            self.energyLine.calculate()
        except:
            self.energyLine.success = False
            pass
        
        if self.energyLine.success:
            self.xStart.setValue(self.energyLine.parameters['x start'])
            self.zStart.setValue(self.energyLine.parameters['z start'])
            self.xEnd.setValue(self.energyLine.parameters['x end'])
            self.zEnd.setValue(self.energyLine.parameters['z end'])
            self.angle.setValue(self.energyLine.parameters['angle'])
        else:
            alert = QMessageBox(self)
            alert.setText("Processing failed.")
            alert.exec_()
        
        self.energyLine.update()
        self.pyLong.canvas.draw()
        
    def updateInterface(self):
        if self.methods.currentText() == "start + end":
            self.xStart.setReadOnly(False)
            self.xEnd.setReadOnly(False)
            self.angle.setReadOnly(True)
        elif self.methods.currentText() == "start + angle":
            self.xStart.setReadOnly(False)
            self.xEnd.setReadOnly(True)
            self.angle.setReadOnly(False)
        else:
            self.xStart.setReadOnly(True)
            self.xEnd.setReadOnly(False)
            self.angle.setReadOnly(False)
