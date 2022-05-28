from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ColorsComboBox import *

from pyLong.dictionnaires import *


class DialogRickenmann(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(300)
        
        self.pyLong = parent
        
        i = self.pyLong.listeCalculs.liste.currentRow()
        self.rickenmann = self.pyLong.projet.calculs[i]
        
        self.setWindowTitle("Rickenmann")
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
        
        for zprofil, pprofil in self.pyLong.projet.profils :
            self.profils.addItem(zprofil.intitule)
        layout.addWidget(self.profils, 0, 1, 1, 2)
        
        try:
            self.profils.setCurrentIndex(self.rickenmann.parametres['profil'])
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
        self.abscisseDepart.setRange(-99999.999, 99999.999)
        self.abscisseDepart.setDecimals(3)
        self.abscisseDepart.setValue(self.rickenmann.parametres['abscisse départ'])
        layout.addWidget(self.abscisseDepart, 2, 1)        

        self.altitudeDepart = QDoubleSpinBox()
        self.altitudeDepart.setFixedWidth(90)
        self.altitudeDepart.setSuffix(" m")
        self.altitudeDepart.setLocale(QLocale('English'))
        self.altitudeDepart.setSingleStep(1)
        self.altitudeDepart.setRange(-99999.999, 99999.999)
        self.altitudeDepart.setDecimals(3)
        self.altitudeDepart.setReadOnly(True)
        self.altitudeDepart.setValue(self.rickenmann.parametres['altitude départ'])
        layout.addWidget(self.altitudeDepart, 2, 2)

        self.abscisseArrivee = QDoubleSpinBox()
        self.abscisseArrivee.setFixedWidth(90)
        self.abscisseArrivee.setSuffix(" m")
        self.abscisseArrivee.setLocale(QLocale('English'))
        self.abscisseArrivee.setSingleStep(1)
        self.abscisseArrivee.setRange(-99999.999, 99999.999)
        self.abscisseArrivee.setDecimals(3)
        self.abscisseArrivee.setReadOnly(True)
        self.abscisseArrivee.setValue(self.rickenmann.parametres['abscisse arrivée'])
        layout.addWidget(self.abscisseArrivee, 3, 1)        

        self.altitudeArrivee = QDoubleSpinBox()
        self.altitudeArrivee.setFixedWidth(90)
        self.altitudeArrivee.setSuffix(" m")
        self.altitudeArrivee.setLocale(QLocale('English'))
        self.altitudeArrivee.setSingleStep(1)
        self.altitudeArrivee.setRange(-99999.999, 99999.999)
        self.altitudeArrivee.setDecimals(3)
        self.altitudeArrivee.setReadOnly(True)
        self.altitudeArrivee.setValue(self.rickenmann.parametres['altitude arrivée'])
        layout.addWidget(self.altitudeArrivee, 3, 2)
        
        label = QLabel("Volume :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.volume = QSpinBox()
        self.volume.setFixedWidth(90)
        self.volume.setSuffix(" m^3")
        self.volume.setLocale(QLocale('English'))
        self.volume.setRange(0, 999999)
        self.volume.setValue(self.rickenmann.parametres['volume'])
        layout.addWidget(self.volume, 4, 1)
        
        label = QLabel("Pas de calcul :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.pas2calcul = QDoubleSpinBox()
        self.pas2calcul.setFixedWidth(75)
        self.pas2calcul.setSuffix(" m")
        self.pas2calcul.setLocale(QLocale('English'))
        self.pas2calcul.setRange(0, 1000.0)
        self.pas2calcul.setDecimals(1)
        self.pas2calcul.setSingleStep(0.1)
        self.pas2calcul.setValue(self.rickenmann.parametres['pas de calcul'])
        layout.addWidget(self.pas2calcul, 5, 1)
        
        self.enveloppe = QCheckBox("utiliser l'équation de type courbe enveloppe")
        self.enveloppe.setChecked(self.rickenmann.parametres['enveloppe'])
        layout.addWidget(self.enveloppe, 6, 0, 1, 3)
        
        onglet_parametres.setLayout(layout)
        
        # onglet aspect graphique
        layout = QGridLayout()
        
        label = QLabel("Légende :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.legende = QLineEdit()
        self.legende.setText(self.rickenmann.legende)
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
        self.style2ligne.setCurrentText(self.rickenmann.ligne['style'])
        self.style2ligne.currentTextChanged.connect(self.appliquerStyle)
        layout.addWidget(self.style2ligne, 1, 1, 1, 2)
        
        label = QLabel("Couleur de ligne :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 2, 0)
        
        self.couleur2ligne = ColorsComboBox(self.pyLong.appctxt)
        self.couleur2ligne.setCurrentText(self.rickenmann.ligne['couleur'])
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
        self.epaisseur2ligne.setValue(self.rickenmann.ligne['épaisseur'])
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
        self.opacite.setValue(self.rickenmann.opacite)
        self.opacite.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.opacite, 4, 1, 1, 2)
        
        label = QLabel("Ordre :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 5, 0)
        
        self.ordre = QSpinBox()
        self.ordre.setFixedWidth(50)
        self.ordre.setRange(1, 99)
        self.ordre.setValue(self.rickenmann.ordre)
        self.ordre.valueChanged.connect(self.appliquerStyle)
        layout.addWidget(self.ordre, 5, 1, 1, 2)
        
        layout.addWidget(QWidget(), 6, 0)
        
        onglet_graphique.setLayout(layout)

        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.rickenmann.intitule)
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
        self.rickenmann.intitule = self.intitule.text()
        self.pyLong.listeCalculs.update()

    def appliquerStyle(self):
        self.rickenmann.legende = self.legende.text()
        self.rickenmann.ligne['style'] = self.style2ligne.currentText()
        self.rickenmann.ligne['couleur'] = self.couleur2ligne.currentText()
        self.rickenmann.ligne['épaisseur'] = self.epaisseur2ligne.value()
        self.rickenmann.opacite = self.opacite.value()
        self.rickenmann.ordre = self.ordre.value()

        self.rickenmann.update()
        # self.pyLong.canvas.draw()
        self.pyLong.canvas.updateLegendes()
            
    def appliquer(self):
        self.rickenmann.parametres['profil'] = self.profils.currentIndex()
        self.rickenmann.parametres['abscisse départ'] = self.abscisseDepart.value()
        self.rickenmann.parametres['volume'] = self.volume.value()
        self.rickenmann.parametres['pas de calcul'] = self.pas2calcul.value()
        self.rickenmann.parametres['enveloppe'] = self.enveloppe.isChecked()
        
        try:
            self.rickenmann.calculer(self.pyLong)
        except:
            self.rickenmann.calculReussi = False
            pass
        
        if self.rickenmann.calculReussi:
            self.abscisseDepart.setValue(self.rickenmann.parametres['abscisse départ'])
            self.altitudeDepart.setValue(self.rickenmann.parametres['altitude départ'])
            self.abscisseArrivee.setValue(self.rickenmann.parametres['abscisse arrivée'])
            self.altitudeArrivee.setValue(self.rickenmann.parametres['altitude arrivée'])
        else:
            alerte = QMessageBox(self)
            alerte.setText("Le calcul a échoué.")
            alerte.exec_()
        
        self.rickenmann.update()
        # self.pyLong.canvas.draw()
        self.pyLong.canvas.updateLegendes()
