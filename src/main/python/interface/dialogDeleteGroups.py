from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.Groupe import *

class DialogSupprimerGroupes(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Supprimer des groupes")
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Supprimer les groupes d'annotations :")
        layout = QVBoxLayout()
        
        self.listeGroupes = QListWidget()
        for g in self.pyLong.projet.groupes[1:]:
            item = QListWidgetItem()
            item.setText(g.intitule)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listeGroupes.addItem(item)
        
        layout.addWidget(self.listeGroupes)
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
        
    def valider(self):
        n = self.pyLong.listeAnnotations.groupes.count()
        n -= 1
        for i in range(n-1, -1, -1):
            if self.listeGroupes.item(i).checkState() == Qt.Checked:
                self.pyLong.projet.groupes.pop(i+1)
                self.pyLong.listeAnnotations.groupes.removeItem(i+1)
        self.accept()
