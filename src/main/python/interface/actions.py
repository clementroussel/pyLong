from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def createActions(self):
    appctxt = self.appctxt
    # création de la barre d'outils
    self.outilsProjet = self.addToolBar("Projet")
    self.outilsProjet.setMovable(False)
    self.outilsProjet.setIconSize(QSize(20, 20))

    nouveauProjet = QAction(QIcon(appctxt.get_resource('icones/nouveau.png')), "Créer un nouveau projet", self)
    nouveauProjet.setShortcut(QKeySequence("Ctrl+N"))
    #nouveauProjet.triggered.connect(self.nouveauProjet)
    self.outilsProjet.addAction(nouveauProjet)

    ouvrirProjet = QAction(QIcon(appctxt.get_resource('icones/ouvrir.png')), "Ouvrir un projet", self)
    ouvrirProjet.setShortcut(QKeySequence("Ctrl+O"))
    #ouvrirProjet.triggered.connect(self.ouvrirProjet)
    self.outilsProjet.addAction(ouvrirProjet)

    enregistrerProjet = QAction(QIcon(appctxt.get_resource('icones/enregistrer.png')), "Enregistrer le projet", self)
    enregistrerProjet.setShortcut(QKeySequence("Ctrl+S"))
    #enregistrerProjet.triggered.connect(self.enregistrerProjet)
    self.outilsProjet.addAction(enregistrerProjet)

    enregistrerProjetSous = QAction(QIcon(appctxt.get_resource('icones/enregistrer_sous.png')),
                                    "Enregistrer le projet sous.. ", self)
    enregistrerProjetSous.setShortcut(QKeySequence("Shift+Ctrl+S"))
    #enregistrerProjetSous.triggered.connect(self.enregistrerProjetSous)
    self.outilsProjet.addAction(enregistrerProjetSous)

    optionsProjet = QAction(QIcon(appctxt.get_resource('icones/preferences.png')), "Préférences", self)
    #optionsProjet.triggered.connect(self.gestionPreferences)
    self.outilsProjet.addAction(optionsProjet)

    self.outilsProjet.addSeparator()

    self.outilsInterface = self.addToolBar("Interface")
    self.outilsInterface.setMovable(False)
    self.outilsInterface.setIconSize(QSize(20, 20))

    pleinEcran = QAction(QIcon(appctxt.get_resource('icones/agrandir.png')), "Plein écran", self)
    pleinEcran.setCheckable(True)
    pleinEcran.setShortcut(QKeySequence("F11"))
    #pleinEcran.triggered.connect(self.pleinEcran)
    self.outilsInterface.addAction(pleinEcran)

    agrandirCanvas = QAction(QIcon(appctxt.get_resource('icones/zoom-in.png')), "Agrandir le canvas", self)
    agrandirCanvas.setShortcut(QKeySequence("Ctrl++"))
    #agrandirCanvas.triggered.connect(self.agrandirCanvas)
    self.outilsInterface.addAction(agrandirCanvas)

    retrecirCanvas = QAction(QIcon(appctxt.get_resource('icones/zoom-out.png')), "Rétrécir le canvas", self)
    retrecirCanvas.setShortcut(QKeySequence("Ctrl+-"))
    #retrecirCanvas.triggered.connect(self.retrecirCanvas)
    self.outilsInterface.addAction(retrecirCanvas)

    ajusterLargeur = QAction(QIcon(appctxt.get_resource('icones/ajuster-largeur.png')), "Canvas pleine largeur", self)
    #ajusterLargeur.triggered.connect(self.ajusterLargeur)
    self.outilsInterface.addAction(ajusterLargeur)

    ajusterHauteur = QAction(QIcon(appctxt.get_resource('icones/ajuster-hauteur.png')), "Canvas pleine hauteur", self)
    #ajusterHauteur.triggered.connect(self.ajusterHauteur)
    self.outilsInterface.addAction(ajusterHauteur)

    self.outilsInterface.addSeparator()

    self.outilsFigure = self.addToolBar("Figure")
    self.outilsFigure.setMovable(False)
    self.outilsFigure.setIconSize(QSize(20, 20))

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

    self.action_miseEnPage = QAction(QIcon(appctxt.get_resource('icones/mise_en_page.png')), "Propriétés de la mise en page", self)
    #self.action_miseEnPage.triggered.connect(self.miseEnPage)
    self.outilsFigure.addAction(self.action_miseEnPage)

    self.action_miseEnPage_avancee = QAction(QIcon(appctxt.get_resource('icones/grid.png')), "Propriétés avancées de la mise en page", self)
    #self.action_miseEnPage_avancee.triggered.connect(self.miseEnPage_avancee)
    self.outilsFigure.addAction(self.action_miseEnPage_avancee)

    self.rafraichirFigure = QAction(QIcon(appctxt.get_resource('icones/rafraichir.png')), "Actualiser la figure", self)
    self.rafraichirFigure.setShortcut(QKeySequence("Ctrl+R"))
    #self.rafraichirFigure.triggered.connect(self.rafraichir)
    self.outilsFigure.addAction(self.rafraichirFigure)

    # zoomer = QAction(QIcon(appctxt.get_resource('icones/zoom.png')), "Activer/Désactiver le zoom", self)
    # zoomer.setCheckable(True)
    # zoomer.triggered.connect(self.zoomer)
    # self.outilsFigure.addAction(zoomer)

    # preview = QAction(QIcon(appctxt.get_resource('icones/preview.png')), "Aperçu avant export", self)
    # preview.triggered.connect(self.preview)
    # self.outilsFigure.addAction(preview)

    self.action_exporterFigure = QAction(QIcon(appctxt.get_resource('icones/imprimer.png')), "Exporter la figure", self)
    self.action_exporterFigure.setShortcut(QKeySequence("Ctrl+P"))
    #self.action_exporterFigure.triggered.connect(self.imprimer)
    self.outilsFigure.addAction(self.action_exporterFigure)

    self.action_copierFigure = QAction(QIcon(appctxt.get_resource('icones/copierFigure.png')), "Copier la figure", self)
    self.action_copierFigure.setShortcut(QKeySequence("Ctrl+C"))
    #self.action_copierFigure.triggered.connect(self.copierFigure)
    self.outilsFigure.addAction(self.action_copierFigure)

    self.outilsFigure.addSeparator()

    self.outilsSubplots = self.addToolBar("Subplot")
    self.outilsSubplots.setMovable(False)
    self.outilsSubplots.setIconSize(QSize(20, 20))

    self.action_gestionSubplots = QAction(QIcon(appctxt.get_resource('icones/gestion_subplots.png')), "Gestion des subplots", self)
    #self.action_gestionSubplots.triggered.connect(self.gestionSubplots)
    self.outilsSubplots.addAction(self.action_gestionSubplots)

    self.outilsSubplots.addSeparator()

    self.outilsProfils = self.addToolBar("Profil en long")
    self.outilsProfils.setMovable(False)
    self.outilsProfils.setIconSize(QSize(20, 20))

    self.action_ajouterProfil = QAction(QIcon(appctxt.get_resource('icones/ajouter.png')), "Ajouter un profil en long", self)
    #self.action_ajouterProfil.triggered.connect(self.ajouterProfil)
    self.outilsProfils.addAction(self.action_ajouterProfil)

    self.action_tableauProfil = QAction(QIcon(appctxt.get_resource('icones/tableau.png')), "Tableau des valeurs du profil", self)
    #self.action_tableauProfil.triggered.connect(self.tableauValeurs)
    self.outilsProfils.addAction(self.action_tableauProfil)

    self.action_styleProfil = QAction(QIcon(appctxt.get_resource('icones/style.png')), "Propriétés graphiques du profil", self)
    #self.action_styleProfil.triggered.connect(self.optionsProfil)
    self.outilsProfils.addAction(self.action_styleProfil)

    self.action_trierProfil = QAction(QIcon(appctxt.get_resource('icones/trier.png')), "Trier le profil", self)
    #self.action_trierProfil.triggered.connect(self.trierProfil)
    self.outilsProfils.addAction(self.action_trierProfil)

    self.action_filtrerProfil = QAction(QIcon(appctxt.get_resource('icones/filtrer.png')), "Filtrer le profil", self)
    #self.action_filtrerProfil.triggered.connect(self.filtrerProfil)
    self.outilsProfils.addAction(self.action_filtrerProfil)

    self.action_simplifierProfil = QAction(QIcon(appctxt.get_resource('icones/simplifier.png')), "Simplifier le profil", self)
    #self.action_simplifierProfil.triggered.connect(self.simplifierProfil)
    self.outilsProfils.addAction(self.action_simplifierProfil)

    self.action_exporterProfil = QAction(QIcon(appctxt.get_resource('icones/exporter.png')), "Exporter le profil", self)
    #self.action_exporterProfil.triggered.connect(self.exporterProfil)
    self.outilsProfils.addAction(self.action_exporterProfil)

    self.action_supprimerProfils = QAction(QIcon(appctxt.get_resource('icones/corbeille.png')), "Supprimer les profils", self)
    #self.action_supprimerProfils.triggered.connect(self.supprimerProfils)
    self.action_supprimerProfils.setShortcut(QKeySequence("Alt+P"))
    self.outilsProfils.addAction(self.action_supprimerProfils)

    self.outilsProfils.addSeparator()

    self.outilsEdition = self.addToolBar("Edition interactive")
    self.outilsEdition.setMovable(False)
    self.outilsEdition.setIconSize(QSize(20, 20))

    self.action_editerProfils = QAction(QIcon(appctxt.get_resource('icones/editer.png')), "Edition du profil en long", self)
    self.action_editerProfils.setCheckable(True)
    #self.action_editerProfils.triggered.connect(self.editionProfil)
    self.outilsEdition.addAction(self.action_editerProfils)

    self.ajouterPoint = QAction(QIcon(appctxt.get_resource('icones/ajouter_point.png')), "Ajouter un sommet", self)
    self.ajouterPoint.setCheckable(True)
    #self.ajouterPoint.triggered.connect(self.addPoint)
    self.ajouterPoint.setShortcut(QKeySequence("Shift+A"))
    self.outilsEdition.addAction(self.ajouterPoint)
    self.ajouterPoint.setVisible(False)

    self.supprimerPoint = QAction(QIcon(appctxt.get_resource('icones/supprimer_point.png')), "Supprimer un sommet", self)
    self.supprimerPoint.setCheckable(True)
    #self.supprimerPoint.triggered.connect(self.removePoint)
    self.supprimerPoint.setShortcut(QKeySequence("Shift+S"))
    self.outilsEdition.addAction(self.supprimerPoint)
    self.supprimerPoint.setVisible(False)

    self.magnetisme = QAction(QIcon(appctxt.get_resource('icones/aimant.png')), "Activer l'accrochage sur profil", self)
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

    self.action_texte = QAction(QIcon(appctxt.get_resource('icones/texte.png')), "Ajouter un texte", self)
    #self.action_texte.triggered.connect(self.ajouterTexte)
    self.outilsAnnotations.addAction(self.action_texte)

    self.action_annotationPonctuelle = QAction(QIcon(appctxt.get_resource('icones/annotation_ponctuelle.png')), "Ajouter une annotation ponctuelle", self)
    #self.action_annotationPonctuelle.triggered.connect(self.ajouterAnnotationPonctuelle)
    self.outilsAnnotations.addAction(self.action_annotationPonctuelle)

    self.action_annotationLineaire = QAction(QIcon(appctxt.get_resource('icones/annotation_lineaire.png')), "Ajouter une annotation linéaire", self)
    #self.action_annotationLineaire.triggered.connect(self.ajouterAnnotationLineaire)
    self.outilsAnnotations.addAction(self.action_annotationLineaire)

    self.action_zoneProfil = QAction(QIcon(appctxt.get_resource('icones/zone.png')), "Ajouter une zone", self)
    #self.action_zoneProfil.triggered.connect(self.ajouterZone)
    self.outilsAnnotations.addAction(self.action_zoneProfil)

    self.action_formeRectangulaire = QAction(QIcon(appctxt.get_resource('icones/rectangle.png')), "Ajouter un rectangle", self)
    #self.action_formeRectangulaire.triggered.connect(self.ajouterRectangle)
    self.outilsAnnotations.addAction(self.action_formeRectangulaire)

    self.action_styleAnnotation = QAction(QIcon(appctxt.get_resource('icones/style.png')),"Propriétés graphiques de l'annotation", self)
    #self.action_styleAnnotation.triggered.connect(self.ouvrirStyleAnnotation)
    self.outilsAnnotations.addAction(self.action_styleAnnotation)

    self.action_copierPropriete = QAction(QIcon(appctxt.get_resource('icones/copierProprietes.png')), "Copier les propriétés graphiques", self)
    #self.action_copierPropriete.triggered.connect(self.copierPropriete)
    self.action_copierPropriete.setShortcut(QKeySequence("Ctrl+Alt+C"))
    self.outilsAnnotations.addAction(self.action_copierPropriete)

    self.action_collerPropriete = QAction(QIcon(appctxt.get_resource('icones/collerProprietes.png')), "Appliquer les propriétés graphiques", self)
    #self.action_collerPropriete.triggered.connect(self.collerPropriete)
    self.action_collerPropriete.setShortcut(QKeySequence("Ctrl+Alt+V"))
    self.outilsAnnotations.addAction(self.action_collerPropriete)

    self.action_ajusterAnnotations = QAction(QIcon(appctxt.get_resource('icones/ajuster.png')), "Ajuster les annotations ponctuelles", self)
    self.action_ajusterAnnotations.setShortcut(QKeySequence("Ctrl+Alt+Z"))
    #self.action_ajusterAnnotations.triggered.connect(self.ajusterAnnotations)
    self.outilsAnnotations.addAction(self.action_ajusterAnnotations)

    self.action_dupliquerAnnotation = QAction(QIcon(appctxt.get_resource('icones/dupliquer.png')), "Dupliquer les annotations", self)
    self.action_dupliquerAnnotation.setShortcut(QKeySequence("Ctrl+Alt+D"))
    #self.action_dupliquerAnnotation.triggered.connect(self.dupliquerAnnotations)
    self.outilsAnnotations.addAction(self.action_dupliquerAnnotation)

    self.action_gestionGroupes = QAction(QIcon(appctxt.get_resource('icones/gestion_groupes.png')), "Gérer les groupes d'annotations",
                             self)
    #self.action_gestionGroupes.triggered.connect(self.gestionGroupes)
    self.outilsAnnotations.addAction(self.action_gestionGroupes)

    self.action_supprimerAnnotations = QAction(QIcon(appctxt.get_resource('icones/corbeille.png')), "Supprimer les annotations", self)
    #self.action_supprimerAnnotations.triggered.connect(self.supprimerAnnotation)
    self.action_supprimerAnnotations.setShortcut(QKeySequence("Alt+A"))
    self.outilsAnnotations.addAction(self.action_supprimerAnnotations)

    self.outilsAnnotations.addSeparator()

    self.outilsRappels = self.addToolBar("Ligne de rappel")
    self.outilsRappels.setMovable(False)
    self.outilsRappels.setIconSize(QSize(20, 20))

    self.action_annotations2ligneRappel = QAction(QIcon(appctxt.get_resource('icones/wand.png')), "Annotations >>> Lignes de rappel", self)
    #self.action_annotations2ligneRappel.triggered.connect(self.annotations2ligneRappel)
    self.outilsRappels.addAction(self.action_annotations2ligneRappel)

    self.action_lignesRappel = QAction(QIcon(appctxt.get_resource('icones/rappel.png')), "Gestion des lignes de rappel", self)
    #self.action_lignesRappel.triggered.connect(self.lignesRappel)
    self.outilsRappels.addAction(self.action_lignesRappel)

    self.outilsRappels.addSeparator()

    self.outilsToolBox = self.addToolBar("Toolbox")
    self.outilsToolBox.setMovable(False)
    self.outilsToolBox.setIconSize(QSize(20, 20))

    self.action_toolbox = QAction(QIcon(appctxt.get_resource('icones/toolBox.png')), "Toolbox", self)
    #self.action_toolbox.triggered.connect(self.toolBox)
    self.outilsToolBox.addAction(self.action_toolbox)

    self.action_calcul = QAction(QIcon(appctxt.get_resource('icones/tools.png')), "Propriétés du calcul", self)
    #self.action_calcul.triggered.connect(self.ouvrirStyleCalcul)
    self.outilsToolBox.addAction(self.action_calcul)

    self.action_supprimerCalculs = QAction(QIcon(appctxt.get_resource('icones/corbeille.png')), "Supprimer les calculs", self)
    #self.action_supprimerCalculs.triggered.connect(self.supprimerCalculs)
    self.action_supprimerCalculs.setShortcut(QKeySequence("Alt+C"))
    self.outilsToolBox.addAction(self.action_supprimerCalculs)

    self.outilsToolBox.addSeparator()

    self.outilsAutresDonnees = self.addToolBar("Autres données")
    self.outilsAutresDonnees.setMovable(False)
    self.outilsAutresDonnees.setIconSize(QSize(20, 20))

    self.action_ajouterDonnees = QAction(QIcon(appctxt.get_resource('icones/autres_donnees.png')), "Ajouter des données", self)
    #self.action_ajouterDonnees.triggered.connect(self.ajouterDonnees)
    self.outilsAutresDonnees.addAction(self.action_ajouterDonnees)

    self.action_styleDonnees = QAction(QIcon(appctxt.get_resource('icones/style.png')), "Propriétés graphiques des données", self)
    #self.action_styleDonnees.triggered.connect(self.optionsDonnees)
    self.outilsAutresDonnees.addAction(self.action_styleDonnees)

    self.action_supprimerDonnees = QAction(QIcon(appctxt.get_resource('icones/corbeille.png')), "Supprimer les données", self)
    #self.action_supprimerDonnees.triggered.connect(self.supprimerDonnees)
    self.action_supprimerDonnees.setShortcut(QKeySequence("Alt+D"))
    self.outilsAutresDonnees.addAction(self.action_supprimerDonnees)

    self.outilsAutresDonnees.addSeparator()

    self.outilsRessources = self.addToolBar("Ressources")
    self.outilsRessources.setMovable(False)
    self.outilsRessources.setIconSize(QSize(20, 20))

    documentation = QAction(QIcon(appctxt.get_resource('icones/aide.png')), "Documentation", self)
    #documentation.triggered.connect(self.documentation)
    self.outilsRessources.addAction(documentation)

    aPropos = QAction(QIcon(appctxt.get_resource('icones/propos.png')), "À propos de pyLong", self)
    #aPropos.triggered.connect(self.aboutPyLong)
    self.outilsRessources.addAction(aPropos)

    self.outilsONF = self.addToolBar("ONF")
    self.outilsONF.setMovable(False)
    self.outilsONF.setIconSize(QSize(52, 20))

    onf = QAction(QIcon(appctxt.get_resource('icones/onf.png')), "www.onf.fr ", self)
    #onf.triggered.connect(self.onf)
    self.outilsONF.addAction(onf)

    menu = self.menuBar()

    self.menuProjet = menu.addMenu("Projet")

    self.menuProjet.addAction(nouveauProjet)
    self.menuProjet.addSeparator()
    self.menuProjet.addAction(ouvrirProjet)
    self.menuRecent = self.menuProjet.addMenu("Ouvrir un projet récent")
    for chemin in self.recentFiles:
        self.menuRecent.addAction(f"{chemin}", lambda path=chemin: self.ouvrirProjetRecent(chemin=path))
    self.menuProjet.addSeparator()
    self.menuProjet.addAction(enregistrerProjet)
    self.menuProjet.addAction(enregistrerProjetSous)
    self.menuProjet.addSeparator()
    self.menuProjet.addAction(optionsProjet)
    self.menuProjet.addSeparator()
    quitterPylong = QAction("Quitter pyLong", self)
    quitterPylong.setShortcut(QKeySequence("Ctrl+Q"))
    #quitterPylong.triggered.connect(self.quitterPylong)
    self.menuProjet.addAction(quitterPylong)

    self.menuInterface = menu.addMenu("Interface")
    self.menuInterface.addAction(pleinEcran)
    self.menuInterface.addSeparator()
    self.menuInterface.addAction(agrandirCanvas)
    self.menuInterface.addAction(retrecirCanvas)
    self.menuInterface.addAction(ajusterLargeur)
    self.menuInterface.addAction(ajusterHauteur)


    self.menuFigure = menu.addMenu("Figure")

    # self.menuFigure.addAction(ajouterLayout)
    # self.menuFigure.addAction(renommerLayout)
    # self.menuFigure.addAction(supprimerLayout)
    self.menuFigure.addSeparator()
    self.menuFigure.addAction(self.action_miseEnPage)
    self.menuFigure.addAction(self.action_miseEnPage_avancee)
    self.menuFigure.addSeparator()
    self.menuFigure.addAction(self.rafraichirFigure)
    self.menuFigure.addSeparator()
    self.menuFigure.addAction(self.navigationBar._actions['pan'])
    self.menuFigure.addAction(self.navigationBar._actions['zoom'])
    self.menuFigure.addSeparator()
    self.menuFigure.addAction(self.action_exporterFigure)
    self.menuFigure.addSeparator()
    self.menuFigure.addAction(self.action_copierFigure)

    self.menuSubplot = menu.addMenu("Subplot")

    self.menuSubplot.addAction(self.action_gestionSubplots)

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