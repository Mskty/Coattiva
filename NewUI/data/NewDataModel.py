from data.StoricCleaner import *
from data.Preprocesser import *
from utility.funzioni import *
from utility.Enums import *


class NewDataModel:

    def __init__(self, type: PFPGEnum, filetype:NewFileEnum, columns: list, filename: str ):
        try:
            self.original_df: pd.DataFrame = pd.read_csv(filename)
        except Exception:
            print("no file passed")
        self.type: PFPGEnum = type
        self.filetype = filetype
        self.columns = columns

        # Se dati storici allora eseguo anche la pulizia altrimenti solo preparazione
        if self.filetype == NewFileEnum.OLD:
            # Pulizia dei dati
            cleaner = StoricCleaner(self.type, self.original_df)
            self.cleaned_df = cleaner.clean()
            # Preprocessamento
            preprocesser = Preprocesser(self.type, self.cleaned_df)
            self.df = preprocesser.prepare()
        elif self.filetype == NewFileEnum.NEW:
            # Preprocessamento
            preprocesser = Preprocesser(self.type, self.df)
            self.df = preprocesser.prepare()

        # Mantengo solo le colonne da utilizzare
        self.enabledcolumns = self.df[columns]

    # Getter functions

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    def attach_predictions(self, pred: list):
        self.df.insert(0, "predizione", pred)
        self.enabledcolumns.insert(0, "predizione", pred)

    def remove_predictions(self):
        self.df.drop(columns="predizione", inplace=True)
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)

    def export_full_to_csv(self, export_file_path):
        self.df.to_csv(export_file_path, index=None, header=True)

    def export_just_predictions_to_csv(self, export_file_path):
        self.df["predizione"].to_csv(export_file_path, index=None, header=True)