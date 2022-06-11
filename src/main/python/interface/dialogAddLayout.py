from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.layout import *
from pyLong.subplot import *


class DialogAddLayout(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Add a layout")
        
        mainLayout = QVBoxLayout()
        
        group = QGroupBox("New layout")
        layout = QGridLayout()
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.title = QLineEdit()
        self.title.setText("layout {}".format(Layout.counter + 1))
        layout.addWidget(self.title, 0, 1)
        
        self.duplicate = QCheckBox("Duplicate layout :")
        self.duplicate.stateChanged.connect(self.updateInterface)
        layout.addWidget(self.duplicate, 1, 0)
        
        self.layoutsList = QComboBox()
        for laYout in self.pyLong.project.layouts:
            self.layoutsList.addItem(laYout.title)
        self.layoutsList.setCurrentText(self.pyLong.layoutsList.currentText())
        layout.addWidget(self.layoutsList, 1, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        
        layout = QHBoxLayout()
        layout.addWidget(buttonBox)
        
        mainLayout.addLayout(layout)

        self.setLayout(mainLayout)
        
        self.updateInterface()
        
    def updateInterface(self):
        if self.duplicate.isChecked():
            self.layoutsList.setEnabled(True)
        else:
            self.layoutsList.setEnabled(False)
            
    def validate(self):
        layout = Layout()
        layout.title = self.title.text()
        
        if self.duplicate.isChecked():
            i = self.layoutsList.currentIndex()
            layoutReference = self.pyLong.project.layouts[i]

            layout.dimensions['width'] = layoutReference.dimensions['width']
            layout.dimensions['height'] = layoutReference.dimensions['height']
            layout.format = layoutReference.format
            layout.secondaryAxis = layoutReference.secondaryAxis
            
            layout.xAxisProperties['min'] = layoutReference.xAxisProperties['min']
            layout.xAxisProperties['max'] = layoutReference.xAxisProperties['max']
            layout.xAxisProperties['intervals'] = layoutReference.xAxisProperties['intervals']
            
            layout.zAxisProperties['min'] = layoutReference.zAxisProperties['min']
            layout.zAxisProperties['max'] = layoutReference.zAxisProperties['max']
            layout.zAxisProperties['intervals'] = layoutReference.zAxisProperties['intervals']
            
            layout.slopesAxisProperties['min %'] = layoutReference.slopesAxisProperties['min %']
            layout.slopesAxisProperties['max %'] = layoutReference.slopesAxisProperties['max %']
            layout.slopesAxisProperties['min °'] = layoutReference.slopesAxisProperties['min °']
            layout.slopesAxisProperties['max °'] = layoutReference.slopesAxisProperties['max °']
            layout.slopesAxisProperties['intervals %'] = layoutReference.slopesAxisProperties['intervals %']
            layout.slopesAxisProperties['intervals °'] = layoutReference.slopesAxisProperties['intervals °']
            
            layout.legend['active'] = layoutReference.legend['active']
            layout.legend['frame'] = layoutReference.legend['frame']
            layout.legend['columns'] = layoutReference.legend['columns']
            layout.legend['size'] = layoutReference.legend['size']
            layout.legend['position'] = layoutReference.legend['position']
            
            layout.grid['active'] = layoutReference.grid['active']
            layout.grid['style'] = layoutReference.grid['style']
            layout.grid['thickness'] = layoutReference.grid['thickness']
            layout.grid['opacity'] = layoutReference.grid['opacity']
            
            layout.xAxisProperties['label'] = layoutReference.xAxisProperties['label']
            layout.zAxisProperties['label'] = layoutReference.zAxisProperties['label']
            layout.slopesAxisProperties['label'] = layoutReference.slopesAxisProperties['label']
            
            layout.xAxisProperties['label size'] = layoutReference.xAxisProperties['label size']
            layout.zAxisProperties['label size'] = layoutReference.zAxisProperties['label size']
            layout.slopesAxisProperties['label size'] = layoutReference.slopesAxisProperties['label size']
            
            layout.xAxisProperties['label color'] = layoutReference.xAxisProperties['label color']
            layout.zAxisProperties['label color'] = layoutReference.zAxisProperties['label color']
            layout.slopesAxisProperties['label color'] = layoutReference.slopesAxisProperties['label color']
            
            layout.xAxisProperties['value size'] = layoutReference.xAxisProperties['value size']
            layout.zAxisProperties['value size'] = layoutReference.zAxisProperties['value size']
            layout.slopesAxisProperties['value size'] = layoutReference.slopesAxisProperties['value size']
            
            layout.xAxisProperties['value color'] = layoutReference.xAxisProperties['value color']
            layout.zAxisProperties['value color'] = layoutReference.zAxisProperties['value color']
            layout.slopesAxisProperties['value color'] = layoutReference.slopesAxisProperties['value color']
            
            layout.xAxisProperties['left shift'] = layoutReference.xAxisProperties['left shift']
            layout.xAxisProperties['right shift'] = layoutReference.xAxisProperties['right shift']
            
            layout.zAxisProperties['lower shift'] = layoutReference.zAxisProperties['lower shift']
            layout.zAxisProperties['upper shift'] = layoutReference.zAxisProperties['upper shift']
            
            layout.slopesAxisProperties['lower shift %'] = layoutReference.slopesAxisProperties['lower shift %']
            layout.slopesAxisProperties['upper shift %'] = layoutReference.slopesAxisProperties['upper shift %']
    
            layout.slopesAxisProperties['lower shift °'] = layoutReference.slopesAxisProperties['lower shift °']
            layout.slopesAxisProperties['upper shift °'] = layoutReference.slopesAxisProperties['upper shift °']

            layout.subdivisions = layoutReference.subdivisions
            layout.hspace = layoutReference.hspace

            for subplotReference in layoutReference.subplots:
                subplot = Subplot()

                subplot.id = subplotReference.id

                subplot.subdivisions = subplotReference.subdivisions

                subplot.yAxisProperties['min'] = subplotReference.yAxisProperties['min']
                subplot.yAxisProperties['max'] = subplotReference.yAxisProperties['max']
                subplot.yAxisProperties['label'] = subplotReference.yAxisProperties['label']
                subplot.yAxisProperties['intervals'] = subplotReference.yAxisProperties['intervals']
                subplot.yAxisProperties['label color'] = subplotReference.yAxisProperties['label color']
                subplot.yAxisProperties['value color'] = subplotReference.yAxisProperties['value color']
                subplot.yAxisProperties['lower shift'] = subplotReference.yAxisProperties['lower shift']
                subplot.yAxisProperties['upper shift'] = subplotReference.yAxisProperties['upper shift']

                subplot.legend['active'] = subplotReference.legend['active']
                subplot.legend['position'] = subplotReference.legend['position']
                subplot.legend['columns'] = subplotReference.legend['columns']

                layout.subplots.append(subplot)
            
            self.pyLong.project.layouts.append(layout)
        else:
            self.pyLong.project.layouts.append(layout)
            
        self.pyLong.layoutsList.addItem(layout.title)
        n = self.pyLong.layoutsList.count()
        self.pyLong.layoutsList.setCurrentIndex(n - 1)

        self.pyLong.canvas.updateFigure()
        self.accept()
