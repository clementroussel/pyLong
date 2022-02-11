from PyQt5.QtWidgets import QGroupBox, QListWidget, QAbstractItemView, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

class List(QGroupBox):
    def __init__(self, title, parent):
        super().__init__(title)

        self.pyLong = parent

        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.hide)
        self.setFixedWidth(300)

        self.goTop = QPushButton()
        # goTop.setToolTip("Monter l'annotation en première position")
        self.goTop.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/goTop.png')))
        self.goTop.setIconSize(QSize(10, 10))
        self.goTop.setMaximumWidth(25)

        self.moveUp = QPushButton()
        # moveUp.setToolTip("Monter l'annotation d'un rang")
        self.moveUp.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/moveUp.png')))
        self.moveUp.setIconSize(QSize(10, 10))
        self.moveUp.setMaximumWidth(25)

        self.moveDown = QPushButton()
        # moveDown.setToolTip("Descendre l'annotation d'un rang")
        self.moveDown.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/moveDown.png')))
        self.moveDown.setIconSize(QSize(10, 10))
        self.moveDown.setMaximumWidth(25)

        self.goBottom = QPushButton()
        # goDown.setToolTip("Descendre l'annotation en dernière position")
        self.goBottom.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/goDown.png')))
        self.goBottom.setIconSize(QSize(10, 10))
        self.goBottom.setMaximumWidth(25)

        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def hide(self):
        if self.isChecked():
            self.list.setVisible(True)
            self.goTop.setVisible(True)
            self.moveUp.setVisible(True)
            self.moveDown.setVisible(True)
            self.goBottom.setVisible(True)

        else:
            self.list.setVisible(False)
            self.goTop.setVisible(False)
            self.moveUp.setVisible(False)
            self.moveDown.setVisible(False)
            self.goBottom.setVisible(False)
