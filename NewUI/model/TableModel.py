import pandas as pd

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from data.DataObject import DataObject


class TableModel(QAbstractTableModel):


    def __init__(self, data=None): #al momento variabili private
        # 2 variabili: l'oggetto data su cui effettuare le operazioni e una lista di oggetti data da tenere come cronologia
        #TODO dato che l'app non si apre senza aprire un file csv si dovrebbe passare una stringa e il tipo, ma al momento passo un dataframe per testare
        QAbstractTableModel.__init__(self)
        self._struttura=DataObject(data) #da rifare poi come scritto sopra
        self._data = self._struttura.df #come data prendo il dataframe pandas
        self._cronologia = []

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
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

    def loadDataFromFile(self, filename):
        # modifica della tabella da file caricato
        dft=pd.read_csv(filename) # TODO il metodo di lettura da file dovrebbe essere in dataobject
        self._struttura = DataObject(dft)
        self._data = self._struttura.df
        self.updatemodel()

    def backup(self):
        # aggiunge la struttura alla cronologia prima di una modifica
        pass
        # TODO self._cronologia.append(self._struttura.copy())

    def updatemodel(self):
        # c'è stata un operazione che ha modificato la struttura dati sottostante nella variabile struttura, aggiorno
        # il tablemodel per aggiornare la view e salvo la struttura precedente
        self.beginResetModel()
        self.endResetModel()

    def goback(self):
        # ripristino struttura e data dal passaggio precedente, con pop elimino il backup più recente
        self.beginResetModel()
        #TODO self._struttura=self._cronologia.pop(0)
        #TODO self._data=self._struttura.df
        self.endResetModel()

    def provastampa(self):
        print(self._data.head())

    def setType(self, type: str):
        self._struttura.type = type
