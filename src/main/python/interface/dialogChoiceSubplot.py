from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.Subplot import *


class DialogChoixSubplot(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.pyLong = parent.pyLong

        i = self.pyLong.listeLayouts.currentIndex()
        self.layout = self.pyLong.projet.layouts[i]

        self.setWindowTitle("Choix d'un subplot")

        mainLayout = QVBoxLayout()

        groupe = QGroupBox("Subplots disponibles")
        layout = QVBoxLayout()

        self.listeSubplots = QListWidget()
        self.listeSubplots.doubleClicked.connect(self.valider)
        liste = []
        for i in range(self.parent.listeSubplots.count()):
            liste.append(self.parent.listeSubplots.item(i).text())
        for subplots in self.pyLong.projet.subplots:
            if subplots not in liste:
                self.listeSubplots.addItem(subplots)

        layout.addWidget(self.listeSubplots)

        groupe.setLayout(layout)

        mainLayout.addWidget(groupe)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttonBox.button(QDialogButtonBox.Cancel).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def valider(self):
        i = self.listeSubplots.currentIndex()
        if i == -1:
            pass
        else:
            subplot = Subplot()
            subplot.identifiant = self.listeSubplots.currentItem().text()

            self.layout.subplots.append(subplot)

            self.accept()
