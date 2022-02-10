from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette

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

# from DialogPreferences import *

# from DialogAjoutLayout import *
# from DialogRenommerLayout import *
# from DialogSupprimerLayouts import *

# from DialogLayout import *
# from DialogLayoutAvancee import *
# from DialogImprimer import *

# from DialogGestionSubplots import *

# from DialogAjoutProfil import *
# from DialogOptionsProfils import *
# from DialogTableauValeurs import *
# from DialogTrier import *
# from DialogFiltrer import *
# from DialogSimplifier import *
# from DialogExporter import *

# from DialogAjusterAnnotations import *
# from DialogGestionGroupes import *

# from DialogLignesRappel import *

# from DialogToolBox import *

# from DialogAjoutDonnees import *
# from DialogOptionsDonnees import *

# matplotlib modules
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# python modules
import os
# import pickle
# from pickle import Pickler, Unpickler
import json

# pyLong modules
from pyLong.project import Project

# from pyLong.Texte import *
# from pyLong.AnnotationPonctuelle import *
# from pyLong.AnnotationLineaire import *
# from pyLong.Zone import *
# from pyLong.Rectangle import *


class NavigationBar(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Pan', 'Zoom')]


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

#         self.canvas.initialiser()
#         self.canvas.dessiner()

        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)
        self.showMaximized()

        self.canvas.initialize()
        self.canvas.updateLayout()

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

#             self.listeProfils.update()
#             self.listeAnnotations.updateGroupes()
#             self.listeAnnotations.updateListe()
#             self.listeCalculs.update()
#             self.listeAutresDonnees.update()

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

#     def ouvrirStyleCalcul(self):
#         self.listeCalculs.ouvrirCalcul()

#     def ouvrirStyleAnnotation(self):
#         self.listeAnnotations.ouvrirAnnotation()

#     def annotations2ligneRappel(self):
#         self.listeAnnotations.creerLigneRappel()

#     def lignesRappel(self):
#         DialogLignesRappel(parent=self).exec_()

    def adjustWidth(self):
        self.canvas.adjustWidth()

    def adjustHeight(self):
        self.canvas.adjustHeight()

    def zoomIn(self):
        self.canvas.zoomIn()

    def zoomOut(self):
        self.canvas.zoomOut()

#     def optionsDonnees(self):
#         if self.listeAutresDonnees.selection():
#             DialogOptionsDonnees(parent=self).exec_()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez une donnée avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def ajouterDonnees(self):
#         DialogAjoutDonnees(parent=self).exec_()

#     def miseEnPage_avancee(self):
#         DialogLayoutAvancee(parent=self).exec_()

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

#     def gestionSubplots(self):
#         DialogGestionSubplots(parent=self).exec_()

#     def gestionGroupes(self):
#         i = self.listeAnnotations.groupes.currentIndex()
#         DialogGestionGroupes(parent=self).exec_()
#         self.listeAnnotations.updateGroupes()
#         self.listeAnnotations.groupes.setCurrentIndex(i)
#         self.listeAnnotations.updateListe()
#         self.canvas.dessiner()

#     def dupliquerAnnotations(self):
#         if self.listeAnnotations.selection():
#             j = self.listeAnnotations.groupes.currentIndex()
#             indices = []
#             for item in self.listeAnnotations.liste.selectedIndexes():
#                 indices.append(item.row())

#             for i in indices:
#                 annotation = self.projet.groupes[j].annotations[i]
#                 if type(annotation) == Texte:
#                     txt = annotation.dupliquer()
#                     self.projet.groupes[j].annotations.append(txt)
#                     self.canvas.ax_z.add_artist(txt.text)
#                 elif type(annotation) == AnnotationPonctuelle:
#                     ap = annotation.dupliquer()
#                     self.projet.groupes[j].annotations.append(ap)
#                     self.canvas.ax_z.add_artist(ap.annotation)
#                 elif type(annotation) == AnnotationLineaire:
#                     al = annotation.dupliquer()
#                     self.projet.groupes[j].annotations.append(al)
#                     self.canvas.ax_z.add_artist(al.annotation)
#                     self.canvas.ax_z.add_artist(al.text)
#                 elif type(annotation) == Zone:
#                     zone = annotation.dupliquer()
#                     self.projet.groupes[j].annotations.append(zone)
#                     self.canvas.ax_z.add_artist(zone.text)
#                     self.canvas.ax_z.add_line(zone.left_line)
#                     self.canvas.ax_z.add_line(zone.right_line)
#                 else:
#                     rect = annotation.dupliquer()
#                     self.projet.groupes[j].annotations.append(rect)
#                     self.canvas.ax_z.add_patch(rect.rectangle)

