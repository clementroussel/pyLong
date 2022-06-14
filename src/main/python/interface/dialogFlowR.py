from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *

from pyLong.dictionaries import *


class DialogFlowR(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.listeCalculs.liste.currentRow()
        self.flowr = self.pyLong.projet.calculs[i]
        
        self.setWindowTitle("Flow-R")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/lave.png')))
    
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
            self.profils.setCurrentIndex(self.flowr.parametres['profil'])
        except:
            self.profils.setCurrentIndex(0)
        
        label = QLabel("Abscisse")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1)      

        label = QLabel("Altitude")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 2)
        
        label = QLabel("Départ :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        label = QLabel("Arrivée :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.abscisseDepart = QDoubleSpinBox()
        self.abscisseDepart.setFixedWidth(90)
        self.abscisseDepart.setSuffix(" m")
        self.abscisseDepart.setLocale(QLocale('English'))
        self.abscisseDepart.setSingleStep(0.1)
        self.abscisseDepart.setRange(0, 99999.999)
        self.abscisseDepart.setDecimals(3)
        self.abscisseDepart.setValue(self.flowr.parametres['abscisse départ'])
        layout.addWidget(self.abscisseDepart, 2, 1)        

        self.altitudeDepart = QDoubleSpinBox()
        self.altitudeDepart.setFixedWidth(90)
        self.altitudeDepart.setSuffix(" m")
        self.altitudeDepart.setLocale(QLocale('English'))
        self.altitudeDepart.setSingleStep(1)
        self.altitudeDepart.setRange(0, 99999.999)
        self.altitudeDepart.setDecimals(3)
        self.altitudeDepart.setReadOnly(True)
        self.altitudeDepart.setValue(self.flowr.parametres['altitude départ'])
        layout.addWidget(self.altitudeDepart, 2, 2)

        self.abscisseArrivee = QDoubleSpinBox()
        self.abscisseArrivee.setFixedWidth(90)
        self.abscisseArrivee.setSuffix(" m")
        self.abscisseArrivee.setLocale(QLocale('English'))
        self.abscisseArrivee.setSingleStep(1)
        self.abscisseArrivee.setRange(0, 99999.999)
        self.abscisseArrivee.setDecimals(3)
        self.abscisseArrivee.setReadOnly(True)
        self.abscisseArrivee.setValue(self.flowr.parametres['abscisse arrivée'])
        layout.addWidget(self.abscisseArrivee, 3, 1)        

        self.altitudeArrivee = QDoubleSpinBox()
        self.altitudeArrivee.setFixedWidth(90)
        self.altitudeArrivee.setSuffix(" m")
        self.altitudeArrivee.setLocale(QLocale('English'))
        self.altitudeArrivee.setSingleStep(1)
        self.altitudeArrivee.setRange(0, 99999.999)
        self.altitudeArrivee.setDecimals(3)
        self.altitudeArrivee.setReadOnly(True)
        self.altitudeArrivee.setValue(self.flowr.parametres['altitude arrivée'])
        layout.addWidget(self.altitudeArrivee, 3, 2)
        
        label = QLabel("Angle :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.angle = QDoubleSpinBox()
        self.angle.setFixedWidth(80)
        self.angle.setSuffix(" deg")
        self.angle.setLocale(QLocale('English'))
        self.angle.setRange(0, 89.99)
        self.angle.setDecimals(2)
        self.angle.setSingleStep(0.1)
        self.angle.setValue(self.flowr.parametres['angle'])
        layout.addWidget(self.angle, 4, 1)
        
        label = QLabel("Vitesse initiale :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.vitesseInitiale = QDoubleSpinBox()
        self.vitesseInitiale.setFixedWidth(70)
        self.vitesseInitiale.setSuffix(" m/s")
        self.vitesseInitiale.setLocale(QLocale('English'))
        self.vitesseInitiale.setRange(0, 99.9)
        self.vitesseInitiale.setDecimals(1)
        self.vitesseInitiale.setSingleStep(0.1)
        self.vitesseInitiale.setValue(self.flowr.parametres['vitesse initiale'])
        layout.addWidget(self.vitesseInitiale, 5, 1)
        
        label = QLabel("Vitesse maximale :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 6, 0)
        
        self.vitesseMax = QDoubleSpinBox()
        self.vitesseMax.setFixedWidth(70)
        self.vitesseMax.setSuffix(" m/s")
        self.vitesseMax.setLocale(QLocale('English'))
        self.vitesseMax.setRange(0, 99.9)
        self.vitesseMax.setDecimals(1)
        self.vitesseMax.setSingleStep(0.1)
        self.vitesseMax.setValue(self.flowr.parametres['vitesse maximale'])
        layout.addWidget(self.vitesseMax, 6, 1)
        
        label = QLabel("Pas de calcul :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)
        
        self.pas2calcul = QDoubleSpinBox()
        self.pas2calcul.setFixedWidth(75)
        self.pas2calcul.setSuffix(" m")
        self.pas2calcul.setLocale(QLocale('English'))
        self.pas2calcul.setRange(0, 1000.0)
        self.pas2calcul.setDecimals(1)
        self.pas2calcul.setSingleStep(0.1)
        self.pas2calcul.setValue(self.flowr.parametres['pas de calcul'])
        layout.addWidget(self.pas2calcul, 7, 1)
        
        onglet_parametres.setLayout(layout)
        
        # onglet aspect graphique
        layout = QGridLayout()
        
        label = QLabel("Légende :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.legende = QLineEdit()
        self.legende.setText(self.flowr.legende)
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
        self.style2ligne.setCurrentText(self.flowr.ligne['style'])
        self.style2ligne.currentTextChanged.connect(self.appliquerStyle)
        layout.addWidget(self.style2ligne, 1, 1, 1, 2)
        
        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 2, 0)
        
        self.couleur2ligne = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligne.setCurrentText(self.flowr.ligne['couleur'])
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
        self.epaisseur2ligne.setValue(self.flowr.ligne['épaisseur'])
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
        self.opacite.setValue(self.flowr.opacite)
        self.opacite.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.opacite, 4, 1, 1, 2)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 5, 0)
        
        self.ordre = QSpinBox()
        self.ordre.setFixedWidth(50)
        self.ordre.setRange(0, 99)
        self.ordre.setValue(self.flowr.ordre)
        self.ordre.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.ordre, 5, 1, 1, 2)
        
        layout.addWidget(QWidget(), 6, 0)
        layout.addWidget(QWidget(), 7, 0)
        
        onglet_graphique.setLayout(layout)

        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.flowr.intitule)
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

    def actualiser(self):
        self.pyLong.canvas.dessiner()
        
    def valider(self):
        self.appliquer()
        self.accept()

    def updateIntitule(self):
        self.flowr.intitule = self.intitule.text()
        self.pyLong.listeCalculs.update()

    def appliquerStyle(self):
        self.flowr.legende = self.legende.text()
        self.flowr.ligne['style'] = self.style2ligne.currentText()
        self.flowr.ligne['couleur'] = self.couleur2ligne.currentText()
        self.flowr.ligne['épaisseur'] = self.epaisseur2ligne.value()
        self.flowr.opacite = self.opacite.value()
        self.flowr.ordre = self.ordre.value()

        self.flowr.update()
        # self.pyLong.canvas.draw()
        self.pyLong.canvas.updateLegendes()
    
    def appliquer(self):
        self.flowr.parametres['profil'] = self.profils.currentIndex()
        self.flowr.parametres['abscisse départ'] = self.abscisseDepart.value()
        self.flowr.parametres['angle'] = self.angle.value()
        self.flowr.parametres['vitesse initiale'] = self.vitesseInitiale.value()
        self.flowr.parametres['vitesse maximale'] = self.vitesseMax.value()
        self.flowr.parametres['pas de calcul'] = self.pas2calcul.value()
        
        try:
            self.flowr.calculer(self.pyLong)
        except:
            self.flowr.calculReussi = False
            pass
        
        if self.flowr.calculReussi:
            self.abscisseDepart.setValue(self.flowr.parametres['abscisse départ'])
            self.altitudeDepart.setValue(self.flowr.parametres['altitude départ'])
            self.abscisseArrivee.setValue(self.flowr.parametres['abscisse arrivée'])
            self.altitudeArrivee.setValue(self.flowr.parametres['altitude arrivée'])
        else:
            alerte = QMessageBox(self)
            alerte.setText("Le calcul a échoué.")
            alerte.exec_()
        
        self.flowr.update()
        # self.pyLong.canvas.draw()
        self.pyLong.canvas.updateLegendes()
