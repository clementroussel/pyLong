from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from interface.colorsComboBox import *


class DialogText(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        self.pyLong = parent
    
        i = self.pyLong.annotationsList.groups.currentIndex()
        j = self.pyLong.annotationsList.list.currentRow()
        self.txt = self.pyLong.project.groups[i].annotations[j]
        
        self.setWindowTitle("Text")
        self.setWindowIcon(QIcon(self.pyLong.appctxt.get_resource('icons/text.png')))
 
        mainLayout = QVBoxLayout()
        
        layout = QHBoxLayout()
        
        label = QLabel("Title :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label)
        
        self.title = QLineEdit()
        self.title.setText(self.txt.title)
        self.title.textChanged.connect(self.updateTitle)
        layout.addWidget(self.title)  
        
        mainLayout.addLayout(layout)
        
        group = QGroupBox("Text")
        layout = QGridLayout()
        
        label = QLabel("Label :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 0)
        
        self.label = QLineEdit()
        self.label.setMaxLength(50)
        self.label.setText(self.txt.label)
        self.label.textEdited.connect(self.update)
        layout.addWidget(self.label, 0, 1)
        
        label = QLabel("Size :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.size = QDoubleSpinBox()
        self.size.setMaximumWidth(50)
        self.size.setLocale(QLocale('English'))
        self.size.setRange(0, 99.9)
        self.size.setDecimals(1)
        self.size.setSingleStep(0.1)
        self.size.setValue(self.txt.labelProperties['size'])
        self.size.valueChanged.connect(self.update)
        layout.addWidget(self.size, 1, 1)
        
        label = QLabel("Color :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 2, 0)
        
        self.color = ColorsComboBox(self.pyLong.appctxt)
        self.color.setCurrentText(self.txt.labelProperties['color'])
        self.color.currentTextChanged.connect(self.update)
        layout.addWidget(self.color, 2, 1)
        
        label = QLabel("Style :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 3, 0)

        self.style = QComboBox()
        self.style.addItems(['normal', 'italic'])
        self.style.setCurrentText(self.txt.labelProperties['style'])
        self.style.currentTextChanged.connect(self.update)
        layout.addWidget(self.style, 3, 1)

        label = QLabel("Thickness :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 4, 0)
        
        self.thickness = QComboBox()
        self.thickness.addItems(['normal',
                                 'bold'])
        self.thickness.setCurrentText(self.txt.labelProperties['thickness'])
        self.thickness.currentTextChanged.connect(self.update)
        layout.addWidget(self.thickness, 4, 1)
        
        label = QLabel("Rotation :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 5, 0)
        
        self.rotation = QDoubleSpinBox()
        self.rotation.setMaximumWidth(65)
        self.rotation.setLocale(QLocale('English'))
        self.rotation.setSuffix(" °")
        self.rotation.setRange(-180,180)
        self.rotation.setSingleStep(0.1)
        self.rotation.setDecimals(1)
        self.rotation.setValue(self.txt.labelProperties['rotation'])
        self.rotation.valueChanged.connect(self.update)
        layout.addWidget(self.rotation, 5, 1)       
        
        group.setLayout(layout)
        mainLayout.addWidget(group)
        
        group = QGroupBox("Bottom left corner position")
        layout = QGridLayout()
        
        point = QPushButton()
        # self.pointer.setMaximumWidth(50)
        point.setIcon(QIcon(self.pyLong.appctxt.get_resource('icons/point.png')))
        point.setIconSize(QSize(12,12))
        point.setMaximumWidth(25)
        point.setAutoDefault(False)
        point.clicked.connect(self.point)
        layout.addWidget(point, 0, 0, 2, 1)
        
        label = QLabel("X coordinate :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 0, 1)
        
        self.x = QDoubleSpinBox()
        self.x.setMaximumWidth(90)
        self.x.setSuffix(" m")
        self.x.setLocale(QLocale('English'))
        self.x.setRange(-99999.999, 99999.999)
        self.x.setDecimals(3)
        self.x.setSingleStep(0.1)
        self.x.setValue(self.txt.position['x coordinate'])
        self.x.valueChanged.connect(self.update)
        layout.addWidget(self.x, 0, 2)

        label = QLabel("Z coordinate :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 1)
        
        self.z = QDoubleSpinBox()
        self.z.setMaximumWidth(90)
        self.z.setSuffix(" m")
        self.z.setLocale(QLocale('English'))
        self.z.setRange(-99999.999, 99999.999)
        self.z.setDecimals(3)
        self.z.setSingleStep(0.1)
        self.z.setValue(self.txt.position['z coordinate'])
        self.z.valueChanged.connect(self.update)
        layout.addWidget(self.z, 1, 2)
        
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
        self.opacity.setRange(0,1)
        self.opacity.setDecimals(1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(self.txt.opacity)
        self.opacity.valueChanged.connect(self.update)
        layout.addWidget(self.opacity, 0, 1)
        
        label = QLabel("Order :")
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(label, 1, 0)
        
        self.order = QSpinBox()
        self.order.setMaximumWidth(45)
        self.order.setLocale(QLocale('English'))
        self.order.setRange(1,99)
        self.order.setSingleStep(1)
        self.order.setValue(self.txt.order)
        self.order.valueChanged.connect(self.update)
        layout.addWidget(self.order, 1, 1)
        
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
        self.txt.title = self.title.text()
        self.pyLong.annotationsList.updateList()
        
    def update(self):
        try:
            self.pyLong.canvas.mpl_disconnect(self.cid)
            self.pyLong.canvas.setCursor(Qt.ArrowCursor)
        except:
            pass

        self.txt.label = self.label.text()
        self.txt.labelProperties['size'] = self.size.value()
        self.txt.labelProperties['color'] = self.color.currentText()
        self.txt.labelProperties['style'] = self.style.currentText()
        self.txt.labelProperties['thickness'] = self.thickness.currentText()
        self.txt.labelProperties['rotation'] = self.rotation.value()
        self.txt.position['x coordinate'] = self.x.value()
        self.txt.position['z coordinate'] = self.z.value()
        self.txt.opacity = self.opacity.value()
        self.txt.order = self.order.value()
        
        self.txt.update()
        
        self.pyLong.canvas.draw()
        
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
