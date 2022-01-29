from pyLong.layout import Layout
from pyLong.group import Group
from pyLong.preview import Preview

from pyLong.zProfile import zProfile
#from pyLong.pProfil import *

from pyLong.text import Text
from pyLong.verticalAnnotation import VerticalAnnotation
from pyLong.linearAnnotation import LinearAnnotation
from pyLong.interval import Interval
from pyLong.rectangle import Rectangle

#from pyLong.LigneEnergie import *
#from pyLong.Mezap import *
#from pyLong.FlowR import *
#from pyLong.Rickenmann import *
#from pyLong.Corominas import *

#from pyLong.Donnee import *


class Project:
    
    def __init__(self):
        self.path = ""

        # préférences générales du projet
        #self.preferences = {'pente': '%',
        #                    'sens': 'ascendant',
        #                    'extension': 'png',
        #                    'largeur': 21.0,
        #                    'hauteur': 29.7,
        #                    'dpi': 200,
        #                    'style rappel': 'tiretée',
        #                    'couleur rappel': 'Black',
        #                    'épaisseur rappel': 1,
        #                    'opacité rappel': 1,
        #                    'ordre rappel': 1}

        self.layouts = [Layout()]

        self.subplots = []

        self.profiles = []

        self.groups = [Group()]

        self.calculations = []

        self.otherDatas = []

        self.preview = Preview()

        self.reminderLines = []

    def new(self):
        self.path = ""

        self.layouts.clear()
        Layout.counter = -1
        self.layouts.append(Layout())

        self.subplots.clear()

        self.profiles.clear()
        zProfile.counter = 0
        sProfil.counter = 0

        self.groups.clear()
        Group.counter = -1
        self.groups.append(Group())

        Text.counter = 0
        VerticalAnnotation.counter = 0
        LinearAnnotation.counter = 0
        Interval.counter = 0
        Rectangle.counter = 0

        self.calculations.clear()
        #LigneEnergie.compteur = 0
        #Mezap.compteur = 0
        #FlowR.compteur = 0
        #Rickenmann.compteur = 0
        #Corominas.compteur = 0

        self.otherDatas.clear()
        OtherData.counter = 0

        self.reminderLines.clear()

    def load(self, project):
        self.path = project.path

        #self.preferences = projet.preferences

        self.preview = project.preview

        self.layouts.clear()
        Layout.counter = len(project.layouts) - 1
        self.layouts = project.layouts

        self.subplots = project.subplots

        zProfile.counter = len(project.profiles)
        sProfil.counter = len(project.profiles)
        self.profiles = project.profiles

        self.groups.clear()
        Group.counter = len(project.groups) - 1
        self.groups = project.groups

        Text.counter = 0
        VerticalAnnotation.counter = 0
        LinearAnnotation.counter = 0
        Interval.counter = 0
        Rectangle.counter = 0

        for group in self.groups:
            for annotation in group.annotations:
                if isinstance(annotation, Text):
                    Text.counter += 1
                elif isinstance(annotation, VerticalAnnotation):
                    VerticalAnnotation.counter += 1
                elif isinstance(annotation, LinearAnnotation):
                    LinearAnnotation.counter += 1
                elif isinstance(annotation, Interval):
                    Interval.counter += 1
                else:
                    Rectangle.counter += 1

        self.calculations = project.calculations

        # n_ligneEnergie = 0
        # n_mezap = 0
        # n_rickenmann = 0
        # n_flowr = 0
        # n_corominas = 0

        # for calcul in self.calculs:
        #     if type(calcul) == LigneEnergie:
        #         n_ligneEnergie += 1
        #     elif type(calcul) == Mezap:
        #         n_mezap += 1
        #     elif type(calcul) == Rickenmann:
        #         n_rickenmann += 1
        #     elif type(calcul) == FlowR:
        #         n_flowr += 1
        #     else:
        #         n_corominas += 1

        # LigneEnergie.compteur = n_ligneEnergie
        # Mezap.compteur = n_mezap
        # Rickenmann.compteur = n_rickenmann
        # FlowR.compteur = n_flowr
        # Corominas.compteur = n_corominas

        OtherData.counter = len(project.otherDatas)
        self.otherDatas = project.otherDatas

        self.reminderLines = project.reminderLines
