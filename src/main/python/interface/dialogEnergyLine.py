from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *

from pyLong.dictionnaires import *


class DialogLigneEnergie(QDialog):

    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.listeCalculs.liste.currentRow()
        self.ligneEnergie = self.pyLong.projet.calculs[i]
        
        self.setWindowTitle("Ligne d'énergie")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rock.png')))
    
        tableWidget = QTabWidget()
        onglet_parametres = QWidget()
        onglet_graphique = QWidget() 

        tableWidget.addTab(onglet_parametres, "Paramètres de calcul")
        tableWidget.addTab(onglet_graphique, "Aspect graphique")  
        
        # onglet paramètres
        layout = QGridLayout()
        
        label = QLabel("Profil :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.profils = QComboBox()
        
        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profils.addItem(zprofil.intitule)
        layout.addWidget(self.profils, 0, 1, 1, 2)
        
        try:
            self.profils.setCurrentIndex(self.ligneEnergie.parametres['profil'])
        except:
            self.profils.setCurrentIndex(0)
        
        label = QLabel("Méthode :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0) 
        
        self.methodes = QComboBox()
        self.methodes.addItems(["départ + arrivée", "départ + angle", "arrivée + angle"])
        self.methodes.setCurrentText(self.ligneEnergie.parametres['méthode'])
        self.methodes.currentTextChanged.connect(self.updateInterface)
        layout.addWidget(self.methodes, 1, 1, 1, 2)
        
        label = QLabel("Abscisse")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 2, 1)      

        label = QLabel("Altitude")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 2, 2)
        
        label = QLabel("Départ :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        label = QLabel("Arrivée :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.abscisseDepart = QDoubleSpinBox()
        self.abscisseDepart.setFixedWidth(90)
        self.abscisseDepart.setSuffix(" m")
        self.abscisseDepart.setLocale(QLocale('English'))
        self.abscisseDepart.setSingleStep(1)
        self.abscisseDepart.setRange(0, 99999.999)
        self.abscisseDepart.setDecimals(3)
        self.abscisseDepart.setValue(self.ligneEnergie.parametres['abscisse départ'])
        layout.addWidget(self.abscisseDepart, 3, 1)        

        self.altitudeDepart = QDoubleSpinBox()
        self.altitudeDepart.setFixedWidth(90)
        self.altitudeDepart.setSuffix(" m")
        self.altitudeDepart.setLocale(QLocale('English'))
        self.altitudeDepart.setSingleStep(1)
        self.altitudeDepart.setRange(0, 99999.999)
        self.altitudeDepart.setDecimals(3)
        self.altitudeDepart.setValue(self.ligneEnergie.parametres['altitude départ'])
        self.altitudeDepart.setReadOnly(True)
        layout.addWidget(self.altitudeDepart, 3, 2)

        self.abscisseArrivee = QDoubleSpinBox()
        self.abscisseArrivee.setFixedWidth(90)
        self.abscisseArrivee.setSuffix(" m")
        self.abscisseArrivee.setLocale(QLocale('English'))
        self.abscisseArrivee.setSingleStep(1)
        self.abscisseArrivee.setRange(0, 99999.999)
        self.abscisseArrivee.setDecimals(3)
        self.abscisseArrivee.setValue(self.ligneEnergie.parametres['abscisse arrivée'])
        layout.addWidget(self.abscisseArrivee, 4, 1)        

        self.altitudeArrivee = QDoubleSpinBox()
        self.altitudeArrivee.setFixedWidth(90)
        self.altitudeArrivee.setSuffix(" m")
        self.altitudeArrivee.setLocale(QLocale('English'))
        self.altitudeArrivee.setSingleStep(1)
        self.altitudeArrivee.setRange(0, 99999.999)
        self.altitudeArrivee.setDecimals(3)
        self.altitudeArrivee.setReadOnly(True)
        self.altitudeArrivee.setValue(self.ligneEnergie.parametres['altitude arrivée'])
        layout.addWidget(self.altitudeArrivee, 4, 2)
        
        label = QLabel("Angle :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.angle = QDoubleSpinBox()
        self.angle.setSuffix(" deg")
        self.angle.setLocale(QLocale('English'))
        self.angle.setRange(0, 89.99)
        self.angle.setDecimals(6)
        self.angle.setSingleStep(1)
        self.angle.setValue(self.ligneEnergie.parametres['angle'])
        layout.addWidget(self.angle, 5, 1, 1, 2)
        
        onglet_parametres.setLayout(layout)
        
        # onglet aspect graphique
        layout = QGridLayout()
        
        label = QLabel("Légende :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.legende = QLineEdit()
        self.legende.setText(self.ligneEnergie.legende)
        self.legende.textEdited.connect(self.appliquerStyle)
        layout.addWidget(self.legende, 0, 1)

        actualiser = QPushButton()
        actualiser.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rafraichir.png')))
        actualiser.clicked.connect(self.actualiser)
        actualiser.setAutoDefault(False)
        layout.addWidget(actualiser, 0, 2)
        
        label = QLabel("Style de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.style2ligne = QComboBox()
        self.style2ligne.insertItems(0, list(styles2ligne.keys()))
        self.style2ligne.setCurrentText(self.ligneEnergie.ligne['style'])
        self.style2ligne.currentTextChanged.connect(self.appliquerStyle)
        layout.addWidget(self.style2ligne, 1, 1, 1, 2)
        
        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 2, 0)
        
        self.couleur2ligne = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligne.setCurrentText(self.ligneEnergie.ligne['couleur'])
        self.couleur2ligne.currentTextChanged.connect(self.appliquerStyle)
        layout.addWidget(self.couleur2ligne, 2, 1, 1, 2)
        
        label = QLabel("Épaisseur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 3, 0)
        
        self.epaisseur2ligne = QDoubleSpinBox()
        self.epaisseur2ligne.setFixedWidth(50)
        self.epaisseur2ligne.setLocale(QLocale('English'))
        self.epaisseur2ligne.setRange(0, 99.9)
        self.epaisseur2ligne.setDecimals(1)
        self.epaisseur2ligne.setSingleStep(0.1)
        self.epaisseur2ligne.setValue(self.ligneEnergie.ligne['épaisseur'])
        self.epaisseur2ligne.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.epaisseur2ligne, 3, 1, 1, 2)
        
        label = QLabel("Opacité :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 4, 0)
        
        self.opacite = QDoubleSpinBox()
        self.opacite.setFixedWidth(50)
        self.opacite.setLocale(QLocale('English'))
        self.opacite.setRange(0, 1)
        self.opacite.setDecimals(1)
        self.opacite.setSingleStep(0.1)
        self.opacite.setValue(self.ligneEnergie.opacite)
        self.opacite.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.opacite, 4, 1, 1, 2)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 5, 0)
        
        self.ordre = QSpinBox()
        self.ordre.setFixedWidth(50)
        self.ordre.setRange(1, 99)
        self.ordre.setValue(self.ligneEnergie.ordre)
        self.ordre.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.ordre, 5, 1, 1, 2)
        
        onglet_graphique.setLayout(layout)

        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.ligneEnergie.intitule)
        self.intitule.textChanged.connect(self.updateIntitule)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Apply).setText("Appliquer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        layout = QGridLayout()
        
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.intitule, 0, 1)
        
        layout.addWidget(tableWidget, 1, 0, 1, 2)
        
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)      

        self.updateInterface()

    def actualiser(self):
        self.pyLong.canvas.dessiner()
    
    def valider(self):
        self.appliquer()
        self.accept()

    def appliquerStyle(self):
        self.ligneEnergie.intitule = self.intitule.text()
        self.ligneEnergie.legende = self.legende.text()
        self.ligneEnergie.ligne['style'] = self.style2ligne.currentText()
        self.ligneEnergie.ligne['couleur'] = self.couleur2ligne.currentText()
        self.ligneEnergie.ligne['épaisseur'] = self.epaisseur2ligne.value()
        self.ligneEnergie.opacite = self.opacite.value()
        self.ligneEnergie.ordre = self.ordre.value()

        self.ligneEnergie.update()
        # self.pyLong.canvas.draw()
        self.pyLong.canvas.updateLegendes()

    def updateIntitule(self):
        self.ligneEnergie.intitule = self.intitule.text()
        self.pyLong.listeCalculs.update()
    
    def appliquer(self):
        self.ligneEnergie.parametres['profil'] = self.profils.currentIndex()
        self.ligneEnergie.parametres['méthode'] = self.methodes.currentText()
        self.ligneEnergie.parametres['abscisse départ'] = self.abscisseDepart.value()
        self.ligneEnergie.parametres['abscisse arrivée'] = self.abscisseArrivee.value()
        self.ligneEnergie.parametres['angle'] = self.angle.value()
        
        try:
            self.ligneEnergie.calculer(self.pyLong)
        except:
            self.ligneEnergie.calculReussi = False
            pass
        
        if self.ligneEnergie.calculReussi:
            self.abscisseDepart.setValue(self.ligneEnergie.parametres['abscisse départ'])
            self.altitudeDepart.setValue(self.ligneEnergie.parametres['altitude départ'])
            self.abscisseArrivee.setValue(self.ligneEnergie.parametres['abscisse arrivée'])
            self.altitudeArrivee.setValue(self.ligneEnergie.parametres['altitude arrivée'])
            self.angle.setValue(self.ligneEnergie.parametres['angle'])
        else:
            alerte = QMessageBox(self)
            alerte.setText("Le calcul a échoué.")
            alerte.exec_()
        
        self.ligneEnergie.update()
        self.pyLong.canvas.draw()
        
    def updateInterface(self):
        if self.methodes.currentText() == "départ + arrivée":
            self.abscisseDepart.setReadOnly(False)
            self.abscisseArrivee.setReadOnly(False)
            self.angle.setReadOnly(True)
        elif self.methodes.currentText() == "départ + angle":
            self.abscisseDepart.setReadOnly(False)
            self.abscisseArrivee.setReadOnly(True)
            self.angle.setReadOnly(False)
        else:
            self.abscisseDepart.setReadOnly(True)
            self.abscisseArrivee.setReadOnly(False)
            self.angle.setReadOnly(False)
