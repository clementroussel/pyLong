from PyQt5.QtWidgets import QVBoxLayout, QListWidgetItem, QMessageBox, QMenu, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

from interface.list import List


class OtherDataList(List):
    def __init__(self, title, parent):
        super().__init__(title, parent)

        self.pyLong = parent

        self.list.doubleClicked.connect(self.pyLong.dataStyle)
        self.list.itemChanged.connect(self.activate)

        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.contextMenu)

        self.popMenu = QMenu(self)
        self.popMenu.addAction(self.pyLong.addDataAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.dataStyleAction)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.pyLong.dataDeleteAction)

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
            indexes = []
            for item in self.list.selectedIndexes():
                indexes.append(item.row())

            indexes.sort()
            indexes.reverse()

            if len(indexes) == 1:
                i = indexes[0]
                data = self.pyLong.project.otherData[i]

                dialog = QMessageBox(self)
                dialog.setWindowTitle("Delete a data")
                dialog.setText("Delete data : {} ?".format(data.title))
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
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
                dialog = QMessageBox(self)
                dialog.setWindowTitle("Delete data")
                dialog.setText("Delete the {} selected data ?".format(len(indexes)))
                dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                dialog.setIcon(QMessageBox.Question)
                answer = dialog.exec_()

                if answer == QMessageBox.Yes:
                    for i in indexes:
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
            alert = QMessageBox(self)
            alert.setText("Select at least one before running this command.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()

    def activate(self):
        for j in range(self.list.count()):
            data = self.pyLong.project.otherData[j]

            if self.list.item(j).checkState() == Qt.Checked:
                data.active = True
            else:
                data.active = False

            data.update()

        self.pyLong.canvas.draw()

    def moveUpMethod(self):
        if self.selection():
            j = self.list.currentRow()

            if j != 0:
                self.pyLong.project.otherData[j-1], self.pyLong.project.otherData[j] = \
                    self.pyLong.project.otherData[j], self.pyLong.project.otherData[j-1]
                self.update()
                self.list.setCurrentRow(j-1)

    def moveDownMethod(self):
        if self.selection():
            j = self.list.currentRow()

            n = self.list.count()

            if j != n-1:
                self.pyLong.project.otherData[j+1], self.pyLong.project.otherData[j] = \
                    self.pyLong.project.otherData[j], self.pyLong.project.otherData[j+1]
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