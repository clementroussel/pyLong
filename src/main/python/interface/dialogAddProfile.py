from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionaries import separators, delimiters
from pyLong.zProfile import zProfile
from pyLong.sProfile import sProfile
from pyLong.verticalAnnotation import VerticalAnnotation


class DialogAddProfile(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Add a new profile")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/addProfile.png')))
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Delimiter :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.delimiter = QComboBox()
        self.delimiter.insertItems(0, list(delimiters.keys()))
        self.delimiter.setCurrentText("tabulation")
        layout.addWidget(self.delimiter, 0, 1)
        
        label = QLabel("Decimal separator :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.separator = QComboBox()
        self.separator.insertItems(0, list(separators.keys()))
        layout.addWidget(self.separator, 1, 1)
        
        self.importAnnotations = QCheckBox("Import annotations")
        layout.addWidget(self.importAnnotations, 2, 0, 1, 2)
        
        label = QLabel("Path :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.path = QLineEdit()
        layout.addWidget(self.path, 3, 1)
        
        browse = QPushButton("...")
        browse.setFixedWidth(20)
        browse.clicked.connect(self.browse)
        layout.addWidget(browse, 3, 2)
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.title = QLineEdit()
        self.title.setText("profile n°{}".format(zProfile.counter + 1))
        layout.addWidget(self.title, 4, 1)
    
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        layout = QHBoxLayout()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Close")
        # buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.importer)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(buttonBox)
        mainLayout.addLayout(layout)
        
        self.setLayout(mainLayout)

    # def updateAxes(self):
    #     i = self.pyLong.listeLayouts.currentIndex()
    #     self.layout = self.pyLong.projet.layouts[i]

    #     self.pyLong.canvas.ax_z.set_xlim((self.layout.abscisses['min'] - self.layout.abscisses['delta gauche'],
    #                                       self.layout.abscisses['max'] + self.layout.abscisses['delta droite']))

    #     self.pyLong.canvas.ax_z.set_xticks(np.linspace(self.layout.abscisses['min'],
    #                                                    self.layout.abscisses['max'],
    #                                                    self.layout.abscisses['intervalles'] + 1))

    #     for ax in self.pyLong.canvas.subplots:
    #         ax.set_xlim((self.layout.abscisses['min'] - self.layout.abscisses['delta gauche'],
    #                      self.layout.abscisses['max'] + self.layout.abscisses['delta droite']))

    #         ax.set_xticks(np.linspace(self.layout.abscisses['min'],
    #                                   self.layout.abscisses['max'],
    #                                   self.layout.abscisses['intervalles'] + 1))

    #     self.pyLong.canvas.ax_z.set_ylim((self.layout.altitudes['min'] - self.layout.altitudes['delta bas'],
    #                                       self.layout.altitudes['max'] + self.layout.altitudes['delta haut']))

    #     self.pyLong.canvas.ax_z.set_yticks(np.linspace(self.layout.altitudes['min'],
    #                                                    self.layout.altitudes['max'],
    #                                                    self.layout.altitudes['intervalles'] + 1))

    #     self.pyLong.canvas.draw()
        
    def browse(self):
        path = QFileDialog.getOpenFileName(caption="Add a new profile",
                                           filter="text file (*.txt)")[0]
        self.path.setText(path)

    def importer(self):
        if self.chemin.text() == "":
            alerte = QMessageBox(self)
            alerte.setText("Renseignez un fichier.")
            alerte.exec_()
            return 0

        else:
            try:
                profil = pd.read_csv(self.chemin.text(),
                                     delimiter=delimiteurs[self.delimiteur.currentText()],
                                     decimal=separateurs[self.separateur.currentText()],
                                     skiprows=0,
                                     encoding='utf-8').values

                xz = np.array(profil[:,:2].astype('float'))

                if np.shape(xz[:,0])[0] < 2:
                    alerte = QMessageBox(self)
                    alerte.setText("Le profil doit contenir au moins 2 points.")
                    alerte.exec_()
                    return 0

                else:
                    zprofil = zProfil()

                    zprofil.intitule = self.intitule.text()
                    zprofil.abscisses = xz[:,0]
                    zprofil.altitudes = xz[:,1]

                    zprofil.trier(mode=self.pyLong.projet.preferences['sens'])
                    zprofil.update()

                    if zprofil.altitudes[0] == xz[0, 1]:
                        tri = False
                    else:
                        tri = True

                    pprofil = pProfil()
                    pprofil.updateData(zprofil.abscisses, zprofil.altitudes)
                    pprofil.update()

                    self.pyLong.projet.profils.append((zprofil, pprofil))
                    self.pyLong.listeProfils.update()
                    self.pyLong.canvas.ax_z.add_line(zprofil.line)
                    self.pyLong.canvas.updateLegendes()

                    if len(self.pyLong.projet.profils) == 1:
                        i = self.pyLong.listeLayouts.currentIndex()
                        self.layout = self.pyLong.projet.layouts[i]

                        self.layout.abscisses['min'] = np.min(zprofil.abscisses)
                        self.layout.abscisses['max'] = np.max(zprofil.abscisses)

                        self.layout.altitudes['min'] = np.min(zprofil.altitudes)
                        self.layout.altitudes['max'] = np.max(zprofil.altitudes)

                        self.updateAxes()

                if self.annotations.isChecked():
                    try:
                        annotations = list(profil[:, 2])
                        for i, libelle in enumerate(annotations):
                            if libelle is not np.nan and str(libelle) != 'nan':
                                ap = AnnotationPonctuelle()
                                ap.libelle = str(libelle)
                                ap.intitule = str(libelle)

                                if not tri:
                                    ap.abscisse = xz[i, 0]
                                else:
                                    n = len(annotations)
                                    ap.abscisse = zprofil.abscisses[n-1-i]

                                ap.altitude = xz[i, 1]
                                ap.update()

                                j = self.pyLong.listeAnnotations.groupes.currentIndex()
                                self.pyLong.projet.groupes[j].annotations.append(ap)

                                self.pyLong.canvas.ax_z.add_artist(ap.annotation)

                        self.pyLong.listeAnnotations.updateListe()
                        self.pyLong.canvas.draw()
                        self.accept()

                    except:
                        self.accept()

                else:
                    self.accept()

            except:
                alerte = QMessageBox(self)
                alerte.setText("Fichier illisible.")
                alerte.exec_()
