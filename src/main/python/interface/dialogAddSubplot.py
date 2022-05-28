from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogAjoutSubplot(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.pyLong = parent.pyLong
        
        self.setWindowTitle("Ajouter un subplot")
        self.setMinimumWidth(250)
        
        mainLayout = QVBoxLayout()

        sublayout = QHBoxLayout()

        label = QLabel("Identifiant :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label)

        self.identifiant = QLineEdit()
        sublayout.addWidget(self.identifiant)

        mainLayout.addLayout(sublayout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.rejected.connect(self.accept)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def valider(self):
        if self.identifiant.text().replace(" ", "").replace("\t", "") == "" :
            pass
        elif self.identifiant.text().upper() not in self.pyLong.projet.subplots:
            self.pyLong.projet.subplots.append(self.identifiant.text().upper())
            self.accept()
        else:
            alerte = QMessageBox(self)
            alerte.setText("Cet identifiant est déjà utilisé.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()
