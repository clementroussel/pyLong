from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class DialogAddSubplot(QDialog):

    def __init__(self, parent):
        super().__init__()

        self.pyLong = parent.pyLong
        
        self.setWindowTitle("Add a subplot")
        self.setMinimumWidth(250)
        
        mainLayout = QVBoxLayout()

        sublayout = QHBoxLayout()

        label = QLabel("Id :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label)

        self.id = QLineEdit()
        sublayout.addWidget(self.id)

        mainLayout.addLayout(sublayout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)

        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)

    def validate(self):
        if self.id.text().replace(" ", "").replace("\t", "") == "" :
            pass
        elif self.id.text().upper() not in self.pyLong.project.subplots:
            self.pyLong.project.subplots.append(self.id.text().upper())
            self.accept()
        else:
            alert = QMessageBox(self)
            alert.setText("Id already used.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()
