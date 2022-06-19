from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.toolbox.energyLine import *
from pyLong.toolbox.mezap import *
from pyLong.toolbox.flowR import *
from pyLong.toolbox.rickenmann import *
from pyLong.toolbox.corominas import *

from interface.dialogDeltaZ import *


class DialogToolBox(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Toolbox")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/toolBox.png')))
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Analysis")
        layout = QVBoxLayout()

        deltaZ = QPushButton("Profile substraction")
        deltaZ.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/comparison.png')))
        deltaZ.clicked.connect(self.deltaZ)
        deltaZ.setAutoDefault(False)
        layout.addWidget(deltaZ)

        energyLine = QPushButton("Energy line")
        energyLine.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rock.png')))
        energyLine.clicked.connect(self.energyLine)
        energyLine.setAutoDefault(False)
        layout.addWidget(energyLine)     
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("MEZAP")
        layout = QVBoxLayout()

        mezap = QPushButton("Energy line")
        mezap.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rock.png')))
        mezap.clicked.connect(self.mezap)
        mezap.setAutoDefault(False)
        layout.addWidget(mezap)

        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Debris flow models")
        layout = QVBoxLayout()
        
        flowR = QPushButton("Flow-R")
        flowR.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
        flowR.clicked.connect(self.flowR)
        flowR.setAutoDefault(False)
        layout.addWidget(flowR)
        
        rickenmann = QPushButton("Rickenmann")
        rickenmann.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
        rickenmann.clicked.connect(self.rickenmann)
        rickenmann.setAutoDefault(False)
        layout.addWidget(rickenmann)

        corominas = QPushButton("Corominas")
        corominas.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
        corominas.clicked.connect(self.corominas)
        corominas.setAutoDefault(False)
        layout.addWidget(corominas)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)

        self.setLayout(mainLayout)

    def deltaZ(self):
        self.accept()
        DialogDeltaZ(parent=self.pyLong).exec_()
        
    def energyLine(self):
        calculation = EnergyLine()
        self.pyLong.project.calculations.append(calculation)
        self.pyLong.calculationsList.update()
        self.pyLong.canvas.ax_z.add_line(calculation.line)
        self.accept()

    def mezap(self):
        mezap = Mezap()
        self.pyLong.project.calculations.append(mezap)
        self.pyLong.calculationsList.update()
        self.accept()

    def flowR(self):
        calculation = FlowR()
        self.pyLong.project.calculations.append(calculation)
        self.pyLong.calculationsList.update()
        self.pyLong.canvas.ax_z.add_line(calculation.line)
        self.accept()

    def rickenmann(self):
        calculation = Rickenmann()
        self.pyLong.project.calculations.append(calculation)
        self.pyLong.calculationsList.update()
        self.pyLong.canvas.ax_z.add_line(calculation.line)
        self.accept()

    def corominas(self):
        calculation = Corominas()
        self.pyLong.project.calculations.append(calculation)
        self.pyLong.calculationsList.update()
        self.pyLong.canvas.ax_z.add_line(calculation.line)
        self.accept()
