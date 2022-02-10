from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QIcon

from pyLong.dictionaries import colors

class ColorsComboBox(QComboBox) :
    def __init__(self, appctxt) :
        super().__init__()
        
        self.addItems(colors.keys())
        for i in range(self.count()) :
            self.setItemIcon(i, QIcon(appctxt.get_resource("colors/{}.png".format(self.itemText(i)))))
