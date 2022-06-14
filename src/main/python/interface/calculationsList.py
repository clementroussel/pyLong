from PyQt5.QtWidgets import QVBoxLayout, QListWidgetItem, QMessageBox, QMenu, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from interface.list import List

from pyLong.toolbox.energyLine import EnergyLine
from pyLong.toolbox.mezap import Mezap
from pyLong.toolbox.flowR import FlowR
from pyLong.toolbox.rickenmann import Rickenmann
from pyLong.toolbox.corominas import Corominas

from interface.dialogEnergyLine import *
from interface.dialogMezap import *
from interface.dialogFlowR import *
from interface.dialogRickenmann import *
from interface.dialogCorominas import *


class CalculationsList(List):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.pyLong = parent

        self.list.doubleClicked.connect(self.calculationProperties)
        self.list.itemChanged.connect(self.activate)

        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.toolboxAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.calculationAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.calculationDeleteAction)

        layout = QHBoxLayout()

        sublayout = QVBoxLayout()

        self.goTop.clicked.connect(self.goTopMethod)
        sublayout.addWidget(self.goTop)

        self.moveUp.clicked.connect(self.moveUpMethod)
        sublayout.addWidget(self.moveUp)

        self.moveDown.clicked.connect(self.moveDownMethod)
        sublayout.addWidget(self.moveDown)

        self.goBottom.clicked.connect(self.goBottomMethod)
        sublayout.addWidget(self.goBottom)

        layout.addWidget(self.list)
        layout.addLayout(sublayout)

        self.setLayout(layout)

    def contextMenu(self, point):
        self.popMenu.exec_(self.list.mapToGlobal(point))

    def update(self):
        self.list.clear()
        for calculation in self.pyLong.project.calculations:
            item = QListWidgetItem()
            item.setText(calculation.title)
            if not isinstance(calculation, Mezap):
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if calculation.active:
                    item.setCheckState(Qt.Checked)
                else:
                    item.setCheckState(Qt.Unchecked)
            self.list.addItem(item)

    def selection(self):
        n = self.list.count()
        selections = []

        for i in range(n):
            selections.append(self.list.item(i).isSelected())

        return n > 0 and True in selections

    def calculationProperties(self):
        if self.selection():
            i = self.list.currentRow()
            calculation = self.pyLong.project.calculations[i]

            if isinstance(calculation, EnergyLine):
                DialogEnergyLine(parent=self.pyLong).exec_()
            elif isinstance(calculation, Mezap):
                DialogMezap(parent=self.pyLong).exec_()
            elif isinstance(calculation, FlowR):
                DialogFlowR(parent=self.pyLong).exec_()
            elif isinstance(calculation, Rickenmann):
                DialogRickenmann(parent=self.pyLong).exec_()
            elif isinstance(calculation, Corominas):
                DialogCorominas(parent=self.pyLong).exec_()

        else:
            alerte = QMessageBox(self)
            alerte.setText("Select a calculation before running this command.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def delete(self):
        if self.selection():
            indices = []
            for item in self.list.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]
                calculation = self.pyLong.project.calculations[i]

                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Delete a calculation")
                dialogue.setText("Delete calculation : {} ?".format(calculation.title))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Yes")
                dialogue.button(QMessageBox.No).setText("No")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    if isinstance(calculation, (EnergyLine, Rickenmann, FlowR, Corominas)):
                        calculation.line.remove()

                    self.pyLong.project.calculations.pop(i)
                    self.update()

                    self.pyLong.canvas.updateLegends()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

            else:
                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Delete calculations")
                dialogue.setText("Delete the {} selected calculations ?".format(len(indices)))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Yes")
                dialogue.button(QMessageBox.No).setText("No")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    for i in indices:
                        calculation = self.pyLong.project.calculations[i]
                        if isinstance(calculation, (EnergyLine, Rickenmann, FlowR, Corominas)):
                            calculation.line.remove()

                        self.pyLong.project.calculations.pop(i)

                    self.update()

                    self.pyLong.canvas.updateLegends()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

        else:
            alerte = QMessageBox(self)
            alerte.setText("Select one or more calculation(s) before running this command.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def activate(self):
        for j in range(self.list.count()):
            calculation = self.pyLong.project.calculations[j]
            if not isinstance(calculation, Mezap):
                if self.list.item(j).checkState() == Qt.Checked:
                    calculation.active = True
                else:
                    calculation.active = False

                calculation.update()

        self.pyLong.canvas.draw()

    def moveUpMethod(self):
        if self.selection():
            j = self.list.currentRow()

            if j != 0:
                self.pyLong.project.calculations[j-1], self.pyLong.project.calculations[j] = \
                    self.pyLong.project.calculations[j], self.pyLong.project.calculations[j-1]
                self.update()
                self.list.setCurrentRow(j-1)

    def moveDownMethod(self):
        if self.selection():
            j = self.list.currentRow()

            n = self.list.count()

            if j != n-1:
                self.pyLong.project.calculations[j+1], self.pyLong.project.calculations[j] = \
                    self.pyLong.project.calculations[j], self.pyLong.project.calculations[j+1]
                self.update()
                self.list.setCurrentRow(j+1)

    def goTopMethod(self):
        if self.selection():
            j = self.list.currentRow()

            while j != 0:
                self.moveUpMethod()
                j -= 1

    def goBottomMethod(self):
        if self.selection():
            j = self.list.currentRow()

            n = self.list.count()

            while j != n-1:
                self.moveDownMethod()
                j += 1