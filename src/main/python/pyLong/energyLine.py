from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionaries import *


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
        
        self.parameters = {'profile': -1,
                           'method': '',
                           'x start': 0,
                           'z start': 0,
                           'x end': 0,
                           'z end': 0,
                           'angle': 35}
        
        self.success = False
        
        self.line = Line2D([], [])

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
        
    def run(self, pyLong):
        if self.parameters['profile'] == -1:
            self.success = False
            return 0
        
        elif self.parameters['method'] == "start + end":
            i = self.parameters['profile']
            zprofile, sprofile = pyLong.project.profiles[i]
            xmin = np.min(zprofile.x)
            xmax = np.max(zprofile.x)
            
            xStart = self.parameters['x start']
            xEnd = self.parameters['x end']
            
            if xmin < xStart < xmax:
                self.parameters['z start'] = zprofil.interpolate(xStart)
            elif xStart == xmin or xStart == xmax:
                k = list(zprofile.x).index(xStart)
                self.parameters['z start'] = zprofile.z[k]
            else:
                self.success = False
                return 0
            
            if xmin < xEnd < xmax:
                self.parameters['z end'] = zprofile.interpolate(xEnd) 
            elif xEnd == xmin or xEnd == xmax:
                k = list(zprofil.abscisses).index(xEnd)
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
            i = self.parameters['profile']
            zprofile, sprofile = pyLong.project.profiles[i]
            
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
            xStart = self.parameters['x start']
            angle = self.parameters['angle']
            
            if xmin < xStart < xmax:
                zStart = zprofil.interpolate(xStart)
                self.parameters['z start'] = zStart
            elif xStart == xmin or xStart == xmax:
                k = list(zprofile.x).index(xStart)
                zStart = zprofile.z[k]
                self.parameters['z start'] = zStart
            else:
                self.success = False
                return 0
                
            # representative function of the energy line
            if descending:
                f = lambda x : - np.tan(np.radians(angle)) * (x - xStart) + zStart
                # keeping points on the right of the starting point
                abscisses = list(zprofil.abscisses)
                if xStart not in abscisses:
                    abscisses.append(xStart)
                    abscisses.sort()
                    j = abscisses.index(xStart)
                    altitudes = np.array(zprofil.altitudes[j-1:])
                    altitudes[0] = zprofil.interpolate(xStart)
                else:
                    j = abscisses.index(xStart)
                    altitudes = zprofil.altitudes[j:]
                    
                abscisses = np.array(abscisses[j:])
                
                z = f(abscisses) # altitudes sur la lineProperties d'énergie
                
                auDessus = list(z - altitudes >= 0) # tableau (True : lineProperties au dessus du profil | False : lineProperties en dessous du profil)

                if False in auDessus:
                    k = auDessus.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 = - np.tan(np.radians(angle)) # coefficient directeur de la lineProperties d'énergie
                    b1 = zStart - a1 * xStart # ordonnée à l'origine de la lineProperties d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la lineProperties d'énergie avec le profil
                    
                    self.parameters['x end'] = xInter
                    self.parameters['z end'] = zprofil.interpolate(xInter)
                        
                else:
                    self.parameters['x end'] = abscisses[-1]
                    self.parameters['z end'] = f(abscisses[-1])
                
            else:
                f = lambda x: + np.tan(np.radians(angle)) * (x - xStart) + zStart
                # conservation des points situés "à gauche" du point de début
                abscisses = list(zprofil.abscisses)
                if xStart not in abscisses:
                    abscisses.append(xStart)
                    abscisses.sort()
                    j = abscisses.index(xStart)
                    altitudes = np.array(zprofil.altitudes[:j+1])
                    altitudes[-1] = zprofil.interpolate(xStart)
                else:
                    j = abscisses.index(xStart)
                    altitudes = zprofil.altitudes[:j+1]
                    
                abscisses = np.array(abscisses[:j+1])
                
                z = f(abscisses) # altitudes sur la ligne d'énergie
                
                enDessous = list(altitudes - z >= 0) # tableau (True : lineProperties en dessouss du profil | False : lineProperties au desous du profil)

                if True in enDessous[:-1]:
                    k = enDessous.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 = + np.tan(np.radians(angle)) # coefficient directeur de la lineProperties d'énergie
                    b1 = zStart - a1 * xStart # ordonnée à l'origine de la lineProperties d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la lineProperties d'énergie avec le profil
                    
                    self.parameters['x end'] = xInter
                    self.parameters['z end'] = zprofil.interpolate(xInter)
                    
                else:
                    self.parameters['x end'] = abscisses[0]
                    self.parameters['z end'] = f(abscisses[0])
        
            if np.abs(self.parameters['x start'] - self.parameters['x end']) < 0.001:
                self.success = False
            else:
                self.success = True
                
        else: # méthode : arrivée + angle
            # récupération du profil
            i = self.parameters['profil']
            zprofil, pprofil = pyLong.projet.profils[i]
            
            xmin = np.min(zprofil.abscisses)
            xmax = np.max(zprofil.abscisses)
            
            i = list(zprofil.abscisses).index(xmin)
            zxmin = zprofil.altitudes[i]
            i = list(zprofil.abscisses).index(xmax)
            zxmax = zprofil.altitudes[i]
            
            # tri du profil
            if zxmin > zxmax:
                descending = True
                zprofil.trier(mode="descending")
                pprofil.updateData(zprofil.abscisses, zprofil.altitudes)
                
            else:
                descending = False
                zprofil.trier(mode = "ascendant")
                pprofil.updateData(zprofil.abscisses, zprofil.altitudes)               
            
            # récupération des paramètres dans des variables nommées plus simplement
            xEnd = self.parameters['x end']
            angle = self.parameters['angle']
            
            if xmin < xEnd < xmax:
                altitude2fin = zprofil.interpolate(xEnd)
                self.parameters['z end'] = altitude2fin
            elif xEnd == xmin or xEnd == xmax:
                k = list(zprofil.abscisses).index(xEnd)
                altitude2fin = zprofil.altitudes[k]
                self.parameters['z end'] = altitude2fin
            else:
                self.success = False
                return 0
                
            if descending:
                # fonction représentative de la lineProperties d'énergie
                f = lambda x: - np.tan(np.radians(angle)) * (x - xEnd) + altitude2fin
                
                # conservation des points situés "à gauche" du point de fin
                abscisses = list(zprofil.abscisses)
                
                if xEnd not in abscisses:
                    abscisses.append(xEnd)
                    abscisses.sort()
                    j = abscisses.index(xEnd)
                    altitudes = np.array(zprofil.altitudes[:j+1])
                    altitudes[-1] = zprofil.interpolate(xEnd)
                else:
                    j = abscisses.index(xEnd)
                    altitudes = zprofil.altitudes[:j+1]
                    
                abscisses = np.array(abscisses[:j+1])
                
                z = f(abscisses) # altitudes sur la lineProperties d'énergie
                
                enDessous = list(altitudes - z >= 0) # tableau (True : lineProperties en dessous du profil | False : lineProperties au dessus du profil)   

                if True in enDessous[:-1]:
                    k = enDessous.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 =  - np.tan(np.radians(angle)) # coefficient directeur de la lineProperties d'énergie
                    b1 = altitude2fin - a1 * xEnd # ordonnée à l'origine de la lineProperties d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la lineProperties d'énergie avec le profil
                    
                    self.parameters['x start'] = xInter
                    self.parameters['z start'] = zprofil.interpolate(xInter)
                    
                else:
                    self.parameters['x start'] = abscisses[0]
                    self.parameters['z start'] = f(abscisses[0]) 
            
            else: # profil ascendant
                f = lambda x: + np.tan(np.radians(angle)) * (x - xEnd) + altitude2fin
                
                # conservation des points situés "à droite" du point de fin
                abscisses = list(zprofil.abscisses)
                if xEnd not in abscisses:
                    abscisses.append(xEnd)
                    abscisses.sort()
                    j = abscisses.index(xEnd)
                    altitudes = np.array(zprofil.altitudes[j-1:])
                    altitudes[0] = zprofil.interpolate(xEnd)
                else:
                    j = abscisses.index(xEnd)
                    altitudes = zprofil.altitudes[j:]
                    
                abscisses = np.array(abscisses[j:])
                
                z = f(abscisses) # altitudes sur la lineProperties d'énergie
                
                enDessous = list(z - altitudes >= 0) # tableau (True : lineProperties au dessus du profil | False : lineProperties en dessous du profil)

                if False in enDessous:
                    k = enDessous.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 = + np.tan(np.radians(angle)) # coefficient directeur de la lineProperties d'énergie
                    b1 = altitude2fin - a1 * xEnd # ordonnée à l'origine de la lineProperties d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la lineProperties d'énergie avec le profil
                    
                    self.parameters['x start'] = xInter
                    self.parameters['z start'] = zprofil.interpolate(xInter) 
                    
                else:
                    self.parameters['x start'] = abscisses[-1]
                    self.parameters['z start'] = f(abscisses[-1])
           
            if np.abs(self.parameters['x start'] - self.parameters['x end']) < 0.001:
                self.success = False
            else:
                self.success = True

    def __getstate__(self):
        dict_attr = dict(self.__dict__)
        dict_attr["line"] = Line2D([], [])

        return dict_attr