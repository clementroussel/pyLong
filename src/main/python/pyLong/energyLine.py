from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionnaires import *


class LigneEnergie():
    compteur = 0
    def __init__(self):
        LigneEnergie.compteur += 1
        
        self.actif = True
        
        self.intitule = "Ligne d'énergie n°{}".format(LigneEnergie.compteur)
        
        self.legende = ""
        
        self.ligne = {'style': 'solide',
                      'couleur': 'Black',
                      'épaisseur': 0.8}
        
        self.opacite = 1.
        
        self.ordre = 1
        
        self.parametres = {'profil': -1,
                           'méthode': "...",
                           'abscisse départ': 0,
                           'altitude départ': 0,
                           'abscisse arrivée': 0,
                           'altitude arrivée': 0,
                           'angle': 35}
        
        self.calculReussi = False
        
        self.line = Line2D([], [])

    def clear(self):
        self.line = Line2D([], [])
        
    def update(self) :
        self.line.set_data([self.parametres['abscisse départ'], self.parametres['abscisse arrivée']],
                           [self.parametres['altitude départ'], self.parametres['altitude arrivée']])
        if self.actif:
            self.line.set_label(self.legende)
        else:
            self.line.set_label("")

        self.line.set_linestyle(styles2ligne[self.ligne['style']])
        self.line.set_color(couleurs[self.ligne['couleur']])
        self.line.set_linewidth(self.ligne['épaisseur'])
        self.line.set_alpha(self.opacite)
        self.line.set_zorder(self.ordre)
        self.line.set_visible(self.actif and self.calculReussi)
        
    def __del__(self):
        LigneEnergie.compteur -= 1
        
    def calculer(self, pyLong):
        if self.parametres['profil'] == -1:
            self.calculReussi = False
            return 0
        
        elif self.parametres['méthode'] == "départ + arrivée":
            i = self.parametres['profil']
            zprofil, pprofil = pyLong.projet.profils[i]
            xmin = np.min(zprofil.abscisses)
            xmax = np.max(zprofil.abscisses)
            
            abscisse2debut = self.parametres['abscisse départ']
            abscisse2fin = self.parametres['abscisse arrivée']
            
            if xmin < abscisse2debut < xmax:
                self.parametres['altitude départ'] = zprofil.interpoler(abscisse2debut)
            elif abscisse2debut == xmin or abscisse2debut == xmax:
                k = list(zprofil.abscisses).index(abscisse2debut)
                self.parametres['altitude départ'] = zprofil.altitudes[k]
            else:
                self.calculReussi = False
                return 0
            
            if xmin < abscisse2fin < xmax:
                self.parametres['altitude arrivée'] = zprofil.interpoler(abscisse2fin) 
            elif abscisse2fin == xmin or abscisse2fin == xmax:
                k = list(zprofil.abscisses).index(abscisse2fin)
                self.parametres['altitude arrivée'] = zprofil.altitudes[k]  
            else:
                self.calculReussi = False
                return 0                
                
            x1 = np.abs(self.parametres['altitude arrivée'] - self.parametres['altitude départ'])
            x2 = np.abs(self.parametres['abscisse arrivée'] - self.parametres['abscisse départ'])
            
            angle = np.degrees(np.arctan2(x1, x2))
            
            if 0. <= angle <= 90.:
                self.parametres['angle'] = angle
                self.calculReussi = True
            else:
                self.calculReussi = False
                return 0
            
        elif self.parametres['méthode'] == "départ + angle":
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
                zprofil.trier(mode="ascendant")
                pprofil.updateData(zprofil.abscisses, zprofil.altitudes)               
            
            # récupération des paramètres dans des variables nommées plus simplement
            abscisse2debut = self.parametres['abscisse départ']
            angle = self.parametres['angle']
            
            if xmin < abscisse2debut < xmax:
                altitude2debut = zprofil.interpoler(abscisse2debut)
                self.parametres['altitude départ'] = altitude2debut
            elif abscisse2debut == xmin or abscisse2debut == xmax:
                k = list(zprofil.abscisses).index(abscisse2debut)
                altitude2debut = zprofil.altitudes[k]
                self.parametres['altitude départ'] = altitude2debut
            else:
                self.calculReussi = False
                return 0
                
            # fonction représentative de la ligne d'énergie
            if descendant == True:
                f = lambda x : - np.tan(np.radians(angle)) * (x - abscisse2debut) + altitude2debut
                # conservation des points situés "à droite" du point de début
                abscisses = list(zprofil.abscisses)
                if abscisse2debut not in abscisses:
                    abscisses.append(abscisse2debut)
                    abscisses.sort()
                    j = abscisses.index(abscisse2debut)
                    altitudes = np.array(zprofil.altitudes[j-1:])
                    altitudes[0] = zprofil.interpoler(abscisse2debut)
                else:
                    j = abscisses.index(abscisse2debut)
                    altitudes = zprofil.altitudes[j:]
                    
                abscisses = np.array(abscisses[j:])
                
                z = f(abscisses) # altitudes sur la ligne d'énergie
                
                auDessus = list(z - altitudes >= 0) # tableau (True : ligne au dessus du profil | False : ligne en dessous du profil)

                if False in auDessus:
                    k = auDessus.index(False) # indice du point qui suit l'intersection
                    
                    xa = abscisses[k-1] # abscisse du point qui précède l'intersection
                    za = altitudes[k-1] # altitude du point qui précède l'intersection
                    xb = abscisses[k] # abscisse du point qui suit l'intersection
                    zb = altitudes[k] # altitude du point qui suit l'intersection
                    
                    a2 = (zb - za) / (xb - xa) # coefficient directeur de l'équation du segment du profil contenant l'intersection
                    b2 = za - a2 * xa # ordonnée à l'origine de l'équation du segment du profil contenant l'intersection
                    
                    a1 = - np.tan(np.radians(angle)) # coefficient directeur de la ligne d'énergie
                    b1 = altitude2debut - a1 * abscisse2debut # ordonnée à l'origine de la ligne d'énergie
                    
                    xInter = (b2 - b1) / (a1 - a2) # abscisse de l'intersection de la ligne d'énergie avec le profil
                    
                    self.parametres['abscisse arrivée'] = xInter
                    self.parametres['altitude arrivée'] = zprofil.interpoler(xInter)
                        
                else:
                    self.parametres['abscisse arrivée'] = abscisses[-1]
                    self.parametres['altitude arrivée'] = f(abscisses[-1])
                
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
        dict_attr = dict(self.__dict__)
        dict_attr["line"] = Line2D([], [])

        return dict_attr