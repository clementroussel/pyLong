from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from interface.colorsComboBox import *


class DialogVerticalAnnotation(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setModal(False)
        
        self.pyLong = parent
        
        i = self.pyLong.listeAnnotations.groupes.currentIndex()
        j = self.pyLong.listeAnnotations.liste.currentRow()
        self.ap = self.pyLong.projet.groupes[i].annotations[j]
        
        self.setWindowTitle("Annotation ponctuelle")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/annotation_ponctuelle.png')))
    
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.ap.intitule)
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
        self.libelle.setText(self.ap.libelle)
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
        self.tailleLibelle.setValue(self.ap.texte['taille'])
        self.tailleLibelle.valueChanged.connect(self.appliquer)
        layout.addWidget(self.tailleLibelle, 1, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.couleurLibelle = ColorsComboBox(self.pyLong.appctxt)
        self.couleurLibelle.setCurrentText(self.ap.texte['couleur'])
        self.couleurLibelle.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurLibelle, 2, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Coordonnées du point annoté")
        layout = QGridLayout()
        
        self.pointer = QPushButton()
        self.pointer.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointer.setIconSize(QSize(12,12))
        self.pointer.setMaximumWidth(25)
        self.pointer.setAutoDefault(False)
        self.pointer.clicked.connect(self.pointage)
        layout.addWidget(self.pointer, 0, 0)
        
        label = QLabel("Profil :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.profils = QComboBox()
        
        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profils.addItem(zprofil.intitule)
    
        layout.addWidget(self.profils, 0, 2)
        
        label = QLabel("Abscisse :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.abscisse = QDoubleSpinBox()
        self.abscisse.setMaximumWidth(90)
        self.abscisse.setSuffix(" m")
        self.abscisse.setLocale(QLocale('English'))
        self.abscisse.setRange(-99999.999, 99999.999)
        self.abscisse.setDecimals(3)
        self.abscisse.setSingleStep(0.1)
        self.abscisse.setValue(self.ap.abscisse)
        self.abscisse.valueChanged.connect(self.appliquer)
        layout.addWidget(self.abscisse, 1, 1)
        
        self.interpAbscisse = QPushButton("x, z = f(x)")
        self.interpAbscisse.setToolTip("Résolution de l'abscisse")
        self.interpAbscisse.setAutoDefault(False)
        self.interpAbscisse.clicked.connect(self.resoudreAbscisse)
        layout.addWidget(self.interpAbscisse, 1, 2)

        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.altitude = QDoubleSpinBox()
        self.altitude.setMaximumWidth(90)
        self.altitude.setSuffix(" m")
        self.altitude.setLocale(QLocale('English'))
        self.altitude.setRange(-99999.999, 99999.999)
        self.altitude.setDecimals(3)
        self.altitude.setSingleStep(0.1)
        self.altitude.setValue(self.ap.altitude)
        self.altitude.valueChanged.connect(self.appliquer)
        layout.addWidget(self.altitude, 2, 1)

        self.interpAltitude = QPushButton("z = f(x)")
        self.interpAltitude.setToolTip("Interpoler l'altitude")
        self.interpAltitude.setAutoDefault(False)
        self.interpAltitude.clicked.connect(self.interpolerAltitude)
        layout.addWidget(self.interpAltitude, 2, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Flèche annotative")
        layout = QGridLayout()
        
        label = QLabel("Style de flèche :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.styleFleche = QComboBox()
        self.styleFleche.addItem("-")
        self.styleFleche.addItem("->")
        self.styleFleche.addItem("-|>")
        self.styleFleche.addItem("<-")
        self.styleFleche.addItem("<->")
        self.styleFleche.addItem("<|-")
        self.styleFleche.addItem("<|-|>")
        self.styleFleche.setCurrentText(self.ap.fleche['style de flèche'])
        self.styleFleche.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.styleFleche, 0, 1)
        
        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.styleLigne = QComboBox()
        self.styleLigne.insertItems(0, list(styles2ligne.keys()))
        self.styleLigne.setCurrentText(self.ap.fleche['style de ligne'])
        self.styleLigne.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.styleLigne, 1, 1)
        
        label = QLabel("Épaisseur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.epaisseur = QDoubleSpinBox()
        self.epaisseur.setMaximumWidth(50)
        self.epaisseur.setLocale(QLocale('English'))
        self.epaisseur.setRange(0, 99.9)
        self.epaisseur.setDecimals(1)
        self.epaisseur.setSingleStep(0.1)
        self.epaisseur.setValue(self.ap.fleche['épaisseur'])
        self.epaisseur.valueChanged.connect(self.appliquer)
        layout.addWidget(self.epaisseur, 2, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.couleurFleche = ColorsComboBox(self.pyLong.appctxt)
        self.couleurFleche.setCurrentText(self.ap.fleche['couleur'])
        self.couleurFleche.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurFleche, 3, 1)
        
        label = QLabel("Longueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.longueur = QDoubleSpinBox()
        self.longueur.setMaximumWidth(70)
        self.longueur.setLocale(QLocale('English'))
        self.longueur.setSuffix(" m")
        self.longueur.setRange(0, 9999.9)
        self.longueur.setDecimals(1)
        self.longueur.setSingleStep(0.1)
        self.longueur.setValue(self.ap.fleche['longueur'])
        self.longueur.valueChanged.connect(self.appliquer)
        layout.addWidget(self.longueur, 4, 1)
        
        label = QLabel("Décalage vert. :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.decalageFleche = QDoubleSpinBox()
        self.decalageFleche.setMaximumWidth(70)
        self.decalageFleche.setLocale(QLocale('English'))
        self.decalageFleche.setSuffix(" m")
        self.decalageFleche.setRange(0, 9999.9)
        self.decalageFleche.setDecimals(1)
        self.decalageFleche.setSingleStep(0.1)
        self.decalageFleche.setValue(self.ap.fleche['décalage'])
        self.decalageFleche.valueChanged.connect(self.appliquer)
        layout.addWidget(self.decalageFleche, 5, 1)
        
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
        self.opacite.setRange(0, 1)
        self.opacite.setDecimals(1)
        self.opacite.setSingleStep(0.1)
        self.opacite.setValue(self.ap.opacite)
        self.opacite.valueChanged.connect(self.appliquer)
        layout.addWidget(self.opacite, 0, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.ordre = QSpinBox()
        self.ordre.setMaximumWidth(45)
        self.ordre.setLocale(QLocale('English'))
        self.ordre.setRange(1, 99)
        self.ordre.setSingleStep(1)
        self.ordre.setValue(self.ap.ordre)
        self.ordre.valueChanged.connect(self.appliquer)
        layout.addWidget(self.ordre, 1, 1)
        
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
        self.ap.intitule = self.intitule.text()
        self.pyLong.listeAnnotations.updateListe()
        
    def appliquer(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass

        self.ap.libelle = self.libelle.text()
        self.ap.texte['taille'] = self.tailleLibelle.value()
        self.ap.texte['couleur'] = self.couleurLibelle.currentText()
        self.ap.abscisse = self.abscisse.value()
        self.ap.altitude = self.altitude.value()
        self.ap.fleche['style de flèche'] = self.styleFleche.currentText()
        self.ap.fleche['style de ligne'] = self.styleLigne.currentText()
        self.ap.fleche['épaisseur'] = self.epaisseur.value()
        self.ap.fleche['couleur'] = self.couleurFleche.currentText()
        self.ap.fleche['longueur'] = self.longueur.value()
        self.ap.fleche['décalage'] = self.decalageFleche.value()
        self.ap.opacite = self.opacite.value()
        self.ap.ordre = self.ordre.value()
        
        self.ap.update()
        
        self.pyLong.canvas.draw()
        
    def resoudreAbscisse(self):
        altitude = self.altitude.value()
        abscisse = self.abscisse.value()
        
        if self.profils.currentIndex() != -1:
            i = self.profils.currentIndex()
            zprofil, pprofil = self.pyLong.projet.profils[i]
        else:
            alerte = QMessageBox(self)
            alerte.setText("Aucun profil disponible.")
            alerte.exec_()
            return 0

        if altitude >= np.min(zprofil.altitudes) and altitude <= np.max(zprofil.altitudes):
            try:
                abscisse = zprofil.resoudre(altitude, abscisse)
                self.abscisse.setValue(abscisse)
            except:
                pass
        else:
            alerte = QMessageBox(self)
            alerte.setText("Altitude fournie incorrecte.")
            alerte.exec_()

        self.appliquer()                          
        
    def interpolerAltitude(self):
        abscisse = self.abscisse.value()
        
        if self.profils.currentIndex() != -1:
            i = self.profils.currentIndex()
            zprofil, pprofil = self.pyLong.projet.profils[i]
        else:
            alerte = QMessageBox(self)
            alerte.setText("Aucun profil disponible.")
            alerte.exec_()
            return 0
        
        if abscisse >= np.min(zprofil.abscisses) and abscisse <= np.max(zprofil.abscisses):
            altitude = zprofil.interpoler(abscisse)
            self.altitude.setValue(altitude)
        else:
            alerte = QMessageBox(self)
            alerte.setText("Abscisse fournie incorrecte.")
            alerte.exec_()
            
        self.appliquer()
        
    def pointage(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclick)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclick(self, event):
        try:
            self.abscisse.setValue(event.xdata)
            self.altitude.setValue(event.ydata)
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
