import numpy as np
import pandas as pd

from matplotlib.lines import Line2D

import random

from pyLong.dictionaries import lineStyles, markerStyles, colors


class OtherData:
    counter = 0

    def __init__(self):
        OtherData.counter += 1

        self.active = True
        
        self.title = ""
        
        self.x = np.array([0, 1000])
        
        self.y = np.array([0, 1000])
        
        self.label = ""
        
        self.opacity = 1.
        
        self.order = 1

        self.subplot = "0"
        
        self.lineProperties = {'style': 'solid',
                               'color': 'Black',
                               'thickness': 1}
        
        self.markerProperties = {'style': 'aucun',
                                 'color': 'Black',
                                 'size': 1}
        
        self.clear()

    def clear(self):
        self.line = Line2D([], [])
        
    def update(self):
        self.line.set_data(self.x, self.y)
        
        if not self.visible:
            self.line.set_label("")
        else:
            self.line.set_label(self.label)
            
        self.line.set_linestyle(lineStyles[self.lineProperties['style']])
        self.line.set_color(colors[self.lineProperties['color']])
        self.line.set_linewidth(self.lineProperties['thickness'])
        self.line.set_marker(markerStyles[self.markerProperties['style']])
        self.line.set_markeredgecolor(colors[self.markerProperties['color']])
        self.line.set_markerfacecolor(colors[self.markerProperties['color']])
        self.line.set_markersize(self.markerProperties['size'])
        self.line.set_alpha(self.opacity)
        self.line.set_zorder(self.order)
        self.line.set_visible(self.active)
        
    def __del__(self):
        OtherData.counter -= 1

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes
