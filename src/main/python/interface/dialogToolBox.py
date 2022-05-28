from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# from pyLong_gestionLignesEnergie import *
# from pyLong_gestionMezaps import *
# from pyLong_gestionFlowRs import *
# from pyLong_gestionRickenmanns import *

from DialogLigneEnergie import *
from pyLong.LigneEnergie import *
from pyLong.Mezap import *
from pyLong.FlowR import *
from pyLong.Rickenmann import *
from pyLong.Corominas import *

from DialogDeltaZ import *


class DialogToolBox(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Toolbox")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/toolBox.png')))
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Analyse")
        layout = QVBoxLayout()

        deltaZ = QPushButton("Ecarts altimétriques")
        deltaZ.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/deux-lignes.png')))
        deltaZ.clicked.connect(self.deltaZ)
        deltaZ.setAutoDefault(False)
        layout.addWidget(deltaZ)

        lignesEnergie = QPushButton("Ligne d'énergie")
        lignesEnergie.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rock.png')))
        lignesEnergie.clicked.connect(self.ligneEnergie)
        lignesEnergie.setAutoDefault(False)
        layout.addWidget(lignesEnergie)     
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Chutes de blocs")
        layout = QVBoxLayout()

        mezap = QPushButton("Lignes d'énergie (MEZAP)")
        mezap.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rock.png')))
        mezap.clicked.connect(self.mezap)
        mezap.setAutoDefault(False)
        layout.addWidget(mezap)

        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Laves torrentielles")
        layout = QVBoxLayout()
        
        flowR = QPushButton("Flow-R")
        flowR.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/lave.png')))
        flowR.clicked.connect(self.flowR)
        flowR.setAutoDefault(False)
        layout.addWidget(flowR)
        
        rickenmann = QPushButton("Rickenmann")
        rickenmann.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/lave.png')))
        rickenmann.clicked.connect(self.rickenmann)
        rickenmann.setAutoDefault(False)
        layout.addWidget(rickenmann)

        corominas = QPushButton("Corominas")
        corominas.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/lave.png')))
        corominas.clicked.connect(self.corominas)
        corominas.setAutoDefault(False)
        layout.addWidget(corominas)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)

        # groupe = QGroupBox("Ouvrages")
        # layout = QVBoxLayout()
        #
        # merlon = QPushButton("Merlon pare-blocs")
        # merlon.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/pelleteuse.png')))
        # # merlon.clicked.connect(self.flowR)
        # merlon.setAutoDefault(False)
        # layout.addWidget(merlon)
        #
        # groupe.setLayout(layout)
        # mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.reject)
        
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def deltaZ(self):
        self.accept()
        DialogDeltaZ(parent=self.pyLong).exec_()
        
    def ligneEnergie(self):
        ligneEnergie = LigneEnergie()
        self.pyLong.projet.calculs.append(ligneEnergie)
        self.pyLong.listeCalculs.update()
        self.pyLong.canvas.ax_z.add_line(ligneEnergie.line)
        self.accept()

    def mezap(self):
        mezap = Mezap()
        self.pyLong.projet.calculs.append(mezap)
        self.pyLong.listeCalculs.update()
        self.accept()

    def flowR(self):
        flowr = FlowR()
        self.pyLong.projet.calculs.append(flowr)
        self.pyLong.listeCalculs.update()
        self.pyLong.canvas.ax_z.add_line(flowr.line)
        self.accept()

    def rickenmann(self):
        rickenmann = Rickenmann()
        self.pyLong.projet.calculs.append(rickenmann)
        self.pyLong.listeCalculs.update()
        self.pyLong.canvas.ax_z.add_line(rickenmann.line)
        self.accept()

    def corominas(self):
        corominas = Corominas()
        self.pyLong.projet.calculs.append(corominas)
        self.pyLong.listeCalculs.update()
        self.pyLong.canvas.ax_z.add_line(corominas.line)
        self.accept()
