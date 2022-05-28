from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import pandas as pd
import numpy as np

from pyLong.dictionnaires import *
from pyLong.zProfil import *
from pyLong.pProfil import *
from pyLong.AnnotationPonctuelle import *


class DialogAjusterAnnotations(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Ajuster les annotations ponctuelles")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/ajuster.png')))
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()

        self.zConstant = QRadioButton("Altitude constante")
        self.zConstant.setChecked(True)
        layout.addWidget(self.zConstant, 0, 0)

        self.altitude = QDoubleSpinBox()
        self.altitude.setFixedWidth(90)
        self.altitude.setSuffix(" m")
        self.altitude.setLocale(QLocale('English'))
        self.altitude.setSingleStep(10)
        self.altitude.setRange(-99999.999, 99999.999)
        self.altitude.setDecimals(3)
        layout.addWidget(self.altitude, 0, 1)

        self.surProfil = QRadioButton("Ajuster au profil")
        layout.addWidget(self.surProfil, 1, 0)

        self.profils = QComboBox()

        for zprofil, pprofil in self.pyLong.projet.profils:
            self.profils.addItem(zprofil.intitule)
        layout.addWidget(self.profils, 1, 1)

        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close | QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Close).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).setText("Appliquer")
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.valider)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)

        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

    def valider(self):
        self.appliquer()
        self.accept()

    def appliquer(self):
        indices = []
        for item in self.pyLong.listeAnnotations.liste.selectedIndexes():
            indices.append(item.row())

        indices.sort()
        indices.reverse()

        j = self.pyLong.listeAnnotations.groupes.currentIndex()

        if len(indices) == 1:
            i = indices[0]

            annotation = self.pyLong.projet.groupes[j].annotations[i]

            if type(annotation) == AnnotationPonctuelle:
                if self.zConstant.isChecked():
                    annotation.altitude = self.altitude.value()
                    annotation.update()

                else:
                    k = self.profils.currentIndex()
                    if k != -1:
                        zprofil, pprofil = self.pyLong.projet.profils[k]
                        try:
                            annotation.altitude = zprofil.interpoler(annotation.abscisse)
                            annotation.update()
                        except:
                            pass

                self.pyLong.canvas.draw()

        else:
            for i in indices:
                annotation = self.pyLong.projet.groupes[j].annotations[i]

                if type(annotation) == AnnotationPonctuelle:
                    if self.zConstant.isChecked():
                        annotation.altitude = self.altitude.value()
                        annotation.update()

                    else:
                        k = self.profils.currentIndex()
                        if k != -1:
                            zprofil, pprofil = self.pyLong.projet.profils[k]
                            try:
                                annotation.altitude = zprofil.interpoler(annotation.abscisse)
                                annotation.update()
                            except:
                                pass

            self.pyLong.canvas.draw()


        # if self.zConstant.isChecked():
        #     print("toto")
        # else:
        #     print("tata")
        
    # def parcourir(self):
    #     chemin = QFileDialog.getOpenFileName(caption="Importer un profil",
    #                                          filter="fichier texte (*.txt)")[0]
    #     self.chemin.setText(chemin)
    #
    # def importer(self):
    #     if self.chemin.text() == "":
    #         alerte = QMessageBox(self)
    #         alerte.setText("Renseignez un fichier.")
    #         alerte.exec_()
    #         return 0
    #
    #     else:
    #         try:
    #             profil = pd.read_csv(self.chemin.text(),
    #                                  delimiter=delimiteurs[self.delimiteur.currentText()],
    #                                  decimal=separateurs[self.separateur.currentText()],
    #                                  skiprows=0,
    #                                  encoding='utf-8').values
    #
    #             xz = np.array(profil[:,:2].astype('float'))
    #
    #             if np.shape(xz[:,0])[0] < 2:
    #                 alerte = QMessageBox(self)
    #                 alerte.setText("Le profil doit contenir au moins 2 points.")
    #                 alerte.exec_()
    #                 return 0
    #
    #             else:
    #                 zprofil = zProfil()
    #
    #                 zprofil.intitule = self.intitule.text()
    #                 zprofil.abscisses = xz[:,0]
    #                 zprofil.altitudes = xz[:,1]
    #
    #                 zprofil.trier(mode=self.pyLong.projet.preferences['sens'])
    #                 zprofil.update()
    #
    #                 if zprofil.altitudes[0] == xz[0, 1]:
    #                     tri = False
    #                 else:
    #                     tri = True
    #
    #                 pprofil = pProfil()
    #                 pprofil.updateData(zprofil.abscisses, zprofil.altitudes)
    #                 pprofil.update()
    #
    #                 self.pyLong.projet.profils.append((zprofil, pprofil))
    #                 self.pyLong.listeProfils.update()
    #                 # self.pyLong.canvas.dessiner()
    #                 self.pyLong.canvas.ax_z.add_line(zprofil.line)
    #                 self.pyLong.canvas.draw()
    #
    #             if self.annotations.isChecked():
    #                 try:
    #                     annotations = list(profil[:, 2])
    #                     for i, libelle in enumerate(annotations):
    #                         if libelle is not np.nan and str(libelle) != 'nan':
    #                             ap = AnnotationPonctuelle()
    #                             ap.libelle = str(libelle)
    #                             ap.intitule = str(libelle)
    #
    #                             if not tri:
    #                                 ap.abscisse = xz[i, 0]
    #                             else:
    #                                 n = len(annotations)
    #                                 ap.abscisse = zprofil.abscisses[n-1-i]
    #
    #                             ap.altitude = xz[i, 1]
    #                             ap.update()
    #
    #                             j = self.pyLong.listeAnnotations.groupes.currentIndex()
    #                             self.pyLong.projet.groupes[j].annotations.append(ap)
    #
    #                             self.pyLong.canvas.ax_z.add_artist(ap.annotation)
    #
    #                     self.pyLong.listeAnnotations.updateListe()
    #                     self.pyLong.canvas.draw()
    #                     self.accept()
    #
    #                 except:
    #                     self.accept()
    #
    #             else:
    #                 self.accept()
    #
    #         except:
    #             alerte = QMessageBox(self)
    #             alerte.setText("Fichier illisible.")
    #             alerte.exec_()
