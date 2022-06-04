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

from interface.dialogText import *
from interface.dialogVerticalAnnotation import *
from interface.dialogLinearAnnotation import *
from interface.dialogInterval import *
from interface.dialogRectangle import *
from interface.dialogManageGroups import *

from interface.dialogAddGroup import *
from interface.dialogRenameGroup import *
from interface.dialogDeleteGroups import *

from pyLong.reminderLine import ReminderLine


class AnnotationsList(List):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.pyLong = parent

        # self.list.doubleClicked.connect(self.annotationStyle)
        # self.list.itemChanged.connect(self.activate)

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

        subsublayout = QVBoxLayout()

        self.groups = CheckableComboBox()
        for i, group in enumerate(self.pyLong.project.groups):
            self.groups.addItem(group.title)
            self.groups.setItemChecked(i, group.active)

        self.groups.activated.connect(self.activateGroup)
        self.groups.currentIndexChanged.connect(self.updateList)
        self.groups.setContextMenuPolicy(Qt.CustomContextMenu)
        self.groups.customContextMenuRequested.connect(self.contextMenuGroups)

        self.popMenuGroups = QMenu(self)

        self.popMenuGroups.addAction(self.pyLong.addGroupAction)
        self.popMenuGroups.addSeparator()
        self.popMenuGroups.addAction(self.pyLong.renameGroupAction)
        self.popMenuGroups.addSeparator()
        self.popMenuGroups.addAction(self.pyLong.deleteGroupsAction)

        layout.addWidget(self.groups)

        sublayout.addWidget(self.list)

        self.goTop.clicked.connect(self.goTopMethod)
        subsublayout.addWidget(self.goTop)

        self.moveUp.clicked.connect(self.moveUpMethod)
        subsublayout.addWidget(self.moveUp)

        self.moveDown.clicked.connect(self.moveDownMethod)
        subsublayout.addWidget(self.moveDown)

        self.goBottom.clicked.connect(self.goBottomMethod)
        subsublayout.addWidget(self.goBottom)

        sublayout.addLayout(subsublayout)
        layout.addLayout(sublayout)
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
        n = self.list.count()
        selections = []

        for i in range(n):
            selections.append(self.list.item(i).isSelected())

        return n > 0 and True in selections

    def annotationStyle(self):
        if self.selection():
            self.pyLong.checkNavigationTools()
            i = self.groups.currentIndex()
            j = self.list.currentRow()
            annotation = self.pyLong.project.groups[i].annotations[j]
            if type(annotation) == Text:
                self.dialog = DialogText(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == VerticalAnnotation:
                self.dialog = DialogVerticalAnnotation(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == LinearAnnotation:
                self.dialog = DialogLinearAnnotation(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == Interval:
                self.dialog = DialogInterval(parent=self.pyLong)
                self.dialog.show()
            elif type(annotation) == Rectangle:
                self.dialog = DialogRectangle(parent=self.pyLong)
                self.dialog.show()

        else:
            alert = QMessageBox(self)
            alert.setText("Select an annotation before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def addGroup(self):
        DialogAddGroup(parent=self.pyLong).exec_()

    def renameGroup(self) :
        i = self.groups.currentIndex()
        if i != 0:
            DialogRenameGroup(parent=self.pyLong).exec_()

    def deleteGroups(self):
        DialogDeleteGroups(parent=self.pyLong).exec_()

    def updateGroups(self):
        self.groups.clear()
        for i, group in enumerate(self.pyLong.project.groups):
            self.groups.addItem(group.title)
            self.groups.setItemChecked(i, group.active)

    def updateList(self):
        self.list.clear()
        i = self.groups.currentIndex()
        for annotation in self.pyLong.project.groups[i].annotations:
            item = QListWidgetItem()
            item.setText(annotation.title)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if annotation.active:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.list.addItem(item)

    def moveUpMethod(self):
        if self.selection():
            i = self.groups.currentIndex()
            j = self.list.currentRow()

            if j != 0:
                self.pyLong.project.groups[i].annotations[j-1], self.pyLong.project.groups[i].annotations[j] = \
                    self.pyLong.project.groups[i].annotations[j], self.pyLong.project.groups[i].annotations[j-1]
                self.updateList()
                self.list.setCurrentRow(j-1)

    def moveDownMethod(self):
        if self.selection():
            i = self.groups.currentIndex()
            j = self.list.currentRow()

            n = self.list.count()

            if j != n-1:
                self.pyLong.project.groups[i].annotations[j+1], self.pyLong.project.groups[i].annotations[j] = \
                    self.pyLong.project.groups[i].annotations[j], self.pyLong.project.groups[i].annotations[j+1]
                self.updateList()
                self.list.setCurrentRow(j+1)

    def goTopMethod(self):
        if self.selection():
            i = self.groups.currentIndex()
            j = self.list.currentRow()

            while j != 0:
                self.moveUpMethod()
                j -= 1

    def goBottomMethod(self):
        if self.selection():
            i = self.groups.currentIndex()
            j = self.list.currentRow()

            n = self.list.count()

            while j != n-1:
                self.moveDownMethod()
                j += 1

    def delete(self):
        if self.selection():
            indexes = []
            for item in self.list.selectedIndexes():
                indexes.append(item.row())

            indexes.sort()
            indexes.reverse()

            if len(indexes) == 1:
                i = indexes[0]
                annotation = self.pyLong.project.groups[self.groups.currentIndex()].annotations[i]

                dialog = QMessageBox(self)
                dialog.setWindowTitle("Delete an annotation")
                dialog.setText("Delete : {} ?".format(annotation.title))
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
                    if type(annotation) == Text:
                        annotation.text.remove()

                    elif type(annotation) == VerticalAnnotation:
                        annotation.annotation.remove()

                    elif type(annotation) == LinearAnnotation:
                        annotation.annotation.remove()
                        annotation.text.remove()

                    elif type(annotation) == Interval:
                        annotation.text.remove()
                        annotation.left_line.remove()
                        annotation.right_line.remove()

                    elif type(annotation) == Rectangle:
                        annotation.rectangle.remove()

                    self.pyLong.project.groups[self.groups.currentIndex()].annotations.pop(i)
                    self.updateListe()
                    self.pyLong.canvas.updateLegends()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

            else:
                dialog = QMessageBox(self)
                dialog.setWindowTitle("Delete annotations")
                dialog.setText("Delete the {} annotations selected ?".format(len(indexes)))
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
                    for i in indexes:
                        annotation = self.pyLong.project.groups[self.groups.currentIndex()].annotations[i]
                        if type(annotation) == Text:
                            annotation.text.remove()

                        elif type(annotation) == VerticalAnnotation:
                            annotation.annotation.remove()

                        elif type(annotation) == LinearAnnotation:
                            annotation.annotation.remove()
                            annotation.text.remove()

                        elif type(annotation) == Interval:
                            annotation.text.remove()
                            annotation.left_line.remove()
                            annotation.right_line.remove()

                        elif type(annotation) == Rectangle:
                            annotation.rectangle.remove()

                        self.pyLong.project.groups[self.groups.currentIndex()].annotations.pop(i)

                    self.updateListe()
                    self.pyLong.canvas.updateLegends()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

        else:
            alert = QMessageBox(self)
            alert.setText("Select at least one annotation before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def activateAnnotation(self):
        i = self.groups.currentIndex()
        for j in range(self.list.count()):

            annotation = self.pyLong.project.groups[i].annotations[j]

            if self.list.item(j).checkState() == Qt.Checked:
                annotation.active = True
            else:
                annotation.active = False

            annotation.update()

        self.pyLong.canvas.updateLegends()

    def activateGroup(self):
        for i in range(self.groups.count()):
            if self.groups.itemChecked(i):
                self.pyLong.project.groups[i].active = True
            else:
                self.pyLong.project.groups[i].active = False

        self.pyLong.canvas.updateFigure()

    # def creerLigneRappel(self):
    #     if self.selection():
    #         indexes = []
    #         for item in self.liste.selectedIndexes():
    #             indexes.append(item.row())

    #         indexes.sort()
    #         indexes.reverse()

    #         if len(indexes) == 1:
    #             i = indexes[0]
    #             annotation = self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations[i]

    #             if type(annotation) == Texte:
    #                 pass

    #             elif type(annotation) == AnnotationPonctuelle:
    #                 ligne = LigneRappel()
    #                 ligne.abscisse = annotation.abscisse
    #                 ligne.subplots = list(self.pyLong.projet.subplots)
    #                 self.pyLong.projet.lignesRappel.append(ligne)

    #             elif type(annotation) == AnnotationLineaire:
    #                 ligne1 = LigneRappel()
    #                 ligne1.abscisse = annotation.fleche['abscisse de début']
    #                 ligne1.subplots = list(self.pyLong.projet.subplots)
    #                 self.pyLong.projet.lignesRappel.append(ligne1)

    #                 ligne2 = LigneRappel()
    #                 ligne2.abscisse = annotation.fleche['abscisse de fin']
    #                 ligne2.subplots = list(self.pyLong.projet.subplots)
    #                 self.pyLong.projet.lignesRappel.append(ligne2)

    #             elif type(annotation) == Zone:
    #                 ligne1 = LigneRappel()
    #                 ligne1.abscisse = annotation.zone['abscisse de début']
    #                 ligne1.subplots = list(self.pyLong.projet.subplots)
    #                 self.pyLong.projet.lignesRappel.append(ligne1)

    #                 ligne2 = LigneRappel()
    #                 ligne2.abscisse = annotation.zone['abscisse de fin']
    #                 ligne2.subplots = list(self.pyLong.projet.subplots)
    #                 self.pyLong.projet.lignesRappel.append(ligne2)

    #             elif type(annotation) == Rectangle:
    #                 pass

    #             self.pyLong.canvas.dessiner()

    #         else:
    #             for i in indexes:
    #                 annotation = self.pyLong.projet.groupes[self.groupes.currentIndex()].annotations[i]

    #                 if type(annotation) == Texte:
    #                     pass

    #                 elif type(annotation) == AnnotationPonctuelle:
    #                     ligne = LigneRappel()
    #                     ligne.abscisse = annotation.abscisse
    #                     ligne.subplots = list(self.pyLong.projet.subplots)
    #                     self.pyLong.projet.lignesRappel.append(ligne)

    #                 elif type(annotation) == AnnotationLineaire:
    #                     ligne1 = LigneRappel()
    #                     ligne1.abscisse = annotation.fleche['abscisse de début']
    #                     ligne1.subplots = list(self.pyLong.projet.subplots)
    #                     self.pyLong.projet.lignesRappel.append(ligne1)

    #                     ligne2 = LigneRappel()
    #                     ligne2.abscisse = annotation.fleche['abscisse de fin']
    #                     ligne2.subplots = list(self.pyLong.projet.subplots)
    #                     self.pyLong.projet.lignesRappel.append(ligne2)

    #                 elif type(annotation) == Zone:
    #                     ligne1 = LigneRappel()
    #                     ligne1.abscisse = annotation.zone['abscisse de début']
    #                     ligne1.subplots = list(self.pyLong.projet.subplots)
    #                     self.pyLong.projet.lignesRappel.append(ligne1)

    #                     ligne2 = LigneRappel()
    #                     ligne2.abscisse = annotation.zone['abscisse de fin']
    #                     ligne2.subplots = list(self.pyLong.projet.subplots)
    #                     self.pyLong.projet.lignesRappel.append(ligne2)

    #                 elif type(annotation) == Rectangle:
    #                     pass

    #             self.pyLong.canvas.dessiner()

    #     else:
    #         alerte = QMessageBox(self)
    #         alerte.setText("Sélectionnez une ou plusieurs annotation(s) avant de lancer cette commande.")
    #         alerte.setIcon(QMessageBox.Warning)
    #         alerte.exec_()

