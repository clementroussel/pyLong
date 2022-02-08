from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Liste import *


class ListeAutresDonnees(Liste):
    def __init__(self, intitule, parent):
        super().__init__(intitule)

        self.pyLong = parent

        self.liste.doubleClicked.connect(self.pyLong.optionsDonnees)
        self.liste.itemChanged.connect(self.activer)

        self.liste.setContextMenuPolicy(Qt.CustomContextMenu)
        self.liste.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.action_ajouterDonnees)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.action_styleDonnees)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.action_supprimerDonnees)

        layout = QVBoxLayout()

        layout.addWidget(self.liste)
        self.setLayout(layout)

    def contextMenu(self, point):
        self.popMenu.exec_(self.liste.mapToGlobal(point))

    def update(self):
        self.liste.clear()
        for donnee in self.pyLong.projet.autresDonnees:
            item = QListWidgetItem()
            item.setText(donnee.intitule)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if donnee.visible:
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

    def supprimer(self):
        if self.selection():
            indices = []
            for item in self.liste.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]
                donnee = self.pyLong.projet.autresDonnees[i]

                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Supprimer une donnée")
                dialogue.setText("Supprimer la donnée : {} ?".format(donnee.intitule))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Oui")
                dialogue.button(QMessageBox.No).setText("Non")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    try:
                        donnee.line.remove()
                    except:
                        pass
                    self.pyLong.projet.autresDonnees.pop(i)
                    self.update()
                    self.pyLong.canvas.draw()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

            else:
                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Supprimer plusieurs données")
                dialogue.setText("Supprimer les {} données sélectionnées ?".format(len(indices)))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Oui")
                dialogue.button(QMessageBox.No).setText("Non")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    for i in indices:
                        donnee = self.pyLong.projet.autresDonnees[i]
                        donnee.line.remove()
                        self.pyLong.projet.autresDonnees.pop(i)

                    self.update()
                    self.pyLong.canvas.draw()

                    try:
                        self.liste.setCurrentRow(i)
                    except:
                        pass

        else:
            alerte = QMessageBox(self)
            alerte.setText("Sélectionnez une ou plusieurs donnée(s) avant de lancer cette commande.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def activer(self):
        for j in range(self.liste.count()):
            donnee = self.pyLong.projet.autresDonnees[j]

            if self.liste.item(j).checkState() == Qt.Checked:
                donnee.visible = True
            else:
                donnee.visible = False

            donnee.update()

        self.pyLong.canvas.draw()
