from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.dictionnaires import *

from ColorsComboBox import *


class DialogLayoutSubplot(QDialog):

    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent.pyLong

        i = self.pyLong.listeLayouts.currentIndex()
        self.layout = self.pyLong.projet.layouts[i]

        self.parent = parent

        j = self.parent.listeSubplots.currentRow()
        self.subplot = self.layout.subplots[j]
        
        self.setWindowTitle("Options de mise en page du subplot : {}".format(self.subplot.identifiant))

        tableWidget = QTabWidget()
        onglet_subdivisions = QWidget()
        onglet_ordonnees = QWidget()
        onglet_legende = QWidget()

        tableWidget.addTab(onglet_subdivisions, "Subdivisions")
        tableWidget.addTab(onglet_ordonnees, "Ordonnées")
        tableWidget.addTab(onglet_legende, "Légende")
        
        layout = QGridLayout()

        label = QLabel("Nombre de subdivisions occupées :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        n_actuel = self.subplot.subdivisions
        n_total = self.layout.subdivisions

        n = 0
        for subplot in self.layout.subplots:
            n += subplot.subdivisions

        n_max = n_total - n - 1 + n_actuel

        self.subdivisions = QSpinBox()
        self.subdivisions.setFixedWidth(40)
        self.subdivisions.setSingleStep(1)
        self.subdivisions.setRange(1, n_max)
        self.subdivisions.setValue(self.subplot.subdivisions)
        self.subdivisions.valueChanged.connect(self.appliquer)
        layout.addWidget(self.subdivisions, 0, 1)

        layout.addWidget(QLabel(), 1, 0, 7, 1)

        onglet_subdivisions.setLayout(layout)

        layout = QGridLayout()

        label = QLabel("Ordonnée min. :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.ordonneesMin = QDoubleSpinBox()
        self.ordonneesMin.setFixedWidth(90)
        self.ordonneesMin.setLocale(QLocale('English'))
        self.ordonneesMin.setSingleStep(10)
        self.ordonneesMin.setRange(-99999.999, 99999.999)
        self.ordonneesMin.setDecimals(3)
        self.ordonneesMin.setValue(self.subplot.ordonnees['min'])
        self.ordonneesMin.valueChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.ordonneesMin, 0, 1)

        label = QLabel("Ordonnée max. :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.ordonneesMax = QDoubleSpinBox()
        self.ordonneesMax.setFixedWidth(90)
        self.ordonneesMax.setLocale(QLocale('English'))
        self.ordonneesMax.setSingleStep(10)
        self.ordonneesMax.setRange(-99999.999, 99999.999)
        self.ordonneesMax.setDecimals(3)
        self.ordonneesMax.setValue(self.subplot.ordonnees['max'])
        self.ordonneesMax.valueChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.ordonneesMax, 1, 1)

        label = QLabel("Intervalles :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.ordonneesInt = QSpinBox()
        self.ordonneesInt.setFixedWidth(40)
        self.ordonneesInt.setSingleStep(1)
        self.ordonneesInt.setRange(1,99)
        self.ordonneesInt.setValue(self.subplot.ordonnees['intervalles'])
        self.ordonneesInt.valueChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.ordonneesInt, 2, 1)

        label = QLabel("Libellé de l'axe :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.libelle = QLineEdit()
        self.libelle.setText(self.subplot.ordonnees['libellé'])
        self.libelle.textChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.libelle, 3, 1)

        label = QLabel("Couleur du libellé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.couleurLibelle = ColorsComboBox(self.pyLong.appctxt)
        self.couleurLibelle.setCurrentText(self.subplot.ordonnees['couleur libellé'])
        self.couleurLibelle.currentTextChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.couleurLibelle, 4, 1)

        label = QLabel("Couleur des valeurs :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)

        self.couleurValeur = ColorsComboBox(self.pyLong.appctxt)
        self.couleurValeur.setCurrentText(self.subplot.ordonnees['couleur valeur'])
        self.couleurValeur.currentTextChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.couleurValeur, 5, 1)

        label = QLabel("Décalage bas :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 6, 0)

        self.deltaBas = QDoubleSpinBox()
        self.deltaBas.setLocale(QLocale('English'))
        self.deltaBas.setFixedWidth(65)
        self.deltaBas.setRange(0, 9999.999)
        self.deltaBas.setDecimals(3)
        self.deltaBas.setSingleStep(1)
        self.deltaBas.setValue(self.subplot.ordonnees['delta bas'])
        self.deltaBas.valueChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.deltaBas, 6, 1)

        label = QLabel("Décalage haut :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)

        self.deltaHaut = QDoubleSpinBox()
        self.deltaHaut.setLocale(QLocale('English'))
        self.deltaHaut.setFixedWidth(65)
        self.deltaHaut.setRange(0, 9999.999)
        self.deltaHaut.setDecimals(3)
        self.deltaHaut.setSingleStep(1)
        self.deltaHaut.setValue(self.subplot.ordonnees['delta haut'])
        self.deltaHaut.valueChanged.connect(self.updateOrdonneesSubplot)
        layout.addWidget(self.deltaHaut, 7, 1)

        onglet_ordonnees.setLayout(layout)

        layout = QGridLayout()

        self.dessinerLegende = QCheckBox("Dessiner la légende")
        self.dessinerLegende.setChecked(self.subplot.legende['active'])
        self.dessinerLegende.stateChanged.connect(self.updateLegende)
        layout.addWidget(self.dessinerLegende, 0, 0, 1, 3)

        label = QLabel("Position :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.positionLegende = QComboBox()
        self.positionLegende.insertItems(0, placementsLegende.keys())
        self.positionLegende.setCurrentText(self.subplot.legende['position'])
        self.positionLegende.currentTextChanged.connect(self.updateLegende)
        layout.addWidget(self.positionLegende, 1, 1)

        label = QLabel("Colonnes :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.colonnesLegende = QSpinBox()
        self.colonnesLegende.setFixedWidth(45)
        self.colonnesLegende.setRange(1, 99)
        self.colonnesLegende.setValue(self.subplot.legende['nombre de colonnes'])
        self.colonnesLegende.valueChanged.connect(self.updateLegende)
        layout.addWidget(self.colonnesLegende, 2, 1)

        layout.addWidget(QLabel(), 3, 0, 5, 1)

        onglet_legende.setLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)

        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainlayout = QVBoxLayout()

        mainlayout.addWidget(tableWidget)

        mainlayout.addWidget(buttonBox)

        self.setLayout(mainlayout)

    def appliquer(self):
        self.subplot.subdivisions = self.subdivisions.value()
        self.pyLong.canvas.dessiner()

    def updateLegende(self):
        self.subplot.legende['active'] = self.dessinerLegende.isChecked()
        self.subplot.legende['position'] = self.positionLegende.currentText()
        self.subplot.legende['nombre de colonnes'] = self.colonnesLegende.value()

        self.pyLong.canvas.updateLegendes()

    def updateOrdonneesSubplot(self):
        i = self.parent.listeSubplots.currentRow()

        self.subplot.ordonnees['min'] = self.ordonneesMin.value()
        self.subplot.ordonnees['max'] = self.ordonneesMax.value()
        self.subplot.ordonnees['intervalles'] = self.ordonneesInt.value()
        self.subplot.ordonnees['libellé'] = self.libelle.text()
        self.subplot.ordonnees['couleur libellé'] = self.couleurLibelle.currentText()
        self.subplot.ordonnees['couleur valeur'] = self.couleurValeur.currentText()
        self.subplot.ordonnees['delta bas'] = self.deltaBas.value()
        self.subplot.ordonnees['delta haut'] = self.deltaHaut.value()

        self.pyLong.canvas.subplots[i].set_ylim((self.subplot.ordonnees['min'] - self.subplot.ordonnees['delta bas'],
                                                 self.subplot.ordonnees['max'] + self.subplot.ordonnees['delta haut']))

        self.pyLong.canvas.subplots[i].set_yticks(np.linspace(self.subplot.ordonnees['min'],
                                                              self.subplot.ordonnees['max'],
                                                              self.subplot.ordonnees['intervalles'] + 1))

        self.pyLong.canvas.subplots[i].set_ylabel(self.subplot.ordonnees['libellé'],
                                                  {'color': couleurs[self.subplot.ordonnees['couleur libellé']],
                                                   'fontsize': self.layout.altitudes['taille libellé']})

        self.pyLong.canvas.subplots[i].tick_params(axis='y',
                                                   colors=couleurs[self.subplot.ordonnees['couleur valeur']],
                                                   labelsize=self.layout.altitudes['taille valeur'])

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)
        self.pyLong.canvas.draw()
