from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *

from pyLong.dictionnaires import *


class DialogOptionsDonnees(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
        
        i = self.pyLong.listeAutresDonnees.liste.currentRow()
        self.donnee = self.pyLong.projet.autresDonnees[i]

        mainLayout = QVBoxLayout()

        self.setWindowTitle("Options graphiques de la donnée \"{}\"".format(self.donnee.intitule))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/style.png')))

        layout = QHBoxLayout()

        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)

        self.intitule = QLineEdit()
        self.intitule.setText(self.donnee.intitule)
        self.intitule.textChanged.connect(self.updateIntitule)
        layout.addWidget(self.intitule)

        mainLayout.addLayout(layout)

        layout = QHBoxLayout()

        label = QLabel("Subplot : {}".format(self.donnee.subplot))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)

        layout.addWidget(QLabel())

        mainLayout.addLayout(layout)

        layout = QGridLayout()
        
        label = QLabel("Légende :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.legendeProfil = QLineEdit()
        self.legendeProfil.setText(self.donnee.legende)
        self.legendeProfil.textChanged.connect(self.updateLegende)
        layout.addWidget(self.legendeProfil, 1, 1)
        
        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.style2ligne = QComboBox()
        self.style2ligne.insertItems(0, list(styles2ligne.keys()))
        self.style2ligne.setCurrentText(self.donnee.ligne['style'])
        self.style2ligne.currentTextChanged.connect(self.updateStyle2ligne)
        layout.addWidget(self.style2ligne, 2, 1)
        
        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 3, 0)
        
        self.couleur2ligne = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligne.setCurrentText(self.donnee.ligne['couleur'])
        self.couleur2ligne.currentTextChanged.connect(self.updateCouleur2ligne)
        layout.addWidget(self.couleur2ligne, 3, 1)
        
        label = QLabel("Épaisseur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 4, 0)
        
        self.epaisseur2ligne = QDoubleSpinBox()
        self.epaisseur2ligne.setMaximumWidth(50)
        self.epaisseur2ligne.setLocale(QLocale('English'))
        self.epaisseur2ligne.setRange(0, 99.9)
        self.epaisseur2ligne.setDecimals(1)
        self.epaisseur2ligne.setSingleStep(0.1)
        self.epaisseur2ligne.setValue(self.donnee.ligne['épaisseur'])
        self.epaisseur2ligne.valueChanged.connect(self.updateEpaisseur2ligne)
        layout.addWidget(self.epaisseur2ligne, 4, 1)

        label = QLabel("Style de marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 5, 0)
        
        self.style2marqueur = QComboBox()
        self.style2marqueur.insertItems(0, list(styles2marqueur.keys()))
        self.style2marqueur.setCurrentText(self.donnee.marqueur['style'])
        self.style2marqueur.currentTextChanged.connect(self.updateStyle2marqueur)
        layout.addWidget(self.style2marqueur, 5, 1)
        
        label = QLabel("Couleur du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 6, 0)
        
        self.couleur2marqueur = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2marqueur.setCurrentText(self.donnee.marqueur['couleur'])
        self.couleur2marqueur.currentTextChanged.connect(self.updateCouleur2marqueur)
        layout.addWidget(self.couleur2marqueur, 6, 1)
        
        label = QLabel("Taille du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 7, 0)
        
        self.taille2marqueur = QDoubleSpinBox()
        self.taille2marqueur.setMaximumWidth(50)
        self.taille2marqueur.setLocale(QLocale('English'))
        self.taille2marqueur.setRange(0, 99.9)
        self.taille2marqueur.setSingleStep(0.1)
        self.taille2marqueur.setDecimals(1)
        self.taille2marqueur.setValue(self.donnee.marqueur['taille'])
        self.taille2marqueur.valueChanged.connect(self.updateTaille2marqueur)
        layout.addWidget(self.taille2marqueur, 7, 1)
        
        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 8, 0)
        
        self.opacite = QDoubleSpinBox()
        self.opacite.setFixedWidth(45)
        self.opacite.setLocale(QLocale('English'))
        self.opacite.setRange(0, 1)
        self.opacite.setDecimals(1)
        self.opacite.setSingleStep(0.1)
        self.opacite.setValue(self.donnee.opacite)
        self.opacite.valueChanged.connect(self.updateOpacite)
        layout.addWidget(self.opacite, 8, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 9, 0)
        
        self.ordre = QSpinBox()
        self.ordre.setFixedWidth(45)
        self.ordre.setRange(0, 99)
        self.ordre.setValue(self.donnee.ordre)
        self.ordre.valueChanged.connect(self.updateOrdre)
        layout.addWidget(self.ordre, 9, 1)

        mainLayout.addLayout(layout)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def updateIntitule(self, value):
        self.donnee.intitule = value
        self.setWindowTitle("Options graphiques de la donnée \"{}\"".format(value))
        self.pyLong.listeAutresDonnees.update()

    def updateLegende(self, value):
        self.donnee.legende = value
        self.donnee.line.set_label(value)

        self.pyLong.canvas.updateLegendes()

    def updateStyle2ligne(self, value):
        self.donnee.ligne['style'] = value
        self.donnee.line.set_linestyle(styles2ligne[value])
        self.pyLong.canvas.updateLegendes()

    def updateCouleur2ligne(self, value):
        self.donnee.ligne['couleur'] = value
        self.donnee.line.set_color(couleurs[value])
        self.pyLong.canvas.updateLegendes()

    def updateEpaisseur2ligne(self, value):
        self.donnee.ligne['épaisseur'] = value
        self.donnee.line.set_linewidth(value)
        self.pyLong.canvas.updateLegendes()

    def updateStyle2marqueur(self, value):
        self.donnee.marqueur['style'] = value
        self.donnee.line.set_marker(styles2marqueur[value])
        self.pyLong.canvas.updateLegendes()

    def updateCouleur2marqueur(self, value):
        self.donnee.marqueur['couleur'] = value
        self.donnee.line.set_markeredgecolor(couleurs[value])
        self.donnee.line.set_markerfacecolor(couleurs[value])
        self.pyLong.canvas.updateLegendes()

    def updateTaille2marqueur(self, value):
        self.donnee.marqueur['taille'] = value
        self.donnee.line.set_markersize(value)
        self.pyLong.canvas.updateLegendes()

    def updateOpacite(self, value):
        self.donnee.opacite = value
        self.donnee.line.set_alpha(value)
        self.pyLong.canvas.updateLegendes()

    def updateOrdre(self, value):
        self.donnee.ordre = value
        self.donnee.line.set_zorder(value)
        self.pyLong.canvas.updateLegendes()
