from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Liste import *

from pyLong.LigneEnergie import *
from pyLong.Mezap import *
from pyLong.FlowR import *
from pyLong.Rickenmann import *
from pyLong.Corominas import *

from DialogLigneEnergie import *
from DialogMezap import *
from DialogFlowR import *
from DialogRickenmann import *
from DialogCorominas import *


class ListeCalculs(Liste):
    def __init__(self, intitule, parent):
        super().__init__(intitule)

        self.pyLong = parent

        self.liste.doubleClicked.connect(self.ouvrirCalcul)
        self.liste.itemChanged.connect(self.activer)

        self.liste.setContextMenuPolicy(Qt.CustomContextMenu)
        self.liste.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.action_toolbox)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.action_calcul)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.action_supprimerCalculs)

        layout = QVBoxLayout()

        layout.addWidget(self.liste)
        self.setLayout(layout)

    def contextMenu(self, point):
        self.popMenu.exec_(self.liste.mapToGlobal(point))

    def update(self):
        self.liste.clear()
        for calcul in self.pyLong.projet.calculs:
            item = QListWidgetItem()
            item.setText(calcul.intitule)
            if type(calcul) != Mezap:
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if calcul.actif:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
            self.liste.addItem(item)

    def selection(self):
        n = self.liste.count()
        selections = []

        for i in range(n):
            selections.append(self.liste.item(i).isSelected())

        return n > 0 and True in selections

    def ouvrirCalcul(self):
        if self.selection():
            i = self.liste.currentRow()
            calcul = self.pyLong.projet.calculs[i]

            if type(calcul) == LigneEnergie:
                DialogLigneEnergie(parent=self.pyLong).exec_()
            elif type(calcul) == Mezap:
                DialogMezap(parent=self.pyLong).exec_()
            elif type(calcul) == FlowR:
                DialogFlowR(parent=self.pyLong).exec_()
            elif type(calcul) == Rickenmann:
                DialogRickenmann(parent=self.pyLong).exec_()
            elif type(calcul) == Corominas:
                DialogCorominas(parent=self.pyLong).exec_()

        else:
            alerte = QMessageBox(self)
            alerte.setText("Sélectionnez un calcul avant de lancer cette commande.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def supprimer(self):
        if self.selection():
            indices = []
            for item in self.liste.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]
                calcul = self.pyLong.projet.calculs[i]

                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Supprimer un calcul")
                dialogue.setText("Supprimer le calcul : {} ?".format(calcul.intitule))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Oui")
                dialogue.button(QMessageBox.No).setText("Non")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    if type(calcul) in [LigneEnergie, Rickenmann, FlowR, Corominas]:
                        calcul.line.remove()

                    self.pyLong.projet.calculs.pop(i)
                    self.update()
                    # self.pyLong.canvas.draw()
                    self.pyLong.canvas.updateLegendes()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

            else:
                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Supprimer plusieurs calculs")
                dialogue.setText("Supprimer les {} calculs sélectionnés ?".format(len(indices)))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Oui")
                dialogue.button(QMessageBox.No).setText("Non")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    for i in indices:
                        calcul = self.pyLong.projet.calculs[i]
                        if type(calcul) in [LigneEnergie, Rickenmann, FlowR, Corominas]:
                            calcul.line.remove()

                        self.pyLong.projet.calculs.pop(i)

                    self.update()
                    # self.pyLong.canvas.draw()
                    self.pyLong.canvas.updateLegendes()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

        else:
            alerte = QMessageBox(self)
            alerte.setText("Sélectionnez un ou plusieurs calcul(s) avant de lancer cette commande.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def activer(self):
        for j in range(self.liste.count()):
            calcul = self.pyLong.projet.calculs[j]
            if type(calcul) != Mezap:
                if self.liste.item(j).checkState() == Qt.Checked:
                    calcul.actif = True
                else:
                    calcul.actif = False

                calcul.update()

        self.pyLong.canvas.draw()
