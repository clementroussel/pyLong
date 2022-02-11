from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QGridLayout, QLabel, QDoubleSpinBox, QLineEdit, QSpinBox, QDialogButtonBox
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QLocale

from interface.colorsComboBox import ColorsComboBox

from pyLong.dictionaries import colors

import numpy as np
from matplotlib import pyplot as plt


class DialogAxisOptions(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.parent = parent
        self.pyLong = parent.pyLong
        self.layout = parent.layout
        self.slopeSymbol = self.parent.slopeSymbol
        
        self.setWindowTitle("Options")
        
        mainLayout = QVBoxLayout()
        subLayout = QHBoxLayout()
        
        group = QGroupBox("X-Axis")
        layout = QGridLayout()
        
        label = QLabel("Axis label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.xAxisLabel = QLineEdit()
        self.xAxisLabel.setText(self.layout.xAxisProperties['label'])
        self.xAxisLabel.textEdited.connect(self.updateXAxis)
        layout.addWidget(self.xAxisLabel, 0, 1)
        
        label = QLabel("Label size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.xAxisLabelSize = QDoubleSpinBox()
        self.xAxisLabelSize.setLocale(QLocale('English'))
        self.xAxisLabelSize.setFixedWidth(50)
        self.xAxisLabelSize.setRange(0, 99.9)
        self.xAxisLabelSize.setSingleStep(0.1)
        self.xAxisLabelSize.setDecimals(1)
        self.xAxisLabelSize.setValue(self.layout.xAxisProperties['label size'])
        self.xAxisLabelSize.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xAxisLabelSize, 1, 1)
        
        label = QLabel("Label color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.xAxisLabelColor = ColorsComboBox(self.pyLong.appctxt)
        self.xAxisLabelColor.setCurrentText(self.layout.xAxisProperties['label color'])
        self.xAxisLabelColor.currentTextChanged.connect(self.updateXAxis)
        layout.addWidget(self.xAxisLabelColor, 2, 1)
        
        layout.addWidget(QLabel(""), 3, 0, 1, 2)
        
        label = QLabel("Value size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.xAxisValueSize = QDoubleSpinBox()
        self.xAxisValueSize.setLocale(QLocale('English'))
        self.xAxisValueSize.setFixedWidth(50)
        self.xAxisValueSize.setRange(0, 99.9)
        self.xAxisValueSize.setSingleStep(0.1)
        self.xAxisValueSize.setDecimals(1)
        self.xAxisValueSize.setValue(self.layout.xAxisProperties['value size'])
        self.xAxisValueSize.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xAxisValueSize, 4, 1)
        
        label = QLabel("Value color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.xAxisValueColor = ColorsComboBox(self.pyLong.appctxt)
        self.xAxisValueColor.setCurrentText(self.layout.xAxisProperties['value color'])
        self.xAxisValueColor.currentTextChanged.connect(self.updateXAxis)
        layout.addWidget(self.xAxisValueColor, 5, 1)
        
        layout.addWidget(QLabel(""), 6, 0, 1, 2)
        
        label = QLabel("Left shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)
        
        self.xAxisLeftShift = QSpinBox()
        self.xAxisLeftShift.setSuffix(" m")
        self.xAxisLeftShift.setFixedWidth(65)
        self.xAxisLeftShift.setRange(0, 9999)
        self.xAxisLeftShift.setSingleStep(1)
        self.xAxisLeftShift.setValue(self.layout.xAxisProperties['left shift'])
        self.xAxisLeftShift.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xAxisLeftShift, 7, 1)
        
        label = QLabel("Right shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 8, 0)
        
        self.xAxisRightShift = QSpinBox()
        self.xAxisRightShift.setSuffix(" m")
        self.xAxisRightShift.setFixedWidth(65)
        self.xAxisRightShift.setRange(0, 9999)
        self.xAxisRightShift.setSingleStep(1)
        self.xAxisRightShift.setValue(self.layout.xAxisProperties['right shift'])
        self.xAxisRightShift.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xAxisRightShift, 8, 1)        
        
        group.setLayout(layout)
        subLayout.addWidget(group)
        
        group = QGroupBox("Z-Axis")
        layout = QGridLayout()
        
        label = QLabel("Axis label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.zAxisLabel = QLineEdit()
        self.zAxisLabel.setText(self.layout.zAxisProperties['label'])
        self.zAxisLabel.textEdited.connect(self.updateZAxis)
        layout.addWidget(self.zAxisLabel, 0, 1)
        
        label = QLabel("Label size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.zAxisLabelSize = QDoubleSpinBox()
        self.zAxisLabelSize.setLocale(QLocale('English'))
        self.zAxisLabelSize.setFixedWidth(50)
        self.zAxisLabelSize.setRange(0, 99.9)
        self.zAxisLabelSize.setSingleStep(0.1)
        self.zAxisLabelSize.setDecimals(1)
        self.zAxisLabelSize.setValue(self.layout.zAxisProperties['label size'])
        self.zAxisLabelSize.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zAxisLabelSize, 1, 1)
        
        label = QLabel("Label color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.zAxisLabelColor = ColorsComboBox(self.pyLong.appctxt)
        self.zAxisLabelColor.setCurrentText(self.layout.zAxisProperties['label color'])
        self.zAxisLabelColor.currentTextChanged.connect(self.updateZAxis)
        layout.addWidget(self.zAxisLabelColor, 2, 1)
        
        layout.addWidget(QLabel(""), 3, 0, 1, 2)
        
        label = QLabel("Value size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.zAxisValueSize = QDoubleSpinBox()
        self.zAxisValueSize.setLocale(QLocale('English'))
        self.zAxisValueSize.setFixedWidth(50)
        self.zAxisValueSize.setRange(0, 99.9)
        self.zAxisValueSize.setSingleStep(0.1)
        self.zAxisValueSize.setDecimals(1)
        self.zAxisValueSize.setValue(self.layout.zAxisProperties['value size'])
        self.zAxisValueSize.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zAxisValueSize, 4, 1)
        
        label = QLabel("Value color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.zAxisValueColor = ColorsComboBox(self.pyLong.appctxt)
        self.zAxisValueColor.setCurrentText(self.layout.zAxisProperties['value color'])
        self.zAxisValueColor.currentTextChanged.connect(self.updateZAxis)
        layout.addWidget(self.zAxisValueColor, 5, 1)
        
        layout.addWidget(QLabel(""), 6, 0, 1, 2)
            
        label = QLabel("Lower shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)
        
        self.zAxisLowerShift = QSpinBox()
        self.zAxisLowerShift.setSuffix(" m")
        self.zAxisLowerShift.setFixedWidth(65)
        self.zAxisLowerShift.setRange(0, 9999)
        self.zAxisLowerShift.setSingleStep(1)
        self.zAxisLowerShift.setValue(self.layout.zAxisProperties['lower shift'])
        self.zAxisLowerShift.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zAxisLowerShift, 7, 1)
        
        label = QLabel("Upper shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 8, 0)
        
        self.zAxisUpperShift = QSpinBox()
        self.zAxisUpperShift.setSuffix(" m")
        self.zAxisUpperShift.setFixedWidth(65)
        self.zAxisUpperShift.setRange(0, 9999)
        self.zAxisUpperShift.setSingleStep(1)
        self.zAxisUpperShift.setValue(self.layout.zAxisProperties['upper shift'])
        self.zAxisUpperShift.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zAxisUpperShift, 8, 1)
        
        group.setLayout(layout)
        subLayout.addWidget(group)

        group = QGroupBox("Slopes Axis")
        layout = QGridLayout()
        
        label = QLabel("Axis label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.sAxisLabel = QLineEdit()
        self.sAxisLabel.setText(self.layout.slopesAxisProperties['label'])
        self.sAxisLabel.textEdited.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisLabel, 0, 1)
        
        label = QLabel("Label size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.sAxisLabelSize = QDoubleSpinBox()
        self.sAxisLabelSize.setLocale(QLocale('English'))
        self.sAxisLabelSize.setFixedWidth(50)
        self.sAxisLabelSize.setRange(0, 99.9)
        self.sAxisLabelSize.setSingleStep(0.1)
        self.sAxisLabelSize.setDecimals(1)
        self.sAxisLabelSize.setValue(self.layout.slopesAxisProperties['label size'])
        self.sAxisLabelSize.valueChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisLabelSize, 1, 1)
        
        label = QLabel("Label color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.sAxisLabelColor = ColorsComboBox(self.pyLong.appctxt)
        self.sAxisLabelColor.setCurrentText(self.layout.slopesAxisProperties['label color'])
        self.sAxisLabelColor.currentTextChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisLabelColor, 2, 1)
        
        layout.addWidget(QLabel(""), 3, 0, 1, 2)
        
        label = QLabel("Value size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.sAxisValueSize = QDoubleSpinBox()
        self.sAxisValueSize.setLocale(QLocale('English'))
        self.sAxisValueSize.setFixedWidth(50)
        self.sAxisValueSize.setRange(0, 99.9)
        self.sAxisValueSize.setSingleStep(0.1)
        self.sAxisValueSize.setDecimals(1)
        self.sAxisValueSize.setValue(self.layout.slopesAxisProperties['value size'])
        self.sAxisValueSize.valueChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisValueSize, 4, 1)
        
        label = QLabel("Value color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.sAxisValueColor = ColorsComboBox(self.pyLong.appctxt)
        self.sAxisValueColor.setCurrentText(self.layout.slopesAxisProperties['value color'])
        self.sAxisValueColor.currentTextChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisValueColor, 5, 1)
        
        layout.addWidget(QLabel(""), 6, 0, 1, 2)
        
        label = QLabel("Lower shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)
        
        self.sAxisLowerShift = QSpinBox()
        self.sAxisLowerShift.setSuffix(" {}".format(self.slopeSymbol))
        if self.slopeSymbol == "%":
            self.sAxisLowerShift.setFixedWidth(65)
            self.sAxisLowerShift.setRange(0, 9999)
        else:
            self.sAxisLowerShift.setFixedWidth(45)
            self.sAxisLowerShift.setRange(0, 90)
        self.sAxisLowerShift.setSingleStep(1)
        self.sAxisLowerShift.setValue(self.layout.slopesAxisProperties['lower shift {}'.format(self.slopeSymbol)])

        self.sAxisLowerShift.valueChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisLowerShift, 7, 1)
        
        label = QLabel("Upper shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 8, 0)
        
        self.sAxisUpperShift = QSpinBox()
        self.sAxisUpperShift.setSuffix(" {}".format(self.slopeSymbol))
        if self.slopeSymbol == "%":
            self.sAxisUpperShift.setFixedWidth(65)
            self.sAxisUpperShift.setRange(0, 9999)
        else:
            self.sAxisUpperShift.setFixedWidth(45)
            self.sAxisUpperShift.setRange(0, 90)
        self.sAxisUpperShift.setSingleStep(1)
        self.sAxisUpperShift.setValue(self.layout.slopesAxisProperties['upper shift {}'.format(self.slopeSymbol)])

        self.sAxisUpperShift.valueChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sAxisUpperShift, 8, 1)
        
        group.setLayout(layout)
        
        if self.parent.secondaryAxis.isChecked():
            subLayout.addWidget(group)
            
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainLayout.addLayout(subLayout)
        mainLayout.addWidget(buttonBox)
            
        self.setLayout(mainLayout)

    def updateXAxis(self):
        self.layout.xAxisProperties['label'] = self.xAxisLabel.text()
        self.layout.xAxisProperties['label size'] = self.xAxisLabelSize.value()
        self.layout.xAxisProperties['label color'] = self.xAxisLabelColor.currentText()
        self.layout.xAxisProperties['value size'] = self.xAxisValueSize.value()
        self.layout.xAxisProperties['value color'] = self.xAxisValueColor.currentText()
        self.layout.xAxisProperties['left shift'] = self.xAxisLeftShift.value()
        self.layout.xAxisProperties['right shift'] = self.xAxisRightShift.value()

        n_subdivisions = self.layout.subdivisions
        n_subplots = len(self.layout.subplots)

        self.pyLong.canvas.ax_z.set_xlim((self.layout.xAxisProperties['min'] - self.layout.xAxisProperties['left shift'],
                                          self.layout.xAxisProperties['max'] + self.layout.xAxisProperties['right shift']))

        self.pyLong.canvas.ax_z.tick_params(axis='x',
                                            colors=colors[self.layout.xAxisProperties['value color']],
                                            labelsize=self.layout.xAxisProperties['value size'])

        if n_subdivisions > 1 and n_subplots > 0:
            pass
        else:
            self.pyLong.canvas.ax_z.set_xlabel(self.layout.xAxisProperties['label'],
                                               {'color': colors[self.layout.xAxisProperties['label color']],
                                                'fontsize': self.layout.xAxisProperties['label size']})

        for i in range(n_subplots):
            self.pyLong.canvas.subplots[i].set_xlim((self.layout.xAxisProperties['min'] - self.layout.xAxisProperties['left shift'],
                                                     self.layout.xAxisProperties['max'] + self.layout.xAxisProperties['right shift']))

            self.pyLong.canvas.subplots[i].tick_params(axis='x',
                                                       colors=colors[self.layout.xAxisProperties['value color']],
                                                       labelsize=self.layout.xAxisProperties['value size'])

            if i != n_subplots - 1:
                plt.setp(self.pyLong.canvas.subplots[i].get_xticklabels(), visible=False)
                self.pyLong.canvas.subplots[i].tick_params(axis='x', length=0)
            else:
                self.pyLong.canvas.subplots[i].set_xlabel(self.layout.xAxisProperties['label'],
                                                          {'color': colors[self.layout.xAxisProperties['label color']],
                                                           'fontsize': self.layout.xAxisProperties['label size']})

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)
        self.pyLong.canvas.draw()

    def updateZAxis(self):
        self.layout.zAxisProperties['label'] = self.zAxisLabel.text()
        self.layout.zAxisProperties['label size'] = self.zAxisLabelSize.value()
        self.layout.zAxisProperties['label color'] = self.zAxisLabelColor.currentText()
        self.layout.zAxisProperties['value size'] = self.zAxisValueSize.value()
        self.layout.zAxisProperties['value color'] = self.zAxisValueColor.currentText()
        self.layout.zAxisProperties['lower shift'] = self.zAxisLowerShift.value()
        self.layout.zAxisProperties['upper shift'] = self.zAxisUpperShift.value()

        n_subplots = len(self.layout.subplots)

        self.pyLong.canvas.ax_z.set_ylim((self.layout.zAxisProperties['min'] - self.layout.zAxisProperties['lower shift'],
                                          self.layout.zAxisProperties['max'] + self.layout.zAxisProperties['upper shift']))

        self.pyLong.canvas.ax_z.set_ylabel(self.layout.zAxisProperties['label'],
                                           {'color': colors[self.layout.zAxisProperties['label color']],
                                            'fontsize': self.layout.zAxisProperties['label size']})

        self.pyLong.canvas.ax_z.tick_params(axis='y',
                                            colors=colors[self.layout.zAxisProperties['value color']],
                                            labelsize=self.layout.zAxisProperties['value size'])

        for i in range(n_subplots):
            self.pyLong.canvas.subplots[i].set_ylim((self.layout.subplots[i].yAxisProperties['min'] - self.layout.subplots[i].yAxisProperties['lower shift'],
                                                     self.layout.subplots[i].yAxisProperties['max'] + self.layout.subplots[i].yAxisProperties['upper shift']))

            self.pyLong.canvas.subplots[i].set_ylabel(self.layout.subplots[i].yAxisProperties['label'],
                                                      {'color': colors[self.layout.subplots[i].yAxisProperties['label color']],
                                                       'fontsize': self.layout.zAxisProperties['label size']})

            self.pyLong.canvas.subplots[i].tick_params(axis='y',
                                                       colors=colors[self.layout.subplots[i].yAxisProperties['value color']],
                                                       labelsize=self.layout.zAxisProperties['value size'])

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)
        self.pyLong.canvas.draw()


    def updateSlopesAxis(self):
        self.layout.slopesAxisProperties['label'] = self.sAxisLabel.text()
        self.layout.slopesAxisProperties['label size'] = self.sAxisLabelSize.value()
        self.layout.slopesAxisProperties['label color'] = self.sAxisLabelColor.currentText()
        self.layout.slopesAxisProperties['value size'] = self.sAxisValueSize.value()
        self.layout.slopesAxisProperties['value color'] = self.sAxisValueColor.currentText()


        self.layout.slopesAxisProperties['lower shift {}'.format(self.slopeSymbol)] = self.sAxisLowerShift.value()
        self.layout.slopesAxisProperties['upper shift {}'.format(self.slopeSymbol)] = self.sAxisUpperShift.value()

        self.pyLong.canvas.ax_p.set_ylim((self.layout.slopesAxisProperties['min {}'.format(self.slopeSymbol)] - self.layout.slopesAxisProperties['lower shift {}'.format(self.slopeSymbol)],
                                          self.layout.slopesAxisProperties['max {}'.format(self.slopeSymbol)] + self.layout.slopesAxisProperties['upper shift {}'.format(self.slopeSymbol)]))

        self.pyLong.canvas.ax_p.set_ylabel(self.layout.slopesAxisProperties['label'],
                                           {'color': colors[self.layout.slopesAxisProperties['label color']],
                                            'fontsize': self.layout.slopesAxisProperties['label size']})

        self.pyLong.canvas.ax_p.tick_params(axis='y',
                                            colors=colors[self.layout.slopesAxisProperties['value color']],
                                            labelsize=self.layout.slopesAxisProperties['value size'])

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)
        self.pyLong.canvas.draw()
