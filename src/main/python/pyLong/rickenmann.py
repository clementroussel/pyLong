from matplotlib.lines import Line2D
import numpy as np

from pyLong.dictionnaires import *

from pyLong.intersect import *

class Rickenmann() :
    compteur = 0
    
    def __init__(self):
        Rickenmann.compteur += 1
        
        self.actif = True
        
        self.intitule = "Rickenmann n°{}".format(Rickenmann.compteur)
        
        self.legende = ""
        
        self.ligne = {'style': 'solide',
                      'couleur': 'Black',
                      'épaisseur': 0.8}
        
        self.opacite = 1.
        
        self.ordre = 1
        
        self.parametres = {'profil': -1,
                           'abscisse départ': 0,
                           'altitude départ': 0,
                           'abscisse arrivée': 0,
                           'altitude arrivée': 0,
                           'volume': 0,
                           'pas de calcul': 5,
                           'enveloppe': False}
        
        self.resultats = {'abscisses': [],
                          'énergies': []}
        
        self.calculReussi = False
        
        self.line = Line2D([], [])

    def clear(self):
        self.line = Line2D([], [])
        
    def update(self):
        self.line.set_data(self.resultats['abscisses'], self.resultats['énergies'])
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
        Rickenmann.compteur -= 1
        
    def calculer(self, pyLong):
        if self.parametres['profil'] == -1:
            self.calculReussi = False
            return 0
        
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

        # récupération des paramètres dans des variables locales
        abscisses = zprofil.abscisses
        altitudes = zprofil.altitudes
        abscisse2debut = self.parametres['abscisse départ']
        volume = self.parametres['volume']
        pas = self.parametres['pas de calcul']
            
        # calcul dans le cas ascendant
        if not descendant:
            # calcul de l'altitude du point de départ
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
            
            altitudesLave = list(np.arange(altitude2debut, zxmin, -pas))
            altitudesLave.append(zxmin)
            
            if not self.parametres['enveloppe']:
                abscissesLave = [abscisse2debut - 1.9 * volume**0.16 * (altitude2debut - z)**0.83 for z in altitudesLave]
            else:
                abscissesLave = [abscisse2debut - 6.0 * volume**0.16 * (altitude2debut - z)**0.83 for z in altitudesLave]
                
            try:
                xInter, zInter = intersection(np.array(abscisses), np.array(altitudes), np.array(abscissesLave), np.array(altitudesLave))
                xInter = xInter[0]
                zInter = zInter[0]
                
                if np.abs(xInter - self.parametres['abscisse départ']) < 0.01:
                    xInter = abscissesLave[-1]
                    zInter = altitudesLave[-1]
                else:
                    abscissesLave.append(xInter)
                    abscissesLave.sort()
                    abscissesLave.reverse()
                    
                    k = abscissesLave.index(xInter)
                    abscissesLave = abscissesLave[:k+1]
                    
                    altitudesLave = altitudesLave[:k+1]
                    altitudesLave[-1] = zInter
                            
            except:
                self.calculReussi = False
                return 0     

            self.parametres['abscisse arrivée'] = xInter
            self.parametres['altitude arrivée'] = zInter

            self.resultats['abscisses'] = abscissesLave
            self.resultats['énergies'] = altitudesLave
            
            if np.abs(self.parametres['abscisse départ'] - self.parametres['abscisse arrivée']) < 0.01 :
                self.calculReussi = False
            else :
                self.calculReussi = True
                
        # calcul dans le cas descendant
        else:
            # calcul de l'altitude du point de départ
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
            
            altitudesLave = list(np.arange(altitude2debut, zxmax, -pas))
            altitudesLave.append(zxmax)

            if not self.parametres['enveloppe']:
                abscissesLave = [abscisse2debut + 1.9 * volume**0.16 * (altitude2debut - z)**0.83 for z in altitudesLave]
            else:
                abscissesLave = [abscisse2debut + 6.0 * volume**0.16 * (altitude2debut - z)**0.83 for z in altitudesLave]
                
            try:
                xInter, zInter = intersection(np.array(abscisses), np.array(altitudes), np.array(abscissesLave[1:]), np.array(altitudesLave[1:]))
                xInter = xInter[0]
                zInter = zInter[0]
                
                abscissesLave.append(xInter)
                abscissesLave.sort()
                
                k = abscissesLave.index(xInter)
                abscissesLave = abscissesLave[:k+1]
                
                altitudesLave = altitudesLave[:k+1]
                altitudesLave[-1] = zInter
            except:
                xInter = abscissesLave[-1]
                zInter = altitudesLave[-1]
            
            self.parametres['abscisse arrivée'] = xInter
            self.parametres['altitude arrivée'] = zInter

            self.resultats['abscisses'] = abscissesLave
            self.resultats['énergies'] = altitudesLave
            
            if np.abs(self.parametres['abscisse départ'] - self.parametres['abscisse arrivée']) < 0.001:
                self.calculReussi = False
            else:
                self.calculReussi = True

    def __getstate__(self):
        dict_attr = dict(self.__dict__)
        dict_attr["line"] = Line2D([], [])

        return dict_attr