#             self.listeAnnotations.updateListe()
#             self.canvas.updateLegendes()

#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez une annotation avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def copierPropriete(self):
#         if self.listeAnnotations.selection():
#             i = self.listeAnnotations.groupes.currentIndex()
#             j = self.listeAnnotations.liste.currentRow()
#             self.projet.annotationModele = self.projet.groupes[i].annotations[j]
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez une annotation avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def collerPropriete(self):
#         if self.listeAnnotations.selection():
#             j = self.listeAnnotations.groupes.currentIndex()
#             indices = []
#             for item in self.listeAnnotations.liste.selectedIndexes():
#                 indices.append(item.row())

#             for i in indices:
#                 annotation = self.projet.groupes[j].annotations[i]
#                 annotation.imiter(self.projet.annotationModele)
#             self.canvas.draw()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez une ou plusieurs annotation(s) avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

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

#                 self.listeProfils.update()
#                 self.listeAnnotations.updateGroupes()
#                 self.listeAnnotations.updateListe()
#                 self.listeCalculs.update()
#                 self.listeAutresDonnees.update()

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

#             self.listeProfils.update()
#             self.listeAnnotations.updateGroupes()
#             self.listeAnnotations.updateListe()
#             self.listeCalculs.update()
#             self.listeAutresDonnees.update()

#             self.setWindowTitle("pyLong")

#             self.freeze = False
#             self.canvas.dessiner()

#         elif reponse == QMessageBox.No:
#             self.freeze = True
#             self.projet.nouveau()

#             self.listeLayouts.clear()
#             for layout in self.projet.layouts:
#                 self.listeLayouts.addItem(layout.intitule)

#             self.listeProfils.update()
#             self.listeAnnotations.updateGroupes()
#             self.listeAnnotations.updateListe()
#             self.listeCalculs.update()
#             self.listeAutresDonnees.update()

#             self.setWindowTitle("pyLong")

#             self.freeze = False
#             self.canvas.dessiner()
#         else:
#             return 0

#     def imprimer(self):
#         DialogImprimer(parent=self).exec_()

#     def ajusterAnnotations(self):
#         if self.listeAnnotations.selection():
#             DialogAjusterAnnotations(parent=self).exec()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez une ou plusieurs annotation(s) avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def supprimerDonnees(self):
#         self.listeAutresDonnees.supprimer()

#     def supprimerProfils(self):
#         self.listeProfils.supprimer()

#     def supprimerCalculs(self):
#         self.listeCalculs.supprimer()

#     def supprimerAnnotation(self):
#         self.listeAnnotations.supprimer()

#     def toolBox(self):
#         DialogToolBox(parent=self).exec_()

#     def tableauValeurs(self):
#         if self.listeProfils.selection():
#             DialogTableauValeurs(parent=self).exec_()

#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def onDoubleClick(self, event):
#         pass

#     def optionsProfil(self):
#         if self.listeProfils.selection():
#             DialogOptionsProfils(parent=self).exec_()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def addPoint(self, checked):
#         self.controleOutilsNavigation()

#         if checked:
#             self.supprimerPoint.setChecked(False)
#             try:
#                 self.canvas.customContextMenuRequested.disconnect(self.canvas.contextMenu)
#             except:
#                 pass

#             self.barreDeNavigation._actions['pan'].setEnabled(False)
#             self.barreDeNavigation._actions['zoom'].setEnabled(False)

#             try:
#                 self.projet.apercu.line.figure.canvas.mpl_disconnect(self.projet.apercu.cid)
#             except:
#                 pass

#             # self.canvas.setCursor(Qt.CrossCursor)

#             if not self.magnetisme.isChecked():
#                 self.projet.apercu.cid = self.projet.apercu.line.figure.canvas.mpl_connect('button_press_event', self.projet.apercu.addOnClick)
#             else:
#                 i = self.listingProfils.currentIndex()
#                 zprofil, pprofil = self.projet.profils[i]
#                 self.projet.apercu.profil = zprofil
#                 self.projet.apercu.cid = self.projet.apercu.line.figure.canvas.mpl_connect('button_press_event', self.projet.apercu.addOnClickOnProfile)

#         else:
#             try:
#                 self.canvas.customContextMenuRequested.connect(self.canvas.contextMenu)
#             except:
#                 pass
#             self.barreDeNavigation._actions['pan'].setEnabled(True)
#             self.barreDeNavigation._actions['zoom'].setEnabled(True)

