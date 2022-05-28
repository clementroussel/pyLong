from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.Layout import *


class DialogSupprimerLayouts(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Supprimer des mises en page")
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Supprimer les mises en page :")
        layout = QVBoxLayout()
        
        self.listeLayouts = QListWidget()
        for l in self.pyLong.projet.layouts[1:]:
            item = QListWidgetItem()
            item.setText(l.intitule)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listeLayouts.addItem(item)
        
        layout.addWidget(self.listeLayouts)
        groupe.setLayout(layout)
        
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonBox)
        
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
        
    def valider(self):
        n = self.pyLong.listeLayouts.count()
        n -= 1
        for i in range(n-1, -1, -1):
            if self.listeLayouts.item(i).checkState() == Qt.Checked:
                self.pyLong.projet.layouts.pop(i+1)
                self.pyLong.listeLayouts.removeItem(i+1)
        self.accept()
