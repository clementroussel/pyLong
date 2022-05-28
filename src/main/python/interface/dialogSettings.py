from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyLong.dictionnaires import *
from pyLong.Preference import *

from ColorsComboBox import *

from pyLong.LigneRappel import *


class DialogPreferences(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Préférences")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/preferences.png')))

        mainLayout = QVBoxLayout()

        tableWidget = QTabWidget()
        onglet_general = QWidget()
        onglet_apercu = QWidget()
        onglet_rappel = QWidget()

        tableWidget.addTab(onglet_general, "Général")
        tableWidget.addTab(onglet_apercu, "Profil aperçu")
        tableWidget.addTab(onglet_rappel, "Lignes de rappel")

        # onglet général
        layout = QVBoxLayout()

        groupe = QGroupBox("Préférences")
        sublayout = QGridLayout()

        label = QLabel("Expression des pentes :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.unitePente = QComboBox()
        self.unitePente.addItems(["%", "°"])
        self.unitePente.setCurrentText(self.pyLong.projet.preferences['pente'])
        sublayout.addWidget(self.unitePente, 0, 1)

        label = QLabel("Sens des profils :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.sens = QComboBox()
        self.sens.addItems(["ascendant", "descendant"])
        self.sens.setCurrentText(self.pyLong.projet.preferences['sens'])
        sublayout.addWidget(self.sens, 1, 1)

        groupe.setLayout(sublayout)
        layout.addWidget(groupe)

        groupe = QGroupBox("Export de la figure")
        sublayout = QGridLayout()

        label = QLabel("Format :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.extension = QComboBox()
        self.extension.insertItems(0, list(extensions.keys()))
        self.extension.setCurrentText(self.pyLong.projet.preferences['extension'])
        sublayout.addWidget(self.extension, 0, 1)

        label = QLabel("Résolution :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.dpi = QSpinBox()
        self.dpi.setFixedWidth(75)
        self.dpi.setSuffix(" dpi")
        self.dpi.setSingleStep(25)
        self.dpi.setRange(25, 1000)
        self.dpi.setValue(self.pyLong.projet.preferences['dpi'])
        sublayout.addWidget(self.dpi, 1, 1)

        groupe.setLayout(sublayout)
        layout.addWidget(groupe)

        layout.addWidget(QLabel())
        layout.addWidget(QLabel())

        onglet_general.setLayout(layout)

        # onglet aperçu
        layout = QVBoxLayout()

        groupe = QGroupBox("Propriétés graphiques")
        sublayout = QGridLayout()

        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.style2ligne = QComboBox()
        self.style2ligne.insertItems(0, list(styles2ligne.keys()))
        self.style2ligne.setCurrentText(self.pyLong.projet.apercu.ligne['style'])
        sublayout.addWidget(self.style2ligne, 0, 1)

        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.couleur2ligne = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligne.setCurrentText(self.pyLong.projet.apercu.ligne['couleur'])
        sublayout.addWidget(self.couleur2ligne, 1, 1)

        label = QLabel("Épaisseur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 2, 0)

        self.epaisseur2ligne = QDoubleSpinBox()
        self.epaisseur2ligne.setFixedWidth(50)
        self.epaisseur2ligne.setLocale(QLocale('English'))
        self.epaisseur2ligne.setDecimals(1)
        self.epaisseur2ligne.setRange(0, 99.9)
        self.epaisseur2ligne.setSingleStep(0.1)
        self.epaisseur2ligne.setValue(self.pyLong.projet.apercu.ligne['épaisseur'])
        sublayout.addWidget(self.epaisseur2ligne, 2, 1)

        label = QLabel("Style de marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 3, 0)

        self.style2marqueur = QComboBox()
        self.style2marqueur.insertItems(0, list(styles2marqueur.keys()))
        self.style2marqueur.setCurrentText(self.pyLong.projet.apercu.marqueur['style'])
        sublayout.addWidget(self.style2marqueur, 3, 1)

        label = QLabel("Couleur du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 4, 0)

        self.couleur2marqueur = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2marqueur.setCurrentText(self.pyLong.projet.apercu.marqueur['couleur'])
        sublayout.addWidget(self.couleur2marqueur, 4, 1)

        label = QLabel("Taille du marqueur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 5, 0)

        self.taille2marqueur = QDoubleSpinBox()
        self.taille2marqueur.setFixedWidth(50)
        self.taille2marqueur.setLocale(QLocale('English'))
        self.taille2marqueur.setRange(0, 99.9)
        self.taille2marqueur.setSingleStep(0.1)
        self.taille2marqueur.setDecimals(1)
        self.taille2marqueur.setValue(self.pyLong.projet.apercu.marqueur['taille'])
        sublayout.addWidget(self.taille2marqueur, 5, 1)

        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 6, 0)

        self.opacite = QDoubleSpinBox()
        self.opacite.setFixedWidth(50)
        self.opacite.setLocale(QLocale('English'))
        self.opacite.setRange(0, 1)
        self.opacite.setDecimals(1)
        self.opacite.setSingleStep(0.1)
        self.opacite.setValue(self.pyLong.projet.apercu.opacite)
        sublayout.addWidget(self.opacite, 6, 1)

        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 7, 0)

        self.ordre = QSpinBox()
        self.ordre.setFixedWidth(50)
        self.ordre.setRange(0, 99)
        self.ordre.setValue(self.pyLong.projet.apercu.ordre)
        sublayout.addWidget(self.ordre, 7, 1)

        groupe.setLayout(sublayout)
        layout.addWidget(groupe)

        onglet_apercu.setLayout(layout)

        # onglet rappel
        layout = QVBoxLayout()

        groupe = QGroupBox("Propriétés graphiques")
        sublayout = QGridLayout()

        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.style2ligneRappel = QComboBox()
        self.style2ligneRappel.insertItems(0, list(styles2ligne.keys()))
        self.style2ligneRappel.setCurrentText(self.pyLong.projet.preferences['style rappel'])
        sublayout.addWidget(self.style2ligneRappel, 0, 1)

        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.couleur2ligneRappel = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligneRappel.setCurrentText(self.pyLong.projet.preferences['couleur rappel'])
        sublayout.addWidget(self.couleur2ligneRappel, 1, 1)

        label = QLabel("Épaisseur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 2, 0)

        self.epaisseur2ligneRappel = QDoubleSpinBox()
        self.epaisseur2ligneRappel.setFixedWidth(50)
        self.epaisseur2ligneRappel.setLocale(QLocale('English'))
        self.epaisseur2ligneRappel.setDecimals(1)
        self.epaisseur2ligneRappel.setRange(0, 99.9)
        self.epaisseur2ligneRappel.setSingleStep(0.1)
        self.epaisseur2ligneRappel.setValue(self.pyLong.projet.preferences['épaisseur rappel'])
        sublayout.addWidget(self.epaisseur2ligneRappel, 2, 1)

        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 3, 0)

        self.opaciteRappel = QDoubleSpinBox()
        self.opaciteRappel.setFixedWidth(50)
        self.opaciteRappel.setLocale(QLocale('English'))
        self.opaciteRappel.setRange(0, 1)
        self.opaciteRappel.setDecimals(1)
        self.opaciteRappel.setSingleStep(0.1)
        self.opaciteRappel.setValue(self.pyLong.projet.preferences['opacité rappel'])
        sublayout.addWidget(self.opaciteRappel, 3, 1)

        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 4, 0)

        self.ordreRappel = QSpinBox()
        self.ordreRappel.setFixedWidth(50)
        self.ordreRappel.setRange(0, 99)
        self.ordreRappel.setValue(self.pyLong.projet.preferences['ordre rappel'])
        sublayout.addWidget(self.ordreRappel, 4, 1)

        sublayout.addWidget(QLabel(), 5, 0)
        sublayout.addWidget(QLabel(), 6, 0)
        sublayout.addWidget(QLabel(), 7, 0)

        groupe.setLayout(sublayout)
        layout.addWidget(groupe)

        onglet_rappel.setLayout(layout)

        mainLayout.addWidget(tableWidget)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Apply).setText("Actualiser")
        buttonBox.button(QDialogButtonBox.Apply).setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rafraichir.png')))
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

    def valider(self):
        self.appliquer()
        self.accept()
        
    def appliquer(self):
        self.pyLong.projet.preferences['pente'] = self.unitePente.currentText()
        self.pyLong.projet.preferences['sens'] = self.sens.currentText()
        self.pyLong.projet.preferences['extension'] = self.extension.currentText()
        self.pyLong.projet.preferences['dpi'] = self.dpi.value()
        
        self.pyLong.projet.apercu.ligne['style'] = self.style2ligne.currentText()
        self.pyLong.projet.apercu.ligne['couleur'] = self.couleur2ligne.currentText()
        self.pyLong.projet.apercu.ligne['épaisseur'] = self.epaisseur2ligne.value()
        self.pyLong.projet.apercu.marqueur['style'] = self.style2marqueur.currentText()
        self.pyLong.projet.apercu.marqueur['couleur'] = self.couleur2marqueur.currentText()
        self.pyLong.projet.apercu.marqueur['taille'] = self.taille2marqueur.value()
        self.pyLong.projet.apercu.opacite = self.opacite.value()
        self.pyLong.projet.apercu.ordre = self.ordre.value()

        self.pyLong.projet.preferences['style rappel'] = self.style2ligneRappel.currentText()
        self.pyLong.projet.preferences['couleur rappel'] = self.couleur2ligneRappel.currentText()
        self.pyLong.projet.preferences['épaisseur rappel'] = self.epaisseur2ligneRappel.value()
        self.pyLong.projet.preferences['opacité rappel'] = self.opaciteRappel.value()
        self.pyLong.projet.preferences['ordre rappel'] = self.ordreRappel.value()
        
        self.pyLong.canvas.dessiner()
