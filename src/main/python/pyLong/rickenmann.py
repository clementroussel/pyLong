from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionaries import *

from pyLong.intersect import *

class Rickenmann() :
    counter = 0
    
    def __init__(self):
        Rickenmann.counter += 1
        
        self.active = True
        
        self.title = "Rickenmann n°{}".format(Rickenmann.counter)
        
        self.label = ""
        
        self.lineProperties = {'style': 'solid',
                               'color': 'Black',
                               'thickness': 1}
        
        self.opacity = 1.
        
        self.order = 1
        
        self.parameters = {'profile': -1,
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
        
        self.line = Line2D([], [])

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
        
    def run(self, pyLong):
        if self.parameters['profile'] == -1:
            self.success = False
            return 0
        
        # getting hands on profile
        i = self.parameters['profile']
        zprofile, sprofile = pyLong.project.profils[i]
        
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
            
        # ascending case
        if not descending:
            # altitude of starting point
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
                abscissesLave = [xStart - 1.9 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
            else:
                abscissesLave = [xStart - 6.0 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
                
            try:
                xInter, zInter = intersection(np.array(x), np.array(z), np.array(abscissesLave), np.array(zDebrisFlow))
                xInter = xInter[0]
                zInter = zInter[0]
                
                if np.abs(xInter - self.parameters['x start']) < 0.01:
                    xInter = abscissesLave[-1]
                    zInter = zDebrisFlow[-1]
                else:
                    abscissesLave.append(xInter)
                    abscissesLave.sort()
                    abscissesLave.reverse()
                    
                    k = abscissesLave.index(xInter)
                    abscissesLave = abscissesLave[:k+1]
                    
                    zDebrisFlow = zDebrisFlow[:k+1]
                    zDebrisFlow[-1] = zInter
                            
            except:
                self.success = False
                return 0     

            self.parameters['x end'] = xInter
            self.parameters['z end'] = zInter

            self.results['x'] = abscissesLave
            self.results['z'] = zDebrisFlow
            
            if np.abs(self.parameters['x start'] - self.parameters['x end']) < 0.01 :
                self.success = False
            else :
                self.success = True
                
        # descending case
        else:
            # altitude of starting point
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
                abscissesLave = [xStart + 1.9 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
            else:
                abscissesLave = [xStart + 6.0 * volume**0.16 * (zStart - z)**0.83 for z in zDebrisFlow]
                
            try:
                xInter, zInter = intersection(np.array(x), np.array(z), np.array(abscissesLave[1:]), np.array(zDebrisFlow[1:]))
                xInter = xInter[0]
                zInter = zInter[0]
                
                abscissesLave.append(xInter)
                abscissesLave.sort()
                
                k = abscissesLave.index(xInter)
                abscissesLave = abscissesLave[:k+1]
                
                zDebrisFlow = zDebrisFlow[:k+1]
                zDebrisFlow[-1] = zInter
            except:
                xInter = abscissesLave[-1]
                zInter = zDebrisFlow[-1]
            
            self.parameters['x end'] = xInter
            self.parameters['z end'] = zInter

            self.results['x'] = abscissesLave
            self.results['z'] = zDebrisFlow
            
            if np.abs(self.parameters['x start'] - self.parameters['x end']) < 0.01:
                self.success = False
            else:
                self.success = True

    def __getstate__(self):
        dict_attr = dict(self.__dict__)
        dict_attr["line"] = Line2D([], [])

        return dict_attr
