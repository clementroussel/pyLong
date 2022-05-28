from matplotlib.lines import Line2D
import numpy as np
from scipy import interpolate

from pyLong.dictionnaires import *


class FlowR():
    compteur = 0

    def __init__(self):
        FlowR.compteur += 1
        
        self.actif = True
        
        self.intitule = "Flow-R n°{}".format(FlowR.compteur)
        
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
                           'angle': 0,
                           'vitesse initiale': 0,
                           'vitesse maximale': 0,
                           'pas de calcul': 1}
        
        self.resultats = {'abscisses': [],
                          'vitesses': [],
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
        FlowR.compteur -= 1
        
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
        angle = self.parametres['angle']
        vitesseIni = self.parametres['vitesse initiale']
        vitesseMax = self.parametres['vitesse maximale']
        pas = self.parametres['pas de calcul']
        
        # accélération de la pesanteur
        g = 9.81
            
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
            
            # fonction d'interpolation du profil en long
            f = interpolate.interp1d(np.array(abscisses), np.array(altitudes))

            abscissesLave = list(np.arange(xmin, abscisse2debut, pas))
            abscissesLave.append(abscisse2debut)
            altitudesLave = list(f(np.array(abscissesLave)))

            n = len(abscissesLave)
            vitessesLave = list(-1 * np.ones(n))
            energiesLave = list(np.zeros(n))
            
            vitessesLave[-1] = vitesseIni
            energiesLave[-1] = altitude2debut + vitesseIni**2 / (2 * g)

            for i in range(1, n):
                expr = vitessesLave[-i]**2 + 2*g*(altitudesLave[-i] - altitudesLave[-i-1]) - 2*g*(abscissesLave[-i] - abscissesLave[-i-1])*np.tan(np.radians(angle))
                if expr > 0:
                    vitessesLave[-i-1] = min(np.sqrt(expr), vitesseMax)
                else:
                    vitessesLave[-i-1] = 0
                    k = -i-1
                    energiesLave[-i-1] = altitudesLave[-i-1]
                    break
                energiesLave[-i-1] = altitudesLave[-i-1] + vitessesLave[-i-1]**2 / (2 * g)
            
            try:
                k = np.argwhere(np.array(vitessesLave) == 0.)[0][0]
            except:
                self.calculReussi = False
                return 0
                
            self.parametres['abscisse arrivée'] = abscissesLave[k]
            self.parametres['altitude arrivée'] = altitudesLave[k]
            self.resultats['vitesses'] = vitessesLave[k:]
            self.resultats['abscisses'] = abscissesLave[k:]
            self.resultats['énergies'] = energiesLave[k:]
            
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
            
            # fonction d'interpolation du profil en long
            f = interpolate.interp1d(np.array(abscisses), np.array(altitudes))

            abscissesLave = list(np.arange(abscisse2debut, xmax, pas))
            abscissesLave.append(xmax)
            altitudesLave = list(f(np.array(abscissesLave)))

            n = len(abscissesLave)
            vitessesLave = list(-1 * np.ones(n))
            energiesLave = list(np.zeros(n))
            
            vitessesLave[0] = vitesseIni
            energiesLave[0] = altitude2debut + vitesseIni**2 / (2 * g)

            for i in range(1,n):
                expr = vitessesLave[i-1]**2 + 2*g*(altitudesLave[i-1] - altitudesLave[i]) - 2*g*(abscissesLave[i] - abscissesLave[i-1])*np.tan(np.radians(angle))
                if expr > 0:
                    vitessesLave[i] = min(np.sqrt(expr), vitesseMax)
                else:
                    vitessesLave[i] = 0
                    k = i
                    energiesLave[i] = altitudesLave[i]
                    break
                energiesLave[i] = altitudesLave[i] + vitessesLave[i]**2 / (2 * g)
            
            try:
                k = np.argwhere(np.array(vitessesLave) == 0.)[0][0]
            except:
                self.calculReussi = False
                return 0
                
            self.parametres['abscisse arrivée'] = abscissesLave[k]
            self.parametres['altitude arrivée'] = altitudesLave[k]
            self.resultats['vitesses'] = vitessesLave[:k+1]
            self.resultats['abscisses'] = abscissesLave[:k+1]
            self.resultats['énergies'] = energiesLave[:k+1]
            
            self.calculReussi = True

    def __getstate__(self):
        dict_attr = dict(self.__dict__)
        dict_attr["line"] = Line2D([], [])

        return dict_attr