#             try:
#                 self.projet.apercu.line.figure.canvas.mpl_disconnect(self.projet.apercu.cid)
#             except:
#                 pass

#             # self.canvas.setCursor(Qt.ArrowCursor)

#     def removePoint(self, checked):
#         self.controleOutilsNavigation()

#         if checked:
#             self.ajouterPoint.setChecked(False)
#             try:
#                 self.canvas.customContextMenuRequested.disconnect(self.canvas.contextMenu)
#             except:
#                 pass

#             self.barreDeNavigation._actions['pan'].setEnabled(False)
#             self.barreDeNavigation._actions['zoom'].setEnabled(False)

#             try:
#                 self.projet.apercu.line.figure.canvas.mpl_disconnect(self.projet.apercu.cid)
#             except:
#                 pass

#             # self.canvas.setCursor(Qt.CrossCursor)

#             self.projet.apercu.cid = self.projet.apercu.line.figure.canvas.mpl_connect('pick_event', self.projet.apercu.deleteOnPick)

#         else:
#             try:
#                 self.canvas.customContextMenuRequested.connect(self.canvas.contextMenu)
#             except:
#                 pass
#             self.barreDeNavigation._actions['pan'].setEnabled(True)
#             self.barreDeNavigation._actions['zoom'].setEnabled(True)
#             try:
#                 self.projet.apercu.line.figure.canvas.mpl_disconnect(self.projet.apercu.cid)
#             except:
#                 pass

#             # self.canvas.setCursor(Qt.ArrowCursor)

#     def activerMagnetisme(self):
#         self.controleOutilsNavigation()

#         self.ajouterPoint.setChecked(False)
#         self.supprimerPoint.setChecked(False)

#         try:
#             self.projet.apercu.line.figure.canvas.mpl_disconnect(self.projet.apercu.cid)
#         except:
#             pass

#         # self.canvas.setCursor(Qt.ArrowCursor)

#     def updateListingProfils(self, checked):
#         self.listingProfils.clear()
#         if checked:
#             self.actionListingProfils.setEnabled(True)
#             for zprofil, pprofil in self.projet.profils:
#                 self.listingProfils.addItem(zprofil.intitule)
#         else:
#             self.actionListingProfils.setEnabled(False)

#     def editionProfil(self, checked):
#         if not self.listeProfils.selection():
#             self.action_editerProfils.setChecked(False)

#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()
#             return 0

#         else:
#             if checked:
#                 i = self.listeProfils.liste.currentRow()
#                 zprofil, pprofil = self.projet.profils[i]

#                 self.editionActive = True

#                 self.listeProfils.setEnabled(False)
#                 self.listeAnnotations.setEnabled(False)
#                 self.listeCalculs.setEnabled(False)
#                 self.listeAutresDonnees.setEnabled(False)

#                 self.action_miseEnPage.setEnabled(False)
#                 self.action_miseEnPage_avancee.setEnabled(False)
#                 self.rafraichirFigure.setEnabled(False)
#                 self.action_exporterFigure.setEnabled(False)
#                 self.action_copierFigure.setEnabled(False)
#                 self.action_gestionSubplots.setEnabled(False)

#                 self.outilsProjet.setEnabled(False)
#                 self.outilsFigure.setEnabled(False)
#                 self.outilsSubplots.setEnabled(False)
#                 self.outilsProfils.setEnabled(False)
#                 self.outilsAnnotations.setEnabled(False)
#                 self.outilsRappels.setEnabled(False)
#                 self.outilsToolBox.setEnabled(False)
#                 self.outilsAutresDonnees.setEnabled(False)
#                 self.outilsRessources.setEnabled(False)
#                 self.outilsONF.setEnabled(False)

#                 self.menuProjet.setEnabled(False)
#                 self.menuFigure.setEnabled(False)
#                 self.menuSubplot.setEnabled(False)
#                 self.menuProfil.setEnabled(False)
#                 self.menuAnnotation.setEnabled(False)
#                 self.menuRappel.setEnabled(False)
#                 self.menuToolBox.setEnabled(False)
#                 self.menuAutresDonnees.setEnabled(False)
#                 self.menuRessources.setEnabled(False)

