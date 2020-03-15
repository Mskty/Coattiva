import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    """
    Classe modello che deriva QAbstractTableModel per gestire i dati all'interno delle QTableWiew presenti nella
    mainwindow
    """

    def __init__(self, data: pd.DataFrame):
        QAbstractTableModel.__init__(self)
        self.data = data

    def rowCount(self, parent=None):
        return self.data.shape[0]

    def columnCount(self, parnet=None):
        return self.data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        # Vertical header
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data.columns[col]
        # Horizontal header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return col
        return None

    def updatemodel(self):
        """
        c'è stata un operazione che ha modificato la struttura dati sottostante nella variabile struttura, aggiorno
        il tablemodel per aggiornare la view e salvo la struttura precedente
        :returns: None
        """
        self.beginResetModel()
        self.endResetModel()

