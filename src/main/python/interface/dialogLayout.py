from PyQt5.QtWidgets import QDialog, QTabWidget, QWidget, QLabel, QDoubleSpinBox, QPushButton, QSpinBox, QGridLayout, QCheckBox, QComboBox, QDialogButtonBox
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QLocale

import numpy as np

from matplotlib.ticker import AutoMinorLocator

from pyLong.dictionaries import legendPlacements, lineStyles

from interface.dialogAxisOptions import DialogAxisOptions


class DialogLayout(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent

        i = self.pyLong.layoutsList.currentIndex()
        self.layout = self.pyLong.project.layouts[i]
        
        self.slopeSymbol = self.pyLong.project.settings.slopeSymbol
        
        self.setWindowTitle("Layout <{}> properties".format(self.layout.title))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/layout.png')))

        tabWidget = QTabWidget()
        dimensionsTab = QWidget()
        axisTab = QWidget()
        gridTab = QWidget()
        legendTab = QWidget()

        tabWidget.addTab(dimensionsTab, "Dimensions")
        tabWidget.addTab(axisTab, "Axis")
        tabWidget.addTab(gridTab, "Grid")
        tabWidget.addTab(legendTab, "Legend")

        layout = QGridLayout()

        label = QLabel("Width :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)

        self.width = QDoubleSpinBox()
        self.width.setFixedWidth(75)
        self.width.setSuffix(" cm")
        self.width.setLocale(QLocale('English'))
        self.width.setSingleStep(0.1)
        self.width.setRange(0.1, 118.9)
        self.width.setDecimals(1)
        self.width.setValue(self.layout.dimensions['width'])
        self.width.valueChanged.connect(self.updateDimensions)
        layout.addWidget(self.width, 0, 1)

        label = QLabel("Height :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.height = QDoubleSpinBox()
        self.height.setFixedWidth(75)
        self.height.setSuffix(" cm")
        self.height.setLocale(QLocale('English'))
        self.height.setSingleStep(0.1)
        self.height.setRange(0.1, 118.9)
        self.height.setDecimals(1)
        self.height.setValue(self.layout.dimensions['height'])
        self.height.valueChanged.connect(self.updateDimensions)
        layout.addWidget(self.height, 1, 1)

        invert = QPushButton()
        invert.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/invert.png')))
        invert.setAutoDefault(False)
        invert.clicked.connect(self.invert)
        layout.addWidget(invert, 0, 2, 2, 1)

        # layout.addWidget(QLabel(), 3, 2, 1, 2)

        layout.addWidget(QLabel(), 3, 0, 1, 4)
        layout.addWidget(QLabel(), 4, 0)
        layout.addWidget(QLabel(), 5, 0)
        layout.addWidget(QLabel(), 6, 0)

        dimensionsTab.setLayout(layout)

        layout = QGridLayout()

        self.secondaryAxis = QCheckBox("Draw slopes on a secondary axis")
        self.secondaryAxis.setChecked(self.layout.secondaryAxis)
        self.secondaryAxis.stateChanged.connect(self.updateSecondaryAxis)
        layout.addWidget(self.secondaryAxis, 0, 0, 1, 3)

        label = QLabel("min.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1)

        label = QLabel("max.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 2)

        label = QLabel("int.")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 3)

        label = QLabel("X-Axis :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.xMin = QDoubleSpinBox()
        self.xMin.setFixedWidth(90)
        self.xMin.setSuffix(" m")
        self.xMin.setLocale(QLocale('English'))
        self.xMin.setSingleStep(10)
        self.xMin.setRange(0, 99999.999)
        self.xMin.setDecimals(3)
        self.xMin.setValue(self.layout.xAxisProperties['min'])
        self.xMin.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xMin, 2, 1)

        self.xMax = QDoubleSpinBox()
        self.xMax.setFixedWidth(90)
        self.xMax.setSuffix(" m")
        self.xMax.setLocale(QLocale('English'))
        self.xMax.setSingleStep(10)
        self.xMax.setRange(0, 99999.999)
        self.xMax.setDecimals(3)
        self.xMax.setValue(self.layout.xAxisProperties['max'])
        self.xMax.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xMax, 2, 2)

        self.xIntervals = QSpinBox()
        self.xIntervals.setFixedWidth(40)
        self.xIntervals.setSingleStep(1)
        self.xIntervals.setRange(1, 99)
        self.xIntervals.setValue(self.layout.xAxisProperties['intervals'])
        self.xIntervals.valueChanged.connect(self.updateXAxis)
        layout.addWidget(self.xIntervals, 2, 3)

        label = QLabel("Z-Axis :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.zMin = QDoubleSpinBox()
        self.zMin.setFixedWidth(90)
        self.zMin.setSuffix(" m")
        self.zMin.setLocale(QLocale('English'))
        self.zMin.setSingleStep(10)
        self.zMin.setRange(0, 99999.999)
        self.zMin.setDecimals(3)
        self.zMin.setValue(self.layout.zAxisProperties['min'])
        self.zMin.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zMin, 3, 1)

        self.zMax = QDoubleSpinBox()
        self.zMax.setFixedWidth(90)
        self.zMax.setSuffix(" m")
        self.zMax.setLocale(QLocale('English'))
        self.zMax.setSingleStep(10)
        self.zMax.setRange(0, 99999.999)
        self.zMax.setDecimals(3)
        self.zMax.setValue(self.layout.zAxisProperties['max'])
        self.zMax.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zMax, 3, 2)

        self.zIntervals = QSpinBox()
        self.zIntervals.setFixedWidth(40)
        self.zIntervals.setSingleStep(1)
        self.zIntervals.setRange(1, 99)
        self.zIntervals.setValue(self.layout.zAxisProperties['intervals'])
        self.zIntervals.valueChanged.connect(self.updateZAxis)
        layout.addWidget(self.zIntervals, 3, 3)

        label = QLabel("Slopes-Axis :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)

        self.sMin = QDoubleSpinBox()
        self.sMin.setFixedWidth(90)
        self.sMin.setLocale(QLocale('English'))
        self.sMin.setDecimals(1)
        self.sMin.setSingleStep(1)

        if self.slopeSymbol == "%":
            self.sMin.setSuffix(" %")
            self.sMin.setRange(-9999.9, 9999.9)
            self.sMin.setValue(self.layout.slopesAxisProperties['min %'])

        else:
            self.sMin.setSuffix(" °")
            self.sMin.setRange(-90, 90)
            self.sMin.setValue(self.layout.slopesAxisProperties['min °'])

        self.sMin.valueChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sMin, 4, 1)

        self.sMax = QDoubleSpinBox()
        self.sMax.setFixedWidth(90)
        self.sMax.setLocale(QLocale('English'))
        self.sMax.setDecimals(1)
        self.sMax.setSingleStep(1)

        if self.slopeSymbol == "%":
            self.sMax.setSuffix(" %")
            self.sMax.setRange(-9999.9, 9999.9)
            self.sMax.setValue(self.layout.slopesAxisProperties['max %'])

        else:
            self.sMax.setSuffix(" °")
            self.sMax.setRange(-90, 90)
            self.sMax.setValue(self.layout.slopesAxisProperties['max °'])

        self.sMax.valueChanged.connect(self.updateSlopesAxis)
        layout.addWidget(self.sMax, 4, 2)

        self.sIntervals = QSpinBox()
        self.sIntervals.setFixedWidth(40)
        self.sIntervals.setSingleStep(1)
        self.sIntervals.setRange(1, 99)
        self.sIntervals.valueChanged.connect(self.updateSlopesAxis)

        if self.slopeSymbol == "%":
            self.sIntervals.setValue(self.layout.slopesAxisProperties['intervals %'])

        else:
            self.sIntervals.setValue(self.layout.slopesAxisProperties['intervals °'])

        layout.addWidget(self.sIntervals, 4, 3)

        axisOptions = QPushButton("Options")
        axisOptions.setAutoDefault(False)
        axisOptions.clicked.connect(self.axisOptions)
        layout.addWidget(axisOptions, 5, 0)

        axisTab.setLayout(layout)

        layout = QGridLayout()

        self.drawLegend = QCheckBox("Draw the legend")
        self.drawLegend.setChecked(self.layout.legend['active'])
        self.drawLegend.stateChanged.connect(self.updateLegend)
        layout.addWidget(self.drawLegend, 0, 0)

        self.legendFrame = QCheckBox("Frame")
        self.legendFrame.setChecked(self.layout.legend['frame'])
        self.legendFrame.stateChanged.connect(self.updateLegend)
        layout.addWidget(self.legendFrame, 0, 1)

        layout.addWidget(QLabel(), 0, 2)

        label = QLabel("Position :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.legendPosition = QComboBox()
        self.legendPosition.insertItems(0, legendPlacements.keys())
        self.legendPosition.setCurrentText(self.layout.legend['position'])
        self.legendPosition.currentTextChanged.connect(self.updateLegend)
        layout.addWidget(self.legendPosition, 1, 1)

        label = QLabel("Size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.legendSize = QDoubleSpinBox()
        self.legendSize.setFixedWidth(50)
        self.legendSize.setRange(0, 99.9)
        self.legendSize.setDecimals(1)
        self.legendSize.setSingleStep(0.1)
        self.legendSize.setValue(self.layout.legend['size'])
        self.legendSize.setLocale(QLocale('English'))
        self.legendSize.valueChanged.connect(self.updateLegend)
        layout.addWidget(self.legendSize, 2, 1)

        label = QLabel("Columns :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.legendColumns = QSpinBox()
        self.legendColumns.setFixedWidth(45)
        self.legendColumns.setRange(1, 99)
        self.legendColumns.setValue(self.layout.legend['columns'])
        self.legendColumns.valueChanged.connect(self.updateLegend)
        layout.addWidget(self.legendColumns, 3, 1)

        layout.addWidget(QLabel(), 4, 0)
        layout.addWidget(QLabel(), 5, 0)
        layout.addWidget(QLabel(), 6, 0)

        legendTab.setLayout(layout)

        layout = QGridLayout()

        self.drawGrid = QCheckBox("Draw the grid")
        self.drawGrid.setChecked(self.layout.grid['active'])
        self.drawGrid.stateChanged.connect(self.updateGrid)
        layout.addWidget(self.drawGrid, 0, 0)

        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)

        self.gridStyle = QComboBox()
        self.gridStyle.insertItems(0, list(lineStyles.keys()))
        self.gridStyle.setCurrentText(self.layout.grid['style'])
        self.gridStyle.currentTextChanged.connect(self.updateGrid)
        layout.addWidget(self.gridStyle, 1, 1)

        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)

        self.gridThickness = QDoubleSpinBox()
        self.gridThickness.setFixedWidth(50)
        self.gridThickness.setLocale(QLocale('English'))
        self.gridThickness.setRange(0.1, 99.9)
        self.gridThickness.setSingleStep(0.1)
        self.gridThickness.setDecimals(1)
        self.gridThickness.setValue(self.layout.grid['thickness'])
        self.gridThickness.valueChanged.connect(self.updateGrid)
        layout.addWidget(self.gridThickness, 2, 1)

        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.gridOpacity = QDoubleSpinBox()
        self.gridOpacity.setFixedWidth(45)
        self.gridOpacity.setLocale(QLocale('English'))
        self.gridOpacity.setRange(0, 1)
        self.gridOpacity.setSingleStep(0.1)
        self.gridOpacity.setDecimals(1)
        self.gridOpacity.setValue(self.layout.grid['opacity'])
        self.gridOpacity.valueChanged.connect(self.updateGrid)
        layout.addWidget(self.gridOpacity, 3, 1)

        layout.addWidget(QLabel(), 3, 2)
        layout.addWidget(QLabel(), 4, 0)
        layout.addWidget(QLabel(), 5, 0)
        layout.addWidget(QLabel(), 6, 0)

        gridTab.setLayout(layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)

        mainlayout = QGridLayout()

        mainlayout.addWidget(tabWidget, 0, 0)

        mainlayout.addWidget(buttonBox, 1, 0)

        self.setLayout(mainlayout)

    def updateDimensions(self):
        self.layout.dimensions['width'] = self.width.value()
        self.layout.dimensions['height'] = self.height.value()

        self.pyLong.canvas.adjustRatio()

    def updateSecondaryAxis(self):
        self.layout.secondaryAxis = self.secondaryAxis.isChecked()
        self.pyLong.canvas.updateFigure()

    def refresh(self):
        self.pyLong.canvas.updateFigure()

    def updateXAxis(self):
        self.layout.xAxisProperties['min'] = self.xMin.value()
        self.layout.xAxisProperties['max'] = self.xMax.value()
        self.layout.xAxisProperties['intervals'] = self.xIntervals.value()

        self.pyLong.canvas.ax_z.set_xlim((self.layout.xAxisProperties['min'] - self.layout.xAxisProperties['left shift'],
                                          self.layout.xAxisProperties['max'] + self.layout.xAxisProperties['right shift']))

        self.pyLong.canvas.ax_z.set_xticks(np.linspace(self.layout.xAxisProperties['min'],
                                                       self.layout.xAxisProperties['max'],
                                                       self.layout.xAxisProperties['intervals'] + 1))

        for ax in self.pyLong.canvas.subplots:
            ax.set_xlim((self.layout.xAxisProperties['min'] - self.layout.xAxisProperties['left shift'],
                         self.layout.xAxisProperties['max'] + self.layout.xAxisProperties['right shift']))

            ax.set_xticks(np.linspace(self.layout.xAxisProperties['min'],
                                      self.layout.xAxisProperties['max'],
                                      self.layout.xAxisProperties['intervals'] + 1))

        self.pyLong.canvas.draw()

    def updateZAxis(self):
        self.layout.zAxisProperties['min'] = self.zMin.value()
        self.layout.zAxisProperties['max'] = self.zMax.value()
        self.layout.zAxisProperties['intervals'] = self.zIntervals.value()

        self.pyLong.canvas.ax_z.set_ylim((self.layout.zAxisProperties['min'] - self.layout.zAxisProperties['lower shift'],
                                          self.layout.zAxisProperties['max'] + self.layout.zAxisProperties['upper shift']))

        self.pyLong.canvas.ax_z.set_yticks(np.linspace(self.layout.zAxisProperties['min'],
                                                       self.layout.zAxisProperties['max'],
                                                       self.layout.zAxisProperties['intervals'] + 1))

        self.pyLong.canvas.draw()

    def updateSlopesAxis(self):
        self.layout.slopesAxisProperties['min {}'.format(self.slopeSymbol)] = self.sMin.value()
        self.layout.slopesAxisProperties['max {}'.format(self.slopeSymbol)] = self.sMax.value()
        self.layout.slopesAxisProperties['intervals {}'.format(self.slopeSymbol)] = self.sIntervals.value()

        self.pyLong.canvas.ax_p.set_ylim(
            (self.layout.slopesAxisProperties['min {}'.format(self.slopeSymbol)] - self.layout.slopesAxisProperties['lower shift {}'.format(self.slopeSymbol)],
             self.layout.slopesAxisProperties['max {}'.format(self.slopeSymbol)] + self.layout.slopesAxisProperties['upper shift {}'.format(self.slopeSymbol)]))

        self.pyLong.canvas.ax_p.set_yticks(np.linspace(self.layout.slopesAxisProperties['min {}'.format(self.slopeSymbol)],
                                                       self.layout.slopesAxisProperties['max {}'.format(self.slopeSymbol)],
                                                       self.layout.slopesAxisProperties['intervals {}'.format(self.slopeSymbol)] + 1))

        slopeLabels = [str(np.round(p, 1)) + '{}'.format(self.slopeSymbol) for p in np.linspace(self.layout.slopesAxisProperties['min {}'.format(self.slopeSymbol)],
                                                                                                self.layout.slopesAxisProperties['max {}'.format(self.slopeSymbol)],
                                                                                                self.layout.slopesAxisProperties['intervals {}'.format(self.slopeSymbol)] + 1)]

        self.pyLong.canvas.ax_p.set_yticklabels(slopeLabels)

        self.pyLong.canvas.draw()

    def updateGrid(self):
        self.layout.grid['active'] = self.drawGrid.isChecked()
        self.layout.grid['style'] = self.gridStyle.currentText()
        self.layout.grid['thickness'] = self.gridThickness.value()
        self.layout.grid['opacity'] = self.gridOpacity.value()

        for i, ax in enumerate(self.pyLong.canvas.figure.axes):
            if i != 1:
                ax.grid(visible=self.layout.grid['active'],
                        which='major',
                        axis='both',
                        linestyle=lineStyles[self.layout.grid['style']],
                        linewidth=self.layout.grid['thickness'],
                        alpha=self.layout.grid['opacity'],
                        zorder=self.layout.grid['order'])

        self.pyLong.canvas.draw()

    def updateLegend(self):
        self.layout.legend['active'] = self.drawLegend.isChecked()
        self.layout.legend['position'] = self.legendPosition.currentText()
        self.layout.legend['columns'] = self.legendColumns.value()
        self.layout.legend['size'] = self.legendSize.value()
        self.layout.legend['frame'] = self.legendFrame.isChecked()

        self.pyLong.canvas.updateLegends()

        self.pyLong.canvas.draw()

    def axisOptions(self) :
        DialogAxisOptions(self).exec_()

    def invert(self):
        width = self.width.value()
        height = self.height.value()
        self.width.setValue(height)
        self.height.setValue(width)

        self.updateDimensions()
