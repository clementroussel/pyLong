from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionaries import lineStyles, colors


class EnergyLine():
    counter = 0

    def __init__(self):
        EnergyLine.counter += 1
        
        self.active = True
        
        self.title = "Energy line n°{}".format(EnergyLine.counter)
        
        self.label = ""
        
        self.lineProperties = {'style': 'solid',
                               'color': 'Black',
                               'thickness': 1}
        
        self.opacity = 1.
        
        self.order = 1
        
        self.parameters = {'zprofile': None,
                           'sprofile': None,
                           'method': "",
                           'x start': 0,
                           'z start': 0,
                           'x end': 0,
                           'z end': 0,
                           'angle': 35}
        
        self.success = False
        
        self.clear()

    def clear(self):
        self.line = Line2D([], [])
        
    def update(self) :
        self.line.set_data([self.parameters['x start'], self.parameters['x end']],
                           [self.parameters['z start'], self.parameters['z end']])
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
        EnergyLine.counter -= 1
        
    def calculate(self):
        if self.parameters['zprofile'] is None:
            self.success = False
            return 0
        
        elif self.parameters['method'] == "start + end":
            zprofile = self.parameters['zprofile']
            sprofile = self.parameters['sprofile']

            xmin = np.min(zprofile.x)
            xmax = np.max(zprofile.x)
            
            xStart = self.parameters['x start']
            xEnd = self.parameters['x end']
            
            if xmin < xStart < xmax:
                self.parameters['z start'] = zprofile.interpolate(xStart)
            elif xStart == xmin or xStart == xmax:
                k = list(zprofile.x).index(xStart)
                self.parameters['z start'] = zprofile.z[k]
            else:
                self.success = False
                return 0
            
            if xmin < xEnd < xmax:
                self.parameters['z end'] = zprofile.interpolate(xEnd) 
            elif xEnd == xmin or xEnd == xmax:
                k = list(zprofile.x).index(xEnd)
                self.parameters['z end'] = zprofile.z[k]  
            else:
                self.success = False
                return 0                
                
            x1 = np.abs(self.parameters['z end'] - self.parameters['z start'])
            x2 = np.abs(self.parameters['x end'] - self.parameters['x start'])
            
            angle = np.degrees(np.arctan2(x1, x2))
            
            if 0. <= angle <= 90.:
                self.parameters['angle'] = angle
                self.success = True
            else:
                self.success = False
                return 0
            
        elif self.parameters['method'] == "start + angle":
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
                sprofile.updateData(zprofile.x, zprofile.z)
                
            else:
                descending = False
                zprofile.sort(mode="ascending")
                sprofile.updateData(zprofile.x, zprofile.z)               
            
            # getting hands on parameters
            xStart = self.parameters['x start']
            angle = self.parameters['angle']
            
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
                
            if descending:
                # representative function of the energy line
                f = lambda x : - np.tan(np.radians(angle)) * (x - xStart) + zStart
                # keeping points to the right of the start
                x = list(zprofile.x)
                if xStart not in x:
                    x.append(xStart)
                    x.sort()
                    j = x.index(xStart)
                    z = np.array(zprofile.z[j-1:])
                    z[0] = zprofile.interpolate(xStart)
                else:
                    j = x.index(xStart)
                    z = zprofile.z[j:]
                    
                x = np.array(x[j:])
                
                zEnergyLine = f(x) # altitudes of the energy line
                
                above = list(zEnergyLine - z >= 0) # (True : energy line above profile | False : energy line below profile)

                if False in above:
                    k = above.index(False) # point's index which follows the intersection
                    
                    xa = x[k-1] # point's x-coord which precedes the intersection
                    za = z[k-1] # point's z-coord which precedes the intersection
                    xb = x[k] # point's x-coord which follows the intersection
                    zb = x[k] # point's z-coord which follows the intersection
                    
                    a2 = (zb - za) / (xb - xa) # slope coefficient of the equation of the segment of the profile containing the intersection
                    b2 = za - a2 * xa # ordinate at the origin of the equation of the segment of the profile containing the intersection
                    
                    a1 = - np.tan(np.radians(angle)) # slope coefficient of the energy line
                    b1 = zStart - a1 * xStart # ordinate at the origin of the energy line
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscissa of the intersection of the energy line with the profile
                    
                    self.parameters['x end'] = xInter
                    self.parameters['z end'] = zprofile.interpolate(xInter)
                        
                else:
                    self.parameters['x end'] = x[-1]
                    self.parameters['z end'] = f(x[-1])
                
            else:
                f = lambda x: + np.tan(np.radians(angle)) * (x - xStart) + zStart
                # keeping points to the left of the start
                x = list(zprofile.x)
                if xStart not in x:
                    x.append(xStart)
                    x.sort()
                    j = x.index(xStart)
                    z = np.array(zprofile.z[:j+1])
                    z[-1] = zprofile.interpolate(xStart)
                else:
                    j = x.index(xStart)
                    z = zprofile.z[:j+1]
                    
                x = np.array(x[:j+1])
                
                zEnergyLine = f(x) # altitudes of the energy line
                
                below = list(z - zEnergyLine >= 0) # (True : energy line below profile | False : energy line above profile)

                if True in below[:-1]:
                    k = below.index(False) # point's index which follows the intersection
                    
                    xa = x[k-1] # point's x-coord which precedes the intersection
                    za = z[k-1] # point's z-coord which precedes the intersection
                    xb = x[k] # point's x-coord which follows the intersection
                    zb = z[k] # point's z-coord which follows the intersection
                    
                    a2 = (zb - za) / (xb - xa) # slope coefficient of the equation of the segment of the profile containing the intersection
                    b2 = za - a2 * xa # ordinate at the origin of the equation of the segment of the profile containing the intersection
                    
                    a1 = + np.tan(np.radians(angle)) # slope coefficient of the energy line
                    b1 = zStart - a1 * xStart # ordinate at the origin of the energy line
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscissa of the intersection of the energy line with the profile
                    
                    self.parameters['x end'] = xInter
                    self.parameters['z end'] = zprofile.interpolate(xInter)
                    
                else:
                    self.parameters['x end'] = x[0]
                    self.parameters['z end'] = f(x[0])
        
            if np.abs(self.parameters['x start'] - self.parameters['x end']) < 0.01:
                self.success = False
            else:
                self.success = True
                
        else: # method : end + angle
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
                sprofile.updateData(zprofile.x, zprofile.z)
                
            else:
                descending = False
                zprofile.sort(mode = "ascending")
                sprofile.updateData(zprofile.x, zprofile.z)               
            
            # hands on parameters
            xEnd = self.parameters['x end']
            angle = self.parameters['angle']
            
            if xmin < xEnd < xmax:
                zEnd = zprofile.interpolate(xEnd)
                self.parameters['z end'] = zEnd
            elif xEnd == xmin or xEnd == xmax:
                k = list(zprofile.x).index(xEnd)
                zEnd = zprofile.z[k]
                self.parameters['z end'] = zEnd
            else:
                self.success = False
                return 0
                
            if descending:
                # representative function of the energy line
                f = lambda x: - np.tan(np.radians(angle)) * (x - xEnd) + zEnd
                
                # keeping points to the left of the end
                x = list(zprofile.x)
                
                if xEnd not in x:
                    x.append(xEnd)
                    x.sort()
                    j = x.index(xEnd)
                    z = np.array(zprofile.z[:j+1])
                    z[-1] = zprofile.interpolate(xEnd)
                else:
                    j = x.index(xEnd)
                    z = zprofile.z[:j+1]
                    
                x = np.array(x[:j+1])
                
                zEnergyLine = f(x) # altitudes of the energy line
                
                below = list(z - zEnergyLine >= 0) # (True : energy line below profile | False : energy line above profile)   

                if True in below[:-1]:
                    k = below.index(False) # point's index which follows the intersection
                    
                    xa = x[k-1] # point's x-coord which precedes the intersection
                    za = z[k-1] # point's z-coord which precedes the intersection
                    xb = x[k] # point's x-coord which follows the intersection
                    zb = z[k] # point's z-coord which follows the intersection
                    
                    a2 = (zb - za) / (xb - xa) # slope coefficient of the equation of the segment of the profile containing the intersection
                    b2 = za - a2 * xa # ordinate at the origin of the equation of the segment of the profile containing the intersection
                    
                    a1 =  - np.tan(np.radians(angle)) # slope coefficient of the energy line
                    b1 = zEnd - a1 * xEnd # ordinate at the origin of the energy line
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscissa of the intersection of the energy line with the profile
                    
                    self.parameters['x start'] = xInter
                    self.parameters['z start'] = zprofile.interpolate(xInter)
                    
                else:
                    self.parameters['x start'] = x[0]
                    self.parameters['z start'] = f(x[0]) 
            
            else: # ascending case
                f = lambda x: + np.tan(np.radians(angle)) * (x - xEnd) + zEnd
                
                # keeping points to the right of the end
                x = list(zprofile.x)
                if xEnd not in x:
                    x.append(xEnd)
                    x.sort()
                    j = x.index(xEnd)
                    z = np.array(zprofile.z[j-1:])
                    z[0] = zprofile.interpolate(xEnd)
                else:
                    j = x.index(xEnd)
                    z = zprofile.z[j:]
                    
                x = np.array(x[j:])
                
                zEnergyLine = f(x) # altitudes of the energy line
                
                below = list(zEnergyLine - z >= 0) # (True : energy line above profile | False : energy line below profile)

                if False in below:
                    k = below.index(False) # point's index which follows the intersection
                    
                    xa = x[k-1] # point's x-coord which precedes the intersection
                    za = z[k-1] # point's z-coord which precedes the intersection
                    xb = x[k] # point's x-coord which follows the intersection
                    zb = z[k] # point's z-coord which follows the intersection
                    
                    a2 = (zb - za) / (xb - xa) # slope coefficient of the equation of the segment of the profile containing the intersection
                    b2 = za - a2 * xa # ordinate at the origin of the equation of the segment of the profile containing the intersection
                    
                    a1 = + np.tan(np.radians(angle)) # slope coefficient of the energy line
                    b1 = zEnd - a1 * xEnd # ordinate at the origin of the energy line
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscissa of the intersection of the energy line with the profile
                    
                    self.parameters['x start'] = xInter
                    self.parameters['z start'] = zprofile.interpolate(xInter) 
                    
                else:
                    self.parameters['abscisse départ'] = x[-1]
                    self.parameters['altitude départ'] = f(x[-1])
           
            if np.abs(self.parameters['x start'] - self.parameters['x end']) < 0.01:
                self.success = False
            else:
                self.success = True

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes
