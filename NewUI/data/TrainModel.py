from utility.funzioni import *
from utility.Enums import *


class TrainModel:

    def __init__(self, type: PFPGEnum, data:pd.DataFrame, enabledcolumns: pd.DataFrame, disabledcolumns: pd.DataFrame):
        self.df = data
        self.type = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

"""        self.scaler: ScalingEnum = ScalingEnum.NONE
        self.sampler: SamplingEnum = SamplingEnum.NONE
        self.classifier: ClassifierEnum.LOGISTIC"""

    # Getter functions

    def get_rows(self) -> int:
        return len(self.df)

    def get_positive_label(self) -> int:
        return len(self.df.loc[(self.df.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.df.query("label==0"))

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.df.columns.values))):
            self.disabledcolumns = self.df[columns]
            self.enabledcolumns.drop(columns=columns)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns)
        else:
            print("error: colonne non presenti")


