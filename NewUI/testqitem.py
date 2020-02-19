from PyQt5 import QtCore
from PyQt5.QtGui import QStandardItem


class CheckableItem(QStandardItem):
    def __init__(self, value: str):
        super(CheckableItem, self).__init__(value)
        self.setCheckable(True)

    #Override
    def setCheckState(self, acheckState: QtCore.Qt.CheckState) -> None:
        QStandardItem.setCheckState(self,acheckState)
        if acheckState == QtCore.Qt.Checked:
            print("ciao")
        elif acheckState ==QtCore.Qt.Unchecked:
            print("wohoo")
        elif acheckState ==QtCore.Qt.PartiallyChecked:
            print("hey")

    def checkState(self) -> QtCore.Qt.CheckState:
        if QStandardItem.checkState(self)==QtCore.Qt.Checked:
            print("ciao")
        return QStandardItem.checkState(self)

