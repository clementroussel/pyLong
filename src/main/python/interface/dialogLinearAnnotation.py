from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.dictionnaires import *

from ColorsComboBox import *


class DialogAnnotationLineaire(QDialog):
    def __init__(self, parent) :
        super().__init__(parent=parent)
        
        self.setModal(False)
        
        self.pyLong = parent
        
        i = self.pyLong.listeAnnotations.groupes.currentIndex()
        j = self.pyLong.listeAnnotations.liste.currentRow()
        self.al = self.pyLong.projet.groupes[i].annotations[j]
        
        self.setWindowTitle("Annotation linéaire")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/annotation_lineaire.png')))
 
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.al.intitule)
        self.intitule.textChanged.connect(self.updateIntitule)
        layout.addWidget(self.intitule)  
        
        mainLayout.addLayout(layout)
        
        groupe = QGroupBox("Texte à afficher")
        layout = QGridLayout()
        
        label = QLabel("Libellé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.libelle = QLineEdit()
        self.libelle.setMaxLength(50)
        self.libelle.setText(self.al.libelle)
        self.libelle.textEdited.connect(self.appliquer)
        layout.addWidget(self.libelle, 0, 1)
        
        label = QLabel("Taille :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.tailleLibelle = QDoubleSpinBox()
        self.tailleLibelle.setMaximumWidth(50)
        self.tailleLibelle.setLocale(QLocale('English'))
        self.tailleLibelle.setRange(0, 99.9)
        self.tailleLibelle.setDecimals(1)
        self.tailleLibelle.setSingleStep(0.1)
        self.tailleLibelle.setValue(self.al.texte['taille'])
        self.tailleLibelle.valueChanged.connect(self.appliquer)
        layout.addWidget(self.tailleLibelle, 1, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.couleurLibelle = ColorsComboBox(self.pyLong.appctxt)
        self.couleurLibelle.setCurrentText(self.al.texte['couleur'])
        self.couleurLibelle.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurLibelle, 2, 1)
        
        label = QLabel("Décalage vert. :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3 ,0)
        
        self.decalageLibelle = QDoubleSpinBox()
        self.decalageLibelle.setMaximumWidth(65)
        self.decalageLibelle.setLocale(QLocale('English'))
        self.decalageLibelle.setSuffix(" m")
        self.decalageLibelle.setRange(-9999, 9999)
        self.decalageLibelle.setDecimals(1)
        self.decalageLibelle.setSingleStep(0.1)
        self.decalageLibelle.setValue(self.al.texte['décalage'])
        self.decalageLibelle.valueChanged.connect(self.appliquer)
        layout.addWidget(self.decalageLibelle, 3, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Emprise de la zone annotée")
        layout = QGridLayout()
        
        label = QLabel("Abscisse début :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.abscisse2debut = QDoubleSpinBox()
        self.abscisse2debut.setMaximumWidth(90)
        self.abscisse2debut.setSuffix(" m")
        self.abscisse2debut.setLocale(QLocale('English'))
        self.abscisse2debut.setRange(-99999.999, 99999.999)
        self.abscisse2debut.setDecimals(3)
        self.abscisse2debut.setSingleStep(0.1)
        self.abscisse2debut.setValue(self.al.fleche['abscisse de début'])
        self.abscisse2debut.valueChanged.connect(self.appliquer)
        layout.addWidget(self.abscisse2debut, 0, 1)
        
        self.pointerDebut = QPushButton()
        self.pointerDebut.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointerDebut.setIconSize(QSize(12,12))
        self.pointerDebut.setMaximumWidth(25)
        self.pointerDebut.setAutoDefault(False)
        self.pointerDebut.clicked.connect(self.pointageAbscisseDebut)
        layout.addWidget(self.pointerDebut, 0, 2)

        label = QLabel("Abscisse fin :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.abscisse2fin = QDoubleSpinBox()
        self.abscisse2fin.setMaximumWidth(90)
        self.abscisse2fin.setSuffix(" m")
        self.abscisse2fin.setLocale(QLocale('English'))
        self.abscisse2fin.setRange(-99999.999, 99999.999)
        self.abscisse2fin.setDecimals(3)
        self.abscisse2fin.setSingleStep(0.1)
        self.abscisse2fin.setValue(self.al.fleche['abscisse de fin'])
        self.abscisse2fin.valueChanged.connect(self.appliquer)
        layout.addWidget(self.abscisse2fin, 1, 1)
        
        self.pointerFin = QPushButton()
        self.pointerFin.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointerFin.setIconSize(QSize(12,12))
        self.pointerFin.setMaximumWidth(25)
        self.pointerFin.setAutoDefault(False)
        self.pointerFin.clicked.connect(self.pointageAbscisseFin)
        layout.addWidget(self.pointerFin, 1, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Flèche annotative")
        layout = QGridLayout()
        
        sublayout = QHBoxLayout()
        
        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label)
        
        self.altitudeFleche = QDoubleSpinBox()
        self.altitudeFleche.setMaximumWidth(90)
        self.altitudeFleche.setSuffix(" m")
        self.altitudeFleche.setLocale(QLocale('English'))
        self.altitudeFleche.setRange(-99999.999, 99999.999)
        self.altitudeFleche.setDecimals(3)
        self.altitudeFleche.setSingleStep(0.1)
        self.altitudeFleche.setValue(self.al.fleche['altitude'])
        self.altitudeFleche.valueChanged.connect(self.appliquer)
        sublayout.addWidget(self.altitudeFleche)
        
        self.pointerAltitude = QPushButton()
        self.pointerAltitude.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointerAltitude.setIconSize(QSize(12,12))
        self.pointerAltitude.setMaximumWidth(25)
        self.pointerAltitude.setAutoDefault(False)
        self.pointerAltitude.clicked.connect(self.pointageAltitude)
        sublayout.addWidget(self.pointerAltitude)
        
        layout.addLayout(sublayout, 0, 0, 1, 2)
        
        label = QLabel("Style de flèche :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.styleFleche = QComboBox()
        self.styleFleche.addItem("-")
        self.styleFleche.addItem("<->")
        self.styleFleche.addItem("<|-|>")
        self.styleFleche.setCurrentText(self.al.fleche['style de flèche'])
        self.styleFleche.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.styleFleche, 1, 1)
        
        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.styleLigne = QComboBox()
        self.styleLigne.insertItems(0, list(styles2ligne.keys()))
        self.styleLigne.setCurrentText(self.al.fleche['style de ligne'])
        self.styleLigne.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.styleLigne, 2, 1)
        
        label = QLabel("Épaisseur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.epaisseurFleche = QDoubleSpinBox()
        self.epaisseurFleche.setMaximumWidth(50)
        self.epaisseurFleche.setLocale(QLocale('English'))
        self.epaisseurFleche.setRange(0, 99.9)
        self.epaisseurFleche.setDecimals(1)
        self.epaisseurFleche.setSingleStep(0.1)
        self.epaisseurFleche.setValue(self.al.fleche['épaisseur'])
        self.epaisseurFleche.valueChanged.connect(self.appliquer)
        layout.addWidget(self.epaisseurFleche, 3, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.couleurFleche = ColorsComboBox(self.pyLong.appctxt)
        self.couleurFleche.setCurrentText(self.al.fleche['couleur'])
        self.couleurFleche.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurFleche, 4, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Opacité et ordre")
        layout = QGridLayout()
        
        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.opacite = QDoubleSpinBox()
        self.opacite.setMaximumWidth(45)
        self.opacite.setLocale(QLocale('English'))
        self.opacite.setRange(0,1)
        self.opacite.setDecimals(1)
        self.opacite.setSingleStep(0.1)
        self.opacite.setValue(self.al.opacite)
        self.opacite.valueChanged.connect(self.appliquer)
        layout.addWidget(self.opacite, 0, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 2)
        
        self.ordre = QSpinBox()
        self.ordre.setMaximumWidth(45)
        self.ordre.setLocale(QLocale('English'))
        self.ordre.setRange(1,99)
        self.ordre.setSingleStep(1)
        self.ordre.setValue(self.al.ordre)
        self.ordre.valueChanged.connect(self.appliquer)
        layout.addWidget(self.ordre, 0, 3)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        
    def valider(self):
        self.pyLong.controleOutilsNavigation()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.appliquer()
        self.accept()

    def updateIntitule(self):
        self.al.intitule = self.intitule.text()
        self.pyLong.listeAnnotations.updateListe()
        
    def appliquer(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass

        self.al.libelle = self.libelle.text()
        self.al.texte['taille'] = self.tailleLibelle.value()
        self.al.texte['couleur'] = self.couleurLibelle.currentText()
        self.al.texte['décalage'] = self.decalageLibelle.value()
        
        self.al.fleche['abscisse de début'] = self.abscisse2debut.value()
        self.al.fleche['abscisse de fin'] = self.abscisse2fin.value()
        self.al.fleche['altitude'] = self.altitudeFleche.value()
        self.al.fleche['style de flèche'] = self.styleFleche.currentText()
        self.al.fleche['style de ligne'] = self.styleLigne.currentText()
        self.al.fleche['couleur'] = self.couleurFleche.currentText()
        self.al.fleche['épaisseur'] = self.epaisseurFleche.value()
        
        self.al.opacite = self.opacite.value()
        self.al.ordre = self.ordre.value()
        
        self.al.update()

        self.pyLong.canvas.draw()
        
    def pointageAbscisseDebut(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickAbscisseDebut)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickAbscisseDebut(self, event):
        try:
            self.abscisse2debut.setValue(event.xdata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.appliquer()
        
    def pointageAbscisseFin(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickAbscisseFin)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickAbscisseFin(self, event):
        try:
            self.abscisse2fin.setValue(event.xdata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.appliquer()
        
    def pointageAltitude(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickAltitude)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickAltitude(self, event):
        try:
            self.altitudeFleche.setValue(event.ydata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.appliquer()
        
    def closeEvent(self, event):
        self.pyLong.controleOutilsNavigation()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
    def reject(self):
        self.pyLong.controleOutilsNavigation()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        self.accept()
