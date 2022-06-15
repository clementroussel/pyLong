from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QMessageBox, QApplication
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QImage

# PyQt5 custom modules
# from barreOutils import *
from interface.actions import createActions
from interface.canvas import Canvas

from interface.profilesList import ProfilesList
from interface.annotationsList import AnnotationsList
from interface.calculationsList import CalculationsList
from interface.otherDataList import OtherDataList

from interface.dialogLayout import DialogLayout
# from ListeAnnotations import *
# from ListeCalculs import *
# from ListeAutresDonnees import *

from interface.dialogSettings import *

from interface.dialogAddLayout import *
from interface.dialogRenameLayout import *
from interface.dialogDeleteLayouts import *

# from DialogLayout import *
from interface.dialogLayoutAvanced import *
# from DialogImprimer import *

from interface.dialogManageSubplots import *

from interface.dialogAddProfile import DialogAddProfile
from interface.dialogProfileOptions import *
# from DialogTableauValeurs import *
from interface.dialogSort import *
from interface.dialogFilter import *
from interface.dialogSimplify import *
from interface.dialogExport import *

from interface.dialogAdjustAnnotations import *
from interface.dialogManageGroups import *

from interface.dialogReminderLines import *

from interface.dialogToolBox import *

from interface.dialogAddData import *
from interface.dialogDataOptions import *

# matplotlib modules
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# python modules
import os
# import pickle
# from pickle import Pickler, Unpickler
import json
# from main.python.pyLong.verticalAnnotation import VerticalAnnotation

# pyLong modules
from pyLong.project import Project

from pyLong.text import *
from pyLong.verticalAnnotation import *
from pyLong.linearAnnotation import *
from pyLong.interval import *
from pyLong.rectangle import *


class NavigationBar(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Back', 'Forward', 'Pan', 'Zoom')]


class MainWindow(QMainWindow):
    def __init__(self, appctxt):
        super().__init__()
        self.setWindowTitle("pyLong")

        centralWidget = QWidget()
        mainLayout = QHBoxLayout()
        
        self.appctxt = appctxt

        with open(self.appctxt.get_resource('recent/projects.json')) as file:
            self.recentFiles = json.load(file)['chemins']

        self.project = Project()

        self.interactiveEdition = False

        self.freeze = False

        self.canvas = Canvas(parent=self)
#         self.canvas.mpl_connect('button_press_event', self.onDoubleClick)

        self.navigationBar = NavigationBar(self.canvas, self)
        self.navigationBar.setIconSize(QSize(20, 20))

#         menusEtOutils(self, self.appctxt)
        self.createActions()

        # self.navigationBar._actions['pan'].setText("Se déplacer")
        # self.navigationBar._actions['zoom'].setText("Zoomer")

        self.canvas.addContextMenu()

        layout = QVBoxLayout()
        self.profilesList = ProfilesList("Profiles", parent=self)
        layout.addWidget(self.profilesList)

        self.annotationsList = AnnotationsList("Annotations", parent=self)
        layout.addWidget(self.annotationsList)

        self.calculationsList = CalculationsList("Calculations (Toolbox)", parent=self)
        layout.addWidget(self.calculationsList)

        self.otherDataList = OtherDataList("Other data", parent=self)
        layout.addWidget(self.otherDataList)

        mainLayout.addLayout(layout)

        layout = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.canvas)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setVisible(True)
        layout.addWidget(self.scrollArea)
        layout.addWidget(self.navigationBar)
        mainLayout.addLayout(layout)

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        self.showMaximized()

        self.canvas.initialize()
        self.canvas.updateFigure()

    def createActions(self):
        createActions(self)

#     def ouvrirProjetRecent(self, chemin):
#         self.nouveauProjet()

#         try:
#             with open(chemin, 'rb') as fichier:
#                 myUnpickler = Unpickler(fichier)
#                 projet = myUnpickler.load()

#             self.freeze = True
#             self.projet.charger(projet)

#             self.setWindowTitle(self.projet.chemin)

