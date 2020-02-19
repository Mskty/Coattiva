from utility.funzioni import *
from utility.Enums import *


class TestModel:

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
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 0)])

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.enabledcolumns.columns.values))):
            self.disabledcolumns[columns] = self.enabledcolumns[columns]
            self.enabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def attach_predictions(self, pred: list):
        self.enabledcolumns["predizione"] = pred

    def remove_predictions(self):
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)

