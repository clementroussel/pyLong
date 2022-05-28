from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionnaires import *

from pyLong.Donnee import *

class DialogAjoutDonnees(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.listeLayouts.currentIndex()
        self.layout = self.pyLong.projet.layouts[i]
        
        self.setWindowTitle("Ajouter des données")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/autres_donnees.png')))
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()
        
        label = QLabel("Délimiteur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.delimiteur = QComboBox()
        self.delimiteur.insertItems(0, list(delimiteurs.keys()))
        self.delimiteur.setCurrentText("tabulation")
        layout.addWidget(self.delimiteur, 0, 1)
        
        label = QLabel("Séparateur décimal :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.separateur = QComboBox()
        self.separateur.insertItems(0, list(separateurs.keys()))
        layout.addWidget(self.separateur, 1, 1)
        
        # self.annotations = QCheckBox("Importer les annotations")
        # layout.addWidget(self.annotations, 2, 0, 1, 2)
        
        label = QLabel("Chemin :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.chemin = QLineEdit()
        layout.addWidget(self.chemin, 2, 1)
        
        boutonParcourir = QPushButton("...")
        boutonParcourir.setFixedWidth(20)
        boutonParcourir.clicked.connect(self.parcourir)
        layout.addWidget(boutonParcourir, 2, 2)
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.intitule = QLineEdit()
        self.intitule.setText("donnée n°{}".format(Donnee.compteur + 1))
        layout.addWidget(self.intitule, 3, 1)

        label = QLabel("Subplot :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.subplots = QComboBox()
        self.subplots.addItems(self.pyLong.projet.subplots)
        layout.addWidget(self.subplots, 4, 1)
    
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        layout = QHBoxLayout()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.importer)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)
        mainLayout.addLayout(layout)
        
        self.setLayout(mainLayout)
        
    def parcourir(self):
        chemin = QFileDialog.getOpenFileName(caption="Importer un profil",
                                             filter="fichier texte (*.txt)")[0]
        self.chemin.setText(chemin)

    def importer(self):
        if self.chemin.text() == "":
            alerte = QMessageBox(self)
            alerte.setText("Renseignez un fichier.")
            alerte.exec_()
            return 0

        elif self.subplots.currentIndex() == -1:
            alerte = QMessageBox(self)
            alerte.setText("Aucun subplot disponible.")
            alerte.exec_()
            return 0

        else:
            try:
                data = pd.read_csv(self.chemin.text(),
                                   delimiter=delimiteurs[self.delimiteur.currentText()],
                                   decimal=separateurs[self.separateur.currentText()],
                                   skiprows=0,
                                   encoding='utf-8').values

                xy = np.array(data[:, :2].astype('float'))

                if np.shape(xy[:, 0])[0] < 2:
                    alerte = QMessageBox(self)
                    alerte.setText("Le fichier doit contenir au moins 2 points.")
                    alerte.exec_()
                    return 0

                else:
                    donnee = Donnee()

                    donnee.intitule = self.intitule.text()
                    donnee.abscisses = xy[:, 0]
                    donnee.ordonnees = xy[:, 1]
                    donnee.subplot = self.subplots.currentText()
                    donnee.update()

                    self.pyLong.projet.autresDonnees.append(donnee)
                    self.pyLong.listeAutresDonnees.update()

                    try:
                        i = [subplot.identifiant for subplot in self.layout.subplots].index(donnee.subplot)

                    except:
                        i = -1

                    if i != -1:
                        self.pyLong.canvas.subplots[i].add_line(donnee.line)
                        # self.pyLong.canvas.draw()
                        self.pyLong.canvas.updateLegendes()

                    self.accept()

            except:
                alerte = QMessageBox(self)
                alerte.setText("Fichier illisible.")
                alerte.exec_()