#             self.listeLayouts.clear()
#             for layout in self.projet.layouts:
#                 self.listeLayouts.addItem(layout.intitule)

#             self.profilesList.update()
#             self.annotationsList.updateGroupes()
#             self.annotationsList.updateListe()
#             self.calculationsList.update()
#             self.otherDataList.update()

#             self.freeze = False
#             self.canvas.dessiner()

#         except:
#             alerte = QMessageBox(self)
#             alerte.setText("Le chargement du projet a échoué.")
#             alerte.exec_()
#             pass

#     def updateProjetsRecents(self, chemin):
#         chemins = self.recentFiles

#         chemins.reverse()
#         if chemin not in chemins:
#             chemins.append(chemin)

#         chemins.reverse()

#         if len(chemins) > 20:
#             chemins.pop()

#         with open(self.appctxt.get_resource('recent/projets.json'), 'w') as file:
#             json.dump({"chemins": chemins}, file)

#         self.menuRecent.clear()
#         for chemin in chemins:
#             self.menuRecent.addAction(f"{chemin}", lambda path=chemin: self.ouvrirProjetRecent(chemin=path))

    def calculation(self):
        self.calculationsList.calculationProperties()

    def annotationStyle(self):
        self.annotationsList.annotationStyle()

    def annotation2reminderLine(self):
        self.annotationsList.reminderLine()

    def reminderLinesManager(self):
        DialogReminderLines(parent=self).exec_()

    def adjustWidth(self):
        self.canvas.adjustWidth()

    def adjustHeight(self):
        self.canvas.adjustHeight()

    def zoomIn(self):
        self.canvas.zoomIn()

    def zoomOut(self):
        self.canvas.zoomOut()

    def dataStyle(self):
        if self.otherDataList.selection():
            DialogDataOptions(parent=self).exec_()
        else:
            alert = QMessageBox(self)
            alert.setText("Select a data before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def addData(self):
        DialogAddData(parent=self).exec_()

    def advancedLayout(self):
        DialogLayoutAdvanced(parent=self).exec_()

    def fullScreen(self, checked):
        if checked:
            self.projectToolBar.setVisible(False)
            self.interfaceToolBar.setVisible(False)
            self.figureToolBar.setVisible(False)
            self.subplotToolBar.setVisible(False)
            self.profileToolBar.setVisible(False)
            self.editingToolBar.setVisible(False)
            self.annotationToolBar.setVisible(False)
            self.reminderLineToolBar.setVisible(False)
            self.toolboxToolBar.setVisible(False)
            self.otherDataToolBar.setVisible(False)
            self.resourceToolBar.setVisible(False)
            self.onfToolBar.setVisible(False)
            self.profilesList.setVisible(False)
            self.annotationsList.setVisible(False)
            self.calculationsList.setVisible(False)
            self.otherDataList.setVisible(False)
        else:
            self.projectToolBar.setVisible(True)
            self.interfaceToolBar.setVisible(True)
            self.figureToolBar.setVisible(True)
            self.subplotToolBar.setVisible(True)
            self.profileToolBar.setVisible(True)
            self.editingToolBar.setVisible(True)
            self.annotationToolBar.setVisible(True)
            self.reminderLineToolBar.setVisible(True)
            self.toolboxToolBar.setVisible(True)
            self.otherDataToolBar.setVisible(True)
            self.resourceToolBar.setVisible(True)
            self.onfToolBar.setVisible(True)
            self.profilesList.setVisible(True)
            self.annotationsList.setVisible(True)
            self.calculationsList.setVisible(True)
            self.otherDataList.setVisible(True)

#     def quitterPylong(self):
#         dialogue = QMessageBox(self)
#         dialogue.setWindowTitle("Quitter pyLong")
#         dialogue.setText("Enregistrer le projet ?")
#         dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
#         dialogue.button(QMessageBox.Yes).setText("Oui")
#         dialogue.button(QMessageBox.No).setText("Non")
#         dialogue.button(QMessageBox.Cancel).setText("Annuler")
#         dialogue.setIcon(QMessageBox.Question)
#         reponse = dialogue.exec_()

#         if reponse == QMessageBox.Yes:
#             self.enregistrerProjet()
#             self.appctxt.app.quit()
#         elif reponse == QMessageBox.No:
#             self.appctxt.app.quit()
#         else:
#             pass

#     def closeEvent(self, event):
#         dialogue = QMessageBox(self)
#         dialogue.setWindowTitle("Quitter pyLong")
#         dialogue.setText("Enregistrer le projet ?")
#         dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
#         dialogue.button(QMessageBox.Yes).setText("Oui")
#         dialogue.button(QMessageBox.No).setText("Non")
#         dialogue.button(QMessageBox.Cancel).setText("Annuler")
#         dialogue.setIcon(QMessageBox.Question)
#         reponse = dialogue.exec_()

#         if reponse == QMessageBox.Yes:
#             self.enregistrerProjet()
#         elif reponse == QMessageBox.No:
#             event.accept()
#         else:
#             event.ignore()

    def subplotsManager(self):
        DialogManageSubplots(parent=self).exec_()

    def groupsManager(self):
        i = self.annotationsList.groups.currentIndex()
        DialogManageGroups(parent=self).exec_()
        self.annotationsList.updateGroups()
        self.annotationsList.groups.setCurrentIndex(i)
        self.annotationsList.updateList()
        self.canvas.updateFigure()

    def duplicate(self):
        if self.annotationsList.selection():
            j = self.annotationsList.groups.currentIndex()
            indexes = []
            for item in self.annotationsList.list.selectedIndexes():
                indexes.append(item.row())

            for i in indexes:
                annotation = self.project.groups[j].annotations[i]
                if type(annotation) == Text:
                    newAnnotation = annotation.duplicate()
                    self.project.groups[j].annotations.append(newAnnotation)
                    self.canvas.ax_z.add_artist(newAnnotation.text)
                elif type(annotation) == VerticalAnnotation:
                    newAnnotation = annotation.duplicate()
                    self.project.groups[j].annotations.append(newAnnotation)
                    self.canvas.ax_z.add_artist(newAnnotation.annotation)
                elif type(annotation) == LinearAnnotation:
                    newAnnotation = annotation.duplicate()
                    self.project.groups[j].annotations.append(newAnnotation)
                    self.canvas.ax_z.add_artist(newAnnotation.annotation)
                    self.canvas.ax_z.add_artist(newAnnotation.text)
                elif type(annotation) == Interval:
                    newAnnotation = annotation.duplicate()
                    self.project.groups[j].annotations.append(newAnnotation)
                    self.canvas.ax_z.add_artist(newAnnotation.text)
                    self.canvas.ax_z.add_line(newAnnotation.startLine)
                    self.canvas.ax_z.add_line(newAnnotation.endLine)
                else:
                    newAnnotation = annotation.duplicate()
                    self.project.groups[j].annotations.append(newAnnotation)
                    self.canvas.ax_z.add_patch(newAnnotation.rectangle)

            self.annotationsList.updateList()
            self.canvas.updateLegends()

        else:
            alert = QMessageBox(self)
            alert.setText("Select at least one annotation before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def copyStyle(self):
        if self.annotationsList.selection():
            i = self.annotationsList.groups.currentIndex()
            j = self.annotationsList.list.currentRow()
            self.project.modelAnnotation = self.project.groups[i].annotations[j]
        else:
            alert = QMessageBox(self)
            alert.setText("Select an annotation before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def pasteStyle(self):
        if self.annotationsList.selection():
            j = self.annotationsList.groups.currentIndex()
            indexes = []
            for item in self.annotationsList.list.selectedIndexes():
                indexes.append(item.row())

            for i in indexes:
                annotation = self.project.groups[j].annotations[i]
                annotation.imitate(self.project.modelAnnotation)
            self.canvas.draw()
        else:
            alert = QMessageBox(self)
            alert.setText("Select at least one annotation before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

#     def enregistrerProjet(self):
#         try:
#             if self.projet.chemin == "":
#                 chemin = QFileDialog.getSaveFileName(caption="Enregistrer le projet pyLong",
#                                                      filter="fichier pyLong (*.pyLong)")[0]
#                 if chemin == "":
#                     return 0
#                 else:
#                     nomProjet = QFileInfo(chemin).fileName()
#                     repertoireProjet = QFileInfo(chemin).absolutePath()
#                     nomProjet = nomProjet.split(".")[0]

#                     nomProjet += ".pyLong"
#                     chemin = repertoireProjet + "/" + nomProjet

#                     self.projet.chemin = chemin
#                     self.setWindowTitle(chemin)

#                     with open(chemin, 'wb') as fichier:
#                         myPickler = Pickler(fichier)
#                         myPickler.dump(self.projet)

#                     self.updateProjetsRecents(self.projet.chemin)

#             else:
#                 with open(self.projet.chemin, 'wb') as fichier:
#                     myPickler = Pickler(fichier)
#                     myPickler.dump(self.projet)

#                 self.updateProjetsRecents(self.projet.chemin)

#         except:
#             alerte = QMessageBox(self)
#             alerte.setText("L'enregistrement du projet a échoué.")
#             alerte.exec_()
#             pass

#     def enregistrerProjetSous(self):
#         try:
#             chemin = QFileDialog.getSaveFileName(caption="Enregistrer le projet pyLong sous...",
#                                                  filter="fichier pyLong (*.pyLong)")[0]
#             if chemin == "":
#                 return 0
#             else:
#                 nomProjet = QFileInfo(chemin).fileName()
#                 repertoireProjet = QFileInfo(chemin).absolutePath()
#                 nomProjet = nomProjet.split(".")[0]

#                 nomProjet += ".pyLong"
#                 chemin = repertoireProjet + "/" + nomProjet

#                 self.projet.chemin = chemin
#                 self.setWindowTitle(chemin)

#                 with open(chemin, 'wb') as fichier:
#                     myPickler = Pickler(fichier)
#                     myPickler.dump(self.projet)

#                 self.updateProjetsRecents(self.projet.chemin)

#         except:
#             alerte = QMessageBox(self)
#             alerte.setText("L'enregistrement du projet a échoué.")
#             alerte.exec_()
#             pass

#     def ouvrirProjet(self):
#         self.nouveauProjet()

#         try:
#             chemin = QFileDialog.getOpenFileName(caption="Ouvrir un projet pyLong",
#                                                  filter="fichier pyLong (*.pyLong)")[0]
#             if chemin == "":
#                 return 0
#             else:
#                 with open(chemin, 'rb') as fichier:
#                     myUnpickler = Unpickler(fichier)
#                     projet = myUnpickler.load()

#                 self.freeze = True
#                 self.projet.charger(projet)

#                 self.setWindowTitle(self.projet.chemin)

#                 self.listeLayouts.clear()
#                 for layout in self.projet.layouts:
#                     self.listeLayouts.addItem(layout.intitule)

#                 self.profilesList.update()
#                 self.annotationsList.updateGroupes()
#                 self.annotationsList.updateListe()
#                 self.calculationsList.update()
#                 self.otherDataList.update()

#                 self.freeze = False
#                 self.canvas.dessiner()

#                 self.updateProjetsRecents(chemin)

#         except:
#             alerte = QMessageBox(self)
#             alerte.setText("Le chargement du projet a échoué.")
#             alerte.exec_()
#             pass

#     def nouveauProjet(self):
#         dialogue = QMessageBox(self)
#         dialogue.setWindowTitle("Nouveau projet pyLong")
#         dialogue.setText("Voulez-vous enregistrer le projet actuel ?")
#         dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
#         dialogue.button(QMessageBox.Yes).setText("Oui")
#         dialogue.button(QMessageBox.No).setText("Non")
#         dialogue.button(QMessageBox.Cancel).setText("Annuler")
#         dialogue.setIcon(QMessageBox.Question)
#         reponse = dialogue.exec_()

#         if reponse == QMessageBox.Yes:
#             self.enregistrerProjet()

#             self.freeze = True
#             self.projet.nouveau()

#             self.listeLayouts.clear()
#             for layout in self.projet.layouts:
#                 self.listeLayouts.addItem(layout.intitule)

#             self.profilesList.update()
#             self.annotationsList.updateGroupes()
#             self.annotationsList.updateListe()
#             self.calculationsList.update()
#             self.otherDataList.update()

#             self.setWindowTitle("pyLong")

#             self.freeze = False
#             self.canvas.dessiner()

#         elif reponse == QMessageBox.No:
#             self.freeze = True
#             self.projet.nouveau()

#             self.listeLayouts.clear()
#             for layout in self.projet.layouts:
#                 self.listeLayouts.addItem(layout.intitule)

#             self.profilesList.update()
#             self.annotationsList.updateGroupes()
#             self.annotationsList.updateListe()
#             self.calculationsList.update()
#             self.otherDataList.update()

#             self.setWindowTitle("pyLong")

#             self.freeze = False
#             self.canvas.dessiner()
#         else:
#             return 0

#     def imprimer(self):
#         DialogImprimer(parent=self).exec_()

    def adjustVerticalAnnotation(self):
        if self.annotationsList.selection():
            DialogAdjustAnnotations(parent=self).exec()
        else:
            alert = QMessageBox(self)
            alert.setText("Select at least one vertical annotation before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def dataDelete(self):
        self.otherDataList.delete()

    def profileDelete(self):
        self.profilesList.delete()

    def calculationDelete(self):
        self.calculationsList.delete()

    def annotationDelete(self):
        self.annotationsList.delete()

    def toolBox(self):
        DialogToolBox(parent=self).exec_()

    # def tableauValeurs(self):
    #     if self.profilesList.selection():
    #         DialogTableauValeurs(parent=self).exec_()

        # else:
        #     alerte = QMessageBox(self)
        #     alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
        #     alerte.setIcon(QMessageBox.Warning)
        #     alerte.exec_()

#     def onDoubleClick(self, event):
#         pass

    def profileStyle(self):
        self.checkNavigationTools()
        if self.profilesList.selection():
            DialogProfileOptions(parent=self).exec_()
        else:
            alert = QMessageBox(self)
            alert.setText("Select a profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def addPoint(self, checked):
        self.checkNavigationTools()

        if checked:
            self.deletePointAction.setChecked(False)
            try:
                self.canvas.customContextMenuRequested.disconnect(self.canvas.contextMenu)
            except:
                pass

            self.navigationBar._actions['pan'].setEnabled(False)
            self.navigationBar._actions['zoom'].setEnabled(False)
            self.navigationBar._actions['back'].setEnabled(False)
            self.navigationBar._actions['forward'].setEnabled(False)

            try:
                self.project.preview.line.figure.canvas.mpl_disconnect(self.project.preview.cid)
            except:
                pass

            if not self.magnetismAction.isChecked():
                self.project.preview.cid = self.project.preview.line.figure.canvas.mpl_connect('button_press_event', self.project.preview.addOnClick)
            else:
                i = self.profilesComboBox.currentIndex()
                zprofile, sprofile = self.project.profiles[i]
                self.project.preview.profile = zprofile
                self.project.preview.cid = self.project.preview.line.figure.canvas.mpl_connect('button_press_event', self.project.preview.addOnClickOnProfile)

        else:
            try:
                self.canvas.customContextMenuRequested.connect(self.canvas.contextMenu)
            except:
                pass
            self.navigationBar._actions['pan'].setEnabled(True)
            self.navigationBar._actions['zoom'].setEnabled(True)
            self.navigationBar._actions['back'].setEnabled(True)
            self.navigationBar._actions['forward'].setEnabled(True)

            try:
                self.project.preview.line.figure.canvas.mpl_disconnect(self.project.preview.cid)
            except:
                pass

    def removePoint(self, checked):
        self.checkNavigationTools()

        if checked:
            self.addPointAction.setChecked(False)
            try:
                self.canvas.customContextMenuRequested.disconnect(self.canvas.contextMenu)
            except:
                pass

            self.navigationBar._actions['pan'].setEnabled(False)
            self.navigationBar._actions['zoom'].setEnabled(False)
            self.navigationBar._actions['back'].setEnabled(False)
            self.navigationBar._actions['forward'].setEnabled(False)

            try:
                self.project.preview.line.figure.canvas.mpl_disconnect(self.project.preview.cid)
            except:
                pass

            self.project.preview.cid = self.project.preview.line.figure.canvas.mpl_connect('pick_event', self.project.preview.deleteOnPick)

        else:
            try:
                self.canvas.customContextMenuRequested.connect(self.canvas.contextMenu)
            except:
                pass
            self.barreDeNavigation._actions['pan'].setEnabled(True)
            self.barreDeNavigation._actions['zoom'].setEnabled(True)
            self.barreDeNavigation._actions['back'].setEnabled(True)
            self.barreDeNavigation._actions['forward'].setEnabled(True)
            try:
                self.project.preview.line.figure.canvas.mpl_disconnect(self.project.prview.cid)
            except:
                pass

    def activateMagnetism(self):
        self.checkNavigationTools()

        self.addPointAction.setChecked(False)
        self.deletePointAction.setChecked(False)

        try:
            self.project.preview.line.figure.canvas.mpl_disconnect(self.project.preview.cid)
        except:
            pass

    def updateProfilesList(self, checked):
        self.profilesComboBox.clear()
        if checked:
            self.profilesComboBox.setEnabled(True)
            for zprofile, sprofile in self.project.profiles:
                self.profilesComboBox.addItem(zprofile.title)
        else:
            self.profilesComboBox.setEnabled(False)

    def edit(self, checked):
        if not self.profilesList.selection():
            self.editingAction.setChecked(False)

            alert = QMessageBox(self)
            alert.setText("Select a profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()
            return 0

        else:
            if checked:
                i = self.profilesList.list.currentRow()
                zprofile, sprofile = self.project.profiles[i]

                self.interactiveEdition = True

                self.profilesList.setEnabled(False)
                self.annotationsList.setEnabled(False)
                self.calculationsList.setEnabled(False)
                self.otherDataList.setEnabled(False)

                self.projectToolBar.setEnabled(False)
                self.figureToolBar.setEnabled(False)
                self.subplotToolBar.setEnabled(False)
                self.profileToolBar.setEnabled(False)
                self.annotationToolBar.setEnabled(False)
                self.reminderLineToolBar.setEnabled(False)
                self.toolboxToolBar.setEnabled(False)
                self.otherDataToolBar.setEnabled(False)
                self.resourceToolBar.setEnabled(False)
                self.onfToolBar.setEnabled(False)

                self.projectMenu.setEnabled(False)
                self.figureMenu.setEnabled(False)
                self.subplotMenu.setEnabled(False)
                self.profileMenu.setEnabled(False)
                self.annotationMenu.setEnabled(False)
                self.reminderLineMenu.setEnabled(False)
                self.toolboxMenu.setEnabled(False)
                self.otherDataMenu.setEnabled(False)
                self.resourceMenu.setEnabled(False)

                self.addPointAction.setEnabled(True)
                self.addPointAction.setVisible(True)
                self.addPointAction.setChecked(False)
                self.deletePointAction.setEnabled(True)
                self.deletePointAction.setVisible(True)
                self.deletePointAction.setChecked(False)
                self.magnetismAction.setVisible(True)
                self.magnetismAction.setChecked(False)
                self.profilesListAction.setVisible(True)
                self.profilesListAction.setEnabled(False)

                self.project.preview.x = zprofile.x
                self.project.preview.z = zprofile.z
                self.project.preview.visible = True
                self.project.preview.update()

                self.canvas.draw()

            else:
                dialog = QMessageBox(self)
                dialog.setWindowTitle("Sortie du mode édition interactive")
                dialog.setText("Enregistrer les modifications ?")
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.button(QMessageBox.Yes).setText("Oui")
                dialog.button(QMessageBox.No).setText("Non")
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
                    xs = self.project.preview.line.get_xdata()
                    ys = self.project.preview.line.get_ydata()

                    i = self.profilesList.list.currentRow()
                    zprofile, sprofile = self.project.profiles[i]

                    zprofile.x = np.array(xs)
                    zprofile.z = np.array(ys)

                    zprofile.update()

                    sprofile.updateData(zprofile.x, zprofile.z)
                    sprofile.update()

                    if sprofile.annotationsVisible:
                        self.canvas.updateCanvas()

                self.interactiveEdition = False

                self.profilesList.setEnabled(True)
                self.annotationsList.setEnabled(True)
                self.calculationsList.setEnabled(True)
                self.otherDataList.setEnabled(True)

                self.projectToolBar.setEnabled(True)
                self.figureToolBar.setEnabled(True)
                self.subplotToolBar.setEnabled(True)
                self.profileToolBar.setEnabled(True)
                self.annotationToolBar.setEnabled(True)
                self.reminderLineToolBar.setEnabled(True)
                self.toolboxToolBar.setEnabled(True)
                self.otherDataToolBar.setEnabled(True)
                self.resourceToolBar.setEnabled(True)
                self.onfToolBar.setEnabled(True)

                self.projectMenu.setEnabled(True)
                self.figureMenu.setEnabled(True)
                self.subplotMenu.setEnabled(True)
                self.profileMenu.setEnabled(True)
                self.annotationMenu.setEnabled(True)
                self.reminderLineMenu.setEnabled(True)
                self.toolboxMenu.setEnabled(True)
                self.otherDataMenu.setEnabled(True)
                self.resourceMenu.setEnabled(True)

                self.navigationBar._actions['pan'].setEnabled(True)
                self.navigationBar._actions['zoom'].setEnabled(True)
                self.navigationBar._actions['back'].setEnabled(True)
                self.navigationBar._actions['forward'].setEnabled(True)

                self.addPointAction.setEnabled(False)
                self.addPointAction.setVisible(False)
                self.addPointAction.setChecked(False)
                self.deletePointAction.setEnabled(False)
                self.deletePointAction.setVisible(False)
                self.deletePointAction.setChecked(False)
                self.magnetismAction.setVisible(False)
                self.magnetismAction.setChecked(False)
                self.profilesListAction.setVisible(False)
                self.profilesListAction.setEnabled(False)

                self.project.preview.visible = False
                self.project.preview.update()
                self.canvas.draw()

            try:
                self.canvas.customContextMenuRequested.connect(self.canvas.contextMenu)
            except:
                pass

    def export(self):
        if self.profilesList.selection():
            DialogExport(parent=self).exec_()
        else:
            alert = QMessageBox(self)
            alert.setText("Select a profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def simplify(self):
        if self.profilesList.selection():
            DialogSimplify(parent=self).exec_()

            self.project.preview.visible = False
            self.project.preview.update()
            self.canvas.draw()
        else:
            alert = QMessageBox(self)
            alert.setText("Select a profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def filter(self):
        if self.profilesList.selection():
            DialogFilter(parent=self).exec_()

            self.project.preview.visible = False
            self.project.preview.update()
            self.canvas.draw()

        else:
            alert = QMessageBox(self)
            alert.setText("Select a profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def sort(self):
        if self.profilesList.selection():
            DialogSort(parent=self).exec_()

            self.project.preview.visible = False
            self.project.preview.update()
            self.canvas.draw()
        else:
            alert = QMessageBox(self)
            alert.setText("Select a profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def addProfile(self):
        DialogAddProfile(parent=self).exec_()

    def addText(self):
        annotation = Text()
        i = self.annotationsList.groups.currentIndex()
        annotation.group = i
        annotation.update()
        self.project.groups[i].annotations.append(annotation)
        self.annotationsList.updateList()
        self.canvas.ax_z.add_artist(annotation.text)
        self.canvas.draw()

    def addVerticalAnnotation(self):
        annotation = VerticalAnnotation()
        i = self.annotationsList.groups.currentIndex()
        annotation.group = i
        annotation.update()
        self.project.groups[i].annotations.append(annotation)
        self.annotationsList.updateList()
        self.canvas.ax_z.add_artist(annotation.annotation)
        self.canvas.draw()

    def addLinearAnnotation(self):
        annotation = LinearAnnotation()
        i = self.annotationsList.groups.currentIndex()
        annotation.group = i
        annotation.update()
        self.project.groups[i].annotations.append(annotation)
        self.annotationsList.updateList()
        self.canvas.ax_z.add_artist(annotation.annotation)
        self.canvas.ax_z.add_artist(annotation.text)
        self.canvas.draw()

    def addInterval(self):
        annotation = Interval()
        i = self.annotationsList.groups.currentIndex()
        annotation.group = i
        annotation.update()
        self.project.groups[i].annotations.append(annotation)
        self.annotationsList.updateList()
        self.canvas.ax_z.add_artist(annotation.text)
        self.canvas.ax_z.add_line(annotation.startLine)
        self.canvas.ax_z.add_line(annotation.endLine)
        self.canvas.draw()

    def addRectangle(self):
        annotation = Rectangle()
        i = self.annotationsList.groups.currentIndex()
        annotation.group = i
        annotation.update()
        self.project.groups[i].annotations.append(annotation)
        self.annotationsList.updateList()
        self.canvas.ax_z.add_patch(annotation.rectangle)
        self.canvas.updateLegends()

    def deleteGroups(self):
        self.annotationsList.deleteGroups()

    def renameGroup(self):
        self.annotationsList.renameGroup()

    def addGroup(self):
        self.annotationsList.addGroup()

    def deleteLayouts(self):
        DialogDeleteLayouts(parent=self).exec_()

    def renameLayout(self):
        i = self.layoutsList.currentIndex()
        if i != 0:
            DialogRenameLayout(parent=self).exec_()

    def addLayout(self):
        DialogAddLayout(parent=self).exec_()

    def settings(self):
        DialogSettings(parent=self).exec_()

    def layout(self):
        DialogLayout(self).exec_()

    def refresh(self):
        self.checkNavigationTools()
        self.canvas.updateFigure()

    def contextMenuLayouts(self, point):
        self.popMenuLayouts.exec_(self.layoutsList.mapToGlobal(point))

    def copyFigure(self):
        self.checkNavigationTools()
        clipBoard = QApplication.clipboard()
        figure = QImage(self.canvas.grab())
        clipBoard.setImage(figure)

    def checkNavigationTools(self):
        if self.navigationBar._actions['pan'].isChecked():
            self.navigationBar.pan()
        elif self.navigationBar._actions['zoom'].isChecked():
            self.navigationBar.zoom()
        else:
            pass

    def documentation(self):
        cmd = r"start https://pyLong-doc.readthedocs.io/fr/latest/#"
        os.system(cmd)

    def about(self):
        text = "<center>" \
               "<h1>pyLong</h1>" \
               "<p>Version dev" \
               "<hr />" \
               "&#8291;" \
               "<img src="+self.appctxt.get_resource('images/logo_onf.png')+">" \
               "<br/>" \
               "<img src="+self.appctxt.get_resource('images/logo_rtm.png') + ">" \
               "<hr /><br/>" \
               "Conception : Damien KUSS<br/>" \
               "damien.kuss@onf.fr<br/><br/>" \
               "Support : Clément ROUSSEL<br/>" \
               "clement.roussel@onf.fr<\p>"
               
        dialogue = QMessageBox(self)
        dialogue.setText(text)
        dialogue.exec_()

    def onf(self):
        cmd = r"start https://www.onf.fr/onf"
        os.system(cmd)