from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyLong.dictionaries import *
from pyLong.setting import *

from interface.colorsComboBox import *

from pyLong.reminderLine import *


class DialogSettings(QDialog):
    def __init__(self, parent):
        super().__init__()
        
        self.pyLong = parent
        
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/settings.png')))

        mainLayout = QVBoxLayout()

        tableWidget = QTabWidget()
        generalTab = QWidget()
        previewTab = QWidget()
        reminderTab = QWidget()

        tableWidget.addTab(generalTab, "General")
        tableWidget.addTab(previewTab, "Preview")
        tableWidget.addTab(reminderTab, "Reminder lines")

        # general tab
        layout = QVBoxLayout()

        group = QGroupBox("Preferences")
        sublayout = QGridLayout()

        label = QLabel("Slope unit :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.slopeUnit = QComboBox()
        self.slopeUnit.addItems(["%", "°"])
        self.slopeUnit.setCurrentText(self.pyLong.project.settings.slopeSymbol)
        sublayout.addWidget(self.slopeUnit, 0, 1)

        label = QLabel("Profile direction :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.direction = QComboBox()
        self.direction.addItems(["ascending", "descending"])
        self.direction.setCurrentText(self.pyLong.project.settings.profileDirection)
        sublayout.addWidget(self.direction, 1, 1)

        group.setLayout(sublayout)
        layout.addWidget(group)

        group = QGroupBox("Figure export")
        sublayout = QGridLayout()

        label = QLabel("Format :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.extension = QComboBox()
        self.extension.insertItems(0, list(extensions.keys()))
        self.extension.setCurrentText(self.pyLong.project.settings.exportFileFormat)
        sublayout.addWidget(self.extension, 0, 1)

        label = QLabel("Resolution :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.dpi = QSpinBox()
        self.dpi.setFixedWidth(75)
        self.dpi.setSuffix(" dpi")
        self.dpi.setSingleStep(25)
        self.dpi.setRange(25, 1000)
        self.dpi.setValue(self.pyLong.project.settings.figureDpi)
        sublayout.addWidget(self.dpi, 1, 1)

        group.setLayout(sublayout)
        layout.addWidget(group)

        layout.addWidget(QLabel())
        layout.addWidget(QLabel())

        generalTab.setLayout(layout)

        # preview tab
        layout = QVBoxLayout()

        group = QGroupBox("Style")
        sublayout = QGridLayout()

        label = QLabel("Line style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.lineStyle = QComboBox()
        self.lineStyle.insertItems(0, list(lineStyles.keys()))
        self.lineStyle.setCurrentText(self.pyLong.project.preview.lineProperties['style'])
        sublayout.addWidget(self.lineStyle, 0, 1)

        label = QLabel("Line color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.lineColor = ColorsComboBox(self.pyLong.appctxt)
        self.lineColor.setCurrentText(self.pyLong.project.preview.lineProperties['color'])
        sublayout.addWidget(self.lineColor, 1, 1)

        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 2, 0)

        self.thickness = QDoubleSpinBox()
        self.thickness.setFixedWidth(50)
        self.thickness.setLocale(QLocale('English'))
        self.thickness.setDecimals(1)
        self.thickness.setRange(0, 99.9)
        self.thickness.setSingleStep(0.1)
        self.thickness.setValue(self.pyLong.project.preview.lineProperties['thickness'])
        sublayout.addWidget(self.thickness, 2, 1)

        label = QLabel("Marker style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 3, 0)

        self.markerStyle = QComboBox()
        self.markerStyle.insertItems(0, list(markerStyles.keys()))
        self.markerStyle.setCurrentText(self.pyLong.project.preview.markerProperties['style'])
        sublayout.addWidget(self.markerStyle, 3, 1)

        label = QLabel("Marker color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 4, 0)

        self.markerColor = ColorsComboBox(self.pyLong.appctxt)
        self.markerColor.setCurrentText(self.pyLong.project.preview.markerProperties['color'])
        sublayout.addWidget(self.markerColor, 4, 1)

        label = QLabel("Marker size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 5, 0)

        self.markerSize = QDoubleSpinBox()
        self.markerSize.setFixedWidth(50)
        self.markerSize.setLocale(QLocale('English'))
        self.markerSize.setRange(0, 99.9)
        self.markerSize.setSingleStep(0.1)
        self.markerSize.setDecimals(1)
        self.markerSize.setValue(self.pyLong.project.preview.markerProperties['size'])
        sublayout.addWidget(self.markerSize, 5, 1)

        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 6, 0)

        self.opacity = QDoubleSpinBox()
        self.opacity.setFixedWidth(50)
        self.opacity.setLocale(QLocale('English'))
        self.opacity.setRange(0, 1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.pyLong.project.preview.opacity)
        sublayout.addWidget(self.opacity, 6, 1)

        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 7, 0)

        self.order = QSpinBox()
        self.order.setFixedWidth(50)
        self.order.setRange(0, 99)
        self.order.setValue(self.pyLong.project.preview.order)
        sublayout.addWidget(self.order, 7, 1)

        group.setLayout(sublayout)
        layout.addWidget(group)

        previewTab.setLayout(layout)

        # reminder lines tab
        layout = QVBoxLayout()

        group = QGroupBox("Style")
        sublayout = QGridLayout()

        label = QLabel("Line style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 0, 0)

        self.reminderLineStyle = QComboBox()
        self.reminderLineStyle.insertItems(0, list(lineStyles.keys()))
        self.reminderLineStyle.setCurrentText(self.pyLong.project.settings.reminderLineProperties['style'])
        sublayout.addWidget(self.reminderLineStyle, 0, 1)

        label = QLabel("Line color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 1, 0)

        self.reminderLineColor = ColorsComboBox(self.pyLong.appctxt)
        self.reminderLineColor.setCurrentText(self.pyLong.project.settings.reminderLineProperties['color'])
        sublayout.addWidget(self.reminderLineColor, 1, 1)

        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 2, 0)

        self.reminderLineThickness = QDoubleSpinBox()
        self.reminderLineThickness.setFixedWidth(50)
        self.reminderLineThickness.setLocale(QLocale('English'))
        self.reminderLineThickness.setDecimals(1)
        self.reminderLineThickness.setRange(0, 99.9)
        self.reminderLineThickness.setSingleStep(0.1)
        self.reminderLineThickness.setValue(self.pyLong.project.settings.reminderLineProperties['thickness'])
        sublayout.addWidget(self.reminderLineThickness, 2, 1)

        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 3, 0)

        self.reminderLineOpacity = QDoubleSpinBox()
        self.reminderLineOpacity.setFixedWidth(50)
        self.reminderLineOpacity.setLocale(QLocale('English'))
        self.reminderLineOpacity.setRange(0, 1)
        self.reminderLineOpacity.setDecimals(1)
        self.reminderLineOpacity.setSingleStep(0.1)
        self.reminderLineOpacity.setValue(self.pyLong.project.settings.reminderLineProperties['opacity'])
        sublayout.addWidget(self.reminderLineOpacity, 3, 1)

        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        sublayout.addWidget(label, 4, 0)

        self.reminderLineOrder = QSpinBox()
        self.reminderLineOrder.setFixedWidth(50)
        self.reminderLineOrder.setRange(0, 99)
        self.reminderLineOrder.setValue(self.pyLong.project.settings.reminderLineProperties['order'])
        sublayout.addWidget(self.reminderLineOrder, 4, 1)

        sublayout.addWidget(QLabel(), 5, 0)
        sublayout.addWidget(QLabel(), 6, 0)
        sublayout.addWidget(QLabel(), 7, 0)

        group.setLayout(sublayout)
        layout.addWidget(group)

        reminderTab.setLayout(layout)

        mainLayout.addWidget(tableWidget)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(False)
        buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)

    def validate(self):
        self.apply()
        self.accept()
        
    def apply(self):
        self.pyLong.project.settings.slopeSymbol = self.slopeUnit.currentText()
        self.pyLong.project.settings.profileDirection = self.direction.currentText()
        self.pyLong.project.settings.exportFileFormat = self.extension.currentText()
        self.pyLong.project.settings.figureDpi = self.dpi.value()
        
        self.pyLong.project.preview.lineProperties['style'] = self.lineStyle.currentText()
        self.pyLong.project.preview.lineProperties['color'] = self.lineColor.currentText()
        self.pyLong.project.preview.lineProperties['thickness'] = self.thickness.value()
        self.pyLong.project.preview.markerProperties['style'] = self.markerStyle.currentText()
        self.pyLong.project.preview.markerProperties['color'] = self.markerColor.currentText()
        self.pyLong.project.preview.markerProperties['size'] = self.markerSize.value()
        self.pyLong.project.preview.opacity = self.opacity.value()
        self.pyLong.project.preview.order = self.order.value()

        self.pyLong.project.settings.reminderLineProperties['style'] = self.reminderLineStyle.currentText()
        self.pyLong.project.settings.reminderLineProperties['color'] = self.reminderLineColor.currentText()
        self.pyLong.project.settings.reminderLineProperties['thickness'] = self.reminderLineThickness.value()
        self.pyLong.project.settings.reminderLineProperties['opacity'] = self.reminderLineOpacity.value()
        self.pyLong.project.settings.reminderLineProperties['order'] = self.reminderLineOrder.value()
        
        self.pyLong.canvas.updateFigure()
