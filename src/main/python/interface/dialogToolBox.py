from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.toolbox.energyLine import *
from pyLong.toolbox.mezap import *
from pyLong.toolbox.flowR import *
from pyLong.toolbox.rickenmann import *
from pyLong.toolbox.corominas import *

# from interface.dialogDeltaZ import *


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
        deltaZ.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/substraction.png')))
        # deltaZ.clicked.connect(self.deltaZ)
        deltaZ.setAutoDefault(False)
        layout.addWidget(deltaZ)

        energyLine = QPushButton("Energy line")
        energyLine.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rock.png')))
        # energyLine.clicked.connect(self.energyLine)
        energyLine.setAutoDefault(False)
        layout.addWidget(energyLine)     
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("MEZAP")
        layout = QVBoxLayout()

        mezap = QPushButton("Energy line")
        mezap.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rock.png')))
        # mezap.clicked.connect(self.mezap)
        mezap.setAutoDefault(False)
        layout.addWidget(mezap)

        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Debris flow models")
        layout = QVBoxLayout()
        
        flowR = QPushButton("Flow-R")
        flowR.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
        # flowR.clicked.connect(self.flowR)
        flowR.setAutoDefault(False)
        layout.addWidget(flowR)
        
        rickenmann = QPushButton("Rickenmann")
        rickenmann.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
        # rickenmann.clicked.connect(self.rickenmann)
        rickenmann.setAutoDefault(False)
        layout.addWidget(rickenmann)

        corominas = QPushButton("Corominas")
        corominas.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/debrisFlow.png')))
        # corominas.clicked.connect(self.corominas)
        corominas.setAutoDefault(False)
        layout.addWidget(corominas)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        # buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        # buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        # buttonBox.rejected.connect(self.reject)
        
        # mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    # def deltaZ(self):
    #     self.accept()
    #     DialogDeltaZ(parent=self.pyLong).exec_()
        
    # def ligneEnergie(self):
    #     ligneEnergie = LigneEnergie()
    #     self.pyLong.projet.calculs.append(ligneEnergie)
    #     self.pyLong.listeCalculs.update()
    #     self.pyLong.canvas.ax_z.add_line(ligneEnergie.line)
    #     self.accept()

    # def mezap(self):
    #     mezap = Mezap()
    #     self.pyLong.projet.calculs.append(mezap)
    #     self.pyLong.listeCalculs.update()
    #     self.accept()

    # def flowR(self):
    #     flowr = FlowR()
    #     self.pyLong.projet.calculs.append(flowr)
    #     self.pyLong.listeCalculs.update()
    #     self.pyLong.canvas.ax_z.add_line(flowr.line)
    #     self.accept()

    # def rickenmann(self):
    #     rickenmann = Rickenmann()
    #     self.pyLong.projet.calculs.append(rickenmann)
    #     self.pyLong.listeCalculs.update()
    #     self.pyLong.canvas.ax_z.add_line(rickenmann.line)
    #     self.accept()

    # def corominas(self):
    #     corominas = Corominas()
    #     self.pyLong.projet.calculs.append(corominas)
    #     self.pyLong.listeCalculs.update()
    #     self.pyLong.canvas.ax_z.add_line(corominas.line)
    #     self.accept()
