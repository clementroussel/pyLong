from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

from pyLong.dictionnaires import *

from pyLong.intersect import *

import matplotlib.pyplot as plt


class Mezap():
    compteur = 0
    def __init__(self):
        Mezap.compteur += 1
        
        self.actif = True
        
        self.intitule = "Mezap n°{}".format(Mezap.compteur)
        
        self.legender = True
        
        self.cheminRapport = ""

        self.exporterValeurs = False

        self.cheminValeur = ""
        
        self.ligne = {'style': 'solide',
                      'épaisseur': 0.8}
        
        self.opacite = 1.
        
        self.ordre = 1
        
        self.parametres = {'profil': -1,
                           'abscisse départ': 0,
                           'altitude départ': 0,
                           'abscisses arrivée': [0, 0, 0],
                           'altitudes arrivée': [0, 0, 0],
                           'angles': [0,0,0]}

        self.abscisses = []
        self.angles = []
        self.airesNormalisees = []
        
        self.calculReussi = False

        self.lineFaible = Line2D([], [])
        self.lineMoyenne = Line2D([], [])
        self.lineForte = Line2D([], [])
        
    def __del__(self) :
        Mezap.compteur -= 1

    def clear(self):
        self.lineFaible = Line2D([], [])
        self.lineMoyenne = Line2D([], [])
        self.lineForte = Line2D([], [])

    def update(self):
        self.lineFaible.set_data([self.parametres['abscisse départ'], self.parametres['abscisses arrivée'][0]],
                                 [self.parametres['altitude départ'], self.parametres['altitudes arrivée'][0]])
        self.lineMoyenne.set_data([self.parametres['abscisse départ'], self.parametres['abscisses arrivée'][1]],
                                 [self.parametres['altitude départ'], self.parametres['altitudes arrivée'][1]])
        self.lineForte.set_data([self.parametres['abscisse départ'], self.parametres['abscisses arrivée'][2]],
                                 [self.parametres['altitude départ'], self.parametres['altitudes arrivée'][2]])

        if self.actif == True and self.legender == True :
            self.lineFaible.set_label("proba. d'atteinte faible ({}°)".format(np.round(self.parametres['angles'][0], 1)))
            self.lineMoyenne.set_label("proba. d'atteinte moyenne ({}°)".format(np.round(self.parametres['angles'][1], 1)))
            self.lineForte.set_label("proba. d'atteinte forte ({}°)".format(np.round(self.parametres['angles'][2], 1)))
        else:
            self.lineFaible.set_label("")
            self.lineMoyenne.set_label("")
            self.lineForte.set_label("")

        self.lineFaible.set_linestyle(styles2ligne[self.ligne['style']])
        self.lineMoyenne.set_linestyle(styles2ligne[self.ligne['style']])
        self.lineForte.set_linestyle(styles2ligne[self.ligne['style']])

        self.lineFaible.set_color("Green")
        self.lineMoyenne.set_color("Orange")
        self.lineForte.set_color("Red")

        self.lineFaible.set_linewidth(self.ligne['épaisseur'])
        self.lineMoyenne.set_linewidth(self.ligne['épaisseur'])
        self.lineForte.set_linewidth(self.ligne['épaisseur'])

        self.lineFaible.set_alpha(self.opacite)
        self.lineMoyenne.set_alpha(self.opacite)
        self.lineForte.set_alpha(self.opacite)

        self.lineFaible.set_zorder(self.ordre)
        self.lineMoyenne.set_zorder(self.ordre)
        self.lineForte.set_zorder(self.ordre)

        self.lineFaible.set_visible(self.actif and self.calculReussi)
        self.lineMoyenne.set_visible(self.actif and self.calculReussi)
        self.lineForte.set_visible(self.actif and self.calculReussi)

    def calculer(self, pyLong):
        if self.parametres['profil'] == -1:
            alerte = QMessageBox()
            alerte.setText("Aucun profil disponible.")
            alerte.exec_()
            self.calculReussi = False
            return 0

        if self.cheminRapport == "":
            alerte = QMessageBox()
            alerte.setText("Indiquer un chemin d'accès au rapport.")
            alerte.exec_()
            self.calculReussi = False
            return 0

        i = self.parametres['profil']
        zprofil, pprofil = pyLong.projet.profils[i]
        xmin = np.min(zprofil.abscisses)
        xmax = np.max(zprofil.abscisses)

        abscisse2debut = self.parametres['abscisse départ']

        # interpolation de l'altitude du point de départ
        if xmin < abscisse2debut < xmax:
            self.parametres['altitude départ'] = zprofil.interpoler(abscisse2debut)
            altitude2debut = self.parametres['altitude départ']
        elif abscisse2debut == xmin or abscisse2debut == xmax:
            k = list(zprofil.abscisses).index(abscisse2debut)
            self.parametres['altitude départ'] = zprofil.altitudes[k]
            altitude2debut = self.parametres['altitude départ']
        else:
            alerte = QMessageBox()
            alerte.setText("L'abscisse de départ est hors intervalle.")
            alerte.exec_()
            self.calculReussi = False
            return 0

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

        if not descendant:
            alerte = QMessageBox()
            alerte.setText("Le calcul n'est possible qu'avec un profil en long descendant.")
            alerte.exec_()
            return 0

        # traitement dans le cas d'un profil descendant
        else:
            abscisses = list(zprofil.abscisses)
            if abscisse2debut not in abscisses:
                abscisses.append(abscisse2debut)
                abscisses.sort()
                j = abscisses.index(abscisse2debut)
                altitudes = np.array(zprofil.altitudes[j - 1:])
                altitudes[0] = zprofil.interpoler(abscisse2debut)
            else:
                j = abscisses.index(abscisse2debut)
                altitudes = zprofil.altitudes[j:]

            abscisses = np.array(abscisses[j:])

            # calcul des angles d'énergie entre le point de départ et chaque point du profil
            betas = np.zeros(len(abscisses))
            betas[0] = 0
            betas[1:] = np.degrees([np.arctan2(np.abs(altitudes[0] - z), np.abs(abscisses[0] - x)) for x, z in zip(abscisses[1:], altitudes[1:])])

            # calcul des aires partielles
            airesPartielles = np.zeros(len(abscisses))
            airesPartielles[0] = 0
            airesPartielles[1:] = (abscisses[1:] + abscisses[:-1]) * (altitudes[:-1] - altitudes[1:])
            airesPartielles /= 2.

            # calcul des aires cumulées
            airesCumulees = np.cumsum(airesPartielles)

            # calcul des aires normalisées
            denominateurs = np.ones(len(abscisses))
            denominateurs[1:] = (altitudes[0] - altitudes[1:]) ** 2
            airesNormalisees = airesCumulees / denominateurs

            if self.exporterValeurs:
                self.abscisses = list(abscisses)
                self.angles = list(betas)
                self.airesNormalisees = list(airesNormalisees)

            # base de données
            chemin = pyLong.appctxt.get_resource('mezap/echantillon.txt')
            df = pd.read_csv(chemin,
                             delimiter='\t',
                             decimal=',')
            donnees = np.array(df)
            chemin = pyLong.appctxt.get_resource('mezap/limites_atteinte.txt')
            limites = np.loadtxt(chemin)

            # intersections
            AiresInter, betasInter = intersection(airesNormalisees[1:], betas[1:], limites[:, 0], limites[:, 1])
            airesFaible = list(AiresInter)
            betasFaible = list(betasInter)

            AiresInter, betasInter = intersection(airesNormalisees[1:], betas[1:], limites[:, 0], limites[:, 2])
            airesMoyen = list(AiresInter)
            betasMoyen = list(betasInter)

            AiresInter, betasInter = intersection(airesNormalisees[1:], betas[1:], limites[:, 0], limites[:, 3])
            airesFort = list(AiresInter)
            betasFort = list(betasInter)

            airesInter = []
            betasInter = []

            airesInter += airesFort
            airesInter += airesMoyen
            airesInter += airesFaible

            betasInter += betasFort
            betasInter += betasMoyen
            betasInter += betasFaible

            data = []
            for i in range(len(airesInter)) :
                data.append([str(np.round(airesInter[i],2)), str(np.round(betasInter[i],2))])

            colors = []

            for i in range(len(airesFort)) :
                colors.append(['Red', 'Red'])
            for i in range(len(airesMoyen)) :
                colors.append(['Orange', 'Orange'])
            for i in range(len(airesFaible)) :
                colors.append(['Green', 'Green'])

            # rapport
            plt.rcParams['pdf.fonttype'] = 42
            fig, (ax0, ax) = plt.subplots(2, 1)
            fig.set_size_inches(21 / 2.54, 29.7 / 2.54)
            ax0.set_title("Rapport de calcul")
            ax0.axis('off')
            ax0.text(0, 0.7, "pyLong ©ONF-RTM")
            ax0.text(0, 0.5,"Calcul de lignes d’énergie à partir de l’aire normalisée et d’échantillon de valeurs relevées\n(Méthode MEZAP, rapport BRGM RP-66589-FR).")
            ax0.text(0, 0.3,"Les échantillons de valeurs sont issus d’une base de données collectées par l’IRSTEA et le\nBRGM (dont des données RTM).")
            ax0.text(0, 0.1,"Les valeurs de probabilité d’atteinte forte, moyenne et faible sont des valeurs proposées\ndans le cadre de la méthode MEZAP par analyse statistique de l’échantillon.")

            ax.set_xlim(0, 1)
            ax.set_ylim(20, 70)

            ax.set_xlabel("Aire normalisée", {'fontsize': 9})
            ax.set_ylabel("Angle d'énergie (deg)", {'fontsize': 9})
            ax.tick_params(axis='x', labelsize=9)
            ax.tick_params(axis='y', labelsize=9)
            ax.grid(True,
                    alpha=0.5,
                    linestyle='--',
                    linewidth=0.5)

            ax.scatter(donnees[:, 0], donnees[:, 1], s=0.5, color='blue', label="échantillon")
            ax.plot(limites[:, 0], limites[:, 1], color="Green", label="proba. d'atteinte faible", linewidth=0.8)
            ax.plot(limites[:, 0], limites[:, 2], color="Orange", label="proba. d'atteinte moyenne", linewidth=0.8)
            ax.plot(limites[:, 0], limites[:, 3], color="Red", label="proba. d'atteinte forte", linewidth=0.8)
            ax.plot(airesNormalisees[1:], betas[1:], color='black', linewidth=0.8, label="profil normalisé")

            ax.legend(loc='upper right',
                      ncol=1,
                      fontsize=8,
                      frameon=True,
                      bbox_to_anchor=(1, 1),
                      bbox_transform=ax.transAxes)

            ax.xaxis.tick_top()
            ax.xaxis.set_label_position('top')

            try:
                ax.table(cellText=data,
                         cellColours=colors,
                         colLabels=['aire normalisée', "angle d'énergie (deg)"],
                         rowLoc='center',
                         cellLoc='center',
                         bbox=[0.125, -1, 0.75, 0.75])

                plt.tight_layout()

            except:
                alerte = QMessageBox()
                alerte.setText("Aucune intersection n'a été trouvée.")
                alerte.exec_()
                pass

            try:
                plt.savefig(self.cheminRapport)
                self.calculReussi = True

            except:
                alerte = QMessageBox()
                alerte.setText("Le chemin d'accès au rapport n'existe pas ou le rapport est déjà ouvert.")
                alerte.exec_()
                self.calculReussi = True
                pass
