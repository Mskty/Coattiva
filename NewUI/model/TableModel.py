import pandas as pd

from PyQt5.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):

    def __init__(self, data: pd.DataFrame):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        # Vertical header
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        # Horizontal header
        if orientation ==Qt.Vertical and role == Qt.DisplayRole:
            return col
        return None

    def updatemodel(self):
        # c'è stata un operazione che ha modificato la struttura dati sottostante nella variabile struttura, aggiorno
        # il tablemodel per aggiornare la view e salvo la struttura precedente
        self.beginResetModel()
        self.endResetModel()

