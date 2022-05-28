from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *
import os
from pyLong.dictionnaires import *

import numpy as np
import pandas as pd


class DialogMezap(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.listeCalculs.liste.currentRow()
        self.mezap = self.pyLong.projet.calculs[i]
        
        self.setWindowTitle("Lignes d'énergie (MEZAP)")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rock.png')))
    
        tableWidget = QTabWidget()
        onglet_parametres = QWidget()

        tableWidget.addTab(onglet_parametres, "Paramètres de calcul")
        
        # onglet paramètres
        layout = QGridLayout()
        
        label = QLabel("Profil :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.profils = QComboBox()
        
        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profils.addItem(zprofil.intitule)

        try:
            self.profils.setCurrentIndex(self.mezap.parametres['profil'])
        except:
            pass

        layout.addWidget(self.profils, 0, 1, 1, 2)
        
        label = QLabel("Abscisse")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1)      

        label = QLabel("Altitude")
        label.setAlignment(Qt.AlignCenter)
        label.setVisible(False)
        layout.addWidget(label, 1, 2)
        
        label = QLabel("Départ :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.abscisseDepart = QDoubleSpinBox()
        self.abscisseDepart.setFixedWidth(90)
        self.abscisseDepart.setSuffix(" m")
        self.abscisseDepart.setLocale(QLocale('English'))
        self.abscisseDepart.setSingleStep(1)
        self.abscisseDepart.setRange(0, 99999.999)
        self.abscisseDepart.setDecimals(3)
        self.abscisseDepart.setValue(self.mezap.parametres['abscisse départ'])
        layout.addWidget(self.abscisseDepart, 2, 1)        

        self.altitudeDepart = QDoubleSpinBox()
        self.altitudeDepart.setFixedWidth(90)
        self.altitudeDepart.setSuffix(" m")
        self.altitudeDepart.setLocale(QLocale('English'))
        self.altitudeDepart.setSingleStep(1)
        self.altitudeDepart.setRange(0, 99999.999)
        self.altitudeDepart.setDecimals(3)
        self.altitudeDepart.setReadOnly(True)
        self.altitudeDepart.setValue(self.mezap.parametres['altitude départ'])
        self.altitudeDepart.setVisible(False)
        layout.addWidget(self.altitudeDepart, 2, 2)
        
        label = QLabel("Rapport :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        sublayout = QHBoxLayout()
        
        self.cheminRapport = QLineEdit()
        self.cheminRapport.setText(self.mezap.cheminRapport)
        sublayout.addWidget(self.cheminRapport)
        
        self.boutonParcourir = QPushButton("...")
        self.boutonParcourir.setFixedWidth(20)
        self.boutonParcourir.clicked.connect(self.parcourir)
        self.boutonParcourir.setAutoDefault(False)
        sublayout.addWidget(self.boutonParcourir)

        layout.addLayout(sublayout, 3, 1, 1, 2)

        self.exporterValeurs = QCheckBox("Exporter angles d'énergie et aires normalisées")
        self.exporterValeurs.setChecked(self.mezap.exporterValeurs)

        layout.addWidget(self.exporterValeurs, 4, 0, 1, 3)

        label = QLabel("Chemin :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)

        sublayout = QHBoxLayout()

        self.cheminValeurs = QLineEdit()
        self.cheminValeurs.setText(self.mezap.cheminValeur)
        sublayout.addWidget(self.cheminValeurs)

        self.boutonParcourirValeurs = QPushButton("...")
        self.boutonParcourirValeurs.setFixedWidth(20)
        self.boutonParcourirValeurs.clicked.connect(self.parcourirValeurs)
        self.boutonParcourirValeurs.setAutoDefault(False)
        sublayout.addWidget(self.boutonParcourirValeurs)

        layout.addLayout(sublayout, 5, 1, 1, 2)
        
        onglet_parametres.setLayout(layout)

        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.mezap.intitule)
        self.intitule.textChanged.connect(self.updateIntitule)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Apply).setText("Appliquer")
        buttonBox.rejected.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        layout = QGridLayout()
        
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.intitule, 0, 1)
        
        layout.addWidget(tableWidget, 1, 0, 1, 2)
        
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)

    def parcourir(self):
        chemin = QFileDialog.getSaveFileName(caption="Enregistrer le rapport de calcul",
                                             filter="fichier pdf (*.pdf)")[0]
        if chemin == "":
            return 0
        else:
            nomFichier = QFileInfo(chemin).fileName()
            repertoireFichier = QFileInfo(chemin).absolutePath()
            nomFichier = nomFichier.split(".")[0]

            nomFichier += ".pdf"
            chemin = repertoireFichier + "/" + nomFichier

            self.cheminRapport.setText(chemin)

    def parcourirValeurs(self):
        chemin = QFileDialog.getSaveFileName(caption="Exporter angles d'énergie et aires normalisées",
                                             filter="fichier txt (*.txt)")[0]
        if chemin == "":
            return 0
        else:
            nomFichier = QFileInfo(chemin).fileName()
            repertoireFichier = QFileInfo(chemin).absolutePath()
            nomFichier = nomFichier.split(".")[0]

            nomFichier += ".txt"
            chemin = repertoireFichier + "/" + nomFichier

            self.cheminValeurs.setText(chemin)

    def updateIntitule(self):
        self.mezap.intitule = self.intitule.text()
        self.pyLong.listeCalculs.update()

    def valider(self):
        self.appliquer()
        self.accept()

    def appliquer(self):
        self.mezap.intitule = self.intitule.text()
        self.mezap.cheminRapport = self.cheminRapport.text()

        self.mezap.parametres['profil'] = self.profils.currentIndex()
        self.mezap.parametres['abscisse départ'] = self.abscisseDepart.value()

        self.mezap.exporterValeurs = self.exporterValeurs.isChecked()
        self.mezap.cheminValeur = self.cheminValeurs.text()

        self.mezap.calculer(self.pyLong)

        if self.mezap.calculReussi:
            try:
                if self.exporterValeurs.isChecked():
                    data = np.array([self.mezap.abscisses, self.mezap.angles, self.mezap.airesNormalisees]).T
                    data = pd.DataFrame(data)
                    data.to_csv(self.cheminValeurs.text(),
                                sep="\t",
                                float_format="%.3f",
                                decimal=".",
                                index=False,
                                header=['X', 'Angle_Energie', 'Aire_Normalisee'])

                self.mezap.abscisses = []
                self.mezap.angles = []
                self.mezap.airesNormalisees = []

                os.startfile(self.mezap.cheminRapport)
            except:
                pass
        else:
            alerte = QMessageBox(self)
            alerte.setText("Le calcul a échoué.")
            alerte.exec_()