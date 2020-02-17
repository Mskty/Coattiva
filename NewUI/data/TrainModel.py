from utility.funzioni import *
from utility.Enums import *


class TrainModel:
    """
    Contiene il dataframe di addestramento,
    espone metodo per ritornare AlgorithmPipeline: un modello addestrato solamente sulle colonne enabledcolumns
    """

    def __init__(self, type: PFPGEnum, enabledcolumns: pd.DataFrame, disabledcolumns: pd.DataFrame):
        self.type = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

    # Getter functions

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    def get_positive_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.enabledcolumns.query("label==0"))

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.enabledcolumns.columns.values))):
            self.disabledcolumns = self.enabledcolumns[columns]
            self.enabledcolumns.drop(columns=columns)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns)
        else:
            print("error: colonne non presenti")




"""        self.scaler: ScalingEnum = ScalingEnum.NONE
        self.sampler: SamplingEnum = SamplingEnum.NONE
        self.classifier: ClassifierEnum.LOGISTIC"""