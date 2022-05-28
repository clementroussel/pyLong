from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import AutoMinorLocator
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

from pyLong.dictionaries import lineStyles, colors, legendPlacements

import numpy as np


class Canvas(FigureCanvas):
    def __init__(self, parent, figure=Figure(figsize=(29.7/2.54, 21/2.54))):
        super().__init__(figure)

        self.pyLong = parent

    def addContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.layoutAction)
        self.popMenu.addAction(self.pyLong.advancedLayoutAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.refreshAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.navigationBar._actions['pan'])
        self.popMenu.addAction(self.pyLong.navigationBar._actions['zoom'])
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.printAction)
        self.popMenu.addAction(self.pyLong.copyFigureAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.subplotsManagerAction)

    def contextMenu(self, point):
        if not (self.pyLong.navigationBar._actions['pan'].isChecked() or self.pyLong.navigationBar._actions['zoom'].isChecked()):
            self.popMenu.exec_(self.mapToGlobal(point))
        else:
            pass

    def initialize(self):
        if not self.pyLong.freeze:
            gs = GridSpec(1, 1, figure=self.figure)
            self.ax_z = self.figure.add_subplot(gs[0:, :])
            self.ax_p = self.ax_z.twinx()

            self.figure.tight_layout(pad=1.75)

    def erase(self):
        if not self.pyLong.freeze:
            for ax in self.figure.axes:
                ax.clear()

    def updateLayout(self):
        if not self.pyLong.freeze:
            self.erase()
            self.figure.clear()

            i = self.pyLong.layoutsList.currentIndex()
            layout = self.pyLong.project.layouts[i]

            slopeSymbol = self.pyLong.project.settings.slopeSymbol

            n_subdivisions = layout.subdivisions
            n_subplots = len(layout.subplots)
            n_subdivisions_subplots = 0
            for subplot in layout.subplots:
                n_subdivisions_subplots += subplot.subdivisions

            gs = GridSpec(n_subdivisions, 1, figure=self.figure)
            self.ax_z = self.figure.add_subplot(gs[0:n_subdivisions - n_subdivisions_subplots, :])
            self.ax_p = self.ax_z.twinx()

            self.ax_z.set_xlim((layout.xAxisProperties['min'] - layout.xAxisProperties['left shift'],
                                layout.xAxisProperties['max'] + layout.xAxisProperties['right shift']))

            self.ax_z.tick_params(axis='x',
                                  colors=colors[layout.xAxisProperties['value color']],
                                  labelsize=layout.xAxisProperties['value size'])

            self.ax_z.set_xticks(np.linspace(layout.xAxisProperties['min'],
                                             layout.xAxisProperties['max'],
                                             layout.xAxisProperties['intervals'] + 1))

            self.ax_z.set_ylim((layout.zAxisProperties['min'] - layout.zAxisProperties['lower shift'],
                                layout.zAxisProperties['max'] + layout.zAxisProperties['upper shift']))

            self.ax_z.set_ylabel(layout.zAxisProperties['label'],
                                 {'color': colors[layout.zAxisProperties['label color']],
                                  'fontsize': layout.zAxisProperties['label size']})

            self.ax_z.tick_params(axis='y',
                                  colors=colors[layout.zAxisProperties['value color']],
                                  labelsize=layout.zAxisProperties['value size'])

            self.ax_z.set_yticks(np.linspace(layout.zAxisProperties['min'],
                                             layout.zAxisProperties['max'],
                                             layout.zAxisProperties['intervals'] + 1))

            if n_subdivisions > 1 and n_subplots > 0:
                self.ax_z.xaxis.set_ticks_position('top')
            else:
                self.ax_z.set_xlabel(layout.xAxisProperties['label'],
                                     {'color': colors[layout.xAxisProperties['label color']],
                                      'fontsize': layout.xAxisProperties['label size']})

            self.ax_z.grid(visible=layout.grid['active'],
                           which='major',
                           axis='both',
                           linestyle=lineStyles[layout.grid['style']],
                           linewidth=layout.grid['thickness'],
                           alpha=layout.grid['opacity'],
                           zorder=layout.grid['order'])

            self.ax_p.set_ylim(
                (layout.slopesAxisProperties['min {}'.format(slopeSymbol)] - layout.slopesAxisProperties['lower shift {}'.format(slopeSymbol)],
                 layout.slopesAxisProperties['max {}'.format(slopeSymbol)] + layout.slopesAxisProperties['upper shift {}'.format(slopeSymbol)]))

            self.ax_p.set_ylabel(layout.slopesAxisProperties['label'],
                                 {'color': colors[layout.slopesAxisProperties['label color']],
                                  'fontsize': layout.slopesAxisProperties['label size']})

            self.ax_p.tick_params(axis='y',
                                  colors=colors[layout.slopesAxisProperties['value color']],
                                  labelsize=layout.slopesAxisProperties['value size'])

            self.ax_p.set_yticks(np.linspace(layout.slopesAxisProperties['min {}'.format(slopeSymbol)],
                                             layout.slopesAxisProperties['max {}'.format(slopeSymbol)],
                                             layout.slopesAxisProperties['intervals {}'.format(slopeSymbol)] + 1))

            slopeLabels = [str(np.round(p, 1)) + '{}'.format(slopeSymbol) for p in np.linspace(layout.slopesAxisProperties['min {}'.format(slopeSymbol)],
                                                                                               layout.slopesAxisProperties['max {}'.format(slopeSymbol)],
                                                                                               layout.slopesAxisProperties['intervals {}'.format(slopeSymbol)] + 1)]

            self.ax_p.set_yticklabels(slopeLabels)

            if layout.secondaryAxis:
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

                self.subplots[i].set_yticks(np.linspace(layout.subplots[i].yAxisProperties['min'],
                                                        layout.subplots[i].yAxisProperties['max'],
                                                        layout.subplots[i].yAxisProperties['intervals'] + 1))

                self.subplots[i].set_ylabel(layout.subplots[i].yAxisProperties['label'],
                                            {'color': colors[layout.subplots[i].yAxisProperties['label color']],
                                             'fontsize': layout.zAxisProperties['label size']})

                self.subplots[i].tick_params(axis='y',
                                             colors=colors[layout.subplots[i].yAxisProperties['value color']],
                                             labelsize=layout.zAxisProperties['value size'])

                self.subplots[i].grid(visible=layout.grid['active'],
                                      which='major',
                                      axis='both',
                                      linestyle=lineStyles[layout.grid['style']],
                                      linewidth=layout.grid['thickness'],
                                      alpha=layout.grid['opacity'],
                                      zorder=layout.grid['order'])

                self.subplots[i].set_xlim((layout.xAxisProperties['min'] - layout.xAxisProperties['left shift'],
                                           layout.xAxisProperties['max'] + layout.xAxisProperties['right shift']))

                self.subplots[i].tick_params(axis='x',
                                             colors=colors[layout.xAxisProperties['value color']],
                                             labelsize=layout.xAxisProperties['value size'])

                self.subplots[i].set_xticks(np.linspace(layout.xAxisProperties['min'],
                                                        layout.xAxisProperties['max'],
                                                        layout.xAxisProperties['intervals'] + 1))

                if i != n_subplots - 1:
                    plt.setp(self.subplots[i].get_xticklabels(), visible=False)
                    self.subplots[i].tick_params(axis='x', length=0)
                else:
                    self.subplots[i].set_xlabel(layout.xAxisProperties['label'],
                                                {'color': colors[layout.xAxisProperties['label color']],
                                                 'fontsize': layout.xAxisProperties['label size']})

            self.figure.align_ylabels()
            self.figure.tight_layout(pad=1.75)
            self.figure.subplots_adjust(hspace=layout.hspace)

            self.ax_z.set_zorder(self.ax_p.get_zorder() + 1)
            self.ax_z.patch.set_visible(False)

    def adjustRatio(self):
        i = self.pyLong.layoutsList.currentIndex()
        layout = self.pyLong.project.layouts[i]

        width = layout.dimensions['width']
        height = layout.dimensions['height']

        self.resize(self.width(), self.width() * (height / width))
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def adjustWidth(self):
        i = self.pyLong.layoutsList.currentIndex()
        layout = self.pyLong.project.layouts[i]

        width = layout.dimensions['width']
        height = layout.dimensions['height']

        self.resize(0.99 * self.pyLong.scrollArea.width(), 0.99 * self.pyLong.scrollArea.width() * (height / width))
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def adjustHeight(self):
        i = self.pyLong.layoutsList.currentIndex()
        layout = self.pyLong.project.layouts[i]

        width = layout.dimensions['width']
        height = layout.dimensions['height']

        self.resize(0.99 * self.pyLong.scrollArea.height() * (width / height), 0.99 * self.pyLong.scrollArea.height())
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def zoomIn(self):
        i = self.pyLong.layoutsList.currentIndex()
        layout = self.pyLong.project.layouts[i]

        self.resize(self.width()*1.05, self.height()*1.05)
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def zoomOut(self):
        i = self.pyLong.layoutsList.currentIndex()
        layout = self.pyLong.project.layouts[i]

        self.resize(self.width()/1.05, self.height()/1.05)
        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)
        self.draw()

    def updateFigure(self):
        if not self.pyLong.freeze:
            self.adjustRatio()
            pyLong = self.pyLong

            i = pyLong.layoutsList.currentIndex()
            layout = pyLong.project.layouts[i]

            slopeSymbol = pyLong.project.settings.slopeSymbol

            self.updateLayout()

            # preview profile
            self.pyLong.project.preview.clear()
            self.ax_z.add_line(self.pyLong.project.preview.line)

            # zProfiles and sProfiles
            for zprofile, sprofile in pyLong.project.profiles:
                zprofile.clear()
                zprofile.update()
                sprofile.clear()
                sprofile.update()

                self.ax_z.add_line(zprofile.line)
                self.ax_z.add_line(sprofile.trickLine)

                if not layout.secondaryAxis and sprofile.markersVisible:
                    self.ax_z.add_line(sprofile.line)

                elif layout.secondaryAxis and slopeSymbol == "%" and sprofile.markersVisible:
                    self.ax_p.add_line(sprofile.linePercents)

                elif layout.secondaryAxis and slopeSymbol == "°" and sprofile.markersVisible:
                    self.ax_p.add_line(sprofile.line_degres)
                    
                # slope annotations
                if sprofile.annotationsVisible and sprofile.active:
                    if not layout.secondaryAxis:
                        if slopeSymbol == "%":
                            for i in range(len(sprofile.slopes)):
                                self.ax_z.text(sprofile.x[i],
                                               sprofile.z[i] + sprofile.annotationProperties['z shift'],
                                               s="{}%".format(str(np.round(sprofile.slopesPercents[i], 1))),
                                               fontsize=sprofile.annotationProperties['size'],
                                               color=colors[sprofile.annotationProperties['color']],
                                               alpha=sprofile.opacity,
                                               horizontalalignment='center',
                                               verticalalignment='center',
                                               rotation=0,
                                               zorder=sprofile.order)

                        else:
                            for i in range(len(sprofile.slopes)):
                                self.ax_z.text(sprofile.x[i],
                                               sprofile.z[i] + sprofile.annotationProperties['z shift'],
                                               s="{}°".format(str(np.round(sprofile.slopesDegrees[i], 1))),
                                               fontsize=sprofile.annotationProperties['size'],
                                               color=colors[sprofile.annotationProperties['color']],
                                               alpha=sprofile.opacity,
                                               horizontalalignment='center',
                                               verticalalignment='center',
                                               zorder=sprofile.order)
                    
                    else:
                        if slopeSymbol == "%":
                            for i in range(len(sprofile.slopes)):
                                if layout.slopesAxisProperties['min %'] <= sprofile.slopesPercents[i] <= layout.slopesAxisProperties['max %']:
                                    self.ax_p.text(sprofile.x[i],
                                                   sprofile.slopesPercents[i] + sprofile.annotationProperties['s shift %'],
                                                   s="{}%".format(str(np.round(sprofile.slopesPercents[i], 1))),
                                                   fontsize=sprofile.annotationProperties['size'],
                                                   color=colors[sprofile.annotationProperties['color']],
                                                   alpha=sprofile.opacity,
                                                   horizontalalignment='center',
                                                   verticalalignment='bottom',
                                                   zorder=sprofile.order)

                        else:
                            for i in range(len(sprofile.slopes)):
                                if layout.slopesAxisProperties['min °'] <= sprofile.slopesDegrees[i] <= layout.slopesAxisProperties['max °']:
                                    self.ax_p.text(sprofile.x[i],
                                                   sprofile.slopesDegrees[i] + sprofile.annotationProperties['s shift °'],
                                                   s="{}%".format(str(np.round(sprofile.slopesDegrees[i], 1))),
                                                   fontsize=sprofile.annotationProperties['size'],
                                                   color=colors[sprofile.annotationProperties['color']],
                                                   alpha=sprofile.opacity,
                                                   horizontalalignment='center',
                                                   verticalalignment='bottom',
                                                   zorder=sprofile.order)

            # annotations
            for group in pyLong.project.groups:
                if group.active:
                    for annotation in group.annotations:
                        annotation.clear()
                        annotation.update()
                        if isinstance(annotation, Text):
                            self.ax_z.add_artist(annotation.text)

                        elif isinstance(annotation, VerticalAnnotation):
                            self.ax_z.add_artist(annotation.annotation)

                        elif isinstance(annotation, LinearAnnotation):
                            self.ax_z.add_artist(annotation.annotation)
                            self.ax_z.add_artist(annotation.text)

                        elif isinstance(annotation, Interval):
                            self.ax_z.add_artist(annotation.text)
                            self.ax_z.add_line(annotation.startLine)
                            self.ax_z.add_line(annotation.endLine)

                        elif isinstance(annotation, Rectangle):
                            self.ax_z.add_patch(annotation.rectangle)

            # calculations
            for calculation in pyLong.project.calculations:
                calculation.clear()
                calculation.update()
                if isinstance(calculation, (EnergyLine, Rickenmann, FlowR, Corominas)):
                    self.ax_z.add_line(calculation.line)

            # main legend
            if layout.legend['active']:
                self.ax_z.legend(loc=legendPlacements[layout.legend['position']][0],
                                 ncol=layout.legend['columns'],
                                 fontsize=layout.legend['size'],
                                 frameon=layout.legend['frame'],
                                 bbox_to_anchor=legendPlacements[layout.legend['position']][1],
                                 bbox_transform=self.ax_z.transAxes)

            # other data
            for data in pyLong.project.otherData:
                data.clear()
                data.update()

                try:
                    i = [subplot.id for subplot in layout.subplots].index(data.subplot)
                except:
                    i = -1

                if i != -1:
                    self.subplots[i].add_line(data.line)

            # subplots legend
            for i in range(len(self.subplots)):
                if layout.subplots[i].legend['active']:
                    self.subplots[i].legend(loc=legendPlacements[layout.subplots[i].legend['position']][0],
                                            ncol=layout.subplots[i].legend['columns'],
                                            fontsize=layout.legend['size'],
                                            frameon=layout.legend['frame'],
                                            bbox_to_anchor=legendPlacements[layout.subplots[i].legend['position']][1],
                                            bbox_transform=self.subplots[i].transAxes)


            # reminder lines
            for line in pyLong.project.reminderLines:
                if line.active:
                    for subplot in line.subplots:
                        try:
                            i = [s.id for s in layout.subplots].index(subplot)
                            self.subplots[i].plot([line.x, line.x],
                                                  [layout.subplots[i].yAxisProperties['min'] - layout.subplots[i].yAxisProperties['lower shift'],
                                                   layout.subplots[i].yAxisProperties['max'] + layout.subplots[i].yAxisProperties['upper shift']],
                                                  linestyle=lineStyles[pyLong.project.settings.reminderLineProperties['style']],
                                                  color=colors[pyLong.projet.settings.reminderLineProperties['color']],
                                                  linewidth=pyLong.project.settings.reminderLineProperties['thickness'],
                                                  alpha=pyLong.project.settings.reminderLineProperties['opacity'],
                                                  zorder=pyLong.project.settings.reminderLineProperties['order'])
                        except:
                            pass

            self.draw()

            self.figure.tight_layout(pad=1.75)
            self.figure.subplots_adjust(hspace=layout.hspace)

    def updateLegends(self):
        if not self.pyLong.freeze:
            pyLong = self.pyLong

            i = pyLong.layoutsList.currentIndex()
            layout = pyLong.project.layouts[i]

            try:
                self.ax_z.get_legend().remove()
            except:
                pass

            if layout.legend['active']:
                self.ax_z.legend(loc=legendPlacements[layout.legend['position']][0],
                                 ncol=layout.legend['columns'],
                                 fontsize=layout.legend['size'],
                                 frameon=layout.legend['frame'],
                                 bbox_to_anchor=legendPlacements[layout.legend['position']][1],
                                 bbox_transform=self.ax_z.transAxes)

            for i in range(len(self.subplots)):
                try:
                    self.subplots[i].get_legend().remove()
                except:
                    pass

                if layout.subplots[i].legend['active']:
                    self.subplots[i].legend(loc=legendPlacements[layout.subplots[i].legend['position']][0],
                                            ncol=layout.subplots[i].legend['columns'],
                                            fontsize=layout.legend['size'],
                                            frameon=layout.legend['frame'],
                                            bbox_to_anchor=legendPlacements[layout.subplots[i].legend['position']][1],
                                            bbox_transform=self.subplots[i].transAxes)

            self.draw()
