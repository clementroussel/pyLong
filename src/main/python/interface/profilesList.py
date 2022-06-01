from PyQt5.QtWidgets import QVBoxLayout, QListWidgetItem, QMessageBox, QMenu, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from interface.list import List

class ProfilesList(List):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.pyLong = parent

        self.list.doubleClicked.connect(self.pyLong.profileStyle)
        self.list.itemChanged.connect(self.activate)

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

        layout = QHBoxLayout()

        sublayout = QVBoxLayout()

        sublayout.addWidget(self.goTop)

        sublayout.addWidget(self.moveUp)

        sublayout.addWidget(self.moveDown)

        sublayout.addWidget(self.goBottom)

        layout.addWidget(self.list)
        layout.addLayout(sublayout)

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

                dialog = QMessageBox(self)
                dialog.setWindowTitle("Delete a profile")
                dialog.setText("Delete : {} ?".format(zprofile.title))
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.button(QMessageBox.Yes).setText("Yes")
                dialog.button(QMessageBox.No).setText("No")
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
                    self.pyLong.project.profiles.pop(i)
                    self.update()

                    if sprofile.annotationsVisible:
                        self.pyLong.canvas.updateFigure()
                    else:
                        zprofile.line.remove()
                        sprofile.trickLine.remove()

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
                dialog = QMessageBox(self)
                dialog.setWindowTitle("Delete profiles")
                dialog.setText("Delete the {} selected profiles ?".format(len(indices)))
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.button(QMessageBox.Yes).setText("Yes")
                dialog.button(QMessageBox.No).setText("No")
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
                    for i in indices:
                        zprofile, sprofile = self.pyLong.project.profiles[i]

                        self.pyLong.project.profiles.pop(i)
                        self.update()

                        if sprofile.annotationsVisible:
                            self.pyLong.canvas.updateFigure()
                        else:
                            zprofile.line.remove()
                            sprofile.trickLine.remove()

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
            alert = QMessageBox(self)
            alert.setText("Select at least one profile before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

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
                self.pyLong.canvas.updateFigure()
            else:
                self.pyLong.canvas.draw()
