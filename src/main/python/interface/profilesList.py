from PyQt5.QtWidgets import QVBoxLayout, QListWidgetItem, QMessageBox, QMenu
from PyQt5.QtCore import Qt

from interface.list import List

class ProfilesList(List):
    def __init__(self, title, parent):
        super().__init__(title)

        self.pyLong = parent

        # self.liste.doubleClicked.connect(self.pyLong.optionsProfil)
        # self.liste.itemChanged.connect(self.activer)

        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.addProfileAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.tableAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.profileStyleAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.sortAction)
        self.popMenu.addAction(self.pyLong.filterAction)
        self.popMenu.addAction(self.pyLong.simplifyAction)
        self.popMenu.addAction(self.pyLong.exportAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.profileDeleteAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.editingAction)

        layout = QVBoxLayout()

        layout.addWidget(self.list)
        self.setLayout(layout)

    def contextMenu(self, point):
        self.popMenu.exec_(self.list.mapToGlobal(point))

    def update(self):
        self.list.clear()
        for zprofile, sprofile in self.pyLong.project.profiles:
            item = QListWidgetItem()
            item.setText(zprofile.title)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if zprofile.active:
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

    def delete(self):
        if self.selection():
            indices = []
            for item in self.list.selectedIndexes():
                indices.append(item.row())

            indices.sort()
            indices.reverse()

            if len(indices) == 1:
                i = indices[0]
                zprofile, sprofile = self.pyLong.project.profiles[i]

                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Delete a profile")
                dialogue.setText("Delete profile : {} ?".format(zprofile.title))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Yes")
                dialogue.button(QMessageBox.No).setText("No")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    self.pyLong.project.profiles.pop(i)
                    self.update()

                    if sprofile.annotationsVisible:
                        self.pyLong.canvas.plot()
                    else:
                        zprofile.line.remove()

                        try:
                            sprofile.line.remove()
                        except:
                            pass

                        try:
                            sprofile.linePercents.remove()
                        except :
                            pass

                        try:
                            sprofile.lineDegrees.remove()
                        except :
                            pass

                        self.pyLong.canvas.updateLegends()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

            else:
                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Delete profiles")
                dialogue.setText("Delete the {} selected profiles ?".format(len(indices)))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Yes")
                dialogue.button(QMessageBox.No).setText("No")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    for i in indices:
                        zprofile, sprofile = self.pyLong.project.profiles[i]

                        self.pyLong.project.profiles.pop(i)
                        self.update()

                        if sprofile.annotationsVisible:
                            self.pyLong.canvas.plot()
                        else:
                            zprofile.line.remove()

                            try:
                                sprofile.line.remove()
                            except:
                                pass

                            try:
                                sprofile.linePercents.remove()
                            except:
                                pass

                            try:
                                sprofile.lineDegrees.remove()
                            except:
                                pass

                    self.pyLong.canvas.updateLegends()

                    try:
                        self.list.setCurrentRow(i)
                    except:
                        pass

        else:
            alerte = QMessageBox(self)
            alerte.setText("Select one or more profile(s) before running this command.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def activate(self):
        for j in range(self.list.count()):
            zprofile, sprofile = self.pyLong.project.profiles[j]
            if self.list.item(j).checkState() == Qt.Checked:
                zprofile.active = True
                sprofile.active = True
            else:
                zprofile.active = False
                sprofile.active = False

            zprofile.update()
            sprofile.update()

            if sprofile.annotationsVisible:
                self.pyLong.canvas.plot()
            else:
                self.pyLong.canvas.draw()
