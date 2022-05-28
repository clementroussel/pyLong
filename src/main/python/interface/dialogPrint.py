from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionnaires import *

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib import pyplot as plt

import numpy as np

from pyLong.Texte import *
from pyLong.AnnotationPonctuelle import *
from pyLong.AnnotationLineaire import *
from pyLong.Zone import *
from pyLong.Rectangle import *

from pyLong.LigneEnergie import *
from pyLong.Rickenmann import *
from pyLong.FlowR import *
from pyLong.Corominas import *
from pyLong.Mezap import *

from pyLong.LigneRappel import *


class DialogImprimer(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.listeLayouts.currentIndex()
        self.layout = self.pyLong.projet.layouts[i]

        largeur = self.layout.dimensions['largeur']
        hauteur = self.layout.dimensions['hauteur']

        self.setMinimumWidth(225)
        self.setWindowTitle("Exporter la figure")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/imprimer.png')))
        
        mainLayout = QVBoxLayout()
        
        groupe = QGroupBox("Paramètres")
        layout = QGridLayout()
        
        label = QLabel("Format :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.extension = QComboBox()
        self.extension.insertItems(0, list(extensions.keys()))
        self.extension.setCurrentText(self.pyLong.projet.preferences['extension'])
        layout.addWidget(self.extension, 0, 1)
        
        label = QLabel("Largeur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.largeur = QDoubleSpinBox()
        self.largeur.setFixedWidth(75)
        self.largeur.setSuffix(" cm")
        self.largeur.setLocale(QLocale('English'))
        self.largeur.setSingleStep(0.1)
        self.largeur.setRange(0.1, 118.9)
        self.largeur.setDecimals(1)
        self.largeur.setValue(self.layout.dimensions['largeur'])
        layout.addWidget(self.largeur, 1, 1)

        label = QLabel("Hauteur :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.hauteur = QDoubleSpinBox()
        self.hauteur.setFixedWidth(75)
        self.hauteur.setSuffix(" cm")
        self.hauteur.setLocale(QLocale('English'))
        self.hauteur.setSingleStep(0.1)
        self.hauteur.setRange(0.1, 118.9)
        self.hauteur.setDecimals(1)
        self.hauteur.setValue(self.layout.dimensions['hauteur'])
        layout.addWidget(self.hauteur, 2, 1)

        label = QLabel("Résolution :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.dpi = QSpinBox()
        self.dpi.setFixedWidth(75)
        self.dpi.setSuffix(" dpi")
        self.dpi.setSingleStep(25)
        self.dpi.setRange(25, 1000)
        self.dpi.setValue(self.pyLong.projet.preferences['dpi'])
        layout.addWidget(self.dpi, 3, 1)

        groupe.setLayout(layout)
        mainLayout.addWidget(groupe)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("Fermer")
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.imprimer)
        buttonBox.rejected.connect(self.reject)

        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def imprimer(self):
        i = self.pyLong.listeLayouts.currentIndex()
        layout = self.pyLong.projet.layouts[i]

        symbolePente = self.pyLong.projet.preferences['pente']

        n_subdivisions = layout.subdivisions
        n_subplots = len(layout.subplots)
        n_subdivisions_subplots = 0
        for subplot in layout.subplots:
            n_subdivisions_subplots += subplot.subdivisions

        figure = Figure(figsize=(self.largeur.value() / 2.54, self.hauteur.value() / 2.54))
        gs = GridSpec(n_subdivisions, 1, figure=figure)
        ax_z = figure.add_subplot(gs[0:n_subdivisions - n_subdivisions_subplots, :])

        ax_p = ax_z.twinx()

        ax_z.set_xlim((layout.abscisses['min'] - layout.abscisses['delta gauche'],
                       layout.abscisses['max'] + layout.abscisses['delta droite']))

        ax_z.tick_params(axis='x',
                         colors=couleurs[layout.abscisses['couleur valeur']],
                         labelsize=layout.abscisses['taille valeur'])

        ax_z.set_xticks(np.linspace(layout.abscisses['min'],
                                    layout.abscisses['max'],
                                    layout.abscisses['intervalles'] + 1))

        ax_z.set_ylim((layout.altitudes['min'] - layout.altitudes['delta bas'],
                       layout.altitudes['max'] + layout.altitudes['delta haut']))

        ax_z.set_ylabel(layout.altitudes['libellé'],
                        {'color': couleurs[layout.altitudes['couleur libellé']],
                         'fontsize': layout.altitudes['taille libellé']})

        ax_z.tick_params(axis='y',
                         colors=couleurs[layout.altitudes['couleur valeur']],
                         labelsize=layout.altitudes['taille valeur'])

        ax_z.set_yticks(np.linspace(layout.altitudes['min'],
                                    layout.altitudes['max'],
                                    layout.altitudes['intervalles'] + 1))

        if n_subdivisions > 1 and n_subplots > 0:
            ax_z.xaxis.set_ticks_position('top')
        else:
            ax_z.set_xlabel(layout.abscisses['libellé'],
                            {'color': couleurs[layout.abscisses['couleur libellé']],
                            'fontsize': layout.abscisses['taille libellé']})

        ax_z.grid(visible=layout.grille['active'],
                  which='major',
                  axis='both',
                  linestyle=styles2ligne[layout.grille['style']],
                  linewidth=layout.grille['épaisseur'],
                  alpha=layout.grille['opacité'],
                  zorder=layout.grille['ordre'])

        ax_p.set_ylim(
            (layout.pentes['min {}'.format(symbolePente)] - layout.pentes['delta bas {}'.format(symbolePente)],
             layout.pentes['max {}'.format(symbolePente)] + layout.pentes['delta haut {}'.format(symbolePente)]))

        ax_p.set_ylabel(layout.pentes['libellé'],
                        {'color': couleurs[layout.pentes['couleur libellé']],
                         'fontsize': layout.pentes['taille libellé']})

        ax_p.tick_params(axis='y',
                         colors=couleurs[layout.pentes['couleur valeur']],
                         labelsize=layout.pentes['taille valeur'])

        ax_p.set_yticks(np.linspace(layout.pentes['min {}'.format(symbolePente)],
                                    layout.pentes['max {}'.format(symbolePente)],
                                    layout.pentes['intervalles {}'.format(symbolePente)] + 1))

        labelsPente = [str(np.round(p, 1)) + '{}'.format(symbolePente) for p in
                       np.linspace(layout.pentes['min {}'.format(symbolePente)],
                                   layout.pentes['max {}'.format(symbolePente)],
                                   layout.pentes['intervalles {}'.format(symbolePente)] + 1)]

        ax_p.set_yticklabels(labelsPente)

        if layout.axeSecondaire:
            ax_p.set_visible(True)
        else:
            ax_p.set_visible(False)

        n_start = n_subdivisions - n_subdivisions_subplots
        subplots = []
        for i in range(n_subplots):
            subplots.append(figure.add_subplot(gs[n_start:n_start + layout.subplots[i].subdivisions]))
            n_start += layout.subplots[i].subdivisions

            subplots[i].set_ylim((layout.subplots[i].ordonnees['min'] - layout.subplots[i].ordonnees['delta bas'],
                                  layout.subplots[i].ordonnees['max'] + layout.subplots[i].ordonnees['delta haut']))

            subplots[i].set_yticks(np.linspace(layout.subplots[i].ordonnees['min'],
                                               layout.subplots[i].ordonnees['max'],
                                               layout.subplots[i].ordonnees['intervalles'] + 1))

            subplots[i].set_ylabel(layout.subplots[i].ordonnees['libellé'],
                                   {'color': couleurs[layout.subplots[i].ordonnees['couleur libellé']],
                                    'fontsize': layout.altitudes['taille libellé']})

            subplots[i].tick_params(axis='y',
                                    colors=couleurs[layout.subplots[i].ordonnees['couleur valeur']],
                                    labelsize=layout.altitudes['taille valeur'])

            subplots[i].grid(visible=layout.grille['active'],
                             which='major',
                             axis='both',
                             linestyle=styles2ligne[layout.grille['style']],
                             linewidth=layout.grille['épaisseur'],
                             alpha=layout.grille['opacité'],
                             zorder=layout.grille['ordre'])

            subplots[i].set_xlim((layout.abscisses['min'] - layout.abscisses['delta gauche'],
                                  layout.abscisses['max'] + layout.abscisses['delta droite']))

            subplots[i].tick_params(axis='x',
                                    colors=couleurs[layout.abscisses['couleur valeur']],
                                    labelsize=layout.abscisses['taille valeur'])

            subplots[i].set_xticks(np.linspace(layout.abscisses['min'],
                                               layout.abscisses['max'],
                                               layout.abscisses['intervalles'] + 1))

            if i != n_subplots - 1:
                plt.setp(subplots[i].get_xticklabels(), visible=False)
                subplots[i].tick_params(axis='x', length=0)
            else:
                subplots[i].set_xlabel(layout.abscisses['libellé'],
                                       {'color': couleurs[layout.abscisses['couleur libellé']],
                                        'fontsize': layout.abscisses['taille libellé']})

        ax_z.set_zorder(ax_p.get_zorder() + 1)
        ax_z.patch.set_visible(False)

        # zProfils et pProfils
        for zprofil, pprofil in self.pyLong.projet.profils:
            zprofil.clear()
            zprofil.update()
            pprofil.clear()
            pprofil.update()

            ax_z.add_line(zprofil.line)

            if not layout.axeSecondaire and pprofil.marqueursVisibles:
                ax_z.add_line(pprofil.line)

            elif layout.axeSecondaire and symbolePente == "%" and pprofil.marqueursVisibles:
                ax_p.add_line(pprofil.line_pourcents)

            elif layout.axeSecondaire and symbolePente == "°" and pprofil.marqueursVisibles:
                ax_p.add_line(pprofil.line_degres)

            # écriture des pentes
            if pprofil.pentesVisibles and pprofil.actif:
                if not layout.axeSecondaire:
                    if symbolePente == "%":
                        for i in range(len(pprofil.pentes)):
                            ax_z.text(pprofil.abscisses[i],
                                           pprofil.altitudes[i] + pprofil.annotation['décalage z'],
                                           s="{}%".format(str(np.round(pprofil.pentesPourcents[i], 1))),
                                           fontsize=pprofil.annotation['taille'],
                                           color=couleurs[pprofil.annotation['couleur']],
                                           alpha=pprofil.opacite,
                                           horizontalalignment='center',
                                           verticalalignment='center',
                                           rotation=0,
                                           zorder=pprofil.ordre)

                    else:
                        for i in range(len(pprofil.pentes)):
                            ax_z.text(pprofil.abscisses[i],
                                           pprofil.altitudes[i] + pprofil.annotation['décalage z'],
                                           s="{}°".format(str(np.round(pprofil.pentesDegres[i], 1))),
                                           fontsize=pprofil.annotation['taille'],
                                           color=couleurs[pprofil.annotation['couleur']],
                                           alpha=pprofil.opacite,
                                           horizontalalignment='center',
                                           verticalalignment='center',
                                           zorder=pprofil.ordre)

                else:
                    if symbolePente == "%":
                        for i in range(len(pprofil.pentes)):
                            if layout.pentes['min %'] <= pprofil.pentesPourcents[i] <= layout.pentes['max %']:
                                ax_p.text(pprofil.abscisses[i],
                                               pprofil.pentesPourcents[i] + pprofil.annotation['décalage p %'],
                                               s="{}%".format(str(np.round(pprofil.pentesPourcents[i], 1))),
                                               fontsize=pprofil.annotation['taille'],
                                               color=couleurs[pprofil.annotation['couleur']],
                                               alpha=pprofil.opacite,
                                               horizontalalignment='center',
                                               verticalalignment='bottom',
                                               zorder=pprofil.ordre)

                    else:
                        for i in range(len(pprofil.pentes)):
                            if layout.pentes['min °'] <= pprofil.pentesDegres[i] <= layout.pentes['max °']:
                                ax_p.text(pprofil.abscisses[i],
                                               pprofil.pentesDegres[i] + pprofil.annotation['décalage p °'],
                                               s="{}%".format(str(np.round(pprofil.pentesDegres[i], 1))),
                                               fontsize=pprofil.annotation['taille'],
                                               color=couleurs[pprofil.annotation['couleur']],
                                               alpha=pprofil.opacite,
                                               horizontalalignment='center',
                                               verticalalignment='bottom',
                                               zorder=pprofil.ordre)

        # annotations
        for groupe in self.pyLong.projet.groupes:
            if groupe.actif:
                for annotation in groupe.annotations:
                    annotation.clear()
                    annotation.update()
                    if type(annotation) == Texte:
                        ax_z.add_artist(annotation.text)

                    elif type(annotation) == AnnotationPonctuelle:
                        ax_z.add_artist(annotation.annotation)

                    elif type(annotation) == AnnotationLineaire:
                        ax_z.add_artist(annotation.annotation)
                        ax_z.add_artist(annotation.text)

                    elif type(annotation) == Zone:
                        ax_z.add_artist(annotation.text)
                        ax_z.add_line(annotation.left_line)
                        ax_z.add_line(annotation.right_line)

                    elif type(annotation) == Rectangle:
                        ax_z.add_patch(annotation.rectangle)

        # calculs
        for calcul in self.pyLong.projet.calculs:
            calcul.clear()
            calcul.update()
            if type(calcul) in [LigneEnergie, Rickenmann, FlowR, Corominas]:
                ax_z.add_line(calcul.line)

        # légende principale
        if layout.legende['active']:
            if layout.axeSecondaire:
                figure.legend(loc=placementsLegende[layout.legende['position']][0],
                                   ncol=layout.legende['nombre de colonnes'],
                                   fontsize=layout.legende['taille'],
                                   frameon=layout.legende['cadre'],
                                   bbox_to_anchor=placementsLegende[layout.legende['position']][1],
                                   bbox_transform=ax_z.transAxes)
            else:
                ax_z.legend(loc=placementsLegende[layout.legende['position']][0],
                                 ncol=layout.legende['nombre de colonnes'],
                                 fontsize=layout.legende['taille'],
                                 frameon=layout.legende['cadre'],
                                 bbox_to_anchor=placementsLegende[layout.legende['position']][1],
                                 bbox_transform=ax_z.transAxes)

        # autres données
        for donnee in self.pyLong.projet.autresDonnees:
            donnee.clear()
            donnee.update()

            try:
                i = [subplot.identifiant for subplot in layout.subplots].index(donnee.subplot)
            except:
                i = -1

            if i != -1:
                subplots[i].add_line(donnee.line)

        # légende subplots
        for i in range(len(subplots)):
            if layout.subplots[i].legende['active']:
                subplots[i].legend(loc=placementsLegende[layout.subplots[i].legende['position']][0],
                                   ncol=layout.subplots[i].legende['nombre de colonnes'],
                                   fontsize=layout.legende['taille'],
                                   frameon=layout.legende['cadre'],
                                   bbox_to_anchor=placementsLegende[layout.subplots[i].legende['position']][1],
                                   bbox_transform=subplots[i].transAxes)

        # lignes de rappel
        for ligne in self.pyLong.projet.lignesRappel:
            if ligne.actif:
                for subplot in ligne.subplots:
                    i = [s.identifiant for s in layout.subplots].index(subplot)
                    subplots[i].plot([ligne.abscisse, ligne.abscisse],
                                     [layout.subplots[i].ordonnees['min']-layout.subplots[i].ordonnees['delta bas'],
                                      layout.subplots[i].ordonnees['max']+layout.subplots[i].ordonnees['delta haut']],
                                     linestyle=styles2ligne[self.pyLong.projet.preferences['style rappel']],
                                     color=couleurs[self.pyLong.projet.preferences['couleur rappel']],
                                     linewidth=self.pyLong.projet.preferences['épaisseur rappel'],
                                     alpha=self.pyLong.projet.preferences['opacité rappel'],
                                     zorder=self.pyLong.projet.preferences['ordre rappel'])

        figure.align_ylabels()
        figure.tight_layout(pad=1.75)
        figure.subplots_adjust(hspace=layout.hspace)

        cheminFigure = QFileDialog.getSaveFileName(caption="Exporter la figure")[0]
        nomFigure = QFileInfo(cheminFigure).fileName()
        nomFigure = nomFigure.split(".")[0]

        if nomFigure == "":
            return 0
        else:
            nomFigure += ".{}".format(self.extension.currentText())
            repertoireFigure = QFileInfo(cheminFigure).absolutePath()
            cheminFigure = repertoireFigure + "/" + nomFigure

        figure.savefig(cheminFigure, dpi=self.dpi.value())

        self.pyLong.canvas.dessiner()
        self.accept()
