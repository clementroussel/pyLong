from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from pyLong.dictionnaires import *

import numpy as np
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, symbolePente):
        super().__init__()
        self._data = data
        self.hearder_labels = ['Abscisses (m)', 'Altitudes (m)', 'Pentes ({})'.format(symbolePente)]
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 2:
                value = self._data[index.row(), index.column()]
                return str(np.round(value, 2))
            else:
                value = self._data[index.row(), index.column()]
                return str(np.round(value, 3))
        
        if role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float):
                return Qt.AlignVCenter | Qt.AlignRight
        
    def rowCount(self, index):
        return self._data.shape[0]
    
    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal :
            return self.hearder_labels[section]
        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return section + 1


class DialogTableauValeurs(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.setMinimumWidth(650)
        self.setMinimumHeight(650)
    
        self.pyLong = parent
        
        self.symbolePente = self.pyLong.projet.preferences['pente']
        
        i = self.pyLong.listeProfils.liste.currentRow()
        self.setWindowTitle("Tableau des valeurs du profil \"{}\"".format(self.pyLong.listeProfils.liste.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/tableau.png')))
        
        self.zprofil, self.pprofil = self.pyLong.projet.profils[i]
    
        mainLayout = QGridLayout()
        
        groupe = QGroupBox("Copier vers le presse-papier")
        layout = QGridLayout()
        
        label = QLabel("Délimiteur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.delimiteurCopier = QComboBox()
        self.delimiteurCopier.insertItems(0, list(delimiteurs.keys()))
        self.delimiteurCopier.setCurrentText("tabulation")
        layout.addWidget(self.delimiteurCopier, 0, 1)
        
        label = QLabel("Séparateur décimal :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.separateurCopier = QComboBox()
        self.separateurCopier.insertItems(0, list(separateurs.keys()))
        layout.addWidget(self.separateurCopier, 1, 1)
        
        copier = QPushButton("Copier")
        copier.setAutoDefault(False)
        copier.clicked.connect(self.copier)
        layout.addWidget(copier, 2, 0, 1, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 0, 0)
        
        groupe = QGroupBox("Coller depuis le presse-papier")
        layout = QGridLayout()
        
        label = QLabel("Délimiteur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.delimiteurColler = QComboBox()
        self.delimiteurColler.insertItems(0, list(delimiteurs.keys()))
        self.delimiteurColler.setCurrentText("tabulation")
        layout.addWidget(self.delimiteurColler, 0, 1)
        
        label = QLabel("Séparateur décimal :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.separateurColler = QComboBox()
        self.separateurColler.insertItems(0, list(separateurs.keys()))
        layout.addWidget(self.separateurColler, 1, 1)
        
        coller = QPushButton("Coller")
        coller.setAutoDefault(False)
        coller.clicked.connect(self.coller)
        layout.addWidget(coller, 2, 0, 1, 2)
        
        groupe.setLayout(layout)
        mainLayout.addWidget(groupe, 1, 0)
        
        self.table = QTableView()

        n = np.shape(self.zprofil.abscisses)[0]
        
        self.data = np.nan * np.ones((n, 3))
        
        self.data[:, 0] = self.zprofil.abscisses
        self.data[:, 1] = self.zprofil.altitudes

        if self.symbolePente == "%":
            self.data[:-1, 2] = self.pprofil.pentesPourcents
        else:
            self.data[:-1, 2] = self.pprofil.pentesDegres
        
        self.model = TableModel(self.data, self.symbolePente)
        self.table.setModel(self.model)
        mainLayout.addWidget(self.table, 0, 1, 10, 1)
        
        self.setLayout(mainLayout)
        
    def copier(self):
        if self.separateurCopier.currentText() == "virgule":
            pd.DataFrame(self.data[:,0:2]).applymap(lambda x: str(x).replace('.', ',')).to_clipboard(index=False,
                                                                                                     header=False,
                                                                                                     sep=delimiteurs[self.delimiteurCopier.currentText()])
        else:
            pd.DataFrame(self.data[:, 0:2]).to_clipboard(index=False,
                                                         header=False,
                                                         sep=delimiteurs[self.delimiteurCopier.currentText()])
        
    def coller(self):
        try:
            if self.separateurColler.currentText() == "virgule":
                df = pd.read_clipboard(header=None,
                                       sep=delimiteurs[self.delimiteurColler.currentText()]).dropna().applymap(lambda x: float(x.replace(',', '.')))
            else:
                df = pd.read_clipboard(header=None,
                                       sep=delimiteurs[self.delimiteurColler.currentText()]).dropna()
                
            values = np.array(df)
                
            if np.shape(values)[1] == 2 and np.shape(values)[0] > 1:
                n = np.shape(values)[0]
                self.data = np.nan * np.ones((n, 3))
                
                self.data[:, 0] = values[:, 0]
                self.data[:, 1] = values[:, 1]
                
                self.zprofil.abscisses = values[:, 0]
                self.zprofil.altitudes = values[:, 1]
                
                self.pprofil.updateData(values[:, 0], values[:, 1])
                
                self.zprofil.update()
                self.pprofil.update()

                self.pyLong.canvas.dessiner()
                
                if self.symbolePente == "%":
                    self.data[:-1, 2] = self.pprofil.pentesPourcents
                else:
                    self.data[:-1, 2] = self.pprofil.pentesDegres
                
                self.model = TableModel(self.data, self.symbolePente)
                self.table.setModel(self.model)
            
            else:
                alerte = QMessageBox(self)
                alerte.setText("L'importation des valeurs a échoué.")
                alerte.exec_()
                return 0
            
        except:
            alerte = QMessageBox(self)
            alerte.setText("L'importation des valeurs a échoué.")
            alerte.exec_()
            return 0