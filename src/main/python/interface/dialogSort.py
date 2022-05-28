from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionnaires import *


class DialogTrier(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
 
        mainLayout = QVBoxLayout()
        
        i = self.pyLong.listeProfils.liste.currentRow()
        self.setWindowTitle("Trier le profil \"{}\"".format(self.pyLong.listeProfils.liste.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/trier.png')))
        
        self.zprofil, self.pprofil = self.pyLong.projet.profils[i]
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()
        
        label = QLabel("Sens :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.sens = QComboBox()
        self.sens.addItem("ascendant")
        self.sens.addItem("descendant")
        self.sens.currentTextChanged.connect(self.apercu)
        layout.addWidget(self.sens, 0, 1)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.reject)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

        self.pyLong.projet.apercu.visible = True
        self.pyLong.projet.apercu.abscisses = self.zprofil.abscisses
        self.pyLong.projet.apercu.altitudes = self.zprofil.altitudes
        self.pyLong.projet.apercu.update()
        
        # self.pyLong.canvas.ax_z.add_line(self.pyLong.projet.apercu.line)
        self.pyLong.canvas.draw()
        
        self.apercu()
        
    def apercu(self):
        if self.sens.currentText() == "ascendant":
            self.pyLong.projet.apercu.trier(mode="ascendant")
            
        else:
            self.pyLong.projet.apercu.trier(mode="descendant")

        # self.pyLong.projet.apercu.abscisses = self.zprofil.abscisses
        # self.pyLong.projet.apercu.altitudes = self.zprofil.altitudes
        self.pyLong.projet.apercu.update()
        
        self.pyLong.canvas.draw()
        
    def valider(self):
        if self.sens.currentText() == "ascendant":
            self.zprofil.trier(mode="ascendant")
        else:
            self.zprofil.trier(mode="descendant")
            
        self.pprofil.updateData(self.zprofil.abscisses, self.zprofil.altitudes)
        
        self.zprofil.update()
        self.pprofil.update()

        if self.pprofil.pentesVisibles:
            self.pyLong.canvas.dessiner()
        
        self.accept()
