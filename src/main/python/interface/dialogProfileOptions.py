from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib import lines

from interface.colorsComboBox import *

from pyLong.dictionaries import *


class DialogProfileOptions(QDialog):
    def __init__(self, parent):
        super().__init__()
    
        self.pyLong = parent
        
        i = self.pyLong.layoutsList.currentIndex()
        self.secondaryAxis = self.pyLong.project.layouts[i].secondaryAxis
        
        i = self.pyLong.profilesList.list.currentRow()
        self.zprofile, self.sprofile = self.pyLong.project.profiles[i]
        
        self.setWindowTitle("Graphic properties <{}>".format(self.zprofile.title))
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/style.png')))
        
        self.slopeSymbol = self.pyLong.project.settings.slopeSymbol
        
        self.title = QLineEdit()
        self.title.setText(self.zprofile.title)
        self.title.textChanged.connect(self.updateProfileTitle)
            
        tableWidget = QTabWidget()
        zprofileTab = QWidget()
        sprofileTab = QWidget()
        
        tableWidget.addTab(zprofileTab, "profile")
        tableWidget.addTab(sprofileTab, "slopes")
        
        # profile tab
        layout = QGridLayout()

        self.drawProfile = QCheckBox("Draw profile")
        self.drawProfile.setChecked(self.zprofile.visible)
        self.drawProfile.stateChanged.connect(self.updateProfileVisible)
        layout.addWidget(self.drawProfile, 0, 0, 1, 2)
        
        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.profileLabel = QLineEdit()
        self.profileLabel.setText(self.zprofile.label)
        self.profileLabel.textChanged.connect(self.updateProfileLabel)
        layout.addWidget(self.profileLabel, 1, 1)
        
        label = QLabel("Line style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.profileLineStyle = QComboBox()
        self.profileLineStyle.insertItems(0, list(lineStyles.keys()))
        self.profileLineStyle.setCurrentText(self.zprofile.lineProperties['style'])
        self.profileLineStyle.currentTextChanged.connect(self.updateProfileLineStyle)
        layout.addWidget(self.profileLineStyle, 2, 1)
        
        label = QLabel("Line color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)              
        layout.addWidget(label, 3, 0)
        
        self.profileLineColor = ColorsComboBox(self.pyLong.appctxt)
        self.profileLineColor.setCurrentText(self.zprofile.lineProperties['color'])
        self.profileLineColor.currentTextChanged.connect(self.updateProfileLineColor)
        layout.addWidget(self.profileLineColor, 3, 1)
        
        label = QLabel("Line thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 4, 0)
        
        self.profileLineThickness = QDoubleSpinBox()
        self.profileLineThickness.setMaximumWidth(50)
        self.profileLineThickness.setLocale(QLocale('English'))
        self.profileLineThickness.setRange(0, 99.9)
        self.profileLineThickness.setDecimals(1)
        self.profileLineThickness.setSingleStep(0.1)
        self.profileLineThickness.setValue(self.zprofile.lineProperties['thickness'])
        self.profileLineThickness.valueChanged.connect(self.updateProfileLineThickness)
        layout.addWidget(self.profileLineThickness, 4, 1)

        label = QLabel("Marker style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  
        layout.addWidget(label, 5, 0)
        
        self.profileMarkerStyle = QComboBox()
        self.profileMarkerStyle.insertItems(0, list(markerStyles.keys()))
        self.profileMarkerStyle.setCurrentText(self.zprofile.markerProperties['style'])
        self.profileMarkerStyle.currentTextChanged.connect(self.updateProfileMarkerStyle)
        layout.addWidget(self.profileMarkerStyle, 5, 1)
        
        label = QLabel("Marker color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 6, 0)
        
        self.profileMarkerColor = ColorsComboBox(self.pyLong.appctxt)
        self.profileMarkerColor.setCurrentText(self.zprofile.markerProperties['color'])
        self.profileMarkerColor.currentTextChanged.connect(self.updateProfileMarkerColor)
        layout.addWidget(self.profileMarkerColor, 6, 1)
        
        label = QLabel("Marker size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 7, 0)
        
        self.profileMarkerSize = QDoubleSpinBox()
        self.profileMarkerSize.setMaximumWidth(50)
        self.profileMarkerSize.setLocale(QLocale('English'))
        self.profileMarkerSize.setRange(0, 99.9)
        self.profileMarkerSize.setSingleStep(0.1)
        self.profileMarkerSize.setDecimals(1)
        self.profileMarkerSize.setValue(self.zprofile.markerProperties['size'])
        self.profileMarkerSize.valueChanged.connect(self.updateProfileMarkerSize)
        layout.addWidget(self.profileMarkerSize, 7, 1)
        
        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 8, 0)
        
        self.profileOpacity = QDoubleSpinBox()
        self.profileOpacity.setFixedWidth(45)
        self.profileOpacity.setLocale(QLocale('English'))
        self.profileOpacity.setRange(0, 1)
        self.profileOpacity.setDecimals(1)
        self.profileOpacity.setSingleStep(0.1)
        self.profileOpacity.setValue(self.zprofile.opacity)
        self.profileOpacity.valueChanged.connect(self.updateProfileOpacity)
        layout.addWidget(self.profileOpacity, 8, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 9, 0)
        
        self.profileOrder = QSpinBox()
        self.profileOrder.setFixedWidth(45)
        self.profileOrder.setRange(0, 99)
        self.profileOrder.setValue(self.zprofile.order)
        self.profileOrder.valueChanged.connect(self.updateProfileOrder)
        layout.addWidget(self.profileOrder, 9, 1)

        layout.addWidget(QLabel(), 10, 0)

        zprofileTab.setLayout(layout)
        
        # slopes tab
        layout = QGridLayout()

        self.drawSlopeMarkers = QCheckBox("Draw markers")
        self.drawSlopeMarkers.setChecked(self.sprofile.markersVisible)
        self.drawSlopeMarkers.stateChanged.connect(self.updateSlopeMarkersVisible)
        layout.addWidget(self.drawSlopeMarkers, 0, 0)

        refresh = QPushButton()
        refresh.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/refresh.png')))
        refresh.setMaximumWidth(25)
        refresh.setAutoDefault(False)
        refresh.setDefault(False)
        refresh.clicked.connect(self.refresh)
        layout.addWidget(refresh, 0, 1)

        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter) 
        layout.addWidget(label, 1, 0)

        self.slopeLabel = QLineEdit()
        self.slopeLabel.setText(self.sprofile.label)
        self.slopeLabel.textChanged.connect(self.updateSlopeLabel)
        layout.addWidget(self.slopeLabel, 1, 1)
        
        label = QLabel("Marker style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.slopeMarkerStyle = QComboBox()
        self.slopeMarkerStyle.insertItems(0, list(markerStyles.keys()))
        self.slopeMarkerStyle.setCurrentText(self.sprofile.markerProperties['style'])
        self.slopeMarkerStyle.currentTextChanged.connect(self.updateSlopeMarkerStyle)
        layout.addWidget(self.slopeMarkerStyle, 2, 1)
        
        label = QLabel("Marker color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)
        
        self.slopeMarkerColor = ColorsComboBox(self.pyLong.appctxt)
        self.slopeMarkerColor.setCurrentText(self.sprofile.markerProperties['color'])
        self.slopeMarkerColor.currentTextChanged.connect(self.updateSlopeMarkerColor)
        layout.addWidget(self.slopeMarkerColor, 3, 1)
        
        label = QLabel("Marker size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.slopeMarkerSize = QDoubleSpinBox()
        self.slopeMarkerSize.setMaximumWidth(50)
        self.slopeMarkerSize.setRange(0, 99.9)
        self.slopeMarkerSize.setSingleStep(0.1)
        self.slopeMarkerSize.setDecimals(1)
        self.slopeMarkerSize.setLocale(QLocale('English'))
        self.slopeMarkerSize.setValue(self.sprofile.markerProperties['size'])
        self.slopeMarkerSize.valueChanged.connect(self.updateSlopeMarkerSize)
        layout.addWidget(self.slopeMarkerSize, 4, 1)

        self.drawSlopeAnnotations = QCheckBox("Draw values")
        self.drawSlopeAnnotations.setChecked(self.sprofile.annotationsVisible)
        self.drawSlopeAnnotations.stateChanged.connect(self.updateSlopeAnnotationsVisible)
        layout.addWidget(self.drawSlopeAnnotations, 5, 0, 1, 2)
        
        label = QLabel("Text size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 6, 0)
        
        self.slopeSize = QDoubleSpinBox()
        self.slopeSize.setMaximumWidth(50)
        self.slopeSize.setLocale(QLocale('English'))
        self.slopeSize.setRange(0, 99.9)
        self.slopeSize.setDecimals(1)
        self.slopeSize.setSingleStep(0.1)
        self.slopeSize.setValue(self.sprofile.annotationProperties["size"])
        self.slopeSize.valueChanged.connect(self.updateSlopeSize)
        layout.addWidget(self.slopeSize, 6, 1)
        
        label = QLabel("Text color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 7, 0)
        
        self.slopeColor = ColorsComboBox(self.pyLong.appctxt)
        self.slopeColor.setCurrentText(self.sprofile.annotationProperties["color"])
        self.slopeColor.currentTextChanged.connect(self.updateSlopeColor)
        layout.addWidget(self.slopeColor, 7, 1)
        
        label = QLabel("Offset :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 8, 0)
        
        self.slopeShift = QDoubleSpinBox()
        self.slopeShift.setLocale(QLocale('English'))
        self.slopeShift.setMaximumWidth(65)
        if self.secondaryAxis:
            if self.slopeSymbol == "%":
                self.slopeShift.setRange(-99.9, 99.9)
                self.slopeShift.setValue(self.sprofile.annotationProperties['s shift %'])
            else:
                self.slopeShift.setRange(-45.0, 45.0)
                self.slopeShift.setValue(self.sprofile.annotationProperties['s shift °'])
            self.slopeShift.setSuffix(" {}".format(self.slopeSymbol))
        else:
            self.slopeShift.setSuffix(" m")
            self.slopeShift.setRange(-99.9, 99.9)
            self.slopeShift.setValue(self.sprofile.annotationProperties['z shift'])
        self.slopeShift.setSingleStep(0.1)
        self.slopeShift.setDecimals(1)
        self.slopeShift.valueChanged.connect(self.updateSlopeShift)
        layout.addWidget(self.slopeShift, 8, 1)
            
        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 9, 0)
        
        self.slopeOpacity = QDoubleSpinBox()
        self.slopeOpacity.setFixedWidth(45)
        self.slopeOpacity.setLocale(QLocale('English'))
        self.slopeOpacity.setRange(0,1)
        self.slopeOpacity.setDecimals(1)
        self.slopeOpacity.setSingleStep(0.1)
        self.slopeOpacity.setValue(self.sprofile.opacity)
        self.slopeOpacity.valueChanged.connect(self.updateSlopeOpacity)
        layout.addWidget(self.slopeOpacity, 9, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 10, 0)
        
        self.slopeOrder = QSpinBox()
        self.slopeOrder.setFixedWidth(45)
        self.slopeOrder.setRange(0,99)
        self.slopeOrder.setValue(self.sprofile.order)
        self.slopeOrder.valueChanged.connect(self.updateSlopeOrder)
        layout.addWidget(self.slopeOrder, 10, 1)
        
        sprofileTab.setLayout(layout)
        
        # buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Ok)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        # buttonBox.button(QDialogButtonBox.Apply).setText("Actualiser")
        # buttonBox.button(QDialogButtonBox.Apply).setIcon(QIcon(self.pyLong.appctxt.get_resource('icones/rafraichir.png')))
        # buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        # buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.appliquer)
        # buttonBox.button(QDialogButtonBox.Apply).setAutoDefault(True)
        # buttonBox.button(QDialogButtonBox.Apply).setDefault(True)
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.title, 0, 1)
        layout.addWidget(tableWidget, 1, 0, 1, 2)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        
        self.setLayout(layout)
        
    def refresh(self):
        self.sprofile.update()

        i = self.pyLong.layoutsList.currentIndex()
        secondaryAxis = self.pyLong.project.layouts[i].secondaryAxis
        slopeSymbol = self.pyLong.project.settings.slopeSymbol

        if secondaryAxis:
            if slopeSymbol == "%":
                self.pyLong.canvas.ax_p.add_line(self.sprofile.linePercents)
            else:
                self.pyLong.canvas.ax_p.add_line(self.sprofile.lineDegrees)
        else:
            self.pyLong.canvas.ax_z.add_line(self.sprofile.line)

        self.pyLong.canvas.updateLegends()


    def updateProfileTitle(self, value):
        self.zprofile.title = value
        self.setWindowTitle("Graphic properties <{}>".format(value))
        self.pyLong.profilesList.update()

    def updateProfileLabel(self, value):
        self.zprofile.label = value
        self.zprofile.line.set_label(value)

        if self.zprofile.visible:
            self.pyLong.canvas.updateLegends()

    def updateProfileVisible(self, value):
        self.zprofile.visible = value
        self.zprofile.update()
        self.pyLong.canvas.updateLegends()

    def updateProfileLineStyle(self, value):
        self.zprofile.lineProperties['style'] = value
        self.zprofile.line.set_linestyle(lineStyles[value])
        self.pyLong.canvas.updateLegends()

    def updateProfileLineColor(self, value):
        self.zprofile.lineProperties['color'] = value
        self.zprofile.line.set_color(colors[value])
        self.pyLong.canvas.updateLegends()

    def updateProfileLineThickness(self, value):
        self.zprofile.lineProperties['thickness'] = value
        self.zprofile.line.set_linewidth(value)
        self.pyLong.canvas.updateLegends()

    def updateProfileMarkerStyle(self, value):
        self.zprofile.markerProperties['style'] = value
        self.zprofile.line.set_marker(markerStyles[value])
        self.pyLong.canvas.updateLegends()

    def updateProfileMarkerColor(self, value):
        self.zprofile.markerProperties['color'] = value
        self.zprofile.line.set_markeredgecolor(colors[value])
        self.zprofile.line.set_markerfacecolor(colors[value])
        self.pyLong.canvas.updateLegends()

    def updateProfileMarkerSize(self, value):
        self.zprofile.markerProperties['size'] = value
        self.zprofile.line.set_markersize(value)
        self.pyLong.canvas.updateLegends()

    def updateProfileOpacity(self, value):
        self.zprofile.opacit = value
        self.zprofile.line.set_alpha(value)
        self.pyLong.canvas.updateLegends()

    def updateProfileOrder(self, value):
        self.zprofile.order = value
        self.zprofile.line.set_zorder(value)
        self.pyLong.canvas.updateLegends()

    def updateSlopeMarkersVisible(self, value):
        self.sprofile.markersVisible = value
        self.sprofile.update()
        self.pyLong.canvas.updateLegends()

    def updateSlopeLabel(self, value):
        self.sprofile.label = value
        self.sprofile.trickLine.set_label(value)

        if self.sprofile.markersVisible:
            self.pyLong.canvas.updateLegends()

    def updateSlopeMarkerStyle(self, value):
        self.sprofile.markerProperties['style'] = value
        self.sprofile.line.set_marker(markerStyles[value])
        self.sprofile.linePercents.set_marker(markerStyles[value])
        self.sprofile.lineDegrees.set_marker(markerStyles[value])
        self.sprofile.trickLine.set_marker(markerStyles[value])
        self.pyLong.canvas.updateLegends()

    def updateSlopeMarkerColor(self, value):
        self.sprofile.markerProperties['color'] = value
        self.sprofile.line.set_markeredgecolor(colors[value])
        self.sprofile.linePercents.set_markeredgecolor(colors[value])
        self.sprofile.lineDegrees.set_markeredgecolor(colors[value])
        self.sprofile.trickLine.set_markeredgecolor(colors[value])
        self.sprofile.line.set_markerfacecolor(colors[value])
        self.sprofile.linePercents.set_markerfacecolor(colors[value])
        self.sprofile.lineDegrees.set_markerfacecolor(colors[value])
        self.sprofile.trickLine.set_markerfacecolor(colors[value])
        self.pyLong.canvas.updateLegends()

    def updateSlopeMarkerSize(self, value):
        self.sprofile.markerProperties['size'] = value
        self.sprofile.line.set_markersize(value)
        self.sprofile.linePercents.set_markersize(value)
        self.sprofile.lineDegrees.set_markersize(value)
        self.sprofile.trickLine.set_markersize(value)
        self.pyLong.canvas.updateLegends()

    def updateSlopeOpacity(self, value):
        self.sprofile.opacity = value
        self.sprofile.line.set_alpha(value)
        self.sprofile.linePercents.set_alpha(value)
        self.sprofile.lineDegrees.set_alpha(value)
        self.sprofile.trickLine.set_alpha(value)
        self.pyLong.canvas.updateLegends()

    def updateSlopeOrder(self, value):
        self.sprofile.order = value
        self.sprofile.line.set_zorder(value)
        self.sprofile.linePercents.set_zorder(value)
        self.sprofile.lineDegrees.set_zorder(value)
        self.sprofile.trickLine.set_zorder(value)
        self.pyLong.canvas.updateLegends()

    def updateSlopeAnnotationsVisible(self, value):
        self.sprofile.annotationsVisible = value
        self.sprofile.update()
        self.pyLong.canvas.updateFigure()

    def updateSlopeSize(self, value):
        self.sprofile.annotationProperties['size'] = value
        self.sprofile.update()
        self.pyLong.canvas.updateFigure()

    def updateSlopeColor(self, value):
        self.sprofile.annotationProperties['color'] = value
        self.sprofile.update()
        self.pyLong.canvas.updateFigure()

    def updateSlopeShift(self, value):
        if self.secondaryAxis:
            if self.slopeSymbol == "%":
                self.sprofile.annotationProperties['s shift %'] = value
            else:
                self.sprofile.annotationProperties['s shift °'] = value
        else:
            self.sprofile.annotationProperties['z shift'] = value

        self.sprofile.update()
        self.pyLong.canvas.updateFigure()
