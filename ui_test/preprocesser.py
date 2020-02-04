from funzioni import *
from choose_model_enum import *


class Preprocessor:

    # TODO Deve caricare gli imputer usati nella pulizia del dataset di training originale
    def __init__(self):
        """
        Classe contenente tutti i metodi per preprocessare un dataframe in preparazione alle predizioni
        attravero uno specifico modello
        """

    def preprocess(self, dataset: pd.DataFrame) -> pd.DataFrame:
        # TODO preprocessing dei dati a seconda del modello scelto
        # TODO magari metodi diversi per la pulizia e la preparazione vera e propria con scaling e encoding
        return dataset

    def clean(self, data:pd.DataFrame, remove=False)-> pd.DataFrame:
        # TODO rimuove o sostituisce (remove=False) le righe contenenti valori mancanti usando l'imputer
        # TODO magari ritornare le righe eliminate in un dataset diverso
        return data.copy()
