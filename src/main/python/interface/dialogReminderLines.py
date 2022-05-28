from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.LigneRappel import *

from DialogConfigLigneRappel import *

from pyLong.dictionnaires import *


class DialogLignesRappel(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.listeLayouts.currentIndex()
        self.layout = self.pyLong.projet.layouts[i]

        self.setMinimumWidth(225)
        self.setWindowTitle("Gestion des lignes de rappel")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rappel.png')))
        
        mainLayout = QVBoxLayout()
        
        self.liste = QListWidget()
        self.liste.doubleClicked.connect(self.proprietes)
        self.liste.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.liste.itemChanged.connect(self.update_actif)
        for ligneRappel in self.pyLong.projet.lignesRappel:
            item = QListWidgetItem()
            item.setText("X = {} m".format(ligneRappel.abscisse))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if ligneRappel.actif:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.liste.addItem(item)

        mainLayout.addWidget(self.liste)

        layout = QHBoxLayout()

        ascendant = QPushButton()
        ascendant.setAutoDefault(False)
        ascendant.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/monter.png')))
        ascendant.setFixedSize(QSize(25, 25))
        ascendant.clicked.connect(self.ascendant)
        layout.addWidget(ascendant)

        descendant = QPushButton()
        descendant.setAutoDefault(False)
        descendant.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/descendre.png')))
        descendant.setFixedSize(QSize(25, 25))
        descendant.clicked.connect(self.descendant)
        layout.addWidget(descendant)

        layout.addWidget(QLabel())

        proprietes = QPushButton()
        proprietes.setAutoDefault(False)
        proprietes.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/config.png')))
        proprietes.setFixedSize(QSize(25, 25))
        proprietes.clicked.connect(self.proprietes)
        layout.addWidget(proprietes)

        layout.addWidget(QLabel())

        ajouter = QPushButton("+")
        ajouter.setAutoDefault(False)
        ajouter.setFixedSize(QSize(25, 25))
        ajouter.clicked.connect(self.ajouter)
        layout.addWidget(ajouter)

        supprimer = QPushButton("-")
        supprimer.setAutoDefault(False)
        supprimer.setFixedSize(QSize(25, 25))
        supprimer.clicked.connect(self.supprimer)
        layout.addWidget(supprimer)

        mainLayout.addLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close | QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.Apply).setText("Actualiser")
        buttonBox.button(QDialogButtonBox.Apply).setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rafraichir.png')))
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)

        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def update_actif(self):
        for i in range(self.liste.count()):
            ligne = self.pyLong.projet.lignesRappel[i]
            if self.liste.item(i).checkState() == Qt.Checked:
                ligne.actif = True
            else:
                ligne.actif = False

    def valider(self):
        self.appliquer()
        self.accept()

    def appliquer(self):
        self.pyLong.canvas.dessiner()

    def ascendant(self):
        self.pyLong.projet.lignesRappel.sort()
        self.update()

    def descendant(self):
        self.pyLong.projet.lignesRappel.sort(reverse=True)
        self.update()

    def proprietes(self):
        if self.selection():
            DialogConfigLigneRappel(parent=self).exec_()

    def selection(self):
        n = self.liste.count()
        selections = []

        for i in range(n):
            selections.append(self.liste.item(i).isSelected())

        return n > 0 and True in selections

    def supprimer(self):
        if self.selection():
            indices = []
            for item in self.liste.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]

                self.pyLong.projet.lignesRappel.pop(i)
                self.update()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

            else:
                for i in indices:
                    self.pyLong.projet.lignesRappel.pop(i)

                self.update()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

        else:
            pass

    def ajouter(self):
        ligne = LigneRappel()
        ligne.subplots = list(self.pyLong.projet.subplots)
        self.pyLong.projet.lignesRappel.append(ligne)
        self.update()

    def update(self):
        self.liste.clear()
        for ligneRappel in self.pyLong.projet.lignesRappel:
            item = QListWidgetItem()
            item.setText("X = {} m".format(ligneRappel.abscisse))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if ligneRappel.actif:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.liste.addItem(item)
