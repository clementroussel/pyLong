from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from DialogAjoutSubplot import *


class DialogGestionSubplots(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.pyLong = parent

        self.setWindowTitle("Gestion des subplots")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/gestion_subplots.png')))

        mainLayout = QVBoxLayout()

        groupe = QGroupBox("Subplots disponibles")
        layout = QVBoxLayout()

        self.listeSubplots = QListWidget()
        for subplots in self.pyLong.projet.subplots:
            self.listeSubplots.addItem(subplots)

        layout.addWidget(self.listeSubplots)

        sublayout = QHBoxLayout()

        sublayout.addWidget(QLabel())

        ajouterSubplot = QPushButton("+")
        ajouterSubplot.setAutoDefault(False)
        ajouterSubplot.setFixedSize(QSize(25, 25))
        ajouterSubplot.clicked.connect(self.ajouterSubplot)
        sublayout.addWidget(ajouterSubplot)

        supprimerSubplots = QPushButton("-")
        supprimerSubplots.setAutoDefault(False)
        supprimerSubplots.setFixedSize(QSize(25, 25))
        supprimerSubplots.clicked.connect(self.supprimerSubplot)
        sublayout.addWidget(supprimerSubplots)

        layout.addLayout(sublayout)

        groupe.setLayout(layout)

        mainLayout.addWidget(groupe)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def supprimerSubplot(self):
        i = self.listeSubplots.currentRow()
        subplot = self.pyLong.projet.subplots[i]

        l = []
        for layout in self.pyLong.projet.layouts:
            l += [subplot.identifiant for subplot in layout.subplots]

        l += [donnee.subplot for donnee in self.pyLong.projet.autresDonnees]

        for ligne in self.pyLong.projet.lignesRappel:
            l += [subplot for subplot in ligne.subplots]

        if subplot not in l:
            self.pyLong.projet.subplots.remove(subplot)
        else:
            alerte = QMessageBox(self)
            alerte.setText("Suppression impossible. Le subplot {} est utilisé.".format(subplot))
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

        self.updateListe()

    def ajouterSubplot(self):
        DialogAjoutSubplot(parent=self).exec_()
        self.updateListe()

    def updateListe(self):
        self.listeSubplots.clear()
        for subplots in self.pyLong.projet.subplots:
            self.listeSubplots.addItem(subplots)
