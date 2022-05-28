from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionnaires import *
from pyLong.zProfil import *
from pyLong.pProfil import *


class DialogFiltrer(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        mainLayout = QVBoxLayout()
        
        i = self.pyLong.listeProfils.liste.currentRow()
        self.setWindowTitle("Filtrer le profil \"{}\"".format(self.pyLong.listeProfils.liste.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/filtrer.png')))
        
        self.zprofil, self.pprofil = self.pyLong.projet.profils[i]
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()
        
        label = QLabel("Filtre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.filtres = QComboBox()
        self.filtres.addItems(["Lowess", "Butterworth", "Savitsky-Golay"])
        # self.filtres.addItems(["Lowess", "Butterworth"])
        self.filtres.currentTextChanged.connect(self.updateParametresFiltre)
        layout.addWidget(self.filtres, 0, 1)
        
        self.parametre1Nom = QLabel()
        self.parametre1Nom.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.parametre1Nom, 1, 0)
        
        self.parametre1 = QDoubleSpinBox()
        self.parametre1.setLocale(QLocale('English'))
        self.parametre1.setVisible(False)
        self.parametre1.valueChanged.connect(self.controleParametres)
        self.parametre1.valueChanged.connect(self.apercu)
        layout.addWidget(self.parametre1, 1, 1)
    
        self.parametre2Nom = QLabel()
        self.parametre2Nom.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.parametre2Nom, 2, 0)
        
        self.parametre2 = QDoubleSpinBox()
        self.parametre2.setLocale(QLocale('English'))
        self.parametre2.setVisible(False)
        self.parametre2.valueChanged.connect(self.controleParametres)
        self.parametre2.valueChanged.connect(self.apercu)
        layout.addWidget(self.parametre2, 2, 1)
        
        label = QLabel("Intitulé du profil à créer :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.intitule = QLineEdit()
        self.intitule.setText("profil n°{}".format(zProfil.compteur + 1))
        layout.addWidget(self.intitule, 3, 1) 

        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)
        
        self.updateParametresFiltre()

        self.pyLong.projet.apercu.visible = True
        self.pyLong.projet.apercu.abscisses = self.zprofil.abscisses
        self.pyLong.projet.apercu.altitudes = self.zprofil.altitudes
        self.pyLong.projet.apercu.update()
            
        self.pyLong.canvas.draw()
        
        self.apercu()
        
    def apercu(self):
        if self.filtres.currentText() == "Lowess":
            try:
                x, z = self.zprofil.lowess(self.parametre1.value(), self.parametre2.value())
                
                self.pyLong.projet.apercu.abscisses = x
                self.pyLong.projet.apercu.altitudes = z
                self.pyLong.projet.apercu.update()
                
                self.pyLong.canvas.draw()
            
            except:
                pass
            
        elif self.filtres.currentText() == "Butterworth":
            try:
                x, z = self.zprofil.butterworth(self.parametre1.value(), self.parametre2.value())
                
                self.pyLong.projet.apercu.abscisses = x
                self.pyLong.projet.apercu.altitudes = z
                self.pyLong.projet.apercu.update()
                
                self.pyLong.canvas.draw()
            
            except:
                pass
            
        else:
            try:
                x, z = self.zprofil.savitsky_golay(self.parametre1.value(), self.parametre2.value())
                
                self.pyLong.projet.apercu.abscisses = x
                self.pyLong.projet.apercu.altitudes = z
                self.pyLong.projet.apercu.update()
                
                self.pyLong.canvas.draw()
                
            except:
                pass
            
    def valider(self):
        if self.filtres.currentText() == "Lowess":
            try:
                x, z = self.zprofil.lowess(self.parametre1.value(), self.parametre2.value()) 
                
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
                
            except:
                alerte = QMessageBox(self)
                alerte.setText("Le filtrage a échoué")
                alerte.exec_()
            
        elif self.filtres.currentText() == "Butterworth":
            try:
                x, z = self.zprofil.butterworth(self.parametre1.value(), self.parametre2.value())
                
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
                
            except:
                alerte = QMessageBox(self)
                alerte.setText("Le filtrage a échoué")
                alerte.exec_()
        
        else:
            try:
                x, z = self.zprofil.savitsky_golay(self.parametre1.value(), self.parametre2.value())
                
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
                
            except:
                alerte = QMessageBox(self)
                alerte.setText("Le filtrage a échoué")
                alerte.exec_()
        
    def controleParametres(self):
        if self.filtres.currentText() == "Savitsky-Golay":
            if int(self.parametre1.value()) >= int(self.parametre2.value()):
                self.parametre1.setValue(self.parametre2.value() - 1)
        
    def updateParametresFiltre(self):
        if self.filtres.currentText() == "Lowess":
            self.parametre1Nom.setText("Taille de la fenêtre :")
            self.parametre1Nom.setVisible(True)
            self.parametre1.setDecimals(0)
            self.parametre1.setSingleStep(1)
            self.parametre1.setRange(1, 99999)
            self.parametre1.setValue(1)
            self.parametre1.setVisible(True)
            self.parametre2Nom.setText("Paramètre :")
            self.parametre2Nom.setVisible(True)
            self.parametre2.setDecimals(4)
            self.parametre2.setSingleStep(0.0001)
            self.parametre2.setRange(0.0001, 1)
            self.parametre2.setValue(0.0001)
            self.parametre2.setVisible(True)
            
        elif self.filtres.currentText() == "Butterworth":
            self.parametre1Nom.setText("Ordre du filtre :")
            self.parametre1Nom.setVisible(True)
            self.parametre1.setDecimals(0)
            self.parametre1.setSingleStep(1)
            self.parametre1.setRange(1, 99)
            self.parametre1.setVisible(True)
            self.parametre1.setValue(1)
            self.parametre2Nom.setText("Fréquence critique :")
            self.parametre2Nom.setVisible(True)
            self.parametre2.setDecimals(3)
            self.parametre2.setSingleStep(0.001)
            self.parametre2.setRange(0.001, 0.999)
            self.parametre2.setValue(0.5)
            self.parametre2.setVisible(True)
            
        else:
            self.parametre1Nom.setText("Ordre du polynôme :")
            self.parametre1Nom.setVisible(True)
            self.parametre1.setDecimals(0)
            self.parametre1.setSingleStep(1)
            self.parametre1.setRange(0, 99)
            self.parametre1.setVisible(True)
            self.parametre1.setValue(0)
            self.parametre2Nom.setText("Taille de la fenêtre :")
            self.parametre2Nom.setVisible(True)
            self.parametre2.setDecimals(0)
            self.parametre2.setSingleStep(2)
            self.parametre2.setRange(1, 99999)
            self.parametre2.setVisible(True)
            self.parametre2.setValue(1)
            
        self.apercu()
