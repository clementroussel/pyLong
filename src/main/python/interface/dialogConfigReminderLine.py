from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionnaires import *
from CheckableComboBox import *


class DialogConfigLigneRappel(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.pyLong = parent.pyLong
        
        i = self.parent.liste.currentRow()
        self.ligne = self.pyLong.projet.lignesRappel[i]
        
        self.setWindowTitle("Propriétés")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/config.png')))
        
        mainLayout = QVBoxLayout()

        layout = QGridLayout()
        
        # label = QLabel("Délimiteur :")
        # label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # layout.addWidget(label, 0, 0)
        #
        # self.delimiteur = QComboBox()
        # self.delimiteur.insertItems(0, list(delimiteurs.keys()))
        # self.delimiteur.setCurrentText("tabulation")
        # layout.addWidget(self.delimiteur, 0, 1)
        #
        # label = QLabel("Séparateur décimal :")
        # label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # layout.addWidget(label, 1, 0)
        #
        # self.separateur = QComboBox()
        # self.separateur.insertItems(0, list(separateurs.keys()))
        # layout.addWidget(self.separateur, 1, 1)
    
        label = QLabel("Abscisse :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.abscisse = QDoubleSpinBox()
        self.abscisse.setFixedWidth(90)
        self.abscisse.setSuffix(" m")
        self.abscisse.setLocale(QLocale('English'))
        self.abscisse.setRange(0, 99999.999)
        self.abscisse.setSingleStep(0.1)
        self.abscisse.setDecimals(3)
        self.abscisse.setValue(self.ligne.abscisse)
        layout.addWidget(self.abscisse, 0, 1)

        # label = QLabel("Subplots :")
        # label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # layout.addWidget(label, 1, 0)
        mainLayout.addLayout(layout)

        groupe = QGroupBox("Subplots")
        sublayout = QVBoxLayout()

        self.liste = QListWidget()
        for subplot in self.pyLong.projet.subplots:
            item = QListWidgetItem()
            item.setText(subplot)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if subplot in self.ligne.subplots:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.liste.addItem(item)

        sublayout.addWidget(self.liste)
        groupe.setLayout(sublayout)


        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.rejected.connect(self.reject)
        
        mainLayout.addWidget(buttonBox)        
        self.setLayout(mainLayout)

    def valider(self):
        self.ligne.abscisse = self.abscisse.value()
        self.ligne.subplots.clear()

        for i in range(self.liste.count()):
            if self.liste.item(i).checkState() == Qt.Checked:
                self.ligne.subplots.append(self.liste.item(i).text())

        self.parent.update()
        self.accept()

    # def exporter(self):
    #     try:
    #         i = self.pyLong.listeProfils.liste.currentRow()
    #         zprofil, pprofil = self.pyLong.projet.profils[i]
    #
    #         chemin = QFileDialog.getSaveFileName(caption="Exporter un profil",
    #                                              filter="fichier texte (*.txt)")[0]
    #
    #         if chemin == "":
    #             return 0
    #
    #         else:
    #             nomFichier = QFileInfo(chemin).fileName()
    #             repertoireFichier = QFileInfo(chemin).absolutePath()
    #             nomFichier = nomFichier.split(".")[0]
    #             nomFichier += ".txt"
    #             chemin = repertoireFichier + "/" + nomFichier
    #
    #             delimiteur = delimiteurs[self.delimiteur.currentText()]
    #             formatage = "%.{}f".format(self.decimales.value())
    #             separateur = separateurs[self.separateur.currentText()]
    #
    #             zprofil.exporter(chemin, delimiteur, formatage, separateur)
    #
    #         self.accept()
    #
    #     except:
    #         alerte = QMessageBox(self)
    #         alerte.setText("L'exportation a échoué !")
    #         alerte.exec_()
    #         pass