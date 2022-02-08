from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt


class CheckableComboBox(QComboBox):
    """
    --> définition d'un objet ComboBox avec éléments cochables <--
    """
    def __init__(self) :
        super().__init__()
        self._changed = False

        self.view().pressed.connect(self.handleItemPressed)

    def setItemChecked(self, index, checked=True):
        """
        --> méthode qui permet de rendre l'élément cochable <--
        """
        item = self.model().item(index, self.modelColumn()) # QStandardItem object

        if checked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)

    def handleItemPressed(self, index):
        """
        --> méthode qui gère le comportement du widget lors d'un clic sur un élément
        """
        item = self.model().itemFromIndex(index)

        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self._changed = True

    def hidePopup(self):
        """
        --> méthode qui gère la fermeture du widget <--
        """
        if not self._changed :
            super().hidePopup()
        self._changed = False

    def itemChecked(self, index):
        """
        --> méthode qui permet de connaître l'état coché ou non d'un élément <--
        """
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked