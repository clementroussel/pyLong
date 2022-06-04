from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogRenameGroup(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Renommer le groupe")
        
        i = self.pyLong.listeAnnotations.groupes.currentIndex()
        self.currentGroupe = self.pyLong.projet.groupes[i]
        
        mainLayout = QGridLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        mainLayout.addWidget(label, 0, 0)      
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.currentGroupe.intitule)
        mainLayout.addWidget(self.intitule, 0, 1)        
                
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        
        mainLayout.addWidget(buttonBox, 1, 0, 1, 2)

        self.setLayout(mainLayout)
        
    def valider(self):
        self.currentGroupe.intitule = self.intitule.text()
        self.pyLong.listeAnnotations.groupes.setItemText(self.pyLong.listeAnnotations.groupes.currentIndex(), self.intitule.text())
        self.accept()
