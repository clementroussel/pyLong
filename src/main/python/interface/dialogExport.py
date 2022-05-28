from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionnaires import *


class DialogExporter(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        i = self.pyLong.listeProfils.liste.currentRow()
        
        self.setWindowTitle("Exporter le profil \"{}\"".format(self.pyLong.listeProfils.liste.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/exporter.png')))
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()
        
        label = QLabel("Délimiteur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.delimiteur = QComboBox()
        self.delimiteur.insertItems(0, list(delimiteurs.keys()))
        self.delimiteur.setCurrentText("tabulation")
        layout.addWidget(self.delimiteur, 0, 1)
        
        label = QLabel("Séparateur décimal :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.separateur = QComboBox()
        self.separateur.insertItems(0, list(separateurs.keys()))
        layout.addWidget(self.separateur, 1, 1)
    
        label = QLabel("Nombre de décimales :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)    
        
        self.decimales = QSpinBox()
        self.decimales.setFixedWidth(40)
        self.decimales.setRange(0,99)
        self.decimales.setValue(3)
        layout.addWidget(self.decimales, 2, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.exporter)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout.addWidget(buttonBox)        
        self.setLayout(mainLayout)
        
    def exporter(self):
        try:
            i = self.pyLong.listeProfils.liste.currentRow()
            zprofil, pprofil = self.pyLong.projet.profils[i]
            
            chemin = QFileDialog.getSaveFileName(caption="Exporter un profil",
                                                 filter="fichier texte (*.txt)")[0]
            
            if chemin == "":
                return 0

            else:
                nomFichier = QFileInfo(chemin).fileName()
                repertoireFichier = QFileInfo(chemin).absolutePath()
                nomFichier = nomFichier.split(".")[0]
                nomFichier += ".txt"
                chemin = repertoireFichier + "/" + nomFichier

                delimiteur = delimiteurs[self.delimiteur.currentText()]
                formatage = "%.{}f".format(self.decimales.value())
                separateur = separateurs[self.separateur.currentText()]
                
                zprofil.exporter(chemin, delimiteur, formatage, separateur)

            self.accept()
            
        except:
            alerte = QMessageBox(self)
            alerte.setText("L'exportation a échoué !")
            alerte.exec_()
            pass