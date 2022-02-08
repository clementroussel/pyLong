from PyQt5.QtWidgets import QMenu

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib import pyplot as plt

from pyLong.text import Text
from pyLong.verticalAnnotation import VerticalAnnotation
from pyLong.linearAnnotation import LinearAnnotation
from pyLong.interval import Interval
from pyLong.rectangle import Rectangle

from pyLong.toolbox.energyLine import EnergyLine
from pyLong.toolbox.rickenmann import Rickenmann
from pyLong.toolbox.flowR import FlowR
from pyLong.toolbox.corominas import Corominas
# from pyLong.Mezap import *

from pyLong.reminderLine import ReminderLine

import numpy as np


class Canvas(FigureCanvas):
    def __init__(self, parent, figure=Figure(figsize=(29.7/2.54, 21/2.54))):
        super().__init__(figure)

        self.pyLong = parent

    def addContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.action_miseEnPage)
        self.popMenu.addAction(self.pyLong.action_miseEnPage_avancee)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.rafraichirFigure)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.barreDeNavigation._actions['pan'])
        self.popMenu.addAction(self.pyLong.barreDeNavigation._actions['zoom'])
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.action_exporterFigure)
        self.popMenu.addAction(self.pyLong.action_copierFigure)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.action_gestionSubplots)

    def contextMenu(self, point):
        if not (self.pyLong.barreDeNavigation._actions['pan'].isChecked() or self.pyLong.barreDeNavigation._actions['zoom'].isChecked()):
            self.popMenu.exec_(self.mapToGlobal(point))
        else:
            pass

    def initialiser(self):
        if not self.pyLong.freeze:
            gs = GridSpec(1, 1, figure=self.figure)
            self.ax_z = self.figure.add_subplot(gs[0:, :])
            self.ax_p = self.ax_z.twinx()

            self.figure.tight_layout()

    def effacer(self):
        if not self.pyLong.freeze:
            for ax in self.figure.axes:
                ax.clear()

    def formatter(self):
        if not self.pyLong.freeze:
            self.effacer()
            self.figure.clear()

            i = self.pyLong.listeLayouts.currentIndex()
            layout = self.pyLong.projet.layouts[i]

            symbolePente = self.pyLong.projet.preferences['pente']

            n_subdivisions = layout.subdivisions
            n_subplots = len(layout.subplots)
            n_subdivisions_subplots = 0
            for subplot in layout.subplots:
                n_subdivisions_subplots += subplot.subdivisions

            gs = GridSpec(n_subdivisions, 1, figure=self.figure)
            self.ax_z = self.figure.add_subplot(gs[0:n_subdivisions - n_subdivisions_subplots, :])
            self.ax_p = self.ax_z.twinx()

            self.ax_z.set_xlim((layout.abscisses['min'] - layout.abscisses['delta gauche'],
                                layout.abscisses['max'] + layout.abscisses['delta droite']))

            self.ax_z.tick_params(axis='x',
                                  colors=couleurs[layout.abscisses['couleur valeur']],
                                  labelsize=layout.abscisses['taille valeur'])

            self.ax_z.set_xticks(np.linspace(layout.abscisses['min'],
                                             layout.abscisses['max'],
                                             layout.abscisses['intervalles'] + 1))

            self.ax_z.set_ylim((layout.altitudes['min'] - layout.altitudes['delta bas'],
                                layout.altitudes['max'] + layout.altitudes['delta haut']))

            self.ax_z.set_ylabel(layout.altitudes['libellé'],
                                 {'color': couleurs[layout.altitudes['couleur libellé']],
                                  'fontsize': layout.altitudes['taille libellé']})

            self.ax_z.tick_params(axis='y',
                                  colors=couleurs[layout.altitudes['couleur valeur']],
                                  labelsize=layout.altitudes['taille valeur'])

            self.ax_z.set_yticks(np.linspace(layout.altitudes['min'],
                                             layout.altitudes['max'],
                                             layout.altitudes['intervalles'] + 1))

            if n_subdivisions > 1 and n_subplots > 0:
                self.ax_z.xaxis.set_ticks_position('top')
            else:
                self.ax_z.set_xlabel(layout.abscisses['libellé'],
                                     {'color': couleurs[layout.abscisses['couleur libellé']],
                                      'fontsize': layout.abscisses['taille libellé']})

            self.ax_z.grid(visible=layout.grille['active'],
                           which='major',
                           axis='both',
                           linestyle=styles2ligne[layout.grille['style']],
                           linewidth=layout.grille['épaisseur'],
                           alpha=layout.grille['opacité'],
                           zorder=layout.grille['ordre'])

            self.ax_p.set_ylim(
                (layout.pentes['min {}'.format(symbolePente)] - layout.pentes['delta bas {}'.format(symbolePente)],
                 layout.pentes['max {}'.format(symbolePente)] + layout.pentes['delta haut {}'.format(symbolePente)]))

            self.ax_p.set_ylabel(layout.pentes['libellé'],
                                 {'color': couleurs[layout.pentes['couleur libellé']],
                                  'fontsize': layout.pentes['taille libellé']})

            self.ax_p.tick_params(axis='y',
                                  colors=couleurs[layout.pentes['couleur valeur']],
                                  labelsize=layout.pentes['taille valeur'])

            self.ax_p.set_yticks(np.linspace(layout.pentes['min {}'.format(symbolePente)],
                                             layout.pentes['max {}'.format(symbolePente)],
                                             layout.pentes['intervalles {}'.format(symbolePente)] + 1))

            labelsPente = [str(np.round(p, 1)) + '{}'.format(symbolePente) for p in np.linspace(layout.pentes['min {}'.format(symbolePente)],
                                                                                                layout.pentes['max {}'.format(symbolePente)],
                                                                                                layout.pentes['intervalles {}'.format(symbolePente)] + 1)]

            self.ax_p.set_yticklabels(labelsPente)

            if layout.axeSecondaire:
                self.ax_p.set_visible(True)
            else:
                self.ax_p.set_visible(False)

            n_start = n_subdivisions - n_subdivisions_subplots
            self.subplots = []
            for i in range(n_subplots):
                self.subplots.append(self.figure.add_subplot(gs[n_start:n_start + layout.subplots[i].subdivisions], sharex=self.ax_z))
                n_start += layout.subplots[i].subdivisions

                self.subplots[i].set_ylim((layout.subplots[i].ordonnees['min'] - layout.subplots[i].ordonnees['delta bas'],
                                           layout.subplots[i].ordonnees['max'] + layout.subplots[i].ordonnees['delta haut']))

                self.subplots[i].set_yticks(np.linspace(layout.subplots[i].ordonnees['min'],
                                                        layout.subplots[i].ordonnees['max'],
                                                        layout.subplots[i].ordonnees['intervalles'] + 1))

                self.subplots[i].set_ylabel(layout.subplots[i].ordonnees['libellé'],
                                            {'color': couleurs[layout.subplots[i].ordonnees['couleur libellé']],
                                             'fontsize': layout.altitudes['taille libellé']})

                self.subplots[i].tick_params(axis='y',
                                             colors=couleurs[layout.subplots[i].ordonnees['couleur valeur']],
                                             labelsize=layout.altitudes['taille valeur'])

                self.subplots[i].grid(visible=layout.grille['active'],
                                      which='major',
                                      axis='both',
                                      linestyle=styles2ligne[layout.grille['style']],
                                      linewidth=layout.grille['épaisseur'],
                                      alpha=layout.grille['opacité'],
                                      zorder=layout.grille['ordre'])

                self.subplots[i].set_xlim((layout.abscisses['min'] - layout.abscisses['delta gauche'],
                                           layout.abscisses['max'] + layout.abscisses['delta droite']))

                self.subplots[i].tick_params(axis='x',
                                             colors=couleurs[layout.abscisses['couleur valeur']],
                                             labelsize=layout.abscisses['taille valeur'])

                self.subplots[i].set_xticks(np.linspace(layout.abscisses['min'],
                                                        layout.abscisses['max'],
                                                        layout.abscisses['intervalles'] + 1))

                if i != n_subplots - 1:
                    plt.setp(self.subplots[i].get_xticklabels(), visible=False)
                    self.subplots[i].tick_params(axis='x', length=0)
                else:
                    self.subplots[i].set_xlabel(layout.abscisses['libellé'],
                                                {'color': couleurs[layout.abscisses['couleur libellé']],
                                                 'fontsize': layout.abscisses['taille libellé']})

            self.figure.align_ylabels()
            self.figure.tight_layout(pad=1.75)
            self.figure.subplots_adjust(hspace=layout.hspace)

            self.ax_z.set_zorder(self.ax_p.get_zorder() + 1)
            self.ax_z.patch.set_visible(False)

    def ajusterRatio(self):
        i = self.pyLong.listeLayouts.currentIndex()
        layout = self.pyLong.projet.layouts[i]

        largeur = layout.dimensions['largeur']
        hauteur = layout.dimensions['hauteur']

        self.resize(self.width(), self.width() * (hauteur / largeur))
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def ajusterLargeur(self):
        i = self.pyLong.listeLayouts.currentIndex()
        layout = self.pyLong.projet.layouts[i]

        largeur = layout.dimensions['largeur']
        hauteur = layout.dimensions['hauteur']

        self.resize(0.99 * self.pyLong.scrollArea.width(), 0.99 * self.pyLong.scrollArea.width() * (hauteur / largeur))
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def ajusterHauteur(self):
        i = self.pyLong.listeLayouts.currentIndex()
        layout = self.pyLong.projet.layouts[i]

        largeur = layout.dimensions['largeur']
        hauteur = layout.dimensions['hauteur']

        self.resize(0.99 * self.pyLong.scrollArea.height() * (largeur / hauteur), 0.99 * self.pyLong.scrollArea.height())
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def agrandir(self):
        i = self.pyLong.listeLayouts.currentIndex()
        layout = self.pyLong.projet.layouts[i]

        self.resize(self.width()*1.05, self.height()*1.05)
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def retrecir(self):
        i = self.pyLong.listeLayouts.currentIndex()
        layout = self.pyLong.projet.layouts[i]

        self.resize(self.width()/1.05, self.height()/1.05)
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def dessiner(self):
        if not self.pyLong.freeze:
            self.ajusterRatio()
            pyLong = self.pyLong

            i = pyLong.listeLayouts.currentIndex()
            layout = pyLong.projet.layouts[i]

            symbolePente = pyLong.projet.preferences['pente']

            self.formatter()
            # profil aperçu
            self.pyLong.projet.apercu.clear()
            self.ax_z.add_line(self.pyLong.projet.apercu.line)

            # zProfils et pProfils
            for zprofil, pprofil in pyLong.projet.profils:
                zprofil.clear()
                zprofil.update()
                pprofil.clear()
                pprofil.update()

                self.ax_z.add_line(zprofil.line)

                if not layout.axeSecondaire and pprofil.marqueursVisibles:
                    self.ax_z.add_line(pprofil.line)

                elif layout.axeSecondaire and symbolePente == "%" and pprofil.marqueursVisibles:
                    self.ax_p.add_line(pprofil.line_pourcents)

                elif layout.axeSecondaire and symbolePente == "°" and pprofil.marqueursVisibles:
                    self.ax_p.add_line(pprofil.line_degres)
                    
                # écriture des pentes
                if pprofil.pentesVisibles and pprofil.actif:
                    if not layout.axeSecondaire:
                        if symbolePente == "%":
                            for i in range(len(pprofil.pentes)):
                                self.ax_z.text(pprofil.abscisses[i],
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
                                self.ax_z.text(pprofil.abscisses[i],
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
                                    self.ax_p.text(pprofil.abscisses[i],
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
                                    self.ax_p.text(pprofil.abscisses[i],
                                                   pprofil.pentesDegres[i] + pprofil.annotation['décalage p °'],
                                                   s="{}%".format(str(np.round(pprofil.pentesDegres[i], 1))),
                                                   fontsize=pprofil.annotation['taille'],
                                                   color=couleurs[pprofil.annotation['couleur']],
                                                   alpha=pprofil.opacite,
                                                   horizontalalignment='center',
                                                   verticalalignment='bottom',
                                                   zorder=pprofil.ordre)

            # annotations
            for groupe in pyLong.projet.groupes:
                if groupe.actif:
                    for annotation in groupe.annotations:
                        annotation.clear()
                        annotation.update()
                        if type(annotation) == Texte:
                            self.ax_z.add_artist(annotation.text)

                        elif type(annotation) == AnnotationPonctuelle:
                            self.ax_z.add_artist(annotation.annotation)

                        elif type(annotation) == AnnotationLineaire:
                            self.ax_z.add_artist(annotation.annotation)
                            self.ax_z.add_artist(annotation.text)

                        elif type(annotation) == Zone:
                            self.ax_z.add_artist(annotation.text)
                            self.ax_z.add_line(annotation.left_line)
                            self.ax_z.add_line(annotation.right_line)

                        elif type(annotation) == Rectangle:
                            self.ax_z.add_patch(annotation.rectangle)

            # calculs
            for calcul in pyLong.projet.calculs:
                calcul.clear()
                calcul.update()
                if type(calcul) in [LigneEnergie, Rickenmann, FlowR, Corominas]:
                    self.ax_z.add_line(calcul.line)

            # légende principale
            if layout.legende['active']:
                if layout.axeSecondaire:
                    self.figure.legend(loc=placementsLegende[layout.legende['position']][0],
                                       ncol=layout.legende['nombre de colonnes'],
                                       fontsize=layout.legende['taille'],
                                       frameon=layout.legende['cadre'],
                                       bbox_to_anchor=placementsLegende[layout.legende['position']][1],
                                       bbox_transform=self.ax_z.transAxes)
                else:
                    self.ax_z.legend(loc=placementsLegende[layout.legende['position']][0],
                                     ncol=layout.legende['nombre de colonnes'],
                                     fontsize=layout.legende['taille'],
                                     frameon=layout.legende['cadre'],
                                     bbox_to_anchor=placementsLegende[layout.legende['position']][1],
                                     bbox_transform=self.ax_z.transAxes)

            # autres données
            for donnee in pyLong.projet.autresDonnees:
                donnee.clear()
                donnee.update()

                try:
                    i = [subplot.identifiant for subplot in layout.subplots].index(donnee.subplot)
                except:
                    i = -1

                if i != -1:
                    self.subplots[i].add_line(donnee.line)

            # légende subplots
            for i in range(len(self.subplots)):
                if layout.subplots[i].legende['active']:
                    self.subplots[i].legend(loc=placementsLegende[layout.subplots[i].legende['position']][0],
                                            ncol=layout.subplots[i].legende['nombre de colonnes'],
                                            fontsize=layout.legende['taille'],
                                            frameon=layout.legende['cadre'],
                                            bbox_to_anchor=placementsLegende[layout.subplots[i].legende['position']][1],
                                            bbox_transform=self.subplots[i].transAxes)


            # lignes de rappel
            for ligne in pyLong.projet.lignesRappel:
                if ligne.actif:
                    for subplot in ligne.subplots:
                        try:
                            i = [s.identifiant for s in layout.subplots].index(subplot)
                            self.subplots[i].plot([ligne.abscisse, ligne.abscisse],
                                                  [layout.subplots[i].ordonnees['min']-layout.subplots[i].ordonnees['delta bas'],
                                                   layout.subplots[i].ordonnees['max']+layout.subplots[i].ordonnees['delta haut']],
                                                  linestyle=styles2ligne[pyLong.projet.preferences['style rappel']],
                                                  color=couleurs[pyLong.projet.preferences['couleur rappel']],
                                                  linewidth=pyLong.projet.preferences['épaisseur rappel'],
                                                  alpha=pyLong.projet.preferences['opacité rappel'],
                                                  zorder=pyLong.projet.preferences['ordre rappel'])
                        except:
                            pass

            self.draw()

            self.figure.tight_layout(pad=1.75)
            self.figure.subplots_adjust(hspace=layout.hspace)

    def updateLegendes(self):
        if not self.pyLong.freeze:
            pyLong = self.pyLong

            i = pyLong.listeLayouts.currentIndex()
            layout = pyLong.projet.layouts[i]

            if not layout.axeSecondaire:
                try:
                    self.ax_z.get_legend().remove()
                except:
                    pass

                if layout.legende['active']:
                    self.ax_z.legend(loc=placementsLegende[layout.legende['position']][0],
                                     ncol=layout.legende['nombre de colonnes'],
                                     fontsize=layout.legende['taille'],
                                     frameon=layout.legende['cadre'],
                                     bbox_to_anchor=placementsLegende[layout.legende['position']][1],
                                     bbox_transform=self.ax_z.transAxes)

            for i in range(len(self.subplots)):
                try:
                    self.subplots[i].get_legend().remove()
                except:
                    pass

                if layout.subplots[i].legende['active']:
                    self.subplots[i].legend(loc=placementsLegende[layout.subplots[i].legende['position']][0],
                                            ncol=layout.subplots[i].legende['nombre de colonnes'],
                                            fontsize=layout.legende['taille'],
                                            frameon=layout.legende['cadre'],
                                            bbox_to_anchor=placementsLegende[layout.subplots[i].legende['position']][1],
                                            bbox_transform=self.subplots[i].transAxes)

            self.draw()
