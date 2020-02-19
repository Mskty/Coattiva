from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractListModel, Qt

class ColumnsListModel(QtCore.QAbstractListModel):
    def __init__(self, columns: list):
        super(ColumnsListModel, self).__init__()
        self.columns = columns

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the data structure.
            status, text = self.columns[index.row()]
            # Return the text only
            return text

    def rowCount(self, index):
        return len(self.columns)