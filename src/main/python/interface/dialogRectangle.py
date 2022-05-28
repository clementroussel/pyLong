from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *


class DialogRectangle(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        self.pyLong = parent

        i = self.pyLong.listeAnnotations.groupes.currentIndex()
        j = self.pyLong.listeAnnotations.liste.currentRow()
        self.rect = self.pyLong.projet.groupes[i].annotations[j]
        
        self.setWindowTitle("Rectangle")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rectangle.png')))
        
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.rect.intitule)
        self.intitule.textChanged.connect(self.updateIntitule)
        layout.addWidget(self.intitule)  
    
        mainLayout.addLayout(layout)
        
        groupe = QGroupBox("Légende")
        layout = QVBoxLayout()
        
        self.legende = QLineEdit()
        self.legende.setText(self.rect.legende)
        self.legende.textEdited.connect(self.appliquer)
        layout.addWidget(self.legende)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Coordonnées du somment inférieur gauche")
        layout = QGridLayout()
        
        self.pointer = QPushButton()
        self.pointer.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/cible.png')))
        self.pointer.setIconSize(QSize(12,12))
        self.pointer.setMaximumWidth(25)
        self.pointer.setAutoDefault(False)
        self.pointer.clicked.connect(self.pointage)
        layout.addWidget(self.pointer, 0, 0, 2, 1)
        
        label = QLabel("Abscisse :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.abscisse = QDoubleSpinBox()
        self.abscisse.setMaximumWidth(90)
        self.abscisse.setSuffix(" m")
        self.abscisse.setLocale(QLocale('English'))
        self.abscisse.setRange(-99999.999, 99999.999)
        self.abscisse.setDecimals(3)
        self.abscisse.setSingleStep(0.1)
        self.abscisse.setValue(self.rect.abscisse)
        self.abscisse.valueChanged.connect(self.appliquer)
        layout.addWidget(self.abscisse, 0, 2)
        
        label = QLabel("Altitude :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 1)
        
        self.altitude = QDoubleSpinBox()
        self.altitude.setMaximumWidth(90)
        self.altitude.setSuffix(" m")
        self.altitude.setLocale(QLocale('English'))
        self.altitude.setRange(-99999.999, 99999.999)
        self.altitude.setDecimals(3)
        self.altitude.setSingleStep(0.1)
        self.altitude.setValue(self.rect.altitude)
        self.altitude.valueChanged.connect(self.appliquer)
        layout.addWidget(self.altitude, 1, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Dimensions")
        layout = QGridLayout()
        
        label = QLabel("Largeur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.largeur = QDoubleSpinBox()
        self.largeur.setMaximumWidth(90)
        self.largeur.setSuffix(" m")
        self.largeur.setLocale(QLocale('English'))
        self.largeur.setRange(0, 99999.999)
        self.largeur.setDecimals(3)
        self.largeur.setSingleStep(0.1)
        self.largeur.setValue(self.rect.largeur)
        self.largeur.valueChanged.connect(self.appliquer)
        layout.addWidget(self.largeur, 0, 1)
        
        label = QLabel("Hauteur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.hauteur = QDoubleSpinBox()
        self.hauteur.setMaximumWidth(90)
        self.hauteur.setSuffix(" m")
        self.hauteur.setLocale(QLocale('English'))
        self.hauteur.setRange(0, 99999.999)
        self.hauteur.setDecimals(3)
        self.hauteur.setSingleStep(0.1)
        self.hauteur.setValue(self.rect.hauteur)
        self.hauteur.valueChanged.connect(self.appliquer)
        layout.addWidget(self.hauteur, 1, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Contour")
        layout = QGridLayout()
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.style2ligne = QComboBox()
        self.style2ligne.insertItems(0, list(styles2ligne.keys()))
        self.style2ligne.setCurrentText(self.rect.contour['style de ligne'])
        self.style2ligne.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.style2ligne, 0, 1)
        
        label = QLabel("Épaisseur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.epaisseur = QDoubleSpinBox()
        self.epaisseur.setMaximumWidth(50)
        self.epaisseur.setLocale(QLocale('English'))
        self.epaisseur.setRange(0, 99.9)
        self.epaisseur.setDecimals(1)
        self.epaisseur.setSingleStep(0.1)
        self.epaisseur.setValue(self.rect.contour['épaisseur'])
        self.epaisseur.valueChanged.connect(self.appliquer)
        layout.addWidget(self.epaisseur, 1, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.couleurContour = ColorsComboBox(self.pyLong.appctxt)
        self.couleurContour.setCurrentText(self.rect.contour['couleur'])
        self.couleurContour.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurContour, 2, 1)        
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Remplissage")
        layout = QGridLayout()

        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)        
        layout.addWidget(label, 0, 0)

        self.couleurRemplissage = ColorsComboBox(self.pyLong.appctxt)
        self.couleurRemplissage.setCurrentText(self.rect.remplissage['couleur'])
        self.couleurRemplissage.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleurRemplissage, 0, 1) 
        
        label = QLabel("Style de hachure :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.style2hachure = QComboBox()
        self.style2hachure.addItem('/')
        self.style2hachure.addItem('\\')
        self.style2hachure.addItem('|')
        self.style2hachure.addItem('-')
        self.style2hachure.addItem('+')
        self.style2hachure.addItem('x')
        self.style2hachure.addItem('o')
        self.style2hachure.addItem('O')
        self.style2hachure.addItem('.')
        self.style2hachure.addItem('*')
        self.style2hachure.addItem('')
        self.style2hachure.setCurrentText(self.rect.remplissage['style de hachure'])
        self.style2hachure.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.style2hachure, 1, 1)

        label = QLabel("Densité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.densite = QSpinBox()
        self.densite.setMaximumWidth(45)
        self.densite.setRange(1, 99)
        self.densite.setValue(self.rect.remplissage['densité'])
        self.densite.valueChanged.connect(self.appliquer)
        layout.addWidget(self.densite, 2, 1)               
        
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
        self.opacite.setValue(self.rect.opacite)
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
        self.ordre.setValue(self.rect.ordre)
        self.ordre.valueChanged.connect(self.appliquer)
        layout.addWidget(self.ordre, 0, 3)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Apply).setText("Actualiser")
        buttonBox.button(QDialogButtonBox.Apply).setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rafraichir.png')))
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.actualiser)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

    def actualiser(self):
        self.pyLong.canvas.dessiner()
        
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
        self.rect.intitule = self.intitule.text()
        self.pyLong.listeAnnotations.updateListe()
        
    def appliquer(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.rect.legende = self.legende.text()
        
        self.rect.abscisse = self.abscisse.value()
        self.rect.altitude = self.altitude.value()
        
        self.rect.largeur = self.largeur.value()
        self.rect.hauteur = self.hauteur.value()
        
        self.rect.contour['style de ligne'] = self.style2ligne.currentText()
        self.rect.contour['épaisseur'] = self.epaisseur.value()
        self.rect.contour['couleur'] = self.couleurContour.currentText()
        
        self.rect.remplissage['style de hachure'] = self.style2hachure.currentText()
        self.rect.remplissage['couleur'] = self.couleurRemplissage.currentText()
        self.rect.remplissage['densité'] = self.densite.value()
        
        self.rect.opacite = self.opacite.value()
        self.rect.ordre = self.ordre.value()
        
        self.rect.update()

        self.pyLong.canvas.updateLegendes()
        # self.pyLong.canvas.draw()
        
    def pointage(self):
        self.pyLong.controleOutilsNavigation()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclick)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        # self.setCursor(QCursor(Qt.PointingHandCursor))
        
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