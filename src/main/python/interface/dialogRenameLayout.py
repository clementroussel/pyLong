from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogRenommerLayout(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Renommer la mise en page")
        
        i = self.pyLong.listeLayouts.currentIndex()
        self.currentLayout = self.pyLong.projet.layouts[i]
        
        mainLayout = QGridLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        mainLayout.addWidget(label, 0, 0)      
        
        self.intitule = QLineEdit()
        self.intitule.setText(self.currentLayout.intitule)
        mainLayout.addWidget(self.intitule, 0, 1)        
                
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        
        mainLayout.addWidget(buttonBox, 1, 0, 1, 2)

        self.setLayout(mainLayout)
        
    def valider(self):
        i = self.pyLong.listeLayouts.currentIndex()
        self.currentLayout.intitule = self.intitule.text()
        self.pyLong.listeLayouts.setItemText(i, self.intitule.text())
        self.accept()
