import pandas as pd


class DataObject:
    # oggetto contenitore alla base del modello che esegue tutte le operazioni di machine learning e caricamento sui dati
    # si basa su un dataframe pandas

    def __init__(self, dataframe=pd.DataFrame(), type="PF"):  # tipi pubblici forse da cambiare
        self.df = dataframe
        self.type = type
        self.filename= ""

    def setType(self,type="PF"):
        # cambia il tipo utilizzato per i titoli di credito
        self.type=type

    def loadDataFromFile(self, filename):
        #TODO AL MOMENTO INUTILIZZATO PER VELOCIZZARE TEST
        # carica da file e fa anche controlli su tipo (pf, pg) e formato dal file
        self.filename=filename
        self.df=pd.read_csv(filename)



    def copy(self):
        #TODO
        pass
