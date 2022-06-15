from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionaries import *

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib import pyplot as plt

import numpy as np

from pyLong.text import *
from pyLong.verticalAnnotation import *
from pyLong.linearAnnotation import *
from pyLong.interval import *
from pyLong.rectangle import *

from pyLong.toolbox.energyLine import *
from pyLong.toolbox.rickenmann import *
from pyLong.toolbox.flowR import *
from pyLong.toolbox.corominas import *
from pyLong.toolbox.mezap import *

from pyLong.reminderLine import *


class DialogPrint(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]

        self.setMinimumWidth(225)
        self.setWindowTitle("Print")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/print.png')))
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Format :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.extension = QComboBox()
        self.extension.insertItems(0, list(extensions.keys()))
        self.extension.setCurrentText(self.pyLong.project.settings.exportFileFormat)
        layout.addWidget(self.extension, 0, 1)
        
        label = QLabel("width :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.width = QDoubleSpinBox()
        self.width.setFixedWidth(75)
        self.width.setSuffix(" cm")
        self.width.setLocale(QLocale('English'))
        self.width.setSingleStep(0.1)
        self.width.setRange(0.1, 118.9)
        self.width.setDecimals(1)
        self.width.setValue(self.layout.dimensions['width'])
        layout.addWidget(self.width, 1, 1)

        label = QLabel("height :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.height = QDoubleSpinBox()
        self.height.setFixedWidth(75)
        self.height.setSuffix(" cm")
        self.height.setLocale(QLocale('English'))
        self.height.setSingleStep(0.1)
        self.height.setRange(0.1, 118.9)
        self.height.setDecimals(1)
        self.height.setValue(self.layout.dimensions['height'])
        layout.addWidget(self.height, 2, 1)

        label = QLabel("Resolution :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.dpi = QSpinBox()
        self.dpi.setFixedWidth(75)
        self.dpi.setSuffix(" dpi")
        self.dpi.setSingleStep(25)
        self.dpi.setRange(25, 1000)
        self.dpi.setValue(self.pyLong.project.settings.figureDpi)
        layout.addWidget(self.dpi, 3, 1)

        group.setLayout(layout)
        mainLayout.addWidget(group)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.print)

        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

    def print(self):
        i = self.pyLong.layoutsList.currentIndex()
        layout = self.pyLong.project.layouts[i]

        slopeSymbol = self.pyLong.project.settings.slopeSymbol

        n_subdivisions = layout.subdivisions
        n_subplots = len(layout.subplots)
        n_subdivisions_subplots = 0
        for subplot in layout.subplots:
            n_subdivisions_subplots += subplot.subdivisions

        self.figure = Figure(figsize=(self.width.value() / 2.54, self.height.value() / 2.54))
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

        values = np.linspace(layout.xAxisProperties['min'],
                                layout.xAxisProperties['max'],
                                layout.xAxisProperties['intervals'] + 1)

        if layout.asKm:
            values /= 1000
            values = np.round(values, 2)

            self.ax_z.set_xticklabels(values)

        else:
            self.ax_z.set_xticklabels(values.astype(int))

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

            self.subplots[i].set_ylim((layout.subplots[i].yAxisProperties['min'] - layout.subplots[i].yAxisProperties['lower shift'],
                                        layout.subplots[i].yAxisProperties['max'] + layout.subplots[i].yAxisProperties['upper shift']))

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

        pyLong = self.pyLong

        i = pyLong.layoutsList.currentIndex()
        layout = pyLong.project.layouts[i]

        slopeSymbol = pyLong.project.settings.slopeSymbol

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
                                                color=colors[pyLong.project.settings.reminderLineProperties['color']],
                                                linewidth=pyLong.project.settings.reminderLineProperties['thickness'],
                                                alpha=pyLong.project.settings.reminderLineProperties['opacity'],
                                                zorder=pyLong.project.settings.reminderLineProperties['order'])
                    except:
                        pass

                if line.mainSubplot:
                    self.ax_z.plot([line.x, line.x],
                                    [layout.zAxisProperties['min'] - layout.zAxisProperties['lower shift'],
                                    line.z],
                                    linestyle=lineStyles[pyLong.project.settings.reminderLineProperties['style']],
                                    color=colors[pyLong.project.settings.reminderLineProperties['color']],
                                    linewidth=pyLong.project.settings.reminderLineProperties['thickness'],
                                    alpha=pyLong.project.settings.reminderLineProperties['opacity'],
                                    zorder=pyLong.project.settings.reminderLineProperties['order'])


        self.figure.tight_layout(pad=1.75)
        self.figure.subplots_adjust(hspace=layout.hspace)

        path = QFileDialog.getSaveFileName(caption="Print")[0]
        fileName = QFileInfo(path).fileName()
        fileName = fileName.split(".")[0]

        if fileName == "":
            return 0
        else:
            fileName += ".{}".format(self.extension.currentText())
            fileRepertory = QFileInfo(path).absolutePath()
            fileName = fileRepertory + "/" + fileName

        self.figure.savefig(fileName, dpi=self.dpi.value())

        self.pyLong.canvas.updateFigure()
        self.accept()

