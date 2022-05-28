import numpy as np
from matplotlib.lines import Line2D

import random

from pyLong.dictionaries import markerStyles, colors


class sProfile:
    counter = 0

    def __init__(self):
        sProfile.counter += 1
        
        self.active = True
        
        self.x = np.array([])
        
        self.z = np.array([])
        
        self.slopes = np.array([])
        
        self.slopesPercents = np.array([])
        
        self.slopesDegrees = np.array([])
        
        self.label = ""
        
        self.opacity = 1.
        
        self.order = 1
        
        self.markerProperties = {'style': 'point',
                                 'color': 'Black',
                                 'size': 1}
        
        self.annotationProperties = {'size': 9.,
                                     'color': 'Black',
                                     'z shift': 0,
                                     's shift %': 0,
                                     's shift °': 0}

        self.visible = False

        self.markersVisible = False

        self.annotationsVisible = False

        self.clear()

    def clear(self):
        self.line = Line2D([], [])

        self.linePercents = Line2D([], [])

        self.lineDegrees = Line2D([], [])

        self.trickLine = Line2D([], [])
            
    def updateData(self, x, z):
        if z[0] > z[-1]:
            self.slopes = (-1) * (z[1:] - z[:-1]) / (x[1:] - x[:-1])
        else:
            self.slopes = (z[1:] - z[:-1]) / (x[1:] - x[:-1])
        self.x = (x[1:] + x[:-1]) / 2
        self.z = (z[1:] + z[:-1]) / 2
        
        self.slopesPercents = self.slopes * 100
        self.slopesDegrees = np.degrees(np.arctan(self.slopes))
            
    def update(self):
        self.line.set_data(self.x, self.z)
        self.linePercents.set_data(self.x, self.slopesPercents)
        self.lineDegrees.set_data(self.x, self.slopesDegrees)

        self.line.set_label("")
        self.linePercents.set_label("")
        self.lineDegrees.set_label("")

        if self.active == False or self.markersVisible == False:
            self.trickLine.set_label("")
        else:
            self.trickLine.set_label(self.label)

        self.line.set_linestyle("None")
        self.linePercents.set_linestyle("None")
        self.lineDegrees.set_linestyle("None")
        self.trickLine.set_linestyle("None")
        
        self.line.set_marker(markerStyles[self.markerProperties['style']])
        self.linePercents.set_marker(markerStyles[self.markerProperties['style']])
        self.lineDegrees.set_marker(markerStyles[self.markerProperties['style']])
        self.trickLine.set_marker(markerStyles[self.markerProperties['style']])
        
        self.line.set_markeredgecolor(colors[self.markerProperties['color']])
        self.linePercents.set_markeredgecolor(colors[self.markerProperties['color']])
        self.lineDegrees.set_markeredgecolor(colors[self.markerProperties['color']])
        self.trickLine.set_markeredgecolor(colors[self.markerProperties['color']])
        
        self.line.set_markerfacecolor(colors[self.markerProperties['color']])
        self.linePercents.set_markerfacecolor(colors[self.markerProperties['color']])
        self.lineDegrees.set_markerfacecolor(colors[self.markerProperties['color']])
        self.trickLine.set_markerfacecolor(colors[self.markerProperties['color']])
        
        self.line.set_markersize(self.markerProperties['size'])
        self.linePercents.set_markersize(self.markerProperties['size'])
        self.lineDegrees.set_markersize(self.markerProperties['size'])
        self.trickLine.set_markersize(self.markerProperties['size'])
        
        self.line.set_alpha(self.opacity)
        self.linePercents.set_alpha(self.opacity)
        self.lineDegrees.set_alpha(self.opacity)
        self.trickLine.set_alpha(self.opacity)
        
        self.line.set_zorder(self.order)
        self.linePercents.set_zorder(self.order)
        self.lineDegrees.set_zorder(self.order)
        self.trickLine.set_zorder(self.order)
        
        self.line.set_visible(self.markersVisible and self.active)
        self.linePercents.set_visible(self.markersVisible and self.active)
        self.lineDegrees.set_visible(self.markersVisible and self.active)
        self.trickLine.set_visible(self.markersVisible and self.active)
    
    def __del__(self):
        sProfile.counter -= 1

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])
        attributes["linePercents"] = Line2D([], [])
        attributes["lineDegrees"] = Line2D([], [])
        attributes["trickLine"] = Line2D([], [])

        return attributes
