from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from pyLong.dictionaries import *
from pyLong.rectangle import *

from interface.colorsComboBox import *


class DialogRectangle(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        self.pyLong = parent

        i = self.pyLong.annotationsList.groups.currentIndex()
        j = self.pyLong.annotationsList.list.currentRow()
        self.rect = self.pyLong.project.groups[i].annotations[j]

        if not self.rect.edited:
            Rectangle.counter -= 1
            self.rect.edited = True
        
        self.setWindowTitle("Rectangle")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/rectangle.png')))
        
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.title = QLineEdit()
        self.title.setText(self.rect.title)
        self.title.textChanged.connect(self.updateTitle)
        layout.addWidget(self.title)  
    
        mainLayout.addLayout(layout)
        
        group = QGroupBox("Label")
        layout = QVBoxLayout()
        
        self.label = QLineEdit()
        self.label.setText(self.rect.label)
        self.label.textEdited.connect(self.updateLabel)
        layout.addWidget(self.label)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Bottom left corner position")
        layout = QGridLayout()
        
        point = QPushButton()
        point.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        point.setIconSize(QSize(12,12))
        point.setMaximumWidth(25)
        point.setAutoDefault(False)
        point.clicked.connect(self.point)
        layout.addWidget(point, 0, 0, 2, 1)
        
        label = QLabel("X :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.x = QDoubleSpinBox()
        self.x.setMaximumWidth(90)
        self.x.setSuffix(" m")
        self.x.setLocale(QLocale('English'))
        self.x.setRange(-99999.999, 99999.999)
        self.x.setDecimals(3)
        self.x.setSingleStep(0.1)
        self.x.setValue(self.rect.position['x coordinate'])
        self.x.valueChanged.connect(self.update)
        layout.addWidget(self.x, 0, 2)
        
        label = QLabel("Z :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 1)
        
        self.z = QDoubleSpinBox()
        self.z.setMaximumWidth(90)
        self.z.setSuffix(" m")
        self.z.setLocale(QLocale('English'))
        self.z.setRange(-99999.999, 99999.999)
        self.z.setDecimals(3)
        self.z.setSingleStep(0.1)
        self.z.setValue(self.rect.position['z coordinate'])
        self.z.valueChanged.connect(self.update)
        layout.addWidget(self.z, 1, 2)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Dimensions")
        layout = QGridLayout()
        
        label = QLabel("Width :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.width = QDoubleSpinBox()
        self.width.setMaximumWidth(90)
        self.width.setSuffix(" m")
        self.width.setLocale(QLocale('English'))
        self.width.setRange(0, 99999.999)
        self.width.setDecimals(3)
        self.width.setSingleStep(0.1)
        self.width.setValue(self.rect.dimensions['width'])
        self.width.valueChanged.connect(self.update)
        layout.addWidget(self.width, 0, 1)
        
        label = QLabel("Height :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.height = QDoubleSpinBox()
        self.height.setMaximumWidth(90)
        self.height.setSuffix(" m")
        self.height.setLocale(QLocale('English'))
        self.height.setRange(0, 99999.999)
        self.height.setDecimals(3)
        self.height.setSingleStep(0.1)
        self.height.setValue(self.rect.dimensions['height'])
        self.height.valueChanged.connect(self.update)
        layout.addWidget(self.height, 1, 1)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Outline")
        layout = QGridLayout()
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.lineStyle = QComboBox()
        self.lineStyle.insertItems(0, list(lineStyles.keys()))
        self.lineStyle.setCurrentText(self.rect.outline['line style'])
        self.lineStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineStyle, 0, 1)
        
        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.thickness = QDoubleSpinBox()
        self.thickness.setMaximumWidth(50)
        self.thickness.setLocale(QLocale('English'))
        self.thickness.setRange(0, 99.9)
        self.thickness.setDecimals(1)
        self.thickness.setSingleStep(0.1)
        self.thickness.setValue(self.rect.outline['thickness'])
        self.thickness.valueChanged.connect(self.update)
        layout.addWidget(self.thickness, 1, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.lineColor = ColorsComboBox(self.pyLong.appctxt)
        self.lineColor.setCurrentText(self.rect.outline['color'])
        self.lineColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.lineColor, 2, 1)        
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Filling")
        layout = QGridLayout()

        label = QLabel("Coilor :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)        
        layout.addWidget(label, 0, 0)

        self.fillColor = ColorsComboBox(self.pyLong.appctxt)
        self.fillColor.setCurrentText(self.rect.filling['color'])
        self.fillColor.currentTextChanged.connect(self.update)
        layout.addWidget(self.fillColor, 0, 1) 
        
        label = QLabel("hatch style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.hatchStyle = QComboBox()
        self.hatchStyle.addItem('/')
        self.hatchStyle.addItem('\\')
        self.hatchStyle.addItem('|')
        self.hatchStyle.addItem('-')
        self.hatchStyle.addItem('+')
        self.hatchStyle.addItem('x')
        self.hatchStyle.addItem('o')
        self.hatchStyle.addItem('O')
        self.hatchStyle.addItem('.')
        self.hatchStyle.addItem('*')
        self.hatchStyle.addItem('')
        self.hatchStyle.setCurrentText(self.rect.filling['hatch style'])
        self.hatchStyle.currentTextChanged.connect(self.update)
        layout.addWidget(self.hatchStyle, 1, 1)

        label = QLabel("Density :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.density = QSpinBox()
        self.density.setMaximumWidth(45)
        self.density.setRange(1, 99)
        self.density.setValue(self.rect.filling['density'])
        self.density.valueChanged.connect(self.update)
        layout.addWidget(self.density, 2, 1)               
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Opacity and order")
        layout = QGridLayout()
        
        label = QLabel("Opacity :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.opacity = QDoubleSpinBox()
        self.opacity.setMaximumWidth(45)
        self.opacity.setLocale(QLocale('English'))
        self.opacity.setRange(0, 1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.rect.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 0, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 2)
        
        self.order = QSpinBox()
        self.order.setMaximumWidth(45)
        self.order.setLocale(QLocale('English'))
        self.order.setRange(1, 99)
        self.order.setSingleStep(1)
        self.order.setValue(self.rect.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 0, 3)
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.validate)
        buttonBox.button(QDialogButtonBox.Ok).setAutoDefault(True)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)
        
    def validate(self):
        self.pyLong.checkNavigationTools()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.update()
        self.accept()

    def updateTitle(self):
        self.rect.title = self.title.text()
        self.pyLong.annotationsList.updateList()

    def updateLabel(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.rect.label = self.label.text()

        self.rect.update()

        self.pyLong.canvas.updateLegends()
        
    def update(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
        self.rect.position['x coordinate'] = self.x.value()
        self.rect.position['z coordinate'] = self.z.value()
        
        self.rect.dimensions['width'] = self.width.value()
        self.rect.dimensions['height'] = self.height.value()
        
        self.rect.outline['line style'] = self.lineStyle.currentText()
        self.rect.outline['thickness'] = self.thickness.value()
        self.rect.outline['color'] = self.lineColor.currentText()
        
        self.rect.filling['hatch style'] = self.hatchStyle.currentText()
        self.rect.filling['color'] = self.fillColor.currentText()
        self.rect.filling['density'] = self.density.value()
        
        self.rect.opacity = self.opacity.value()
        self.rect.order = self.order.value()
        
        self.rect.update()

        self.pyLong.canvas.updateFigure()
        
    def point(self):
        self.pyLong.checkNavigationTools()
        self.cid = self.pyLong.canvas.mpl_connect('button_press_event', self.onclick)
        self.pyLong.canvas.setCursor(Qt.CrossCursor)
        
    def onclick(self, event):
        try:
            self.x.setValue(event.xdata)
            self.z.setValue(event.ydata)
        except:
            pass
        
        self.pyLong.canvas.mpl_disconnect(self.cid)
        self.update()
        
    def closeEvent(self, event):
        self.pyLong.checkNavigationTools()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        
    def reject(self):
        self.pyLong.checkNavigationTools()
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass
        self.accept()