#                 self.ajouterPoint.setEnabled(True)
#                 self.ajouterPoint.setVisible(True)
#                 self.ajouterPoint.setChecked(False)
#                 self.supprimerPoint.setEnabled(True)
#                 self.supprimerPoint.setVisible(True)
#                 self.supprimerPoint.setChecked(False)
#                 self.magnetisme.setVisible(True)
#                 self.magnetisme.setChecked(False)
#                 self.actionListingProfils.setVisible(True)
#                 self.actionListingProfils.setEnabled(False)

#                 self.projet.apercu.abscisses = zprofil.abscisses
#                 self.projet.apercu.altitudes = zprofil.altitudes
#                 self.projet.apercu.visible = True
#                 self.projet.apercu.update()

#                 self.canvas.draw()

#             else:
#                 dialogue = QMessageBox(self)
#                 dialogue.setWindowTitle("Sortie du mode édition interactive")
#                 dialogue.setText("Enregistrer les modifications ?")
#                 dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#                 dialogue.button(QMessageBox.Yes).setText("Oui")
#                 dialogue.button(QMessageBox.No).setText("Non")
#                 dialogue.setIcon(QMessageBox.Question)
#                 reponse = dialogue.exec_()

#                 if reponse == QMessageBox.Yes:
#                     xs = self.projet.apercu.line.get_xdata()
#                     ys = self.projet.apercu.line.get_ydata()

#                     i = self.listeProfils.liste.currentRow()
#                     zprofil, pprofil = self.projet.profils[i]

#                     zprofil.abscisses = np.array(xs)
#                     zprofil.altitudes = np.array(ys)

#                     zprofil.update()

#                     pprofil.updateData(zprofil.abscisses, zprofil.altitudes)
#                     pprofil.update()

#                     if pprofil.pentesVisibles:
#                         self.canvas.dessiner()

#                 self.editionActive = False

#                 self.listeProfils.setEnabled(True)
#                 self.listeAnnotations.setEnabled(True)
#                 self.listeCalculs.setEnabled(True)
#                 self.listeAutresDonnees.setEnabled(True)

#                 self.action_miseEnPage.setEnabled(True)
#                 self.action_miseEnPage_avancee.setEnabled(True)
#                 self.rafraichirFigure.setEnabled(True)
#                 self.action_exporterFigure.setEnabled(True)
#                 self.action_copierFigure.setEnabled(True)
#                 self.action_gestionSubplots.setEnabled(True)

#                 self.outilsProjet.setEnabled(True)
#                 self.outilsFigure.setEnabled(True)
#                 self.outilsSubplots.setEnabled(True)
#                 self.outilsProfils.setEnabled(True)
#                 self.outilsAnnotations.setEnabled(True)
#                 self.outilsRappels.setEnabled(True)
#                 self.outilsToolBox.setEnabled(True)
#                 self.outilsAutresDonnees.setEnabled(True)
#                 self.outilsRessources.setEnabled(True)
#                 self.outilsONF.setEnabled(True)

#                 self.menuProjet.setEnabled(True)
#                 self.menuFigure.setEnabled(True)
#                 self.menuSubplot.setEnabled(True)
#                 self.menuProfil.setEnabled(True)
#                 self.menuAnnotation.setEnabled(True)
#                 self.menuRappel.setEnabled(True)
#                 self.menuToolBox.setEnabled(True)
#                 self.menuAutresDonnees.setEnabled(True)
#                 self.menuRessources.setEnabled(True)

#                 self.barreDeNavigation._actions['pan'].setEnabled(True)
#                 self.barreDeNavigation._actions['zoom'].setEnabled(True)

#                 self.ajouterPoint.setEnabled(False)
#                 self.ajouterPoint.setVisible(False)
#                 self.supprimerPoint.setEnabled(False)
#                 self.supprimerPoint.setVisible(False)
#                 self.magnetisme.setVisible(False)
#                 self.actionListingProfils.setVisible(False)

#                 self.projet.apercu.visible = False
#                 self.projet.apercu.update()
#                 self.canvas.draw()

#             try:
#                 self.canvas.customContextMenuRequested.connect(self.canvas.contextMenu)
#             except:
#                 pass

#     def exporterProfil(self):
#         if self.listeProfils.selection():
#             DialogExporter(parent=self).exec_()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def simplifierProfil(self):
#         if self.listeProfils.selection():
#             DialogSimplifier(parent=self).exec_()

#             self.projet.apercu.visible = False
#             self.projet.apercu.update()
#             self.canvas.updateLegendes()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def filtrerProfil(self):
#         if self.listeProfils.selection():
#             DialogFiltrer(parent=self).exec_()

#             self.projet.apercu.visible = False
#             self.projet.apercu.update()
#             self.canvas.updateLegendes()

