from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogGestionGroupes(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Gestion des groupes d'annotations")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/gestion_groupes.png')))
        
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        sublayout = QVBoxLayout()
        
        self.listeGroupesGauche = QComboBox()
        for groupe in self.pyLong.projet.groupes:
            self.listeGroupesGauche.addItem(groupe.intitule)
        self.listeGroupesGauche.currentIndexChanged.connect(self.updateInterface)
        
        self.listeAnnotationsGauche = QListWidget()
        self.listeAnnotationsGauche.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        sublayout.addWidget(self.listeGroupesGauche)
        sublayout.addWidget(self.listeAnnotationsGauche)
        
        layout.addLayout(sublayout)
        
        sublayout = QVBoxLayout()

        deplacerVersLaDroite = QPushButton()
        deplacerVersLaDroite.setAutoDefault(False)
        deplacerVersLaDroite.setToolTip("Déplacer vers la droite")
        deplacerVersLaDroite.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/droite.png')))
        deplacerVersLaDroite.clicked.connect(self.deplacerVersDroite)

        deplacerVersLaGauche = QPushButton()
        deplacerVersLaGauche.setAutoDefault(False)
        deplacerVersLaGauche.setToolTip("Déplacer vers la gauche")
        deplacerVersLaGauche.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/gauche.png')))
        deplacerVersLaGauche.clicked.connect(self.deplacerVersGauche)

        sublayout.addWidget(deplacerVersLaDroite)
        sublayout.addWidget(deplacerVersLaGauche)
        
        layout.addLayout(sublayout)
        
        sublayout = QVBoxLayout()
        
        self.listeGroupesDroite = QComboBox()
        for groupe in self.pyLong.projet.groupes:
            self.listeGroupesDroite.addItem(groupe.intitule)
        self.listeGroupesDroite.currentIndexChanged.connect(self.updateInterface)
        
        self.listeAnnotationsDroite = QListWidget()
        self.listeAnnotationsDroite.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        sublayout.addWidget(self.listeGroupesDroite)
        sublayout.addWidget(self.listeAnnotationsDroite)
        
        layout.addLayout(sublayout)        

        mainLayout.addLayout(layout)
        
        self.setLayout(mainLayout)

        self.updateInterface()

    def updateInterface(self):
        self.listeAnnotationsGauche.clear()
        self.listeAnnotationsDroite.clear()

        i = self.listeGroupesGauche.currentIndex()
        for annotation in self.pyLong.projet.groupes[i].annotations :
            self.listeAnnotationsGauche.addItem(annotation.intitule)

        j = self.listeGroupesDroite.currentIndex()
        for annotation in self.pyLong.projet.groupes[j].annotations :
            self.listeAnnotationsDroite.addItem(annotation.intitule)

    def deplacerVersDroite(self):
        i = self.listeGroupesGauche.currentIndex()
        j = self.listeGroupesDroite.currentIndex()

        indices = []
        for item in self.listeAnnotationsGauche.selectedIndexes():
            indices.append(item.row())

        indices.sort()
        indices.reverse()

        for k in indices:
            annotation = self.pyLong.projet.groupes[i].annotations[k]
            self.pyLong.projet.groupes[j].annotations.append(annotation)
            self.pyLong.projet.groupes[i].annotations.pop(k)

        self.updateInterface()

    def deplacerVersGauche(self):
        i = self.listeGroupesGauche.currentIndex()
        j = self.listeGroupesDroite.currentIndex()

        indices = []
        for item in self.listeAnnotationsDroite.selectedIndexes():
            indices.append(item.row())

        indices.sort()
        indices.reverse()

        for k in indices:
            annotation = self.pyLong.projet.groupes[j].annotations[k]
            self.pyLong.projet.groupes[i].annotations.append(annotation)
            self.pyLong.projet.groupes[j].annotations.pop(k)

        self.updateInterface()

        self.updateInterface()
