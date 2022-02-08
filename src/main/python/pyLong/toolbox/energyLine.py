from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionaries import lineStyles, colors


class EnergyLine():
    counter = 0

    def __init__(self):
        EnergyLine.counter += 1
        
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
        self.line.set_data([self.parametres['x start'], self.parametres['x end']],
                           [self.parametres['z start'], self.parametres['z end']])
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
                
            # representative function of the energy line
            if descending:
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
                
                above = list(zEnergyLine - z >= 0) # (True : energy ligne above profile | False : energy ligne below profile)

                if False in above:
                    k = above.index(False) # point index which follows the intersection
                    
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
                f = lambda x: + np.tan(np.radians(angle)) * (x - abscisse2debut) + altitude2debut
                # conservation des points situés "à gauche" du point de début
                abscisses = list(zprofil.abscisses)
                if abscisse2debut not in abscisses:
                    abscisses.append(abscisse2debut)
                    abscisses.sort()
                    j = abscisses.index(abscisse2debut)
                    altitudes = np.array(zprofil.altitudes[:j+1])
                    altitudes[-1] = zprofil.interpoler(abscisse2debut)
                else:
                    j = abscisses.index(abscisse2debut)
                    altitudes = zprofil.altitudes[:j+1]
                    
                abscisses = np.array(abscisses[:j+1])
                
                z = f(abscisses) # altitudes sur la ligne d'énergie
                
                enDessous = list(altitudes - z >= 0) # tableau (True : ligne en dessouss du profil | False : ligne au desous du profil)

                if True in enDessous[:-1]:
                    k = enDessous.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 = + np.tan(np.radians(angle)) # coefficient directeur de la ligne d'énergie
                    b1 = altitude2debut - a1 * abscisse2debut # ordonnée à l'origine de la ligne d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la ligne d'énergie avec le profil
                    
                    self.parametres['abscisse arrivée'] = xInter
                    self.parametres['altitude arrivée'] = zprofil.interpoler(xInter)
                    
                else:
                    self.parametres['abscisse arrivée'] = abscisses[0]
                    self.parametres['altitude arrivée'] = f(abscisses[0])
        
            if np.abs(self.parametres['abscisse départ'] - self.parametres['abscisse arrivée']) < 0.001:
                self.calculReussi = False
            else:
                self.calculReussi = True
                
        else: # méthode : arrivée + angle
            # récupération du profil
            i = self.parametres['profil']
            zprofil, pprofil = pyLong.projet.profils[i]
            
            xmin = np.min(zprofil.abscisses)
            xmax = np.max(zprofil.abscisses)
            
            i = list(zprofil.abscisses).index(xmin)
            zxmin = zprofil.altitudes[i]
            i = list(zprofil.abscisses).index(xmax)
            zxmax = zprofil.altitudes[i]
            
            # tri du profil
            if zxmin > zxmax:
                descendant = True
                zprofil.trier(mode="descendant")
                pprofil.updateData(zprofil.abscisses, zprofil.altitudes)
                
            else:
                descendant = False
                zprofil.trier(mode = "ascendant")
                pprofil.updateData(zprofil.abscisses, zprofil.altitudes)               
            
            # récupération des paramètres dans des variables nommées plus simplement
            abscisse2fin = self.parametres['abscisse arrivée']
            angle = self.parametres['angle']
            
            if xmin < abscisse2fin < xmax:
                altitude2fin = zprofil.interpoler(abscisse2fin)
                self.parametres['altitude arrivée'] = altitude2fin
            elif abscisse2fin == xmin or abscisse2fin == xmax:
                k = list(zprofil.abscisses).index(abscisse2fin)
                altitude2fin = zprofil.altitudes[k]
                self.parametres['altitude arrivée'] = altitude2fin
            else:
                self.calculReussi = False
                return 0
                
            if descendant:
                # fonction représentative de la ligne d'énergie
                f = lambda x: - np.tan(np.radians(angle)) * (x - abscisse2fin) + altitude2fin
                
                # conservation des points situés "à gauche" du point de fin
                abscisses = list(zprofil.abscisses)
                
                if abscisse2fin not in abscisses:
                    abscisses.append(abscisse2fin)
                    abscisses.sort()
                    j = abscisses.index(abscisse2fin)
                    altitudes = np.array(zprofil.altitudes[:j+1])
                    altitudes[-1] = zprofil.interpoler(abscisse2fin)
                else:
                    j = abscisses.index(abscisse2fin)
                    altitudes = zprofil.altitudes[:j+1]
                    
                abscisses = np.array(abscisses[:j+1])
                
                z = f(abscisses) # altitudes sur la ligne d'énergie
                
                enDessous = list(altitudes - z >= 0) # tableau (True : ligne en dessous du profil | False : ligne au dessus du profil)   

                if True in enDessous[:-1]:
                    k = enDessous.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 =  - np.tan(np.radians(angle)) # coefficient directeur de la ligne d'énergie
                    b1 = altitude2fin - a1 * abscisse2fin # ordonnée à l'origine de la ligne d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la ligne d'énergie avec le profil
                    
                    self.parametres['abscisse départ'] = xInter
                    self.parametres['altitude départ'] = zprofil.interpoler(xInter)
                    
                else:
                    self.parametres['abscisse départ'] = abscisses[0]
                    self.parametres['altitude départ'] = f(abscisses[0]) 
            
            else: # profil ascendant
                f = lambda x: + np.tan(np.radians(angle)) * (x - abscisse2fin) + altitude2fin
                
                # conservation des points situés "à droite" du point de fin
                abscisses = list(zprofil.abscisses)
                if abscisse2fin not in abscisses:
                    abscisses.append(abscisse2fin)
                    abscisses.sort()
                    j = abscisses.index(abscisse2fin)
                    altitudes = np.array(zprofil.altitudes[j-1:])
                    altitudes[0] = zprofil.interpoler(abscisse2fin)
                else:
                    j = abscisses.index(abscisse2fin)
                    altitudes = zprofil.altitudes[j:]
                    
                abscisses = np.array(abscisses[j:])
                
                z = f(abscisses) # altitudes sur la ligne d'énergie
                
                enDessous = list(z - altitudes >= 0) # tableau (True : ligne au dessus du profil | False : ligne en dessous du profil)

                if False in enDessous:
                    k = enDessous.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 = + np.tan(np.radians(angle)) # coefficient directeur de la ligne d'énergie
                    b1 = altitude2fin - a1 * abscisse2fin # ordonnée à l'origine de la ligne d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la ligne d'énergie avec le profil
                    
                    self.parametres['abscisse départ'] = xInter
                    self.parametres['altitude départ'] = zprofil.interpoler(xInter) 
                    
                else:
                    self.parametres['abscisse départ'] = abscisses[-1]
                    self.parametres['altitude départ'] = f(abscisses[-1])
           
            if np.abs(self.parametres['abscisse départ'] - self.parametres['abscisse arrivée']) < 0.001:
                self.calculReussi = False
            else:
                self.calculReussi = True

    def __getstate__(self):
        attributes = dict(self.__dict__)
        attributes["line"] = Line2D([], [])

        return attributes