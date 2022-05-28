from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *

from pyLong.dictionnaires import *


class DialogOptionsProfils(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
        
        i = self.pyLong.listeLayouts.currentIndex()
        self.axeSecondaire = self.pyLong.projet.layouts[i].axeSecondaire
        
        i = self.pyLong.listeProfils.liste.currentRow()
        self.zprofil, self.pprofil = self.pyLong.projet.profils[i]
        
        self.setWindowTitle("Propriétés graphiques du profil \"{}\"".format(self.zprofil.intitule))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/style.png')))
        
        self.symbolePente = self.pyLong.projet.preferences['pente']
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.zprofil.intitule)
        self.intitule.textChanged.connect(self.update_intituleProfil)
            
        tableWidget = QTabWidget()
        onglet_zprofil = QWidget()
        onglet_pprofil = QWidget()
        
        tableWidget.addTab(onglet_zprofil, "profil en long")
        tableWidget.addTab(onglet_pprofil, "pentes")
        
        # onglet profil en long
        layout = QGridLayout()

        self.tracerProfil = QCheckBox("Dessiner le profil en long")
        self.tracerProfil.setChecked(self.zprofil.visible)
        self.tracerProfil.stateChanged.connect(self.update_visibiliteProfil)
        layout.addWidget(self.tracerProfil, 0, 0, 1, 2)
        
        label = QLabel("Légende :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.legendeProfil = QLineEdit()
        self.legendeProfil.setText(self.zprofil.legende)
        self.legendeProfil.textChanged.connect(self.update_legendeProfil)
        layout.addWidget(self.legendeProfil, 1, 1)
        
        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.style2ligneProfil = QComboBox()
        self.style2ligneProfil.insertItems(0, list(styles2ligne.keys()))
        self.style2ligneProfil.setCurrentText(self.zprofil.ligne['style'])
        self.style2ligneProfil.currentTextChanged.connect(self.update_style2ligneProfil)
        layout.addWidget(self.style2ligneProfil, 2, 1)
        
        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 3, 0)
        
        self.couleur2ligneProfil = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligneProfil.setCurrentText(self.zprofil.ligne['couleur'])
        self.couleur2ligneProfil.currentTextChanged.connect(self.update_couleur2ligneProfil)
        layout.addWidget(self.couleur2ligneProfil, 3, 1)
        
        label = QLabel("Épaisseur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 4, 0)
        
        self.epaisseur2ligneProfil = QDoubleSpinBox()
        self.epaisseur2ligneProfil.setMaximumWidth(50)
        self.epaisseur2ligneProfil.setLocale(QLocale('English'))
        self.epaisseur2ligneProfil.setRange(0, 99.9)
        self.epaisseur2ligneProfil.setDecimals(1)
        self.epaisseur2ligneProfil.setSingleStep(0.1)
        self.epaisseur2ligneProfil.setValue(self.zprofil.ligne['épaisseur'])
        self.epaisseur2ligneProfil.valueChanged.connect(self.update_epaisseur2ligneProfil)
        layout.addWidget(self.epaisseur2ligneProfil, 4, 1)

        label = QLabel("Style de marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 5, 0)
        
        self.style2marqueurProfil = QComboBox()
        self.style2marqueurProfil.insertItems(0, list(styles2marqueur.keys()))
        self.style2marqueurProfil.setCurrentText(self.zprofil.marqueur['style'])
        self.style2marqueurProfil.currentTextChanged.connect(self.update_style2marqueurProfil)
        layout.addWidget(self.style2marqueurProfil, 5, 1)
        
        label = QLabel("Couleur du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 6, 0)
        
        self.couleur2marqueurProfil = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2marqueurProfil.setCurrentText(self.zprofil.marqueur['couleur'])
        self.couleur2marqueurProfil.currentTextChanged.connect(self.update_couleur2marqueurProfil)
        layout.addWidget(self.couleur2marqueurProfil, 6, 1)
        
        label = QLabel("Taille du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 7, 0)
        
        self.taille2marqueurProfil = QDoubleSpinBox()
        self.taille2marqueurProfil.setMaximumWidth(50)
        self.taille2marqueurProfil.setLocale(QLocale('English'))
        self.taille2marqueurProfil.setRange(0, 99.9)
        self.taille2marqueurProfil.setSingleStep(0.1)
        self.taille2marqueurProfil.setDecimals(1)
        self.taille2marqueurProfil.setValue(self.zprofil.marqueur['taille'])
        self.taille2marqueurProfil.valueChanged.connect(self.update_taille2marqueurProfil)
        layout.addWidget(self.taille2marqueurProfil, 7, 1)
        
        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 8, 0)
        
        self.opaciteProfil = QDoubleSpinBox()
        self.opaciteProfil.setFixedWidth(45)
        self.opaciteProfil.setLocale(QLocale('English'))
        self.opaciteProfil.setRange(0, 1)
        self.opaciteProfil.setDecimals(1)
        self.opaciteProfil.setSingleStep(0.1)
        self.opaciteProfil.setValue(self.zprofil.opacite)
        self.opaciteProfil.valueChanged.connect(self.update_opaciteProfil)
        layout.addWidget(self.opaciteProfil, 8, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 9, 0)
        
        self.ordreProfil = QSpinBox()
        self.ordreProfil.setFixedWidth(45)
        self.ordreProfil.setRange(0, 99)
        self.ordreProfil.setValue(self.zprofil.ordre)
        self.ordreProfil.valueChanged.connect(self.update_ordreProfil)
        layout.addWidget(self.ordreProfil, 9, 1)

        layout.addWidget(QLabel(), 10, 0)

        onglet_zprofil.setLayout(layout)
        
        # onglet pentes
        layout = QGridLayout()

        self.tracerMarqueursPente = QCheckBox("Dessiner les marqueurs")
        self.tracerMarqueursPente.setChecked(self.pprofil.marqueursVisibles)
        self.tracerMarqueursPente.stateChanged.connect(self.update_visibiliteMarqueursPente)
        layout.addWidget(self.tracerMarqueursPente, 0, 0, 1, 2)

        label = QLabel("Légende :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 1, 0)

        self.legendePente = QLineEdit()
        self.legendePente.setText(self.pprofil.legende)
        self.legendePente.textChanged.connect(self.update_legendePente)
        layout.addWidget(self.legendePente, 1, 1)
        
        label = QLabel("Style de marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.style2marqueurPente = QComboBox()
        self.style2marqueurPente.insertItems(0, list(styles2marqueur.keys()))
        self.style2marqueurPente.setCurrentText(self.pprofil.marqueur['style'])
        self.style2marqueurPente.currentTextChanged.connect(self.update_style2marqueurPente)
        layout.addWidget(self.style2marqueurPente, 2, 1)
        
        label = QLabel("Couleur du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.couleur2marqueurPente = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2marqueurPente.setCurrentText(self.pprofil.marqueur['couleur'])
        self.couleur2marqueurPente.currentTextChanged.connect(self.update_couleur2marqueurPente)
        layout.addWidget(self.couleur2marqueurPente, 3, 1)
        
        label = QLabel("Taille du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.taille2marqueurPente = QDoubleSpinBox()
        self.taille2marqueurPente.setMaximumWidth(50)
        self.taille2marqueurPente.setRange(0, 99.9)
        self.taille2marqueurPente.setSingleStep(0.1)
        self.taille2marqueurPente.setDecimals(1)
        self.taille2marqueurPente.setLocale(QLocale('English'))
        self.taille2marqueurPente.setValue(self.pprofil.marqueur['taille'])
        self.taille2marqueurPente.valueChanged.connect(self.update_taille2marqueurPente)
        layout.addWidget(self.taille2marqueurPente, 4, 1)

        self.tracerValeursPente = QCheckBox("Ecrire les valeurs de pente")
        self.tracerValeursPente.setChecked(self.pprofil.pentesVisibles)
        self.tracerValeursPente.stateChanged.connect(self.update_visibiliteValeursPente)
        layout.addWidget(self.tracerValeursPente, 5, 0, 1, 2)
        
        label = QLabel("Taille du libellé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 6, 0)
        
        self.taillePente = QDoubleSpinBox()
        self.taillePente.setMaximumWidth(50)
        self.taillePente.setLocale(QLocale('English'))
        self.taillePente.setRange(0, 99.9)
        self.taillePente.setDecimals(1)
        self.taillePente.setSingleStep(0.1)
        self.taillePente.setValue(self.pprofil.annotation["taille"])
        self.taillePente.valueChanged.connect(self.update_taillePente)
        layout.addWidget(self.taillePente, 6, 1)
        
        label = QLabel("Couleur du libellé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)
        
        self.couleurPente = ColorsComboBox(self.pyLong.appctxt)
        self.couleurPente.setCurrentText(self.pprofil.annotation["couleur"])
        self.couleurPente.currentTextChanged.connect(self.update_couleurPente)
        layout.addWidget(self.couleurPente, 7, 1)
        
        label = QLabel("Décalage vert. :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 8, 0)
        
        self.decalagePente = QDoubleSpinBox()
        self.decalagePente.setLocale(QLocale('English'))
        self.decalagePente.setMaximumWidth(65)
        if self.axeSecondaire:
            if self.symbolePente == "%":
                self.decalagePente.setRange(-99.9, 99.9)
                self.decalagePente.setValue(self.pprofil.annotation['décalage p %'])
            else:
                self.decalagePente.setRange(-45.0, 45.0)
                self.decalagePente.setValue(self.pprofil.annotation['décalage p °'])
            self.decalagePente.setSuffix(" {}".format(self.symbolePente))
        else:
            self.decalagePente.setSuffix(" m")
            self.decalagePente.setRange(-99.9,99.9)
            self.decalagePente.setValue(self.pprofil.annotation['décalage z'])
        self.decalagePente.setSingleStep(0.1)
        self.decalagePente.setDecimals(1)
        self.decalagePente.valueChanged.connect(self.update_decalagePente)
        layout.addWidget(self.decalagePente, 8, 1)
            
        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 9, 0)
        
        self.opacitePente = QDoubleSpinBox()
        self.opacitePente.setFixedWidth(45)
        self.opacitePente.setLocale(QLocale('English'))
        self.opacitePente.setRange(0,1)
        self.opacitePente.setDecimals(1)
        self.opacitePente.setSingleStep(0.1)
        self.opacitePente.setValue(self.pprofil.opacite)
        self.opacitePente.valueChanged.connect(self.update_opacitePente)
        layout.addWidget(self.opacitePente, 9, 1)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 10, 0)
        
        self.ordrePente = QSpinBox()
        self.ordrePente.setFixedWidth(45)
        self.ordrePente.setRange(0,99)
        self.ordrePente.setValue(self.pprofil.ordre)
        self.ordrePente.valueChanged.connect(self.update_ordrePente)
        layout.addWidget(self.ordrePente, 10, 1)
        
        onglet_pprofil.setLayout(layout)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Apply).setText("Actualiser")
        buttonBox.button(QDialogButtonBox.Apply).setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rafraichir.png')))
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.intitule, 0, 1)
        layout.addWidget(tableWidget, 1, 0, 1, 2)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)
        
    def valider(self):
        self.appliquer()
        self.accept()
        
    def appliquer(self):
        self.pyLong.canvas.dessiner()

    def update_intituleProfil(self, value):
        self.zprofil.intitule = value
        self.setWindowTitle("Propriétés graphiques du profil \"{}\"".format(value))
        self.pyLong.listeProfils.update()

    def update_legendeProfil(self, value):
        self.zprofil.legende = value
        self.zprofil.line.set_label(value)
        self.pyLong.canvas.updateLegendes()

    def update_visibiliteProfil(self, value):
        self.zprofil.visible = value
        self.zprofil.line.set_visible(value and self.zprofil.actif)
        self.pyLong.canvas.updateLegendes()

    def update_style2ligneProfil(self, value):
        self.zprofil.ligne['style'] = value
        self.zprofil.line.set_linestyle(styles2ligne[value])
        self.pyLong.canvas.updateLegendes()

    def update_couleur2ligneProfil(self, value):
        self.zprofil.ligne['couleur'] = value
        self.zprofil.line.set_color(couleurs[value])
        self.pyLong.canvas.updateLegendes()

    def update_epaisseur2ligneProfil(self, value):
        self.zprofil.ligne['épaisseur'] = value
        self.zprofil.line.set_linewidth(value)
        self.pyLong.canvas.updateLegendes()

    def update_style2marqueurProfil(self, value):
        self.zprofil.marqueur['style'] = value
        self.zprofil.line.set_marker(styles2marqueur[value])
        self.pyLong.canvas.updateLegendes()

    def update_couleur2marqueurProfil(self, value):
        self.zprofil.marqueur['couleur'] = value
        self.zprofil.line.set_markeredgecolor(couleurs[value])
        self.zprofil.line.set_markerfacecolor(couleurs[value])
        self.pyLong.canvas.updateLegendes()

    def update_taille2marqueurProfil(self, value):
        self.zprofil.marqueur['taille'] = value
        self.zprofil.line.set_markersize(value)
        self.pyLong.canvas.updateLegendes()

    def update_opaciteProfil(self, value):
        self.zprofil.opacite = value
        self.zprofil.line.set_alpha(value)
        self.pyLong.canvas.updateLegendes()

    def update_ordreProfil(self, value):
        self.zprofil.ordre = value
        self.zprofil.line.set_zorder(value)
        self.pyLong.canvas.updateLegendes()

    def update_visibiliteMarqueursPente(self, value):
        self.pprofil.marqueursVisibles = value
        self.pprofil.line.set_visible(value and self.pprofil.actif)
        self.pprofil.line_pourcents.set_visible(value and self.pprofil.actif)
        self.pprofil.line_degres.set_visible(value and self.pprofil.actif)
        self.pyLong.canvas.updateLegendes()

    def update_legendePente(self, value):
        self.pprofil.legende = value
        self.pprofil.line.set_label(value)
        self.pprofil.line_pourcents.set_label(value)
        self.pprofil.line_degres.set_label(value)

        self.pyLong.canvas.updateLegendes()

    def update_style2marqueurPente(self, value):
        self.pprofil.marqueur['style'] = value
        self.pprofil.line.set_marker(styles2marqueur[value])
        self.pprofil.line_pourcents.set_marker(styles2marqueur[value])
        self.pprofil.line_degres.set_marker(styles2marqueur[value])
        self.pyLong.canvas.updateLegendes()

    def update_couleur2marqueurPente(self, value):
        self.pprofil.marqueur['couleur'] = value
        self.pprofil.line.set_markeredgecolor(couleurs[value])
        self.pprofil.line_pourcents.set_markeredgecolor(couleurs[value])
        self.pprofil.line_degres.set_markeredgecolor(couleurs[value])
        self.pprofil.line.set_markerfacecolor(couleurs[value])
        self.pprofil.line_pourcents.set_markerfacecolor(couleurs[value])
        self.pprofil.line_degres.set_markerfacecolor(couleurs[value])
        self.pyLong.canvas.updateLegendes()

    def update_taille2marqueurPente(self, value):
        self.pprofil.marqueur['taille'] = value
        self.pprofil.line.set_markersize(value)
        self.pprofil.line_pourcents.set_markersize(value)
        self.pprofil.line_degres.set_markersize(value)
        self.pyLong.canvas.updateLegendes()

    def update_opacitePente(self, value):
        self.pprofil.opacite = value
        self.pprofil.line.set_alpha(value)
        self.pprofil.line_pourcents.set_alpha(value)
        self.pprofil.line_degres.set_alpha(value)
        self.pyLong.canvas.updateLegendes()

    def update_ordrePente(self, value):
        self.pprofil.ordre = value
        self.pprofil.line.set_zorder(value)
        self.pprofil.line_pourcents.set_zorder(value)
        self.pprofil.line_degres.set_zorder(value)
        self.pyLong.canvas.updateLegendes()

    def update_visibiliteValeursPente(self, value):
        self.pprofil.pentesVisibles = value

    def update_taillePente(self, value):
        self.pprofil.annotation['taille'] = value

    def update_couleurPente(self, value):
        self.pprofil.annotation['couleur'] = value

    def update_decalagePente(self, value):
        if self.axeSecondaire:
            if self.symbolePente == "%":
                self.pprofil.annotation['décalage p %'] = value
            else:
                self.pprofil.annotation['décalage p °'] = value
        else:
            self.pprofil.annotation['décalage z'] = value
