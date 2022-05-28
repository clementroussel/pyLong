from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *
import os
from pyLong.dictionnaires import *

from scipy.interpolate import interp1d

import numpy as np
import pandas as pd


class DialogDeltaZ(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent

        self.setWindowTitle("Ecarts altimétriques")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/deux-lignes.png')))

        mainlayout = QVBoxLayout()

        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()

        label = QLabel("Profil n°1 :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.profils1 = QComboBox()
        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profils1.addItem(zprofil.intitule)
        layout.addWidget(self.profils1, 0, 1)

        label = QLabel("Profil n°2 :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.profils2 = QComboBox()
        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profils2.addItem(zprofil.intitule)
        layout.addWidget(self.profils2, 1, 1)

        self.interpoler = QCheckBox("Interpolation :")
        self.interpoler.setChecked(False)
        layout.addWidget(self.interpoler, 2, 0)

        self.pas = QDoubleSpinBox()
        self.pas.setFixedWidth(70)
        self.pas.setSuffix(" m")
        self.pas.setLocale(QLocale('English'))
        self.pas.setRange(0.1, 999.9)
        self.pas.setDecimals(1)
        self.pas.setSingleStep(1)
        self.pas.setValue(10)
        layout.addWidget(self.pas, 2, 1)

        label = QLabel("Fichier en sortie :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.chemin = QLineEdit()
        layout.addWidget(self.chemin, 3, 1)

        boutonParcourir = QPushButton("...")
        boutonParcourir.setAutoDefault(False)
        boutonParcourir.setFixedWidth(20)
        boutonParcourir.clicked.connect(self.parcourir)
        layout.addWidget(boutonParcourir, 3, 2)

        groupe.setLayout(layout)
        mainlayout.addWidget(groupe)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainlayout.addWidget(buttonBox)

        self.setLayout(mainlayout)

    def parcourir(self):
        chemin = QFileDialog.getSaveFileName(caption="Ecarts altimétriques",
                                             filter="fichier texte (*.txt)")[0]
        if chemin == "":
            return 0
        else:
            nomFichier = QFileInfo(chemin).fileName()
            repertoireFichier = QFileInfo(chemin).absolutePath()
            nomFichier = nomFichier.split(".")[0]

            nomFichier += ".txt"
            chemin = repertoireFichier + "/" + nomFichier

            self.chemin.setText(chemin)

    def valider(self):
        i = self.profils1.currentIndex()
        j = self.profils2.currentIndex()

        if i != -1 and j != -1:
            zprofil1, pprofil1 = self.pyLong.projet.profils[i]
            abscisses1 = list(zprofil1.abscisses)

            zprofil2, pprofil2 = self.pyLong.projet.profils[j]
            abscisses2 = list(zprofil2.abscisses)

            xmin = max(min(abscisses1), min(abscisses2))
            xmax = min(max(abscisses1), max(abscisses2))

            if (xmin in abscisses1) and (xmin in abscisses2):
                pass
            elif (xmin in abscisses1) and (not xmin in abscisses2):
                abscisses2.append(xmin)
                abscisses2.sort()
            else:
                abscisses1.append(xmin)
                abscisses1.sort()

            if (xmax in abscisses1) and (xmax in abscisses2):
                pass
            elif (xmax in abscisses1) and (not xmax in abscisses2):
                abscisses2.append(xmax)
                abscisses2.sort()
            else:
                abscisses1.append(xmax)
                abscisses1.sort()

            i = abscisses1.index(xmin)
            j = abscisses1.index(xmax)
            abscisses1 = abscisses1[i:j+1]

            i = abscisses2.index(xmin)
            j = abscisses2.index(xmax)
            abscisses2 = abscisses2[i:j + 1]

            abscisses = abscisses1 + abscisses2
            abscisses.sort()
            abscisses = list(np.unique(abscisses))

            altitudes1 = []
            altitudes2 = []

            for i in range(len(abscisses)):
                altitudes1.append(zprofil1.interpoler(abscisses[i]))
                altitudes2.append(zprofil2.interpoler(abscisses[i]))

            abscisses = np.array(abscisses)
            altitudes1 = np.array(altitudes1)
            altitudes2 = np.array(altitudes2)

            if not self.interpoler.isChecked():
                xz = np.array([abscisses, altitudes1 - altitudes2]).T
                xz = pd.DataFrame(xz)
            else:
                f = interp1d(abscisses, altitudes1 - altitudes2)

                new_x = np.arange(abscisses[0], abscisses[-1] + self.pas.value(), self.pas.value())
                new_z = f(new_x)

                xz = np.array([new_x, new_z]).T
                xz = pd.DataFrame(xz)

            try:
                xz.to_csv(self.chemin.text(),
                          sep="\t",
                          float_format="%.3f",
                          decimal=".",
                          index=False,
                          header=['X', 'Dz'])
                self.accept()
            except:
                alerte = QMessageBox(self)
                alerte.setText("Echec de l'écriture du fichier.")
                alerte.setIcon(QMessageBox.Warning)
                alerte.exec_()

        else:
            alerte = QMessageBox(self)
            alerte.setText("Renseignez les deux profils.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()







