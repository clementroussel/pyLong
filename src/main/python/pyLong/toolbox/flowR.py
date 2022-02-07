from matplotlib.lines import Line2D
import numpy as np
from pyparsing import col
from scipy import interpolate

from pyLong.dictionaries import *


class FlowR():
    counter = 0

    def __init__(self):
        FlowR.counter += 1
        
        self.active = True
        
        self.title = ""
        
        self.label = ""
        
        self.lineProperties = {'style': 'solid',
                               'color': 'Black',
                               'thickness': 0.8}
        
        self.opacity = 1.
        
        self.order = 1
        
        self.parameters = {'zprofile': None,
                           'sprofile': None,
                           'x start': 0,
                           'z start': 0,
                           'x end': 0,
                           'z end': 0,
                           'angle': 0,
                           'initial speed': 0,
                           'maximal speed': 0,
                           'step': 1}
        
        self.results = {'x': [],
                        's': [], # speed
                        'z': []}
        
        self.success = False
        
        self.clear()

    def clear(self):
        self.line = Line2D([], [])
        
    def update(self):
        self.line.set_data(self.results['x'], self.results['z'])
        if self.active:
            self.line.set_label(self.label)
        else:
            self.line.set_label("")
        self.line.set_linestyle(lineStyles[self.lineProperties['style']])
        self.line.set_color(colors[self.lineProperties['color']])
        self.line.set_linewidth(self.lineProperties['thickness'])
        self.line.set_alpha(self.opacity)
        self.line.set_zorder(self.order)
        self.line.set_visible(self.active and self.success)
        
    def __del__(self):
        FlowR.counter -= 1
        
    def calculate(self):
        if self.parametres['zprofile'] is None:
            self.success = False
            return 0
        
        # getting hands on profile
        zprofile = self.parameters['zprofile']
        sprofile = self.parameters['sprofile']
        
        xmin = np.min(zprofile.x)
        xmax = np.max(zprofile.x)
        
        i = list(zprofile.x).index(xmin)
        zxmin = zprofile.z[i]
        i = list(zprofile.x).index(xmax)
        zxmax = zprofile.z[i]
        
        # sorting
        if zxmin > zxmax:
            descending = True
            zprofile.sort(mode="descending")
            
        else:
            descending = False
            zprofile.sort(mode="ascending")
        
        sprofile.updateData(zprofile.x, zprofile.z)               

        # getting hands on parameters
        x = zprofile.x
        z = zprofile.z
        xStart = self.parameters['x start']
        angle = self.parameters['angle']
        initialSpeed = self.parameters['initial speed']
        maximalSpeed = self.parameters['maximal speed']
        step = self.parameters['step']
        
        # graviy acceleration
        g = 9.81
            
        # calculation in ascending case
        if not descending:
            # calculation of zStart
            if xmin < xStart < xmax:
                zStart = zprofile.interpolate(xStart)
                self.parameters['z start'] = zStart
            elif xStart == xmin or xStart == xmax:
                k = list(zprofile.x).index(xStart)
                zStart = zprofile.z[k]
                self.parameters['z start'] = zStart
            else:
                self.success = False
                return 0
            
            # interpolation function of the longitudinal profile
            f = interpolate.interp1d(np.array(x), np.array(z))

            xDebrisFlow = list(np.arange(xmin, xStart, step))
            xDebrisFlow.append(xStart)
            zDebrisFlow = list(f(np.array(xDebrisFlow)))

            n = len(xDebrisFlow)
            speedDebrisFlow = list(-1 * np.ones(n))
            energyDebrisFlow = list(np.zeros(n))
            
            speedDebrisFlow[-1] = initialSpeed
            energyDebrisFlow[-1] = zStart + initialSpeed**2 / (2 * g)

            for i in range(1, n):
                expr = speedDebrisFlow[-i]**2 + 2*g*(zDebrisFlow[-i] - zDebrisFlow[-i-1]) - 2*g*(xDebrisFlow[-i] - xDebrisFlow[-i-1])*np.tan(np.radians(angle))
                if expr > 0:
                    speedDebrisFlow[-i-1] = min(np.sqrt(expr), maximalSpeed)
                else:
                    speedDebrisFlow[-i-1] = 0
                    k = -i-1
                    energyDebrisFlow[-i-1] = zDebrisFlow[-i-1]
                    break
                energyDebrisFlow[-i-1] = zDebrisFlow[-i-1] + speedDebrisFlow[-i-1]**2 / (2 * g)
            
            try:
                k = np.argwhere(np.array(speedDebrisFlow) == 0.)[0][0]
            except:
                self.success = False
                return 0
                
            self.parameters['x end'] = xDebrisFlow[k]
            self.parameters['z end'] = zDebrisFlow[k]
            self.results['s'] = speedDebrisFlow[k:]
            self.results['x'] = xDebrisFlow[k:]
            self.results['z'] = energyDebrisFlow[k:]
            
            self.success = True
        
        # calculation in descending case
        else:
            # calculation of zStart
            if xmin < xStart < xmax:
                zStart = zprofile.interpolate(xStart)
                self.parameters['z start'] = zStart
            elif xStart == xmin or xStart == xmax:
                k = list(zprofile.x).index(xStart)
                zStart = zprofile.z[k]
                self.parameters['z start'] = zStart
            else:
                self.success = False
                return 0
            
            # interpolation function of the longitudinal profile
            f = interpolate.interp1d(np.array(x), np.array(z))

            xDebrisFlow = list(np.arange(xStart, xmax, step))
            xDebrisFlow.append(xmax)
            zDebrisFlow = list(f(np.array(xDebrisFlow)))

            n = len(xDebrisFlow)
            speedDebrisFlow = list(-1 * np.ones(n))
            energyDebrisFlow = list(np.zeros(n))
            
            speedDebrisFlow[0] = initialSpeed
            energyDebrisFlow[0] = zStart + initialSpeed**2 / (2 * g)

            for i in range(1, n):
                expr = speedDebrisFlow[i-1]**2 + 2*g*(zDebrisFlow[i-1] - zDebrisFlow[i]) - 2*g*(xDebrisFlow[i] - xDebrisFlow[i-1])*np.tan(np.radians(angle))
                if expr > 0:
                    speedDebrisFlow[i] = min(np.sqrt(expr), maximalSpeed)
                else:
                    speedDebrisFlow[i] = 0
                    k = i
                    energyDebrisFlow[i] = zDebrisFlow[i]
                    break
                energyDebrisFlow[i] = zDebrisFlow[i] + speedDebrisFlow[i]**2 / (2 * g)
            
            try:
                k = np.argwhere(np.array(speedDebrisFlow) == 0.)[0][0]
            except:
                self.success = False
                return 0
                
            self.parameters['x end'] = xDebrisFlow[k]
            self.parameters['z end'] = zDebrisFlow[k]
            self.results['s'] = speedDebrisFlow[:k+1]
            self.results['x'] = xDebrisFlow[:k+1]
            self.results['z'] = energyDebrisFlow[:k+1]
            
            self.success = True

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes
