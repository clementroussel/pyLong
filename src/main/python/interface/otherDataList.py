from PyQt5.QtWidgets import QVBoxLayout, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

from interface.list import List


class OtherDataList(List):
    def __init__(self, title, parent):
        super().__init__(title)

        self.pyLong = parent

        # self.liste.doubleClicked.connect(self.pyLong.optionsDonnees)
        # self.liste.itemChanged.connect(self.activer)

        # self.liste.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.liste.customContextMenuRequested.connect(self.contextMenu)

        # self.popMenu = QMenu(self)
        # self.popMenu.addAction(self.pyLong.action_ajouterDonnees)
        # self.popMenu.addSeparator()
        # self.popMenu.addAction(self.pyLong.action_styleDonnees)
        # self.popMenu.addSeparator()
        # self.popMenu.addAction(self.pyLong.action_supprimerDonnees)

        layout = QVBoxLayout()

        layout.addWidget(self.list)
        self.setLayout(layout)

    def contextMenu(self, point):
        self.popMenu.exec_(self.list.mapToGlobal(point))

    def update(self):
        self.list.clear()
        for data in self.pyLong.project.otherData:
            item = QListWidgetItem()
            item.setText(data.title)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if data.active:
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
                data = self.pyLong.project.otherData[i]

                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Delete a data")
                dialogue.setText("Delete data : {} ?".format(data.title))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Yes")
                dialogue.button(QMessageBox.No).setText("No")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    try:
                        data.line.remove()
                    except:
                        pass
                    self.pyLong.project.otherData.pop(i)
                    self.update()
                    self.pyLong.canvas.draw()

                try:
                    self.list.setCurrentRow(i)
                except:
                    pass

            else:
                dialogue = QMessageBox(self)
                dialogue.setWindowTitle("Delete data")
                dialogue.setText("Data the {} selected data ?".format(len(indices)))
                dialogue.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialogue.button(QMessageBox.Yes).setText("Yes")
                dialogue.button(QMessageBox.No).setText("No")
                dialogue.setIcon(QMessageBox.Question)
                reponse = dialogue.exec_()

                if reponse == QMessageBox.Yes:
                    for i in indices:
                        data = self.pyLong.project.otherData[i]
                        data.line.remove()
                        self.pyLong.project.otherData.pop(i)

                    self.update()
                    self.pyLong.canvas.draw()

                    try:
                        self.list.setCurrentRow(i)
                    except:
                        pass

        else:
            alerte = QMessageBox(self)
            alerte.setText("Select one or more data before running this command.")
            alerte.setIcon(QMessageBox.Warning)
            alerte.exec_()

    def activate(self):
        for j in range(self.list.count()):
            data = self.pyLong.project.otherData[j]

            if self.list.item(j).checkState() == Qt.Checked:
                data.active = True
            else:
                data.active = False

            data.update()

        self.pyLong.canvas.draw()
