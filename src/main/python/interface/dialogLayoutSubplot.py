from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

from pyLong.dictionaries import *

from interface.colorsComboBox import *


class DialogLayoutSubplot(QDialog):

    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent.pyLong

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]

        self.parent = parent

        j = self.parent.subplotsList.currentRow()
        self.subplot = self.layout.subplots[j]
        
        self.setWindowTitle("Subplot {} properties".format(self.subplot.id))

        tableWidget = QTabWidget()
        subdivisionsTab = QWidget()
        yAxisTab = QWidget()
        legendTab = QWidget()

        tableWidget.addTab(subdivisionsTab, "Subdivisions")
        tableWidget.addTab(yAxisTab, "Y-Axis")
        tableWidget.addTab(legendTab, "Legend")
        
        layout = QGridLayout()

        label = QLabel("Subdivisions :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        n_actual = self.subplot.subdivisions
        n_total = self.layout.subdivisions

        n = 0
        for subplot in self.layout.subplots:
            n += subplot.subdivisions

        n_max = n_total - n - 1 + n_actual

        self.subdivisions = QSpinBox()
        self.subdivisions.setFixedWidth(40)
        self.subdivisions.setSingleStep(1)
        self.subdivisions.setRange(1, n_max)
        self.subdivisions.setValue(self.subplot.subdivisions)
        self.subdivisions.valueChanged.connect(self.update)
        layout.addWidget(self.subdivisions, 0, 1)

        layout.addWidget(QLabel(), 1, 0, 7, 1)

        subdivisionsTab.setLayout(layout)

        layout = QGridLayout()

        label = QLabel("Min :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.min = QDoubleSpinBox()
        self.min.setFixedWidth(90)
        self.min.setLocale(QLocale('English'))
        self.min.setSingleStep(10)
        self.min.setRange(-99999.999, 99999.999)
        self.min.setDecimals(3)
        self.min.setValue(self.subplot.yAxisProperties['min'])
        self.min.valueChanged.connect(self.updateYAxis)
        layout.addWidget(self.min, 0, 1)

        label = QLabel("Max :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.max = QDoubleSpinBox()
        self.max.setFixedWidth(90)
        self.max.setLocale(QLocale('English'))
        self.max.setSingleStep(10)
        self.max.setRange(-99999.999, 99999.999)
        self.max.setDecimals(3)
        self.max.setValue(self.subplot.yAxisProperties['max'])
        self.max.valueChanged.connect(self.updateYAxis)
        layout.addWidget(self.max, 1, 1)

        label = QLabel("Intervals :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.intervals = QSpinBox()
        self.intervals.setFixedWidth(40)
        self.intervals.setSingleStep(1)
        self.intervals.setRange(1,99)
        self.intervals.setValue(self.subplot.yAxisProperties['intervals'])
        self.intervals.valueChanged.connect(self.updateYAxis)
        layout.addWidget(self.intervals, 2, 1)

        label = QLabel("Axis label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.axisLabel = QLineEdit()
        self.axisLabel.setText(self.subplot.yAxisProperties['label'])
        self.axisLabel.textChanged.connect(self.updateYAxis)
        layout.addWidget(self.axisLabel, 3, 1)

        label = QLabel("Label color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.labelColor = ColorsComboBox(self.pyLong.appctxt)
        self.labelColor.setCurrentText(self.subplot.yAxisProperties['label color'])
        self.labelColor.currentTextChanged.connect(self.updateYAxis)
        layout.addWidget(self.labelColor, 4, 1)

        label = QLabel("Value color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)

        self.valueColor = ColorsComboBox(self.pyLong.appctxt)
        self.valueColor.setCurrentText(self.subplot.yAxisProperties['value color'])
        self.valueColor.currentTextChanged.connect(self.updateYAxis)
        layout.addWidget(self.valueColor, 5, 1)

        label = QLabel("Lower shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 6, 0)

        self.lowerShift = QDoubleSpinBox()
        self.lowerShift.setLocale(QLocale('English'))
        self.lowerShift.setFixedWidth(65)
        self.lowerShift.setRange(0, 9999.999)
        self.lowerShift.setDecimals(3)
        self.lowerShift.setSingleStep(1)
        self.lowerShift.setValue(self.subplot.yAxisProperties['lower shift'])
        self.lowerShift.valueChanged.connect(self.updateYAxis)
        layout.addWidget(self.lowerShift, 6, 1)

        label = QLabel("Upper shift :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)

        self.upperShift = QDoubleSpinBox()
        self.upperShift.setLocale(QLocale('English'))
        self.upperShift.setFixedWidth(65)
        self.upperShift.setRange(0, 9999.999)
        self.upperShift.setDecimals(3)
        self.upperShift.setSingleStep(1)
        self.upperShift.setValue(self.subplot.yAxisProperties['upper shift'])
        self.upperShift.valueChanged.connect(self.updateYAxis)
        layout.addWidget(self.upperShift, 7, 1)

        yAxisTab.setLayout(layout)

        layout = QGridLayout()

        self.drawLegend = QCheckBox("Draw legend")
        self.drawLegend.setChecked(self.subplot.legend['active'])
        self.drawLegend.stateChanged.connect(self.updateLegend)
        layout.addWidget(self.drawLegend, 0, 0, 1, 3)

        label = QLabel("Position :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.legendPosition = QComboBox()
        self.legendPosition.insertItems(0, legendPlacements.keys())
        self.legendPosition.setCurrentText(self.subplot.legend['position'])
        self.legendPosition.currentTextChanged.connect(self.updateLegend)
        layout.addWidget(self.legendPosition, 1, 1)

        label = QLabel("Columns :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.columns = QSpinBox()
        self.columns.setFixedWidth(45)
        self.columns.setRange(1, 99)
        self.columns.setValue(self.subplot.legend['columns'])
        self.columns.valueChanged.connect(self.updateLegend)
        layout.addWidget(self.columns, 2, 1)

        layout.addWidget(QLabel(), 3, 0, 5, 1)

        legendTab.setLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainlayout = QVBoxLayout()

        mainlayout.addWidget(tableWidget)

        mainlayout.addWidget(buttonBox)

        self.setLayout(mainlayout)

    def update(self):
        self.subplot.subdivisions = self.subdivisions.value()
        self.pyLong.canvas.updateFigure()

    def updateLegend(self):
        self.subplot.legend['active'] = self.drawLegend.isChecked()
        self.subplot.legend['position'] = self.legendPosition.currentText()
        self.subplot.legend['columns'] = self.columns.value()

        self.pyLong.canvas.updateLegends()

    def updateYAxis(self):
        i = self.parent.subplotsList.currentRow()

        self.subplot.yAxisProperties['min'] = self.min.value()
        self.subplot.yAxisProperties['max'] = self.max.value()
        self.subplot.yAxisProperties['intervals'] = self.intervals.value()
        self.subplot.yAxisProperties['label'] = self.axisLabel.text()
        self.subplot.yAxisProperties['label color'] = self.labelColor.currentText()
        self.subplot.yAxisProperties['value color'] = self.valueColor.currentText()
        self.subplot.yAxisProperties['lower shift'] = self.lowerShift.value()
        self.subplot.yAxisProperties['upper shift'] = self.upperShift.value()

        self.pyLong.canvas.subplots[i].set_ylim((self.subplot.yAxisProperties['min'] - self.subplot.yAxisProperties['lower shift'],
                                                 self.subplot.yAxisProperties['max'] + self.subplot.yAxisProperties['upper shift']))

        self.pyLong.canvas.subplots[i].set_yticks(np.linspace(self.subplot.yAxisProperties['min'],
                                                              self.subplot.yAxisProperties['max'],
                                                              self.subplot.yAxisProperties['intervals'] + 1))

        self.pyLong.canvas.subplots[i].set_ylabel(self.subplot.yAxisProperties['label'],
                                                  {'color': colors[self.subplot.yAxisProperties['label color']],
                                                   'fontsize': self.layout.zAxisProperties['label size']})

        self.pyLong.canvas.subplots[i].tick_params(axis='y',
                                                   colors=colors[self.subplot.yAxisProperties['value color']],
                                                   labelsize=self.layout.zAxisProperties['value size'])

        self.pyLong.canvas.figure.tight_layout(pad=1.75)
        self.pyLong.canvas.figure.subplots_adjust(hspace=self.layout.hspace)
        self.pyLong.canvas.draw()
