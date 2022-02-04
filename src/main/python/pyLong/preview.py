from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

import random

from pyLong.dictionaries import lineStyles, markerStyles, colors


class Preview:
    counter = 0
    
    def __init__(self) :
        Preview.counter += 1
        
        self.x = np.array([])
        
        self.z = np.array([])
        
        self.opacity = 0.5
        
        self.order = 99
        
        self.lineProperties = {'style': 'solid',
                               'color': 'Red',
                               'thickness': 4}
        
        self.markerProperties = {'style': 'none',
                                 'color': 'Black',
                                 'size': 4}
        
        self.visible = True
        
        self.cid = None
        
        self.profile = None

        self.clear()

    def clear(self):
        self.line = Line2D([], [])
        
    def addOnClick(self, event):
        try:
            if event.inaxes != self.line.axes:
                return 0
            
            xs = list(self.line.get_xdata())
            ys = list(self.line.get_ydata())
            
            xs.append(event.xdata)
            
            xs.sort()
            i = xs.index(event.xdata)
            ys.insert(i, event.ydata)
            
            self.line.set_data(xs, ys)
            self.line.figure.canvas.draw()
        except:
            pass
        
    def addOnClickOnProfile(self, event):
        try:
            if event.inaxes != self.line.axes:
                return 0
            
            xs = list(self.line.get_xdata())
            ys = list(self.line.get_ydata())
    
            xs.append(event.xdata)
            xs.sort()        
    
            i = xs.index(event.xdata)
            ys.insert(i, self.profil.interpolate(event.xdata))
            
            self.line.set_data(xs, ys)
            self.line.figure.canvas.draw()

        except:
            pass
        
    def deleteOnPick(self, event):
        try:
            ind = event.ind
    
            if type(ind) == np.ndarray:
                ind = ind[-1]
            
            xs = list(self.line.get_xdata())
            ys = list(self.line.get_ydata())
            
            if len(xs) > 2:
                xs.pop(int(ind))
                ys.pop(int(ind))
                
                self.line.set_data(xs, ys)
                self.line.figure.canvas.draw()

        except:
            pass
        
    def update(self):
        self.line.set_data(self.x, self.z)
        self.line.set_linestyle(lineStyles[self.lineProperties['style']])
        self.line.set_color(colors[self.lineProperties['color']])
        self.line.set_linewidth(self.lineProperties['thickness'])
        self.line.set_marker(markerStyles[self.markerProperties['style']])
        self.line.set_markeredgecolor(colors[self.markerProperties['color']])
        self.line.set_markerfacecolor(colors[self.markerProperties['color']])
        self.line.set_markersize(self.markerProperties['size'])
        self.line.set_alpha(self.opacity)
        self.line.set_zorder(self.order)
        self.line.set_visible(self.visible)
        self.line.set_picker(5)

    def sort(self, mode="ascending"):
        ascending, ascending_inverted = False, False
        descending, descending_inverted = False, False

        if (self.x[0] < self.x[-1] and self.z[0] < self.z[-1]):
            # profile is ascending
            ascending = True

        elif (self.x[0] > self.x[-1] and self.z[0] > self.z[-1]):
            # profile is ascending but inverted
            ascending_inverted = True

        elif (self.x[0] < self.x[-1] and self.z[0] > self.z[-1]):
            # profile is descending
            descending = True

        else:
            # profile is descending but inverted
            descending_inverted = True

        if mode == "ascending":
            if ascending:
                pass

            elif ascending_inverted:
                self.x = np.flip(self.x)
                self.z = np.flip(self.z)

            elif descending:
                self.x = self.x[0] + self.x[-1] - np.flip(self.x)
                self.z = np.flip(self.z)

            else:
                self.x = self.x[-1] + self.x[0] - self.x

        else:
            if descending:
                pass

            elif descending_inverted:
                self.x = np.flip(self.x)
                self.z = np.flip(self.z)

            elif ascending:
                self.x = self.x[0] + self.x[-1] - np.flip(self.x)
                self.z = np.flip(self.z)

            else:
                self.x = self.x[-1] + self.x[0] - self.x
        
    def __del__(self):
        Preview.counter -= 1

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes
