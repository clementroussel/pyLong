import numpy as np
import pandas as pd

from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt, savgol_filter
from scipy.optimize import fsolve

from matplotlib.lines import Line2D

import random

from pyLong.dictionaries import lineStyles, markerStyles, colors
from pyLong.visvalingamwyatt import Simplifier
from pyLong.lowess import py_lowess

class zProfile:
    counter = 0
    
    def __init__(self) :
        zProfile.counter += 1
        
        self.active = True
        
        self.title = ""
        
        self.x = np.array([0, 1000])
        
        self.z = np.array([0, 1000])
        
        self.label = ""
        
        self.opacity = 1.
        
        self.order = 1
        
        self.lineProperties = {'style': random.choice(list(lineStyles.keys())),
                               'color': random.choice(list(colors.keys())),
                               'thickness': random.randint(1, 5)}
        
        self.markerProperties = {'style': 'aucun',
                                 'color': random.choice(list(colors.keys())),
                                 'size': random.randint(1, 5)}
        
        self.visible = True
        
        self.clear()

    def clear(self):
        self.line = Line2D([], [])
        
    def solve(self, z, x) :
        f = interp1d(self.x, self.z, kind='cubic')
        def F(x) :
            return float(f(x) - z)
        
        if x >= np.min(self.x) and x <= np.max(self.x):
            return np.round(float(fsolve(F, x)), 3)
        else:
            return np.round(float(fsolve(F, self.x[0])), 3)
        
    def update(self):
        self.line.set_data(self.x, self.z)
        
        if self.active == False or self.visible == False:
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
        self.line.set_visible(self.visible and self.active)
        
    def interpolate(self, x):
        Xs = list(self.x)
        Xs.append(x)
        Xs.sort()
        i = Xs.index(x)

        if x == self.Xs[0]:
            return np.round(self.z[0], 3)
        elif x == self.Xs[-1]:
            return np.round(self.z[-1], 3)
        else:
            f = interp1d(self.x[i - 1:i + 1], self.z[i - 1:i + 1], kind='linear')
            return np.round(float(f(x)), 3)
        
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
                self.znp.flip(self.z)

            elif ascending:
                self.x = self.x[0] + self.x[-1] - np.flip(self.x)
                self.z = np.flip(self.z)

            else:
                self.x = self.x[-1] + self.x[0] - self.x
                
    def lowess(self, lw_n, lw_f, nsteps=2):  
        x = np.copy(self.x)
        z = np.copy(self.z)
        
        n = len(x)
        delta = x.max() - x.min()
        delta *= lw_n
        delta /= n
        
        ys = np.zeros(n)
        rw = np.zeros(n)
        res = np.zeros(n)
        
        z, rw, res = py_lowess(x, z, n, lw_f, nsteps, delta, ys, rw, res)
        
        return np.array(x), np.array(z)
    
    def butterworth(self, but_o, but_f, btype='lowpass', analog=False):
        x = np.copy(self.x)
        z = np.copy(self.z)
        
        X = np.linspace(x.min(), x.max(), len(x)*2)
        Z = np.interp(X, x, z)
        
        b, a = butter(but_o, but_f, btype='lowpass', analog=False)
        low_pass = filtfilt(b, a, Z)
        
        z = np.interp(x, X, low_pass)
        
        return np.array(x), np.array(z)
    
    def savitsky_golay(self, sg_o, sg_f):
        x = np.copy(self.x)
        z = np.copy(self.z)
        
        z = savgol_filter(z, int(sg_f), int(sg_o))
        
        xz = np.array([x,z]).T
        
        return np.array(x), np.array(z)
          
    def simplify(self, ratio):
        xz = np.array([self.x, self.z]).T
        S = Simplifier(xz)
        xzs = S.simplify(ratio=ratio)

        if len(xzs[:,0]) < 2:
            return self.x, self.z
        else:
            if xzs[-1,0] != xz[-1,0] :
                xzs = np.append(xzs, np.reshape(xz[-1,:], (1,2)), axis=0)
            
            x = xzs[:,0]
            z = xzs[:,1]
            
            return x, z
        
    def export(self, path, delimiter, formatting, separator):
        xz = np.array([self.x, self.z]).T
        xz = pd.DataFrame(xz)
        xz.to_csv(path,
                  sep = delimiter,
                  float_format = formatting,
                  decimal = separator,
                  index = False,
                  header = ['X','Z'])
        
    def __del__(self):
        zProfile.counter -= 1

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes
