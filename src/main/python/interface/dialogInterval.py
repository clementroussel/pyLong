from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.dictionnaires import *

from ColorsComboBox import *


class DialogZone(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        self.setModal(False)
        
        self.pyLong = parent

        i = self.pyLong.listeAnnotations.groupes.currentIndex()
        j = self.pyLong.listeAnnotations.liste.currentRow()
        self.zone = self.pyLong.projet.groupes[i].annotations[j]
        
        self.setWindowTitle("Zone")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/zone.png')))
        
        mainLayout = QGridLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.zone.intitule)
        self.intitule.textChanged.connect(self.updateIntitule)
        layout.addWidget(self.intitule)  
        
        mainLayout.addLayout(layout, 0, 0, 1, 2)
        
        groupe = QGroupBox("Texte à afficher")
        layout = QGridLayout()
        
        label = QLabel("Libellé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.libelle = QLineEdit()
        self.libelle.setMaxLength(50)
        self.libelle.setText(self.zone.libelle)
        self.libelle.textEdited.connect(self.appliquer)
        layout.addWidget(self.libelle, 0, 1)
        
        label = QLabel("Taille :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.taille = QDoubleSpinBox()
        self.taille.setMaximumWidth(50)
        self.taille.setLocale(QLocale('English'))
        self.taille.setRange(0, 99.9)
        self.taille.setDecimals(1)
        self.taille.setSingleStep(0.1)
        self.taille.setValue(self.zone.texte['taille'])
        self.taille.valueChanged.connect(self.appliquer)
        layout.addWidget(self.taille, 1, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.couleur = ColorsComboBox(self.pyLong.appctxt)
        self.couleur.setCurrentText(self.zone.texte['couleur'])
        self.couleur.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleur, 2, 1)
        
        sublayout = QHBoxLayout()
        
        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label)
        
        self.altitudeLibelle = QDoubleSpinBox()
        self.altitudeLibelle.setMaximumWidth(90)
        self.altitudeLibelle.setSuffix(" m")
        self.altitudeLibelle.setLocale(QLocale('English'))
        self.altitudeLibelle.setRange(0, 99999.999)
        self.altitudeLibelle.setDecimals(3)
        self.altitudeLibelle.setSingleStep(0.1)
        self.altitudeLibelle.setValue(self.zone.texte['altitude'])
        self.altitudeLibelle.valueChanged.connect(self.appliquer)
        sublayout.addWidget(self.altitudeLibelle)
        
        self.pointerAltitude = QPushButton()
        self.pointerAltitude.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointerAltitude.setIconSize(QSize(12,12))
        self.pointerAltitude.setMaximumWidth(25)
        self.pointerAltitude.setAutoDefault(False)
        self.pointerAltitude.clicked.connect(self.pointageAltitude)
        sublayout.addWidget(self.pointerAltitude)
        
        layout.addLayout(sublayout, 3, 0, 1, 3)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 1, 0)
        
        groupe = QGroupBox("Encadrement du texte")
        layout = QGridLayout()
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.styleCadre = QComboBox()
        self.styleCadre.insertItems(0,list(styles2ligne.keys()))
        self.styleCadre.setCurrentText(self.zone.cadre['style'])
        self.styleCadre.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.styleCadre, 0, 1)
        
        label = QLabel("Épaisseur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.epaisseurCadre = QDoubleSpinBox()
        self.epaisseurCadre.setMaximumWidth(50)
        self.epaisseurCadre.setLocale(QLocale('English'))
        self.epaisseurCadre.setRange(0, 99.9)
        self.epaisseurCadre.setDecimals(1)
        self.epaisseurCadre.setSingleStep(0.1)
        self.epaisseurCadre.setValue(self.zone.cadre['épaisseur'])
        self.epaisseurCadre.valueChanged.connect(self.appliquer)
        layout.addWidget(self.epaisseurCadre, 1, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.couleurCadre = ColorsComboBox(self.pyLong.appctxt)
        self.couleurCadre.setCurrentText(self.zone.cadre['couleur'])
        self.couleurCadre.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurCadre, 2, 1)
        
        layout.addWidget(QWidget(), 3, 0)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 1, 1)
        
        groupe = QGroupBox("Début de la zone")
        layout = QGridLayout()
        
        self.pointerDebut = QPushButton()
        self.pointerDebut.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointerDebut.setIconSize(QSize(12,12))
        self.pointerDebut.setMaximumWidth(25)
        self.pointerDebut.setAutoDefault(False)
        self.pointerDebut.clicked.connect(self.pointageDebut)
        layout.addWidget(self.pointerDebut, 0, 0)
        
        label = QLabel("Profil :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.profilsDebut = QComboBox()
        
        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profilsDebut.addItem(zprofil.intitule)
            
        layout.addWidget(self.profilsDebut, 0, 2)
        
        label = QLabel("Abscisse :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.abscisseDebut = QDoubleSpinBox()
        self.abscisseDebut.setMaximumWidth(90)
        self.abscisseDebut.setSuffix(" m")
        self.abscisseDebut.setLocale(QLocale('English'))
        self.abscisseDebut.setRange(0, 99999.999)
        self.abscisseDebut.setDecimals(3)
        self.abscisseDebut.setSingleStep(0.1)
        self.abscisseDebut.setValue(self.zone.zone['abscisse de début'])
        self.abscisseDebut.valueChanged.connect(self.appliquer)
        layout.addWidget(self.abscisseDebut, 1, 1)
        
        self.interpAbscisseDebut = QPushButton("x, z = f(x)")
        self.interpAbscisseDebut.setToolTip("Résolution de l'abscisse")
        self.interpAbscisseDebut.setAutoDefault(False)
        self.interpAbscisseDebut.clicked.connect(lambda : self.resoudreAbscisse('début'))
        layout.addWidget(self.interpAbscisseDebut, 1, 2)
        
        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.altitudeDebut = QDoubleSpinBox()
        self.altitudeDebut.setMaximumWidth(90)
        self.altitudeDebut.setSuffix(" m")
        self.altitudeDebut.setLocale(QLocale('English'))
        self.altitudeDebut.setRange(0, 99999.999)
        self.altitudeDebut.setDecimals(3)
        self.altitudeDebut.setSingleStep(0.1)
        self.altitudeDebut.setValue(self.zone.zone['altitude de début'])
        self.altitudeDebut.valueChanged.connect(self.appliquer)
        layout.addWidget(self.altitudeDebut, 2, 1)
        
        self.interpAltitudeDebut = QPushButton("z = f(x)")
        self.interpAltitudeDebut.setToolTip("Interpoler l'altitude")
        self.interpAltitudeDebut.setAutoDefault(False)
        self.interpAltitudeDebut.clicked.connect(lambda : self.interpolerAltitude('début'))
        layout.addWidget(self.interpAltitudeDebut, 2, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 2, 0)
        
        groupe = QGroupBox("Fin de la zone")
        layout = QGridLayout()
        
        self.pointerFin = QPushButton()
        self.pointerFin.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointerFin.setIconSize(QSize(12,12))
        self.pointerFin.setMaximumWidth(25)
        self.pointerFin.setAutoDefault(False)
        self.pointerFin.clicked.connect(self.pointageFin)
        layout.addWidget(self.pointerFin, 0, 0)
        
        label = QLabel("Profil :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.profilsFin = QComboBox()

        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profilsFin.addItem(zprofil.intitule)
            
        layout.addWidget(self.profilsFin, 0, 2)
        
        label = QLabel("Abscisse :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.abscisseFin = QDoubleSpinBox()
        self.abscisseFin.setMaximumWidth(90)
        self.abscisseFin.setSuffix(" m")
        self.abscisseFin.setLocale(QLocale('English'))
        self.abscisseFin.setRange(0, 99999.999)
        self.abscisseFin.setDecimals(3)
        self.abscisseFin.setSingleStep(0.1)
        self.abscisseFin.setValue(self.zone.zone['abscisse de fin'])
        self.abscisseFin.valueChanged.connect(self.appliquer)
        layout.addWidget(self.abscisseFin, 1, 1)
        
        self.interpAbscisseFin = QPushButton("x, z = f(x)")
        self.interpAbscisseFin.setToolTip("Résolution de l'abscisse")
        self.interpAbscisseFin.setAutoDefault(False)
        self.interpAbscisseFin.clicked.connect(lambda : self.resoudreAbscisse('fin'))
        layout.addWidget(self.interpAbscisseFin, 1, 2)

        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.altitudeFin = QDoubleSpinBox()
        self.altitudeFin.setMaximumWidth(90)
        self.altitudeFin.setSuffix(" m")
        self.altitudeFin.setLocale(QLocale('English'))
        self.altitudeFin.setRange(0, 99999.999)
        self.altitudeFin.setDecimals(3)
        self.altitudeFin.setSingleStep(0.1)
        self.altitudeFin.setValue(self.zone.zone['altitude de fin'])
        self.altitudeFin.valueChanged.connect(self.appliquer)
        layout.addWidget(self.altitudeFin, 2, 1)
        
        self.interpAltitudeFin = QPushButton("z = f(x)")
        self.interpAltitudeFin.setToolTip("Interpoler l'altitude")
        self.interpAltitudeFin.setAutoDefault(False)
        self.interpAltitudeFin.clicked.connect(lambda : self.interpolerAltitude('fin'))
        layout.addWidget(self.interpAltitudeFin, 2, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 2, 1)
        
        groupe = QGroupBox("Lignes de délimitation")
        layout = QGridLayout()
        
        label = QLabel("Altitude basse :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0) 
        
        self.altitudeBasse = QDoubleSpinBox()
        self.altitudeBasse.setMaximumWidth(90)
        self.altitudeBasse.setSuffix(" m")
        self.altitudeBasse.setLocale(QLocale('English'))
        self.altitudeBasse.setRange(-9999, 99999.999)
        self.altitudeBasse.setDecimals(3)
        self.altitudeBasse.setSingleStep(0.1)
        self.altitudeBasse.setValue(self.zone.zone['altitude basse'])
        self.altitudeBasse.valueChanged.connect(self.appliquer)
        layout.addWidget(self.altitudeBasse, 0, 1)
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.styleLigne = QComboBox()
        self.styleLigne.insertItems(0, list(styles2ligne.keys()))
        self.styleLigne.setCurrentText(self.zone.limites['style'])
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
        self.epaisseur.setValue(self.zone.limites['épaisseur'])
        self.epaisseur.valueChanged.connect(self.appliquer)
        layout.addWidget(self.epaisseur, 2, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.couleurLigne = ColorsComboBox(self.pyLong.appctxt)
        self.couleurLigne.setCurrentText(self.zone.limites['couleur'])
        self.couleurLigne.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurLigne, 3, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 3, 0)
        
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
        self.opacite.setValue(self.zone.opacite)
        self.opacite.valueChanged.connect(self.appliquer)
        layout.addWidget(self.opacite, 0, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 2)
        
        self.ordre = QSpinBox()
        self.ordre.setMaximumWidth(45)
        self.ordre.setLocale(QLocale('English'))
        self.ordre.setRange(1, 99)
        self.ordre.setSingleStep(1)
        self.ordre.setValue(self.zone.ordre)
        self.ordre.valueChanged.connect(self.appliquer)
        layout.addWidget(self.ordre, 0, 3)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 4, 0)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
    
        mainLayout.addWidget(buttonBox, 5, 0, 1, 2)
        
        self.setLayout(mainLayout)
        
    def resoudreAbscisse(self, lieu):
        if lieu == 'début':
            
            if self.profilsDebut.currentIndex() != -1:
                i = self.profilsDebut.currentIndex()
                zprofil, pprofil = self.pyLong.projet.profils[i]
            else:
                alerte = QMessageBox(self)
                alerte.setText("Renseignez un profil.")
                alerte.exec_()
                return 0
            
            abscisse = self.abscisseDebut.value()
            altitude = self.altitudeDebut.value()
            if altitude >= np.min(zprofil.altitudes) and altitude <= np.max(zprofil.altitudes):
                try:
                    abscisse = zprofil.resoudre(altitude, abscisse)
                    self.abscisseDebut.setValue(abscisse)
                except:
                    pass
            else:
                alerte = QMessageBox(self)
                alerte.setText("Altitude fournie incorrecte.")
                alerte.exec_()
                 
        else:
            
            if self.profilsFin.currentIndex() != -1:
                i = self.profilsFin.currentIndex()
                zprofil, pprofil = self.pyLong.projet.profils[i]
            else:
                alerte = QMessageBox(self)
                alerte.setText("Renseignez un profil.")
                alerte.exec_()
                return 0
            
            abscisse = self.abscisseFin.value()
            altitude = self.altitudeFin.value()
            if altitude >= np.min(zprofil.altitudes) and altitude <= np.max(zprofil.altitudes):
                try:
                    abscisse = zprofil.resoudre(altitude, abscisse)
                    self.abscisseFin.setValue(abscisse)
                except:
                    pass
            else:
                alerte = QMessageBox(self)
                alerte.setText("Altitude fournie incorrecte.")
                alerte.exec_()  
                
        self.appliquer()
        
    def interpolerAltitude(self, lieu):
        if lieu == 'début':
            if self.profilsDebut.currentIndex() != -1:
                i = self.profilsDebut.currentIndex()
                zprofil, pprofil = self.pyLong.projet.profils[i]
            else:
                alerte = QMessageBox(self)
                alerte.setText("Renseignez un profil.")
                alerte.exec_()
                return 0
            
            abscisse = self.abscisseDebut.value()
            if abscisse >= np.min(zprofil.abscisses) and abscisse <= np.max(zprofil.abscisses):
                altitude = zprofil.interpoler(abscisse)
                self.altitudeDebut.setValue(altitude)
            else:
                alerte = QMessageBox(self)
                alerte.setText("Abscisse fournie incorrecte.")
                alerte.exec_()
                 
        else:
            if self.profilsFin.currentIndex() != -1:
                i = self.profilsFin.currentIndex()
                zprofil, pprofil = self.pyLong.projet.profils[i]
            else:
                alerte = QMessageBox(self)
                alerte.setText("Renseignez un profil.")
                alerte.ex
            
            abscisse = self.abscisseFin.value()
            if abscisse >= np.min(zprofil.abscisses) and abscisse <= np.max(zprofil.abscisses):
                altitude = zprofil.interpoler(abscisse)
                self.altitudeFin.setValue(altitude)
            else:
                alerte = QMessageBox(self)
                alerte.setText("Abscisse fournie incorrecte.")
                alerte.exec_()  
                
        self.appliquer()
        
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
        self.zone.intitule = self.intitule.text()
        self.pyLong.listeAnnotations.updateListe()
        
    def appliquer(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.zone.libelle = self.libelle.text()
        self.zone.texte['altitude'] = self.altitudeLibelle.value()
        self.zone.texte['taille'] = self.taille.value()
        self.zone.texte['couleur'] = self.couleur.currentText()
        
        self.zone.cadre['style'] = self.styleCadre.currentText()
        self.zone.cadre['épaisseur'] = self.epaisseurCadre.value()
        self.zone.cadre['couleur'] = self.couleurCadre.currentText()
        
        self.zone.zone['abscisse de début'] = self.abscisseDebut.value()
        self.zone.zone['altitude de début'] = self.altitudeDebut.value()
        
        self.zone.zone['abscisse de fin'] = self.abscisseFin.value()
        self.zone.zone['altitude de fin'] = self.altitudeFin.value()
        
        self.zone.zone['altitude basse'] = self.altitudeBasse.value()
        
        self.zone.limites['style'] = self.styleLigne.currentText()
        self.zone.limites['couleur'] = self.couleurLigne.currentText()
        self.zone.limites['épaisseur'] = self.epaisseur.value()
        
        self.zone.opacite = self.opacite.value()
        self.zone.ordre = self.ordre.value()
        
        self.zone.update()
        
        self.pyLong.canvas.draw()
        
    def pointageAltitude(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickAltitude)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickAltitude(self, event):
        try:
            self.altitudeLibelle.setValue(event.ydata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.appliquer()
        
    def pointageDebut(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickDebut)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickDebut(self, event):
        try:
            self.abscisseDebut.setValue(event.xdata)
            self.altitudeDebut.setValue(event.ydata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.appliquer()
        
    def pointageFin(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclickFin)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclickFin(self, event):
        try:
            self.abscisseFin.setValue(event.xdata)
            self.altitudeFin.setValue(event.ydata)
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
