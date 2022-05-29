from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.zProfile import *
from pyLong.sProfile import *
from pyLong.dictionaries import *


class DialogSimplify(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
 
        mainLayout = QVBoxLayout()
        
        i = self.pyLong.profilesList.list.currentRow()
        self.setWindowTitle("Simplify <{}>".format(self.pyLong.profilesList.list.item(i).text()))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/simplify.png')))
        
        self.zprofile, self.sprofile = self.pyLong.project.profiles[i]
        
        group = QGroupBox("Parameters")
        layout = QGridLayout()
        
        label = QLabel("Percentage of points to keep :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.ratio = QDoubleSpinBox()
        self.ratio.setSuffix(" %")
        self.ratio.setFixedWidth(80)
        self.ratio.setSingleStep(1)
        self.ratio.setRange(0.001, 100)
        self.ratio.setDecimals(3)
        self.ratio.setValue(100)
        self.ratio.setLocale(QLocale('English'))
        self.ratio.valueChanged.connect(self.preview)
        layout.addWidget(self.ratio, 0, 1)
        
        label = QLabel("Output profile title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.title = QLineEdit()
        self.title.setText("profile n°{}".format(zProfile.counter + 1))
        layout.addWidget(self.title, 1, 1)

        layout.addWidget(QLabel(), 2, 0, 1, 2)

        label = QLabel("Before simplification : {} vertices".format(np.shape(self.zprofile.x)[0]))
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0, 1, 2)

        self.info = QLabel("After simplification : {} vertices".format(np.shape(self.zprofile.x)[0]))
        self.info.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.info, 4, 0, 1, 2)

        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

        self.pyLong.project.preview.visible = True
        self.pyLong.project.preview.x = self.zprofile.x
        self.pyLong.project.preview.z = self.zprofile.z
        self.pyLong.project.preview.update()

        self.pyLong.canvas.draw()
        
        self.preview()
        
    def preview(self):
        x, z = self.zprofile.simplify(ratio=self.ratio.value()/100)

        self.pyLong.project.preview.x = x
        self.pyLong.project.preview.z = z
        self.pyLong.project.preview.update()
        
        self.pyLong.canvas.draw()

        self.info.setText("After simplification : {} vertices".format(np.shape(x)[0]))
        
    def validate(self):
        x, z = self.zprofile.simplify(ratio=self.ratio.value()/100)
        
        zprofile = zProfile()
        sprofile = sProfile()
        
        zprofile.title = self.title.text()
        zprofile.x = x
        zprofile.z = z
        zprofile.update()
        
        sprofile.updateData(x, z)
        sprofile.update()

        self.pyLong.project.profiles.append((zprofile, sprofile))
        self.pyLong.profilesList.update()

        self.pyLong.canvas.ax_z.add_line(zprofile.line)
    
        self.accept()
