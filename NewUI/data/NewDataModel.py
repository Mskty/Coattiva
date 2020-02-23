from utility.funzioni import *
from utility.Enums import *


class NewDataModel:

    def __init__(self, type: PFPGEnum, filetype:NewFileEnum, columns: list, filename: str ):
        try:
            self.df: pd.DataFrame = pd.read_csv(filename)
        except Exception:
            print("no file passed")
        self.type: PFPGEnum = type
        self.filetype = filetype
        self.columns = columns

        # TODO CLEAN AND PREPROCESS ADEQUATE TO FILETYPE

        # Mantengo solo le colonne da utilizzare
        self.enabledcolumns = self.df[columns]

    # Getter functions

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    def attach_predictions(self, pred: list):
        self.df["predizione"] = pred
        self.enabledcolumns["predizione"] = pred

    def remove_predictions(self):
        self.df.drop(columns="predizione", inplace=True)
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)

    def export_full_to_csv(self, export_file_path):
        self.df.to_csv(export_file_path, index=None, header=True)