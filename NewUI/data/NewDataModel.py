from data.StoricCleaner import *
from data.RecentPreprocesser import *
from utility.funzioni import *
from utility.Enums import *


class NewDataModel:

    def __init__(self, type: PFPGEnum, filetype:NewFileEnum, columns: list, filename: str):
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
            # Usa RecentPreprocesser non storic in quanto non deve mantenere label e DataCaricoTitolo come in DataModel
            preprocesser = RecentPreprocesser(self.type, self.cleaned_df)
            self.df = preprocesser.prepare()
        elif self.filetype == NewFileEnum.NEW:
            # Preprocessamento
            preprocesser = RecentPreprocesser(self.type, self.original_df)
            self.df = preprocesser.prepare()

        # Mantengo solo le colonne da utilizzare
        self.enabledcolumns = self.df[columns]

    # Getter functions

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    def attach_predictions(self, pred: list):
        if self.filetype == NewFileEnum.NEW:
            self.original_df.insert(0, "predizione", pred)
        elif self.filetype == NewFileEnum.OLD:
            self.cleaned_df.insert(0, "predizione", pred)
        self.enabledcolumns.insert(0, "predizione", pred)


    def remove_predictions(self):
        if self.filetype == NewFileEnum.NEW:
            self.original_df.drop(columns="predizione", inplace=True)
        elif self.filetype == NewFileEnum.OLD:
            self.cleaned_df.drop(columns="predizione", inplace=True)
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)

    def export_full_to_csv(self, export_file_path):
        if self.filetype == NewFileEnum.NEW:
            self.original_df.to_csv(export_file_path, index=None, header=True)
        elif self.filetype == NewFileEnum.OLD:
            self.cleaned_df.to_csv(export_file_path, index=None, header=True)

    def export_just_predictions_to_csv(self, export_file_path):
        self.df["predizione"].to_csv(export_file_path, index=None, header=True)