#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def trierProfil(self):
#         if self.listeProfils.selection():
#             DialogTrier(parent=self).exec_()

#             self.projet.apercu.visible = False
#             self.projet.apercu.update()
#             self.canvas.draw()
#         else:
#             alerte = QMessageBox(self)
#             alerte.setText("Sélectionnez un profil avant de lancer cette commande.")
#             alerte.setIcon(QMessageBox.Warning)
#             alerte.exec_()

#     def ajouterProfil(self):
#         DialogAjoutProfil(parent=self).exec_()

#     def ajouterTexte(self):
#         txt = Texte()
#         i = self.listeAnnotations.groupes.currentIndex()
#         txt.groupe = i
#         txt.update()
#         self.projet.groupes[i].annotations.append(txt)
#         self.listeAnnotations.updateListe()
#         self.canvas.ax_z.add_artist(txt.text)
#         self.canvas.draw()

#     def ajouterAnnotationPonctuelle(self):
#         ap = AnnotationPonctuelle()
#         i = self.listeAnnotations.groupes.currentIndex()
#         ap.groupe = i
#         ap.update()
#         self.projet.groupes[i].annotations.append(ap)
#         self.listeAnnotations.updateListe()
#         self.canvas.ax_z.add_artist(ap.annotation)
#         self.canvas.draw()

#     def ajouterAnnotationLineaire(self):
#         al = AnnotationLineaire()
#         i = self.listeAnnotations.groupes.currentIndex()
#         al.groupe = i
#         al.update()
#         self.projet.groupes[i].annotations.append(al)
#         self.listeAnnotations.updateListe()
#         self.canvas.ax_z.add_artist(al.annotation)
#         self.canvas.ax_z.add_artist(al.text)
#         self.canvas.draw()

#     def ajouterZone(self):
#         zone = Zone()
#         i = self.listeAnnotations.groupes.currentIndex()
#         zone.groupe = i
#         zone.update()
#         self.projet.groupes[i].annotations.append(zone)
#         self.listeAnnotations.updateListe()
#         self.canvas.ax_z.add_artist(zone.text)
#         self.canvas.ax_z.add_line(zone.left_line)
#         self.canvas.ax_z.add_line(zone.right_line)
#         self.canvas.draw()

#     def ajouterRectangle(self):
#         rect = Rectangle()
#         i = self.listeAnnotations.groupes.currentIndex()
#         rect.groupe = i
#         rect.update()
#         self.projet.groupes[i].annotations.append(rect)
#         self.listeAnnotations.updateListe()
#         self.canvas.ax_z.add_patch(rect.rectangle)
#         self.canvas.updateLegendes()

#     def supprimerGroupes(self):
#         self.listeAnnotations.supprimerGroupe()

#     def renommerGroupe(self):
#         self.listeAnnotations.renommerGroupe()

#     def ajouterGroupe(self):
#         self.listeAnnotations.ajouterGroupe()

#     def supprimerLayouts(self):
#         DialogSupprimerLayouts(parent=self).exec_()

#     def renommerLayout(self):
#         i = self.listeLayouts.currentIndex()
#         if i != 0:
#             DialogRenommerLayout(parent=self).exec_()

#     def ajouterLayout(self):
#         DialogAjoutLayout(parent=self).exec_()

#     def gestionPreferences(self):
#         DialogPreferences(parent=self).exec_()

    def layout(self):
        DialogLayout(self).exec_()

#     def rafraichir(self):
#         self.controleOutilsNavigation()
#         self.canvas.dessiner()

#     def contextMenuLayouts(self, point):
#         self.popMenuLayouts.exec_(self.listeLayouts.mapToGlobal(point))

#     def copierFigure(self):
#         self.controleOutilsNavigation()
#         clipBoard = QApplication.clipboard()
#         figure = QImage(self.canvas.grab())
#         clipBoard.setImage(figure)





#     def controleOutilsNavigation(self):
#         if self.barreDeNavigation._actions['pan'].isChecked():
#             self.barreDeNavigation.pan()
#         elif self.barreDeNavigation._actions['zoom'].isChecked():
#             self.barreDeNavigation.zoom()
#         else:
#             pass

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
        dialogue = QMessageBox()
        # dialogue.setWindowIcon(QIcon(self.appctxt.get_resource('icones/propos.png')))
        dialogue.about(self, "About pyLong", text)

    def onf(self):
        cmd = r"start https://www.onf.fr/onf"
        os.system(cmd)