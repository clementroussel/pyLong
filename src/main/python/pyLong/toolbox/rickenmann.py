from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionaries import lineStyles, colors
from pyLong.intersect import intersection

class Rickenmann() :
    counter = 0
    
    def __init__(self):
        Rickenmann.counter += 1
        
        self.active = True
        
        self.title = ""
        
        self.label = ""
        
        self.lineProperties = {'style': 'solid',
                               'color': 'Black',
                               'thickness': 0.8}
        
        self.opacity = 1.
        
        self.order = 1
        
        self.parameters = {'zprofil': None,
                           'sprofile': None,
                           'x start': 0,
                           'z start': 0,
                           'x end': 0,
                           'z end': 0,
                           'volume': 0,
                           'step': 5,
                           'envelope': False}
        
        self.results = {'x': [],
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
        Rickenmann.counter -= 1
        
    def calculate(self):
        if self.parametres['zprofile'] is None:
            self.success = False
            return 0
        
        # getting hands on profile
        zprofile = self.parameters['zprofile']
        sprofile = self.parameters['sprofile']
        
        xmin = np.min(zprofile.abscisses)
        xmax = np.max(zprofile.abscisses)
        
        i = list(zprofile.x).index(xmin)
        zxmin = zprofile.z[i]
        i = list(zprofile.x).index(xmax)
        zxmax = zprofile.z[i]
        
        # sorting
        if zxmin > zxmax:
            descending = True
            zprofile.sort(mode="descending")
            sprofile.updateData(zprofile.x, zprofile.z)
            
        else:
            descending = False
            zprofile.sort(mode="ascending")
            sprofile.updateData(zprofile.x, zprofile.z)               

        # getting hands on parameters
        x = zprofile.x
        z = zprofile.z
        xStart = self.parameters['x start']
        volume = self.parameters['volume']
        step = self.parameters['step']
            
        # calculation in ascending case
        if not descending:
            # calculatuion of zStart
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
            
            zDebrisFlow = list(np.arange(zStart, zxmin, -step))
            zDebrisFlow.append(zxmin)
            
            if not self.parameters['envelope']:
                xDebrisFlow = [xStart - 1.9 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
            else:
                xDebrisFlow = [xStart - 6.0 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
                
            try:
                xInter, zInter = intersection(np.array(x), np.array(z), np.array(xDebrisFlow), np.array(zDebrisFlow))
                xInter = xInter[0]
                zInter = zInter[0]
                
                if np.abs(xInter - self.parameters['x start']) < 0.01:
                    xInter = xDebrisFlow[-1]
                    zInter = zDebrisFlow[-1]
                else:
                    xDebrisFlow.append(xInter)
                    xDebrisFlow.sort()
                    xDebrisFlow.reverse()
                    
                    k = xDebrisFlow.index(xInter)
                    xDebrisFlow = xDebrisFlow[:k+1]
                    
                    zDebrisFlow = zDebrisFlow[:k+1]
                    zDebrisFlow[-1] = zInter
                            
            except:
                self.success = False
                return 0     

            self.parameters['x end'] = xInter
            self.parameters['z end'] = zInter

            self.results['x'] = xDebrisFlow
            self.results['z'] = zDebrisFlow
            
            if np.abs(xStart - self.parameters['x end']) < 0.01 :
                self.success = False
            else :
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
            
            zDebrisFlow = list(np.arange(zStart, zxmax, -step))
            zDebrisFlow.append(zxmax)

            if not self.parameters['envelope']:
                xDebrisFlow = [xStart + 1.9 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
            else:
                xDebrisFlow = [xStart + 6.0 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
                
            try:
                xInter, zInter = intersection(np.array(x), np.array(z), np.array(xDebrisFlow[1:]), np.array(zDebrisFlow[1:]))
                xInter = xInter[0]
                zInter = zInter[0]
                
                xDebrisFlow.append(xInter)
                xDebrisFlow.sort()
                
                k = xDebrisFlow.index(xInter)
                xDebrisFlow = xDebrisFlow[:k+1]
                
                zDebrisFlow = zDebrisFlow[:k+1]
                zDebrisFlow[-1] = zInter
            except:
                xInter = xDebrisFlow[-1]
                zInter = zDebrisFlow[-1]
            
            self.parameters['abscisse arrivée'] = xInter
            self.parameters['altitude arrivée'] = zInter

            self.results['abscisses'] = xDebrisFlow
            self.resultats['énergies'] = zDebrisFlow
            
            if np.abs(xStart - self.parameters['x end']) < 0.01:
                self.success = False
            else:
                self.success = True

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes
