from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.zProfil import *
from pyLong.pProfil import *
from pyLong.dictionnaires import *


class DialogSimplifier(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
 
        mainLayout = QVBoxLayout()
        
        i = self.pyLong.listeProfils.liste.currentRow()
        self.setWindowTitle("Simplifier le profil \"{}\"".format(self.pyLong.listeProfils.liste.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/simplifier.png')))
        
        self.zprofil, self.pprofil = self.pyLong.projet.profils[i]
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()
        
        label = QLabel("Pourcentage de points à conserver :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.ratio = QDoubleSpinBox()
        self.ratio.setSuffix(" %")
        self.ratio.setFixedWidth(80)
        self.ratio.setSingleStep(1)
        self.ratio.setRange(0.001, 100)
        self.ratio.setDecimals(3)
        self.ratio.setValue(100)
        self.ratio.setLocale(QLocale('English'))
        self.ratio.valueChanged.connect(self.apercu)
        layout.addWidget(self.ratio, 0, 1)
        
        label = QLabel("Intitulé du profil à créer :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.intitule = QLineEdit()
        self.intitule.setText("profil n°{}".format(zProfil.compteur + 1))
        layout.addWidget(self.intitule, 1, 1)

        layout.addWidget(QLabel(), 2, 0, 1, 2)

        label = QLabel("Avant simplification : {} sommets".format(np.shape(self.zprofil.abscisses)[0]))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0, 1, 2)

        self.info = QLabel("Après simplification : {} sommets".format(np.shape(self.zprofil.abscisses)[0]))
        self.info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.info, 4, 0, 1, 2)

        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

        self.pyLong.projet.apercu.visible = True
        self.pyLong.projet.apercu.abscisses = self.zprofil.abscisses
        self.pyLong.projet.apercu.altitudes = self.zprofil.altitudes
        self.pyLong.projet.apercu.update()

        self.pyLong.canvas.draw()
        
        self.apercu()
        
    def apercu(self):
        x, z = self.zprofil.simplifier(ratio=self.ratio.value()/100)

        self.pyLong.projet.apercu.abscisses = x
        self.pyLong.projet.apercu.altitudes = z
        self.pyLong.projet.apercu.update()
        
        self.pyLong.canvas.draw()

        self.info.setText("Après simplification : {} sommets".format(np.shape(x)[0]))
        
    def valider(self):
        x, z = self.zprofil.simplifier(ratio=self.ratio.value()/100)
        
        zprofil = zProfil()
        pprofil = pProfil()
        
        zprofil.intitule = self.intitule.text()
        zprofil.abscisses = x
        zprofil.altitudes = z
        zprofil.update()
        
        pprofil.updateData(x, z)
        pprofil.update()

        self.pyLong.projet.profils.append((zprofil, pprofil))
        self.pyLong.listeProfils.update()

        self.pyLong.canvas.ax_z.add_line(zprofil.line)
    
        self.accept()
