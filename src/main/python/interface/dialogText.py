from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *


class DialogText(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        self.pyLong = parent
    
        i = self.pyLong.listeAnnotations.groupes.currentIndex()
        j = self.pyLong.listeAnnotations.liste.currentRow()
        self.txt = self.pyLong.projet.groupes[i].annotations[j]
        
        self.setWindowTitle("Texte")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/texte.png')))
 
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.txt.intitule)
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
        self.libelle.setText(self.txt.libelle)
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
        self.taille.setValue(self.txt.texte['taille'])
        self.taille.valueChanged.connect(self.appliquer)
        layout.addWidget(self.taille, 1, 1)
        
        label = QLabel("Couleur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.couleur = ColorsComboBox(self.pyLong.appctxt)
        self.couleur.setCurrentText(self.txt.texte['couleur'])
        self.couleur.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.couleur, 2, 1)
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.style = QComboBox()
        self.style.addItems(['normal', 'italic'])
        self.style.setCurrentText(self.txt.texte['style'])
        self.style.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.style, 3, 1)

        label = QLabel("Épaisseur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.epaisseur = QComboBox()
        self.epaisseur.addItems(['normal',
                                  'bold'])
        self.epaisseur.setCurrentText(self.txt.texte['épaisseur'])
        self.epaisseur.currentTextChanged.connect(self.appliquer)
        layout.addWidget(self.epaisseur, 4, 1)
        
        label = QLabel("Rotation :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.rotation = QDoubleSpinBox()
        self.rotation.setMaximumWidth(65)
        self.rotation.setLocale(QLocale('English'))
        self.rotation.setSuffix(" °")
        self.rotation.setRange(-180,180)
        self.rotation.setSingleStep(0.1)
        self.rotation.setDecimals(1)
        self.rotation.setValue(self.txt.texte['rotation'])
        self.rotation.valueChanged.connect(self.appliquer)
        layout.addWidget(self.rotation, 5, 1)       
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        groupe = QGroupBox("Coordonnées du coin inférieur gauche")
        layout = QGridLayout()
        
        self.pointer = QPushButton()
        # self.pointer.setMaximumWidth(50)
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
        self.abscisse.setValue(self.txt.abscisse)
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
        self.altitude.setValue(self.txt.altitude)
        self.altitude.valueChanged.connect(self.appliquer)
        layout.addWidget(self.altitude, 1, 2)
        
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
        self.opacite.setValue(self.txt.opacite)
        self.opacite.valueChanged.connect(self.appliquer)
        layout.addWidget(self.opacite, 0, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.ordre = QSpinBox()
        self.ordre.setMaximumWidth(45)
        self.ordre.setLocale(QLocale('English'))
        self.ordre.setRange(1,99)
        self.ordre.setSingleStep(1)
        self.ordre.setValue(self.txt.ordre)
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
        self.txt.intitule = self.intitule.text()
        self.pyLong.listeAnnotations.updateListe()
        
    def appliquer(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass

        self.txt.libelle = self.libelle.text()
        self.txt.texte['taille'] = self.taille.value()
        self.txt.texte['couleur'] = self.couleur.currentText()
        self.txt.texte['style'] = self.style.currentText()
        self.txt.texte['épaisseur'] = self.epaisseur.currentText()
        self.txt.texte['rotation'] = self.rotation.value()
        self.txt.abscisse = self.abscisse.value()
        self.txt.altitude = self.altitude.value()
        self.txt.opacite = self.opacite.value()
        self.txt.ordre = self.ordre.value()
        
        self.txt.update()
        
        self.pyLong.canvas.draw()
        
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
