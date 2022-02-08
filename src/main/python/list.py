from PyQt5.QtWidgets import QGroupBox, QListWidget, QAbstractItemView


class List(QGroupBox):
    def __init__(self, title):
        super().__init__(title)

        self.setCheckable(True)
        self.setChecked(True)
        self.clicked.connect(self.hide)
        self.setFixedWidth(300)

        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def hide(self):
        if self.isChecked():
            self.list.setVisible(True)
        else:
            self.list.setVisible(False)
