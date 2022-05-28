from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from DialogChoixSubplot import *
from DialogLayoutSubplot import *


class DialogLayoutAvancee(QDialog):
    def __init__(self, parent):
        super().__init__()

        self.pyLong = parent

        i = self.pyLong.listeLayouts.currentIndex()
        self.layout = self.pyLong.projet.layouts[i]

        self.setWindowTitle("Options avancées de la mise en page : {}".format(self.layout.intitule))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icones/grid.png')))
        
        mainLayout = QVBoxLayout()

        layout = QGridLayout()

        label = QLabel("Nombre total de subdivisions :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.subdivisions = QSpinBox()
        self.subdivisions.setFixedWidth(40)
        self.subdivisions.setRange(1, 99)
        self.subdivisions.setValue(self.layout.subdivisions)
        self.subdivisions.valueChanged.connect(self.appliquer)
        layout.addWidget(self.subdivisions, 0, 1)

        label = QLabel("Espacement :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.espacement = QDoubleSpinBox()
        self.espacement.setFixedWidth(55)
        self.espacement.setLocale(QLocale('English'))
        self.espacement.setRange(0, 1)
        self.espacement.setSingleStep(0.05)
        self.espacement.setDecimals(3)
        self.espacement.setValue(self.layout.hspace)
        self.espacement.valueChanged.connect(self.updateEspacement)
        # self.espacement.valueChanged.connect(self.appliquer)
        layout.addWidget(self.espacement, 1, 1)

        mainLayout.addLayout(layout)

        groupe = QGroupBox("Subplots insérés")
        layout = QVBoxLayout()

        self.listeSubplots = QListWidget()
        self.listeSubplots.doubleClicked.connect(self.proprietesSubplot)
        for subplot in self.layout.subplots:
            self.listeSubplots.addItem("{}".format(subplot.identifiant))

        layout.addWidget(self.listeSubplots)

        sublayout = QHBoxLayout()

        monterSubplot = QPushButton()
        monterSubplot.setAutoDefault(False)
        monterSubplot.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/monter.png')))
        monterSubplot.setFixedSize(QSize(25, 25))
        monterSubplot.clicked.connect(self.monterSubplot)
        sublayout.addWidget(monterSubplot)

        descendreSubplot = QPushButton()
        descendreSubplot.setAutoDefault(False)
        descendreSubplot.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/descendre.png')))
        descendreSubplot.setFixedSize(QSize(25, 25))
        descendreSubplot.clicked.connect(self.descendreSubplot)
        sublayout.addWidget(descendreSubplot)

        sublayout.addWidget(QLabel())

        proprietes = QPushButton()
        proprietes.setAutoDefault(False)
        proprietes.setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/mise_en_page.png')))
        proprietes.setFixedSize(QSize(25, 25))
        proprietes.clicked.connect(self.proprietesSubplot)
        sublayout.addWidget(proprietes)

        sublayout.addWidget(QLabel())

        ajouterSubplot = QPushButton("+")
        ajouterSubplot.setAutoDefault(False)
        ajouterSubplot.setFixedSize(QSize(25, 25))
        ajouterSubplot.clicked.connect(self.ajouterSubplot)
        sublayout.addWidget(ajouterSubplot)

        supprimerSubplots = QPushButton("-")
        supprimerSubplots.setAutoDefault(False)
        supprimerSubplots.setFixedSize(QSize(25, 25))
        supprimerSubplots.clicked.connect(self.supprimerSubplot)
        sublayout.addWidget(supprimerSubplots)

        layout.addLayout(sublayout)

        groupe.setLayout(layout)

        mainLayout.addWidget(groupe)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

        self.checkSubdivisions()

    def monterSubplot(self):
        n = self.listeSubplots.count()
        selections = []

        for i in range(n):
            selections.append(self.listeSubplots.item(i).isSelected())

        i = self.listeSubplots.currentRow()
        if True in selections and i > 0:
            self.layout.subplots[i-1], self.layout.subplots[i] = self.layout.subplots[i], self.layout.subplots[i-1]

            self.updateListeSubplots()
            self.listeSubplots.setCurrentRow(i-1)
            self.pyLong.canvas.dessiner()

    def descendreSubplot(self):
        n = self.listeSubplots.count()
        selections = []

        for i in range(n):
            selections.append(self.listeSubplots.item(i).isSelected())

        i = self.listeSubplots.currentRow()
        if True in selections and i < n-1:
            self.layout.subplots[i + 1], self.layout.subplots[i] = self.layout.subplots[i], self.layout.subplots[i + 1]

            self.updateListeSubplots()
            self.listeSubplots.setCurrentRow(i + 1)
            self.pyLong.canvas.dessiner()

    def proprietesSubplot(self):
        n = self.listeSubplots.count()
        selections = []

        for i in range(n):
            selections.append(self.listeSubplots.item(i).isSelected())

        if True in selections:
            DialogLayoutSubplot(parent=self).exec_()

    def ajouterSubplot(self):
        n = 0
        for subplot in self.layout.subplots:
            n += subplot.subdivisions
        if self.subdivisions.value() > n+1:
            DialogChoixSubplot(parent=self).exec_()
            self.updateListeSubplots()
            self.checkSubdivisions()
            self.appliquer()
        else:
            alerte = QMessageBox(self)
            alerte.setText("Augmenter le nombre de subdivisions pour ajouter un nouveau subplot.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def updateListeSubplots(self):
        self.listeSubplots.clear()
        for subplot in self.layout.subplots:
            self.listeSubplots.addItem("{}".format(subplot.identifiant))

    def appliquer(self):
        self.layout.subdivisions = self.subdivisions.value()
        self.pyLong.canvas.dessiner()

    def checkSubdivisions(self):
        n = 0
        for subplot in self.layout.subplots:
            n += subplot.subdivisions

        self.subdivisions.setMinimum(n+1)

    def updateEspacement(self):
        self.layout.hspace = self.espacement.value()

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)

        self.pyLong.canvas.draw()

    def supprimerSubplot(self):
        i = self.listeSubplots.currentRow()
        if i != -1:
            self.layout.subplots.pop(i)
        self.updateListeSubplots()
        self.checkSubdivisions()
        self.appliquer()
