from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.Layout import *
from pyLong.Subplot import *


class DialogAjoutLayout(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Ajouter une mise en page")
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Nouvelle mise en page")
        layout = QGridLayout()
        
        label = QLabel("Intitulé :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.intitule = QLineEdit()
        self.intitule.setText("layout {}".format(Layout.compteur + 1))
        layout.addWidget(self.intitule, 0, 1)
        
        self.dupliquer = QCheckBox("Dupliquer la mise en page :")
        self.dupliquer.stateChanged.connect(self.updateInterface)
        layout.addWidget(self.dupliquer, 1, 0)
        
        self.listeLayouts = QComboBox()
        for laYout in self.pyLong.projet.layouts:
            self.listeLayouts.addItem(laYout.intitule)
        self.listeLayouts.setCurrentText(self.pyLong.listeLayouts.currentText())
        layout.addWidget(self.listeLayouts, 1, 1)
        
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
        
        self.updateInterface()
        
    def updateInterface(self):
        if self.dupliquer.isChecked():
            self.listeLayouts.setEnabled(True)
        else:
            self.listeLayouts.setEnabled(False)
            
    def appliquer(self):
        layout = Layout()
        layout.intitule = self.intitule.text()
        
        if self.dupliquer.isChecked():
            i = self.listeLayouts.currentIndex()
            layoutReference = self.pyLong.projet.layouts[i]

            layout.dimensions['largeur'] = layoutReference.dimensions['largeur']
            layout.dimensions['hauteur'] = layoutReference.dimensions['hauteur']
            layout.format = layoutReference.format
            layout.axeSecondaire = layoutReference.axeSecondaire
            
            layout.abscisses['min'] = layoutReference.abscisses['min']
            layout.abscisses['max'] = layoutReference.abscisses['max']
            layout.abscisses['intervalles'] = layoutReference.abscisses['intervalles']
            
            layout.altitudes['min'] = layoutReference.altitudes['min']
            layout.altitudes['max'] = layoutReference.altitudes['max']
            layout.altitudes['intervalles'] = layoutReference.altitudes['intervalles']
            
            layout.pentes['min %'] = layoutReference.pentes['min %']
            layout.pentes['max %'] = layoutReference.pentes['max %']
            layout.pentes['min °'] = layoutReference.pentes['min °']
            layout.pentes['max °'] = layoutReference.pentes['max °']
            layout.pentes['intervalles %'] = layoutReference.pentes['intervalles %']
            layout.pentes['intervalles °'] = layoutReference.pentes['intervalles °']
            
            layout.legende['active'] = layoutReference.legende['active']
            layout.legende['cadre'] = layoutReference.legende['cadre']
            layout.legende['nombre de colonnes'] = layoutReference.legende['nombre de colonnes']
            layout.legende['taille'] = layoutReference.legende['taille']
            layout.legende['position'] = layoutReference.legende['position']
            
            layout.grille['active'] = layoutReference.grille['active']
            layout.grille['style'] = layoutReference.grille['style']
            layout.grille['épaisseur'] = layoutReference.grille['épaisseur']
            layout.grille['opacité'] = layoutReference.grille['opacité']
            
            layout.abscisses['libellé'] = layoutReference.abscisses['libellé']
            layout.altitudes['libellé'] = layoutReference.altitudes['libellé']
            layout.pentes['libellé'] = layoutReference.pentes['libellé']
            
            layout.abscisses['taille libellé'] = layoutReference.abscisses['taille libellé']
            layout.altitudes['taille libellé'] = layoutReference.altitudes['taille libellé']
            layout.pentes['taille libellé'] = layoutReference.pentes['taille libellé']
            
            layout.abscisses['couleur libellé'] = layoutReference.abscisses['couleur libellé']
            layout.altitudes['couleur libellé'] = layoutReference.altitudes['couleur libellé']
            layout.pentes['couleur libellé'] = layoutReference.pentes['couleur libellé']
            
            layout.abscisses['taille valeur'] = layoutReference.abscisses['taille valeur']
            layout.altitudes['taille valeur'] = layoutReference.altitudes['taille valeur']
            layout.pentes['taille valeur'] = layoutReference.pentes['taille valeur']
            
            layout.abscisses['couleur valeur'] = layoutReference.abscisses['couleur valeur']
            layout.altitudes['couleur valeur'] = layoutReference.altitudes['couleur valeur']
            layout.pentes['couleur valeur'] = layoutReference.pentes['couleur valeur']
            
            layout.abscisses['delta gauche'] = layoutReference.abscisses['delta gauche']
            layout.abscisses['delta droite'] = layoutReference.abscisses['delta droite']
            
            layout.altitudes['delta bas'] = layoutReference.altitudes['delta bas']
            layout.altitudes['delta haut'] = layoutReference.altitudes['delta haut']
            
            layout.pentes['delta bas %'] = layoutReference.pentes['delta bas %']
            layout.pentes['delta haut %'] = layoutReference.pentes['delta haut %']
    
            layout.pentes['delta bas °'] = layoutReference.pentes['delta bas °']
            layout.pentes['delta haut °'] = layoutReference.pentes['delta haut °']

            layout.subdivisions = layoutReference.subdivisions
            layout.hspace = layoutReference.hspace

            for subplotReference in layoutReference.subplots:
                subplot = Subplot()

                subplot.identifiant = subplotReference.identifiant

                subplot.subdivisions = subplotReference.subdivisions

                subplot.ordonnees['min'] = subplotReference.ordonnees['min']
                subplot.ordonnees['max'] = subplotReference.ordonnees['max']
                subplot.ordonnees['libellé'] = subplotReference.ordonnees['libellé']
                subplot.ordonnees['intervalles'] = subplotReference.ordonnees['intervalles']
                subplot.ordonnees['couleur libellé'] = subplotReference.ordonnees['couleur libellé']
                subplot.ordonnees['couleur valeur'] = subplotReference.ordonnees['couleur valeur']
                subplot.ordonnees['delta bas'] = subplotReference.ordonnees['delta bas']
                subplot.ordonnees['delta haut'] = subplotReference.ordonnees['delta haut']

                subplot.legende['active'] = subplotReference.legende['active']
                subplot.legende['position'] = subplotReference.legende['position']
                subplot.legende['nombre de colonnes'] = subplotReference.legende['nombre de colonnes']

                layout.subplots.append(subplot)
            
            self.pyLong.projet.layouts.append(layout)
        else:
            self.pyLong.projet.layouts.append(layout)
            
        self.pyLong.listeLayouts.addItem(layout.intitule)
        n = self.pyLong.listeLayouts.count()
        self.pyLong.listeLayouts.setCurrentIndex(n - 1)
        
    def valider(self):
        self.appliquer()
        self.pyLong.canvas.dessiner()
        self.accept()
