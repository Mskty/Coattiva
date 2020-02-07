import pandas as pd


class DataObject:
    # oggetto contenitore alla base del modello che esegue tutte le operazioni di machine learning e caricamento sui dati
    # si basa su un dataframe pandas

    def __init__(self, dataframe=pd.DataFrame(), type="PF"):  # tipi pubblici forse da cambiare
        self.df = dataframe
        self.type = type

    def copy(self):
        #TODO
        pass
