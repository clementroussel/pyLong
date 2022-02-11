from PyQt5.QtWidgets import QVBoxLayout, QListWidgetItem, QMessageBox, QHBoxLayout, QMenu, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from interface.list import List
from interface.checkableComboBox import CheckableComboBox

from pyLong.text import Text
from pyLong.verticalAnnotation import VerticalAnnotation
from pyLong.linearAnnotation import LinearAnnotation
from pyLong.interval import Interval
from pyLong.rectangle import Rectangle

# from DialogTexte import *
# from DialogAnnotationPonctuelle import *
# from DialogAnnotationLineaire import *
# from DialogZone import *
# from DialogRectangle import *
# from DialogGestionGroupes import *

# from DialogAjoutGroupe import *
# from DialogRenommerGroupe import *
# from DialogSupprimerGroupes import *

from pyLong.reminderLine import ReminderLine


class AnnotationsList(List):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.pyLong = parent

        # self.liste.doubleClicked.connect(self.ouvrirAnnotation)
        # self.liste.itemChanged.connect(self.activerAnnotation)

        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.addTextAction)
        self.popMenu.addAction(self.pyLong.addVerticalAnnotationAction)
        self.popMenu.addAction(self.pyLong.addLinearAnnotationAction)
        self.popMenu.addAction(self.pyLong.addIntervalAction)
        self.popMenu.addAction(self.pyLong.addRectangleAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.annotationStyleAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.copyStyleAction)
        self.popMenu.addAction(self.pyLong.pasteStyleAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.adjustVerticalAnnotationAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.duplicateAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.groupsManagerAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.annotationDeleteAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.annotation2reminderLineAction)
        self.popMenu.addAction(self.pyLong.reminderLinesManagerAction)

        layout = QVBoxLayout()

        sublayout = QHBoxLayout()

        self.groups = CheckableComboBox()
        for i, group in enumerate(self.pyLong.project.groups):
            self.groups.addItem(group.title)
            self.groups.setItemChecked(i, group.active)

        # self.groupes.activated.connect(self.activerGroupe)
        # self.groupes.currentIndexChanged.connect(self.updateListe)
        self.groups.setContextMenuPolicy(Qt.CustomContextMenu)
        self.groups.customContextMenuRequested.connect(self.contextMenuGroups)

        self.popMenuGroups = QMenu(self)

        self.popMenuGroups.addAction(self.pyLong.addGroupAction)
        self.popMenuGroups.addSeparator()
        self.popMenuGroups.addAction(self.pyLong.renameGroupAction)
        self.popMenuGroups.addSeparator()
        self.popMenuGroups.addAction(self.pyLong.deleteGroupAction)

        sublayout.addWidget(self.groups)

        # self.goUp.clicked.connect(self.goTop)
        sublayout.addWidget(self.goTop)

        # moveUp.clicked.connect(self.moveUp)
        sublayout.addWidget(self.moveUp)

        # moveDown.clicked.connect(self.moveDown)
        sublayout.addWidget(self.moveDown)

        # self.goDown.clicked.connect(self.goDown)
        sublayout.addWidget(self.goBottom)

        layout.addLayout(sublayout)
        layout.addWidget(self.list)
        self.setLayout(layout)

    def contextMenu(self, point):
        self.popMenu.exec_(self.list.mapToGlobal(point))

    def hide(self):
        if self.isChecked():
            self.list.setVisible(True)
            self.groups.setVisible(True)
            self.goTop.setVisible(True)
            self.moveUp.setVisible(True)
            self.moveDown.setVisible(True)
            self.goBottom.setVisible(True)

        else:
            self.list.setVisible(False)
            self.groups.setVisible(False)
            self.goTop.setVisible(False)
            self.moveUp.setVisible(False)
            self.moveDown.setVisible(False)
            self.goBottom.setVisible(False)

    def contextMenuGroups(self, point):
        self.popMenuGroups.exec_(self.groups.mapToGlobal(point))

    def selection(self):
        n = self.liste.count()
        selections = []

        for i in range(n):
            selections.append(self.liste.item(i).isSelected())

        return n > 0 and True in selections

    def ouvrirAnnotation(self):
        if self.selection():
            self.pyLong.controleOutilsNavigation()
            i = self.groupes.currentIndex()
            j = self.liste.currentRow()
            annotation = self.pyLong.projet.groupes[i].annotations[j]
            if type(annotation) == Texte:
                self.dialog = DialogTexte(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == AnnotationPonctuelle:
                self.dialog = DialogAnnotationPonctuelle(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == AnnotationLineaire:
                self.dialog = DialogAnnotationLineaire(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == Zone:
                self.dialog = DialogZone(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == Rectangle:
                self.dialog = DialogRectangle(parent=self.pyLong)
                self.dialog.show()

        else:
            alerte = QMessageBox(self)
            alerte.setText("Sélectionnez une ou plusieurs annotation(s) avant de lancer cette commande.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def ajouterGroupe(self):
        DialogAjoutGroupe(parent=self.pyLong).exec_()

    def renommerGroupe(self) :
        i = self.groupes.currentIndex()
        if i != 0:
            DialogRenommerGroupe(parent=self.pyLong).exec_()

    def supprimerGroupes(self):
        DialogSupprimerGroupes(parent=self.pyLong).exec_()

    def updateGroupes(self):
        self.groupes.clear()
        for i, groupe in enumerate(self.pyLong.projet.groupes):
            self.groupes.addItem(groupe.intitule)
            self.groupes.setItemChecked(i, groupe.actif)

    def updateListe(self):
        self.liste.clear()
        i = self.groupes.currentIndex()
        for annotation in self.pyLong.projet.groupes[i].annotations:
            item = QListWidgetItem()
            item.setText(annotation.intitule)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if annotation.actif:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.liste.addItem(item)

    def monterAnnotation(self):
        if self.selection():
            i = self.groupes.currentIndex()
            j = self.liste.currentRow()

            if j != 0:
                self.pyLong.projet.groupes[i].annotations[j-1], self.pyLong.projet.groupes[i].annotations[j] = \
                    self.pyLong.projet.groupes[i].annotations[j], self.pyLong.projet.groupes[i].annotations[j-1]
                self.updateListe()
                self.liste.setCurrentRow(j-1)

    def descendreAnnotation(self):
        if self.selection():
            i = self.groupes.currentIndex()
            j = self.liste.currentRow()

            n = self.liste.count()

            if j != n-1:
                self.pyLong.projet.groupes[i].annotations[j+1], self.pyLong.projet.groupes[i].annotations[j] = \
                    self.pyLong.projet.groupes[i].annotations[j], self.pyLong.projet.groupes[i].annotations[j+1]
                self.updateListe()
                self.liste.setCurrentRow(j+1)

    def deplacerVersHaut(self):
        if self.selection():
            i = self.groupes.currentIndex()
            j = self.liste.currentRow()

            while j != 0:
                self.monterAnnotation()
                j -= 1

    def deplacerVersBas(self):
        if self.selection():
            i = self.groupes.currentIndex()
            j = self.liste.currentRow()

            n = self.liste.count()

            while j != n-1:
                self.descendreAnnotation()
                j += 1

    def supprimer(self):
        if self.selection():
            indices = []
            for item in self.liste.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]
                annotation = self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations[i]

                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Supprimer une annotation")
                dialogue.setText("Supprimer l'annotation' : {} ?".format(annotation.intitule))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Oui")
                dialogue.button(QMessageBox.No).setText("Non")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    if type(annotation) == Texte:
                        annotation.text.remove()

                    elif type(annotation) == AnnotationPonctuelle:
                        annotation.annotation.remove()

                    elif type(annotation) == AnnotationLineaire:
                        annotation.annotation.remove()
                        annotation.text.remove()

                    elif type(annotation) == Zone:
                        annotation.text.remove()
                        annotation.left_line.remove()
                        annotation.right_line.remove()

                    elif type(annotation) == Rectangle:
                        annotation.rectangle.remove()

                    # self.pyLong.canvas.draw()
                    self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations.pop(i)
                    self.updateListe()
                    self.pyLong.canvas.updateLegendes()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

            else:
                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Supprimer plusieurs annotations")
                dialogue.setText("Supprimer les {} annotations sélectionnées ?".format(len(indices)))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Oui")
                dialogue.button(QMessageBox.No).setText("Non")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    for i in indices:
                        annotation = self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations[i]
                        if type(annotation) == Texte:
                            annotation.text.remove()

                        elif type(annotation) == AnnotationPonctuelle:
                            annotation.annotation.remove()

                        elif type(annotation) == AnnotationLineaire:
                            annotation.annotation.remove()
                            annotation.text.remove()

                        elif type(annotation) == Zone:
                            annotation.text.remove()
                            annotation.left_line.remove()
                            annotation.right_line.remove()

                        elif type(annotation) == Rectangle:
                            annotation.rectangle.remove()

                        # self.pyLong.canvas.draw()
                        self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations.pop(i)

                    self.updateListe()
                    self.pyLong.canvas.updateLegendes()

                try:
                    self.liste.setCurrentRow(i)
                except:
                    pass

        else:
            alerte = QMessageBox(self)
            alerte.setText("Sélectionnez une ou plusieurs annotation(s) avant de lancer cette commande.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def activerAnnotation(self):
        i = self.groupes.currentIndex()
        for j in range(self.liste.count()):

            annotation = self.pyLong.projet.groupes[i].annotations[j]

            if self.liste.item(j).checkState() == Qt.Checked:
                annotation.actif = True
            else:
                annotation.actif = False

            annotation.update()

        # self.pyLong.canvas.draw()
        self.pyLong.canvas.updateLegendes()

    def activerGroupe(self):
        for i in range(self.groupes.count()):
            if self.groupes.itemChecked(i):
                self.pyLong.projet.groupes[i].actif = True
            else:
                self.pyLong.projet.groupes[i].actif = False

        self.pyLong.canvas.dessiner()

    def creerLigneRappel(self):
        if self.selection():
            indices = []
            for item in self.liste.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]
                annotation = self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations[i]

                if type(annotation) == Texte:
                    pass

                elif type(annotation) == AnnotationPonctuelle:
                    ligne = LigneRappel()
                    ligne.abscisse = annotation.abscisse
                    ligne.subplots = list(self.pyLong.projet.subplots)
                    self.pyLong.projet.lignesRappel.append(ligne)

                elif type(annotation) == AnnotationLineaire:
                    ligne1 = LigneRappel()
                    ligne1.abscisse = annotation.fleche['abscisse de début']
                    ligne1.subplots = list(self.pyLong.projet.subplots)
                    self.pyLong.projet.lignesRappel.append(ligne1)

                    ligne2 = LigneRappel()
                    ligne2.abscisse = annotation.fleche['abscisse de fin']
                    ligne2.subplots = list(self.pyLong.projet.subplots)
                    self.pyLong.projet.lignesRappel.append(ligne2)

                elif type(annotation) == Zone:
                    ligne1 = LigneRappel()
                    ligne1.abscisse = annotation.zone['abscisse de début']
                    ligne1.subplots = list(self.pyLong.projet.subplots)
                    self.pyLong.projet.lignesRappel.append(ligne1)

                    ligne2 = LigneRappel()
                    ligne2.abscisse = annotation.zone['abscisse de fin']
                    ligne2.subplots = list(self.pyLong.projet.subplots)
                    self.pyLong.projet.lignesRappel.append(ligne2)

                elif type(annotation) == Rectangle:
                    pass

                self.pyLong.canvas.dessiner()

            else:
                for i in indices:
                    annotation = self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations[i]

                    if type(annotation) == Texte:
                        pass

                    elif type(annotation) == AnnotationPonctuelle:
                        ligne = LigneRappel()
                        ligne.abscisse = annotation.abscisse
                        ligne.subplots = list(self.pyLong.projet.subplots)
                        self.pyLong.projet.lignesRappel.append(ligne)

                    elif type(annotation) == AnnotationLineaire:
                        ligne1 = LigneRappel()
                        ligne1.abscisse = annotation.fleche['abscisse de début']
                        ligne1.subplots = list(self.pyLong.projet.subplots)
                        self.pyLong.projet.lignesRappel.append(ligne1)

                        ligne2 = LigneRappel()
                        ligne2.abscisse = annotation.fleche['abscisse de fin']
                        ligne2.subplots = list(self.pyLong.projet.subplots)
                        self.pyLong.projet.lignesRappel.append(ligne2)

                    elif type(annotation) == Zone:
                        ligne1 = LigneRappel()
                        ligne1.abscisse = annotation.zone['abscisse de début']
                        ligne1.subplots = list(self.pyLong.projet.subplots)
                        self.pyLong.projet.lignesRappel.append(ligne1)

                        ligne2 = LigneRappel()
                        ligne2.abscisse = annotation.zone['abscisse de fin']
                        ligne2.subplots = list(self.pyLong.projet.subplots)
                        self.pyLong.projet.lignesRappel.append(ligne2)

                    elif type(annotation) == Rectangle:
                        pass

                self.pyLong.canvas.dessiner()

        else:
            alerte = QMessageBox(self)
            alerte.setText("Sélectionnez une ou plusieurs annotation(s) avant de lancer cette commande.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

