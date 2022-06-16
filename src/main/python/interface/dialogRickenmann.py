from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *

from pyLong.dictionaries import *


class DialogRickenmann(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.calculationsList.list.currentRow()
        self.rickenmann = self.pyLong.project.calculations[i]
        
        self.setWindowTitle("Rickenmann")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
    
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
        
        for zprofile, sprofile in self.pyLong.project.profiles :
            self.profiles.addItem(zprofile.title)
        layout.addWidget(self.profiles, 0, 1, 1, 2)
        
        try:
            self.profiles.setCurrentIndex(self.rickenmann.parameters['zprofile'])
        except:
            self.profiles.setCurrentIndex(0)
        
        label = QLabel("X")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1)      

        label = QLabel("Z")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 2)
        
        label = QLabel("Start :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        label = QLabel("End :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.xStart = QDoubleSpinBox()
        self.xStart.setFixedWidth(90)
        self.xStart.setSuffix(" m")
        self.xStart.setLocale(QLocale('English'))
        self.xStart.setSingleStep(0.1)
        self.xStart.setRange(-99999.999, 99999.999)
        self.xStart.setDecimals(3)
        self.xStart.setValue(self.rickenmann.parameters['x start'])
        layout.addWidget(self.xStart, 2, 1)        

        self.zStart = QDoubleSpinBox()
        self.zStart.setFixedWidth(90)
        self.zStart.setSuffix(" m")
        self.zStart.setLocale(QLocale('English'))
        self.zStart.setSingleStep(1)
        self.zStart.setRange(-99999.999, 99999.999)
        self.zStart.setDecimals(3)
        self.zStart.setReadOnly(True)
        self.zStart.setValue(self.rickenmann.parameters['z start'])
        layout.addWidget(self.zStart, 2, 2)

        self.xEnd = QDoubleSpinBox()
        self.xEnd.setFixedWidth(90)
        self.xEnd.setSuffix(" m")
        self.xEnd.setLocale(QLocale('English'))
        self.xEnd.setSingleStep(1)
        self.xEnd.setRange(-99999.999, 99999.999)
        self.xEnd.setDecimals(3)
        self.xEnd.setReadOnly(True)
        self.xEnd.setValue(self.rickenmann.parameters['x end'])
        layout.addWidget(self.xEnd, 3, 1)        

        self.zEnd = QDoubleSpinBox()
        self.zEnd.setFixedWidth(90)
        self.zEnd.setSuffix(" m")
        self.zEnd.setLocale(QLocale('English'))
        self.zEnd.setSingleStep(1)
        self.zEnd.setRange(-99999.999, 99999.999)
        self.zEnd.setDecimals(3)
        self.zEnd.setReadOnly(True)
        self.zEnd.setValue(self.rickenmann.parameters['z end'])
        layout.addWidget(self.zEnd, 3, 2)
        
        label = QLabel("Volume :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.volume = QSpinBox()
        self.volume.setFixedWidth(90)
        self.volume.setSuffix(" m^3")
        self.volume.setLocale(QLocale('English'))
        self.volume.setRange(0, 999999)
        self.volume.setValue(self.rickenmann.parameters['volume'])
        layout.addWidget(self.volume, 4, 1)
        
        label = QLabel("Pas de calcul :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.step = QDoubleSpinBox()
        self.step.setFixedWidth(75)
        self.step.setSuffix(" m")
        self.step.setLocale(QLocale('English'))
        self.step.setRange(0, 1000.0)
        self.step.setDecimals(1)
        self.step.setSingleStep(0.1)
        self.step.setValue(self.rickenmann.parameters['step'])
        layout.addWidget(self.step, 5, 1)
        
        self.envelope = QCheckBox("use envelop-type equation.")
        self.envelope.setChecked(self.rickenmann.parameters['envelope'])
        layout.addWidget(self.envelope, 6, 0, 1, 3)
        
        parametersTab.setLayout(layout)
        
        # style tab
        layout = QGridLayout()
        
        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.label = QLineEdit()
        self.label.setText(self.rickenmann.label)
        self.label.textEdited.connect(self.updateLabel)
        layout.addWidget(self.label, 0, 1)
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.style = QComboBox()
        self.style.insertItems(0, list(lineStyles.keys()))
        self.style.setCurrentText(self.rickenmann.lineProperties['style'])
        self.style.currentTextChanged.connect(self.update)
        layout.addWidget(self.style, 1, 1, 1, 2)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 2, 0)
        
        self.color = ColorsComboBox(self.pyLong.appctxt)
        self.color.setCurrentText(self.rickenmann.lineProperties['color'])
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
        self.thickness.setValue(self.rickenmann.lineProperties['thickness'])
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
        self.opacity.setValue(self.rickenmann.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 4, 1, 1, 2)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 5, 0)
        
        self.order = QSpinBox()
        self.order.setFixedWidth(50)
        self.order.setRange(1, 99)
        self.order.setValue(self.rickenmann.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 5, 1, 1, 2)
        
        layout.addWidget(QWidget(), 6, 0)
        
        styleTab.setLayout(layout)

        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.title = QLineEdit()
        self.title.setText(self.rickenmann.title)
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

    def validate(self):
        self.apply()
        self.accept()

    def updateTitle(self):
        self.rickenmann.title = self.title.text()
        self.pyLong.calculationsList.update()

    def updateLabel(self):
        self.rickenmann.label = self.label.text()

        self.rickenmann.update()
        self.pyLong.canvas.updateLegends()

    def update(self):
        self.rickenmann.label = self.label.text()
        self.rickenmann.lineProperties['style'] = self.style.currentText()
        self.rickenmann.lineProperties['color'] = self.color.currentText()
        self.rickenmann.lineProperties['thickness'] = self.thickness.value()
        self.rickenmann.opacity = self.opacity.value()
        self.rickenmann.order = self.order.value()

        self.rickenmann.update()
        self.pyLong.canvas.draw()
            
    def apply(self):
        try:
            self.rickenmann.parameters['zprofile'] = self.pyLong.project.profiles[self.profiles.currentIndex()][0]
            self.rickenmann.parameters['sprofile'] = self.pyLong.project.profiles[self.profiles.currentIndex()][1]
        except:
            self.rickenmann.parameters['zprofile'] = None
            self.rickenmann.parameters['sprofile'] = None
        self.rickenmann.parameters['x start'] = self.xStart.value()
        self.rickenmann.parameters['volume'] = self.volume.value()
        self.rickenmann.parameters['step'] = self.step.value()
        self.rickenmann.parameters['envelope'] = self.envelope.isChecked()
        
        try:
            self.rickenmann.calculate()
        except:
            self.rickenmann.success = False
            pass
        
        if self.rickenmann.success:
            self.xStart.setValue(self.rickenmann.parameters['x start'])
            self.zStart.setValue(self.rickenmann.parameters['z start'])
            self.xEnd.setValue(self.rickenmann.parameters['x end'])
            self.zEnd.setValue(self.rickenmann.parameters['z end'])
        else:
            alert = QMessageBox(self)
            alert.setText("Processing failed.")
            alert.exec_()
        
        self.rickenmann.update()
        self.pyLong.canvas.draw()
