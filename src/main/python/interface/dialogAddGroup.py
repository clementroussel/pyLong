from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.Groupe import *


class DialogAjoutGroupe(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Ajouter un groupe d'annotations")
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Nouveau groupe d'annotations")
        layout = QGridLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.intitule = QLineEdit()
        self.intitule.setText("groupe {}".format(Groupe.compteur + 1))
        layout.addWidget(self.intitule, 0, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonBox)
        
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
            
    def appliquer(self):
        groupe = Groupe()
        groupe.intitule = self.intitule.text()
            
        self.pyLong.projet.groupes.append(groupe)

        self.pyLong.listeAnnotations.updateGroupes()
        self.pyLong.listeAnnotations.groupes.setCurrentIndex(self.pyLong.listeAnnotations.groupes.count() - 1)
        # # self.pyLong.listeAnnotations.groupes.addItem(groupe.intitule)
        # n = self.pyLong.listeAnnotations.liste.count()
        # # self.pyLong.listeAnnotations.groupes.setItemChecked(n - 1, groupe.actif)
        # self.pyLong.listeAnnotations.groupes.setCurrentIndex(n - 1)
        
    def valider(self):
        self.appliquer()
        self.accept()
