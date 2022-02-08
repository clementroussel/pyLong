from PyQt5.QtWidgets import QAction, QComboBox
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import QSize

def createActions(self):
    self.projectToolBar = self.addToolBar("Project")
    self.projectToolBar.setMovable(False)
    self.projectToolBar.setIconSize(QSize(20, 20))

    self.newProjectAction = QAction(QIcon(self.appctxt.get_resource('icons/newProject.png')), "New project", self)
    self.newProjectAction.setShortcut(QKeySequence("Ctrl+N"))
    #self.newProjectAction.triggered.connect(self.newProject)
    self.projectToolBar.addAction(self.newProjectAction)

    self.openProjectAction = QAction(QIcon(self.appctxt.get_resource('icons/openProject.png')), "Open a project", self)
    self.openProjectAction.setShortcut(QKeySequence("Ctrl+O"))
    #self.openProjectAction.triggered.connect(self.openProject)
    self.projectToolBar.addAction(self.openProjectAction)

    self.saveProjectAction = QAction(QIcon(self.appctxt.get_resource('icons/saveProject.png')), "Save project", self)
    self.saveProjectAction.setShortcut(QKeySequence("Ctrl+S"))
    #self.saveProjectAction.triggered.connect(self.saveProject)
    self.projectToolBar.addAction(self.saveProjectAction)

    self.saveProjectAsAction = QAction(QIcon(self.appctxt.get_resource('icons/saveProjectAs.png')), "Save project as... ", self)
    self.saveProjectAsAction.setShortcut(QKeySequence("Shift+Ctrl+S"))
    #self.saveProjectAsAction.triggered.connect(self.saveProjectAs)
    self.projectToolBar.addAction(self.saveProjectAsAction)

    self.settingsAction = QAction(QIcon(self.appctxt.get_resource('icons/settings.png')), "Settings", self)
    #self.settingsAction.triggered.connect(self.settings)
    self.projectToolBar.addAction(self.settingsAction)

    self.projectToolBar.addSeparator() 

    self.interfaceToolBar = self.addToolBar("Interface")
    self.interfaceToolBar.setMovable(False)
    self.interfaceToolBar.setIconSize(QSize(20, 20))

    self.fullScreenAction = QAction(QIcon(self.appctxt.get_resource('icons/fullScreen.png')), "Full screen", self)
    self.fullScreenAction.setCheckable(True)
    self.fullScreenAction.setShortcut(QKeySequence("F11"))
    #self.fullScreenAction.triggered.connect(self.pleinEcran)
    self.interfaceToolBar.addAction(self.fullScreenAction)

    self.zoomInAction = QAction(QIcon(self.appctxt.get_resource('icons/zoomIn.png')), "Zoom in", self)
    self.zoomInAction.setShortcut(QKeySequence("Ctrl++"))
    #self.zoomInAction.triggered.connect(self.zoomIn)
    self.interfaceToolBar.addAction(self.zoomInAction)

    self.zoomOutAction = QAction(QIcon(self.appctxt.get_resource('icons/zoomOut.png')), "Zoom out", self)
    self.zoomOutAction.setShortcut(QKeySequence("Ctrl+-"))
    #self.zoomOutAction.triggered.connect(self.zoomOut)
    self.interfaceToolBar.addAction(self.zoomOutAction)

    self.adjustWidthAction = QAction(QIcon(self.appctxt.get_resource('icons/adjustWidth.png')), "Adjust width", self)
    #self.adjustWidthAction.triggered.connect(self.adjustWidth)
    self.interfaceToolBar.addAction(self.adjustWidthAction)

    self.adjustHeightAction = QAction(QIcon(self.appctxt.get_resource('icons/adjustHeight.png')), "Adjust height", self)
    #self.adjustHeightAction.triggered.connect(self.adjustHieght)
    self.interfaceToolBar.addAction(self.adjustHeightAction)

    self.interfaceToolBar.addSeparator()

    self.figureToolBar = self.addToolBar("Figure")
    self.figureToolBar.setMovable(False)
    self.figureToolBar.setIconSize(QSize(20, 20))

    ##################################################
    # liste des mises en pages + son menu contextuel #
    ##################################################
    # self.listeLayouts = QComboBox()
    # self.listeLayouts.setMinimumWidth(100)
    # for layout in self.projet.layouts:
    #     self.listeLayouts.addItem(layout.intitule)

    # self.listeLayouts.currentIndexChanged.connect(self.canvas.dessiner)

    # self.listeLayouts.setContextMenuPolicy(Qt.CustomContextMenu)
    # self.listeLayouts.customContextMenuRequested.connect(self.contextMenuLayouts)

    # self.popMenuLayouts = QMenu(self)
    # ajouterLayout = QAction('Ajouter une mise en page', self)
    # renommerLayout = QAction('Renommer la mise en page', self)
    # supprimerLayout = QAction('Supprimer des mises en page', self)
    # ajouterLayout.triggered.connect(self.ajouterLayout)
    # renommerLayout.triggered.connect(self.renommerLayout)
    # supprimerLayout.triggered.connect(self.supprimerLayouts)
    # self.popMenuLayouts.addAction(ajouterLayout)
    # self.popMenuLayouts.addSeparator()
    # self.popMenuLayouts.addAction(renommerLayout)
    # self.popMenuLayouts.addSeparator()
    # self.popMenuLayouts.addAction(supprimerLayout)

    # self.outilsFigure.addWidget(self.listeLayouts)
    ##################################################

    self.layoutAction = QAction(QIcon(self.appctxt.get_resource('icons/layout.png')), "Layout properties", self)
    #self.layoutAction.triggered.connect(self.layout)
    self.figureToolBar.addAction(self.layoutAction)

    self.advancedLayoutAction = QAction(QIcon(self.appctxt.get_resource('icons/advancedLayout.png')), "Advanced layout properties", self)
    #self.advancedLayoutAction.triggered.connect(self.advancedLayout)
    self.figureToolBar.addAction(self.advancedLayoutAction)

    self.refreshAction = QAction(QIcon(self.appctxt.get_resource('icons/refresh.png')), "Refresh", self)
    self.refreshAction.setShortcut(QKeySequence("Ctrl+R"))
    #self.rafraichirFigure.triggered.connect(self.refreshAction)
    self.figureToolBar.addAction(self.refreshAction)

    self.printAction = QAction(QIcon(self.appctxt.get_resource('icons/print.png')), "Print", self)
    self.printAction.setShortcut(QKeySequence("Ctrl+P"))
    #self.printAction.triggered.connect(self.print)
    self.figureToolBar.addAction(self.printAction)

    self.copyFigureAction = QAction(QIcon(self.appctxt.get_resource('icons/copyFigure.png')), "Copy", self)
    self.copyFigureAction.setShortcut(QKeySequence("Ctrl+C"))
    #self.copyFigureAction.triggered.connect(self.copyFigure)
    self.figureToolBar.addAction(self.copyFigureAction)

    self.figureToolBar.addSeparator()

    self.subplotToolBar = self.addToolBar("Subplot")
    self.subplotToolBar.setMovable(False)
    self.subplotToolBar.setIconSize(QSize(20, 20))

    self.subplotsManagerAction = QAction(QIcon(self.appctxt.get_resource('icons/subplotsManager.png')), "Subplots manager", self)
    #self.subplotsManagerAction.triggered.connect(self.subplotsManagerAction)
    self.subplotToolBar.addAction(self.subplotsManagerAction)

    self.subplotToolBar.addSeparator()

    self.outilsProfils = self.addToolBar("Profil en long")
    self.outilsProfils.setMovable(False)
    self.outilsProfils.setIconSize(QSize(20, 20))

    self.action_ajouterProfil = QAction(QIcon(self.appctxt.get_resource('icons/ajouter.png')), "Ajouter un profil en long", self)
    #self.action_ajouterProfil.triggered.connect(self.ajouterProfil)
    self.outilsProfils.addAction(self.action_ajouterProfil)

    self.action_tableauProfil = QAction(QIcon(self.appctxt.get_resource('icons/tableau.png')), "Tableau des valeurs du profil", self)
    #self.action_tableauProfil.triggered.connect(self.tableauValeurs)
    self.outilsProfils.addAction(self.action_tableauProfil)

    self.action_styleProfil = QAction(QIcon(self.appctxt.get_resource('icons/style.png')), "Propriétés graphiques du profil", self)
    #self.action_styleProfil.triggered.connect(self.optionsProfil)
    self.outilsProfils.addAction(self.action_styleProfil)

    self.action_trierProfil = QAction(QIcon(self.appctxt.get_resource('icons/trier.png')), "Trier le profil", self)
    #self.action_trierProfil.triggered.connect(self.trierProfil)
    self.outilsProfils.addAction(self.action_trierProfil)

    self.action_filtrerProfil = QAction(QIcon(self.appctxt.get_resource('icons/filtrer.png')), "Filtrer le profil", self)
    #self.action_filtrerProfil.triggered.connect(self.filtrerProfil)
    self.outilsProfils.addAction(self.action_filtrerProfil)

    self.action_simplifierProfil = QAction(QIcon(self.appctxt.get_resource('icons/simplifier.png')), "Simplifier le profil", self)
    #self.action_simplifierProfil.triggered.connect(self.simplifierProfil)
    self.outilsProfils.addAction(self.action_simplifierProfil)

    self.action_exporterProfil = QAction(QIcon(self.appctxt.get_resource('icons/exporter.png')), "Exporter le profil", self)
    #self.action_exporterProfil.triggered.connect(self.exporterProfil)
    self.outilsProfils.addAction(self.action_exporterProfil)

    self.action_supprimerProfils = QAction(QIcon(self.appctxt.get_resource('icons/corbeille.png')), "Supprimer les profils", self)
    #self.action_supprimerProfils.triggered.connect(self.supprimerProfils)
    self.action_supprimerProfils.setShortcut(QKeySequence("Alt+P"))
    self.outilsProfils.addAction(self.action_supprimerProfils)

    self.outilsProfils.addSeparator()

    self.outilsEdition = self.addToolBar("Edition interactive")
    self.outilsEdition.setMovable(False)
    self.outilsEdition.setIconSize(QSize(20, 20))

    self.action_editerProfils = QAction(QIcon(self.appctxt.get_resource('icons/editer.png')), "Edition du profil en long", self)
    self.action_editerProfils.setCheckable(True)
    #self.action_editerProfils.triggered.connect(self.editionProfil)
    self.outilsEdition.addAction(self.action_editerProfils)

    self.ajouterPoint = QAction(QIcon(self.appctxt.get_resource('icons/ajouter_point.png')), "Ajouter un sommet", self)
    self.ajouterPoint.setCheckable(True)
    #self.ajouterPoint.triggered.connect(self.addPoint)
    self.ajouterPoint.setShortcut(QKeySequence("Shift+A"))
    self.outilsEdition.addAction(self.ajouterPoint)
    self.ajouterPoint.setVisible(False)

    self.supprimerPoint = QAction(QIcon(self.appctxt.get_resource('icons/supprimer_point.png')), "Supprimer un sommet", self)
    self.supprimerPoint.setCheckable(True)
    #self.supprimerPoint.triggered.connect(self.removePoint)
    self.supprimerPoint.setShortcut(QKeySequence("Shift+S"))
    self.outilsEdition.addAction(self.supprimerPoint)
    self.supprimerPoint.setVisible(False)

    self.magnetisme = QAction(QIcon(self.appctxt.get_resource('icons/aimant.png')), "Activer l'accrochage sur profil", self)
    self.magnetisme.setCheckable(True)
    self.outilsEdition.addAction(self.magnetisme)
    #self.magnetisme.triggered.connect(self.updateListingProfils)
    #self.magnetisme.triggered.connect(self.activerMagnetisme)
    self.magnetisme.setVisible(False)

    self.listingProfils = QComboBox()
    for profile in self.project.profiles:
        self.listingProfils.addItem(profile.title)
    self.actionListingProfils = self.outilsEdition.addWidget(self.listingProfils)
    self.actionListingProfils.setVisible(False)

    self.outilsEdition.addSeparator()

    self.outilsAnnotations = self.addToolBar("Annotation")
    self.outilsAnnotations.setMovable(False)
    self.outilsAnnotations.setIconSize(QSize(20, 20))

    self.action_texte = QAction(QIcon(self.appctxt.get_resource('icons/texte.png')), "Ajouter un texte", self)
    #self.action_texte.triggered.connect(self.ajouterTexte)
    self.outilsAnnotations.addAction(self.action_texte)

    self.action_annotationPonctuelle = QAction(QIcon(self.appctxt.get_resource('icons/annotation_ponctuelle.png')), "Ajouter une annotation ponctuelle", self)
    #self.action_annotationPonctuelle.triggered.connect(self.ajouterAnnotationPonctuelle)
    self.outilsAnnotations.addAction(self.action_annotationPonctuelle)

    self.action_annotationLineaire = QAction(QIcon(self.appctxt.get_resource('icons/annotation_lineaire.png')), "Ajouter une annotation linéaire", self)
    #self.action_annotationLineaire.triggered.connect(self.ajouterAnnotationLineaire)
    self.outilsAnnotations.addAction(self.action_annotationLineaire)

    self.action_zoneProfil = QAction(QIcon(self.appctxt.get_resource('icons/zone.png')), "Ajouter une zone", self)
    #self.action_zoneProfil.triggered.connect(self.ajouterZone)
    self.outilsAnnotations.addAction(self.action_zoneProfil)

    self.action_formeRectangulaire = QAction(QIcon(self.appctxt.get_resource('icons/rectangle.png')), "Ajouter un rectangle", self)
    #self.action_formeRectangulaire.triggered.connect(self.ajouterRectangle)
    self.outilsAnnotations.addAction(self.action_formeRectangulaire)

    self.action_styleAnnotation = QAction(QIcon(self.appctxt.get_resource('icons/style.png')),"Propriétés graphiques de l'annotation", self)
    #self.action_styleAnnotation.triggered.connect(self.ouvrirStyleAnnotation)
    self.outilsAnnotations.addAction(self.action_styleAnnotation)

    self.action_copierPropriete = QAction(QIcon(self.appctxt.get_resource('icons/copierProprietes.png')), "Copier les propriétés graphiques", self)
    #self.action_copierPropriete.triggered.connect(self.copierPropriete)
    self.action_copierPropriete.setShortcut(QKeySequence("Ctrl+Alt+C"))
    self.outilsAnnotations.addAction(self.action_copierPropriete)

    self.action_collerPropriete = QAction(QIcon(self.appctxt.get_resource('icons/collerProprietes.png')), "Appliquer les propriétés graphiques", self)
    #self.action_collerPropriete.triggered.connect(self.collerPropriete)
    self.action_collerPropriete.setShortcut(QKeySequence("Ctrl+Alt+V"))
    self.outilsAnnotations.addAction(self.action_collerPropriete)

    self.action_ajusterAnnotations = QAction(QIcon(self.appctxt.get_resource('icons/ajuster.png')), "Ajuster les annotations ponctuelles", self)
    self.action_ajusterAnnotations.setShortcut(QKeySequence("Ctrl+Alt+Z"))
    #self.action_ajusterAnnotations.triggered.connect(self.ajusterAnnotations)
    self.outilsAnnotations.addAction(self.action_ajusterAnnotations)

    self.action_dupliquerAnnotation = QAction(QIcon(self.appctxt.get_resource('icons/dupliquer.png')), "Dupliquer les annotations", self)
    self.action_dupliquerAnnotation.setShortcut(QKeySequence("Ctrl+Alt+D"))
    #self.action_dupliquerAnnotation.triggered.connect(self.dupliquerAnnotations)
    self.outilsAnnotations.addAction(self.action_dupliquerAnnotation)

    self.action_gestionGroupes = QAction(QIcon(self.appctxt.get_resource('icons/gestion_groupes.png')), "Gérer les groupes d'annotations",
                             self)
    #self.action_gestionGroupes.triggered.connect(self.gestionGroupes)
    self.outilsAnnotations.addAction(self.action_gestionGroupes)

    self.action_supprimerAnnotations = QAction(QIcon(self.appctxt.get_resource('icons/corbeille.png')), "Supprimer les annotations", self)
    #self.action_supprimerAnnotations.triggered.connect(self.supprimerAnnotation)
    self.action_supprimerAnnotations.setShortcut(QKeySequence("Alt+A"))
    self.outilsAnnotations.addAction(self.action_supprimerAnnotations)

    self.outilsAnnotations.addSeparator()

    self.outilsRappels = self.addToolBar("Ligne de rappel")
    self.outilsRappels.setMovable(False)
    self.outilsRappels.setIconSize(QSize(20, 20))

    self.action_annotations2ligneRappel = QAction(QIcon(self.appctxt.get_resource('icons/wand.png')), "Annotations >>> Lignes de rappel", self)
    #self.action_annotations2ligneRappel.triggered.connect(self.annotations2ligneRappel)
    self.outilsRappels.addAction(self.action_annotations2ligneRappel)

    self.action_lignesRappel = QAction(QIcon(self.appctxt.get_resource('icons/rappel.png')), "Gestion des lignes de rappel", self)
    #self.action_lignesRappel.triggered.connect(self.lignesRappel)
    self.outilsRappels.addAction(self.action_lignesRappel)

    self.outilsRappels.addSeparator()

    self.outilsToolBox = self.addToolBar("Toolbox")
    self.outilsToolBox.setMovable(False)
    self.outilsToolBox.setIconSize(QSize(20, 20))

    self.action_toolbox = QAction(QIcon(self.appctxt.get_resource('icons/toolBox.png')), "Toolbox", self)
    #self.action_toolbox.triggered.connect(self.toolBox)
    self.outilsToolBox.addAction(self.action_toolbox)

    self.action_calcul = QAction(QIcon(self.appctxt.get_resource('icons/tools.png')), "Propriétés du calcul", self)
    #self.action_calcul.triggered.connect(self.ouvrirStyleCalcul)
    self.outilsToolBox.addAction(self.action_calcul)

    self.action_supprimerCalculs = QAction(QIcon(self.appctxt.get_resource('icons/corbeille.png')), "Supprimer les calculs", self)
    #self.action_supprimerCalculs.triggered.connect(self.supprimerCalculs)
    self.action_supprimerCalculs.setShortcut(QKeySequence("Alt+C"))
    self.outilsToolBox.addAction(self.action_supprimerCalculs)

    self.outilsToolBox.addSeparator()

    self.outilsAutresDonnees = self.addToolBar("Autres données")
    self.outilsAutresDonnees.setMovable(False)
    self.outilsAutresDonnees.setIconSize(QSize(20, 20))

    self.action_ajouterDonnees = QAction(QIcon(self.appctxt.get_resource('icons/autres_donnees.png')), "Ajouter des données", self)
    #self.action_ajouterDonnees.triggered.connect(self.ajouterDonnees)
    self.outilsAutresDonnees.addAction(self.action_ajouterDonnees)

    self.action_styleDonnees = QAction(QIcon(self.appctxt.get_resource('icons/style.png')), "Propriétés graphiques des données", self)
    #self.action_styleDonnees.triggered.connect(self.optionsDonnees)
    self.outilsAutresDonnees.addAction(self.action_styleDonnees)

    self.action_supprimerDonnees = QAction(QIcon(self.appctxt.get_resource('icons/corbeille.png')), "Supprimer les données", self)
    #self.action_supprimerDonnees.triggered.connect(self.supprimerDonnees)
    self.action_supprimerDonnees.setShortcut(QKeySequence("Alt+D"))
    self.outilsAutresDonnees.addAction(self.action_supprimerDonnees)

    self.outilsAutresDonnees.addSeparator()

    self.outilsRessources = self.addToolBar("Ressources")
    self.outilsRessources.setMovable(False)
    self.outilsRessources.setIconSize(QSize(20, 20))

    documentation = QAction(QIcon(self.appctxt.get_resource('icons/aide.png')), "Documentation", self)
    #documentation.triggered.connect(self.documentation)
    self.outilsRessources.addAction(documentation)

    aPropos = QAction(QIcon(self.appctxt.get_resource('icons/propos.png')), "À propos de pyLong", self)
    #aPropos.triggered.connect(self.aboutPyLong)
    self.outilsRessources.addAction(aPropos)

    self.outilsONF = self.addToolBar("ONF")
    self.outilsONF.setMovable(False)
    self.outilsONF.setIconSize(QSize(52, 20))

    onf = QAction(QIcon(self.appctxt.get_resource('icons/onf.png')), "www.onf.fr ", self)
    #onf.triggered.connect(self.onf)
    self.outilsONF.addAction(onf)

    menu = self.menuBar()

    self.projectMenu = menu.addMenu("Project")

    self.projectMenu.addAction(self.newProjectAction)
    self.projectMenu.addSeparator()
    self.projectMenu.addAction(self.openProjectAction)
    self.recentFilesMenu = self.projectMenu.addMenu("Open a recent project")
    # for path in self.recentFiles:
    #     self.menuRecent.addAction(f"{chemin}", lambda path=chemin: self.ouvrirProjetRecent(chemin=path))
    self.projectMenu.addSeparator()
    self.projectMenu.addAction(self.saveProjectAction)
    self.projectMenu.addAction(self.saveProjectAsAction)
    self.projectMenu.addSeparator()
    self.projectMenu.addAction(self.settingsAction)
    self.projectMenu.addSeparator()
    
    self.quitPyLongAction = QAction("Quit pyLong", self)
    self.quitPyLongAction.setShortcut(QKeySequence("Ctrl+Q"))
    #self.quitPyLongAction.triggered.connect(self.quitPylong)
    self.projectMenu.addAction(self.quitPyLongAction)

    self.interfaceMenu = menu.addMenu("Interface")
    self.interfaceMenu.addAction(self.fullScreenAction)
    self.interfaceMenu.addSeparator()
    self.interfaceMenu.addAction(self.zoomInAction)
    self.interfaceMenu.addAction(self.zoomOutAction)
    self.interfaceMenu.addAction(self.adjustWidthAction)
    self.interfaceMenu.addAction(self.adjustHeightAction)


    self.figureMenu = menu.addMenu("Figure")

    # self.menuFigure.addAction(ajouterLayout)
    # self.menuFigure.addAction(renommerLayout)
    # self.menuFigure.addAction(supprimerLayout)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.layoutAction)
    self.figureMenu.addAction(self.advancedLayoutAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.refreshAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.navigationBar._actions['pan'])
    self.figureMenu.addAction(self.navigationBar._actions['zoom'])
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.printAction)
    self.figureMenu.addSeparator()
    self.figureMenu.addAction(self.copyFigureAction)

    self.subplotMenu = menu.addMenu("Subplot")

    self.subplotMenu.addAction(self.subplotsManagerAction)

    self.menuProfil = menu.addMenu("Profil en long")

    self.menuProfil.addAction(self.action_ajouterProfil)
    self.menuProfil.addSeparator()
    self.menuProfil.addAction(self.action_tableauProfil)
    self.menuProfil.addSeparator()
    self.menuProfil.addAction(self.action_styleProfil)
    self.menuProfil.addSeparator()
    self.menuProfil.addAction(self.action_trierProfil)
    self.menuProfil.addAction(self.action_filtrerProfil)
    self.menuProfil.addAction(self.action_simplifierProfil)
    self.menuProfil.addAction(self.action_exporterProfil)
    self.menuProfil.addSeparator()
    self.menuProfil.addAction(self.action_supprimerProfils)

    menuEdition = menu.addMenu("Edition interactive")

    menuEdition.addAction(self.action_editerProfils)
    menuEdition.addSeparator()
    menuEdition.addAction(self.ajouterPoint)
    menuEdition.addAction(self.supprimerPoint)
    menuEdition.addAction(self.magnetisme)

    self.menuAnnotation = menu.addMenu("Annotation")
    self.menuAnnotation.addAction(self.action_texte)
    self.menuAnnotation.addAction(self.action_annotationPonctuelle)
    self.menuAnnotation.addAction(self.action_annotationLineaire)
    self.menuAnnotation.addAction(self.action_zoneProfil)
    self.menuAnnotation.addAction(self.action_formeRectangulaire)
    self.menuAnnotation.addSeparator()
    self.menuAnnotation.addAction(self.action_styleAnnotation)
    self.menuAnnotation.addSeparator()
    self.menuAnnotation.addAction(self.action_copierPropriete)
    self.menuAnnotation.addAction(self.action_collerPropriete)
    self.menuAnnotation.addSeparator()
    self.menuAnnotation.addAction(self.action_ajusterAnnotations)
    self.menuAnnotation.addSeparator()
    self.menuAnnotation.addAction(self.action_dupliquerAnnotation)
    self.menuAnnotation.addSeparator()

    ajouterGroupe = QAction('Ajouter un groupe', self)
    #ajouterGroupe.triggered.connect(self.ajouterGroupe)
    self.menuAnnotation.addAction(ajouterGroupe)
    renommerGroupe = QAction('Renommer le groupe', self)
    #renommerGroupe.triggered.connect(self.renommerGroupe)
    self.menuAnnotation.addAction(renommerGroupe)
    supprimerGroupe = QAction('Supprimer des groupes', self)
    #supprimerGroupe.triggered.connect(self.supprimerGroupes)
    self.menuAnnotation.addAction(supprimerGroupe)

    self.menuAnnotation.addAction(self.action_gestionGroupes)
    self.menuAnnotation.addSeparator()
    self.menuAnnotation.addAction(self.action_supprimerAnnotations)

    self.menuRappel = menu.addMenu("Ligne de rappel")
    self.menuRappel.addAction(self.action_annotations2ligneRappel)
    self.menuRappel.addSeparator()
    self.menuRappel.addAction(self.action_lignesRappel)

    self.menuToolBox = menu.addMenu("Toolbox")
    self.menuToolBox.addAction(self.action_toolbox)
    self.menuToolBox.addSeparator()
    self.menuToolBox.addAction(self.action_calcul)
    self.menuToolBox.addSeparator()
    self.menuToolBox.addAction(self.action_supprimerCalculs)

    self.menuAutresDonnees = menu.addMenu("Autres données")
    self.menuAutresDonnees.addAction(self.action_ajouterDonnees)
    self.menuAutresDonnees.addSeparator()
    self.menuAutresDonnees.addAction(self.action_styleDonnees)
    self.menuAutresDonnees.addSeparator()
    self.menuAutresDonnees.addAction(self.action_supprimerDonnees)

    self.menuRessources = menu.addMenu("Ressources")
    self.menuRessources.addAction(documentation)
    self.menuRessources.addSeparator()
    self.menuRessources.addAction(aPropos)
    self.menuRessources.addSeparator()
    self.menuRessources.addAction(onf)

    # self.menuRessources.setEnabled(False)