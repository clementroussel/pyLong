from pyLong.setting import Setting

from pyLong.layout import Layout
from pyLong.group import Group
from pyLong.preview import Preview

from pyLong.zProfile import zProfile
from pyLong.sProfile import sProfile

from pyLong.text import Text
from pyLong.verticalAnnotation import VerticalAnnotation
from pyLong.linearAnnotation import LinearAnnotation
from pyLong.interval import Interval
from pyLong.rectangle import Rectangle

from pyLong.toolbox.energyLine import *
from pyLong.toolbox.mezap import *
from pyLong.toolbox.flowR import *
from pyLong.toolbox.rickenmann import *
from pyLong.toolbox.corominas import *

from pyLong.otherData import *


class Project:
    
    def __init__(self):
        self.path = ""

        self.settings = Setting()

        self.layouts = []

        layout = Layout()
        layout.title = "layout 0"
        self.layouts.append(layout)

        self.subplots = []

        self.profiles = []

        self.groups = []

        group = Group()
        group.title = "group 0"
        self.groups.append(group)

        self.calculations = []

        self.otherData = []

        self.preview = Preview()

        self.reminderLines = []

        self.modelAnnotation = None

    def new(self):
        self.path = ""

        self.settings = Setting()

        self.preview = Preview()

        self.layouts.clear()
        Layout.counter = -1
        self.layouts.append(Layout())

        self.subplots.clear()

        self.profiles.clear()
        zProfile.counter = 0
        sProfile.counter = 0

        self.groups.clear()
        Group.counter = -1
        self.groups.append(Group())

        Text.counter = 0
        VerticalAnnotation.counter = 0
        LinearAnnotation.counter = 0
        Interval.counter = 0
        Rectangle.counter = 0

        self.calculations.clear()
        EnergyLine.counter = 0
        Mezap.counter = 0
        FlowR.counter = 0
        Rickenmann.counter = 0
        Corominas.counter = 0

        self.otherData.clear()
        OtherData.counter = 0

        self.reminderLines.clear()

    def load(self, project):
        self.path = project.path

        self.settings = project.settings

        self.preview = project.preview

        self.layouts.clear()
        Layout.counter = len(project.layouts) - 1
        self.layouts = project.layouts

        self.subplots = project.subplots

        zProfile.counter = len(project.profiles)
        sProfile.counter = len(project.profiles)
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

        energyLineCounter = 0
        mezapCounter = 0
        rickenmannCounter = 0
        flowrCounter = 0
        corominasCounter = 0

        for calcul in self.calculations:
            if type(calcul) == EnergyLine:
                energyLineCounter += 1
            elif type(calcul) == Mezap:
                mezapCounter += 1
            elif type(calcul) == Rickenmann:
                rickenmannCounter += 1
            elif type(calcul) == FlowR:
                flowrCounter += 1
            else:
                corominasCounter += 1

        EnergyLine.counter = energyLineCounter
        Mezap.counter = mezapCounter
        Rickenmann.counter = rickenmannCounter
        FlowR.counter = flowrCounter
        Corominas.counter = corominasCounter

        OtherData.counter = len(project.otherData)
        self.otherData = project.otherData

        self.reminderLines = project.reminderLines
