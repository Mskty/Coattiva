from data.StoricCleaner import *
from data.RecentPreprocesser import *
from data.TracciatoCheck import *
from utility.Imports import *
from utility.Enums import *


class NewDataModel:
    """
    Classe che rappresenta i dati caricati dall'utente (storici o recenti) su cui è possibile ottenere predizioni da un
    classsificatore addestrato sul traininngset. I dati sono gestiti utilizzando Dataframes della libreria pandas.
    Vengono esposti metodi aggiungere e rimuovere le predizioni effettuate sui dati ed esportare su file csv i risultati.
    Durante l'inizializzazione degli oggetti i dati vengono caricati da un file .csv e sottoposti a operazioni di
    pulizia e preprocessamento utilizzando oggetti di tipo StoricCleaner e StoricPreprocesser se si trattano di dati
    storici, mentre vengono effettuate solo operazioni di preprocesamento se si tratta di dati Recenti, attraverso un
    oggetto di tipo RecentPreprocesser.
    PARAMETRI:
    self.original_df: oggetto di tipo pandas.Dataframe contenente i dati originali caricati da file .csv
    self.type: Valore di tipo PFPGEnum rappresentante il tipo di dati contenuti in self.original_df
    self.filetype: Valore di tipo NewFileEnum rappresentante il tipo di file csv caricato
    self.columns: lista di stringhe rappresentanti i nomi delle colonne/features che verranno mantenute dopo
                  le operazioni di pulizia e preprocessamento per essere utilizzabile da un modello addestrato solamente
                  su tali features.
    self.cleaned_df: oggetto di tipo pandas.Dataframe conentene i dati ottenuti dopo la pulizia di quelli contenuti in
                     self.original_df, parametro presente solo se i dati caricati fanno riferimento a dati storici
    self.df: oggetto di tipo pandas.Dataframe contenente i dati ottenuti dopo il preprocessamento di quelli contenuti in
             self.original_df se si tratta di dati recenti o self.cleaned_df se si tratta di dati storici
    self.enabledcolumns: oggetto di tipo pandas.Dataframe contenente i dati presenti in self.df ma mantenendo solo
                         alcune colonne/features. Tali colonne saranno quelle su cui cui è stato addestrato il classificatore
                         e sono quelle contenute nella lista columns
    """

    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self, type: PFPGEnum, filetype: NewFileEnum, columns: list, filename: str):
        self.original_df: pd.DataFrame = pd.read_csv(filename, low_memory=False)
        self.type: PFPGEnum = type
        self.filetype: NewFileEnum = filetype
        self.columns: list = columns
        # Controllo che aderisca al tracciato
        try:
            checker = TracciatoCheck(type, self.filetype, self.original_df)
            # Lancia errore ValueError se non aderisce
            checker.checkcolumns()
        except ValueError as e:
            # Gestione eccezione nella view
            raise e

        # Se dati storici allora eseguo anche la pulizia altrimenti solo preparazione
        if self.filetype == NewFileEnum.OLD:
            # Pulizia dei dati
            try:
                cleaner = StoricCleaner(self.type, self.original_df)
                self.cleaned_df = cleaner.clean()
            except Exception:
                raise ValueError("C'è stato un errore nella pulizia dei dati storici, controlla che i valori nel file"
                                 "corrispondano alle indicazioni del tracciato")
            # Preprocessamento
            # Usa RecentPreprocesser non storic in quanto non deve mantenere label e DataCaricoTitolo come in DataModel
            try:
                preprocesser = RecentPreprocesser(self.type, self.cleaned_df)
                self.df = preprocesser.prepare()
            except Exception:
                raise ValueError(
                    "C'è stato un errore nella preparazione dei dati storici, controlla che i valori nel file"
                    "corrispondano alle indicazioni del tracciato")
        elif self.filetype == NewFileEnum.NEW:
            # Preprocessamento
            try:
                preprocesser = RecentPreprocesser(self.type, self.original_df)
                self.df = preprocesser.prepare()
            except Exception:
                raise ValueError(
                    "C'è stato un errore nella preparazione dei dati, controlla che i valori nel file"
                    "corrispondano alle indicazioni del tracciato")

        # Mantengo solo le colonne da utilizzare
        self.enabledcolumns = self.df[columns].copy()

    """---------------------------------------------------Funzioni Getter-------------------------------------------"""

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    """-------------------------------------------------Funzioni Business-------------------------------------------"""

    def attach_predictions(self, pred: list):
        """
        @PRE: nessuna
        Aggiunge la lista di predizioni contenute nel parametro pred a self.enabledcolumns tramite la nuova colonna
        "predizione", Le aggiunge nel medesimo modo anche a a self.original_df se l'oggetto NewDataModel contiene
        dati recenti, mentre le aggiunge a self.cleaned_df se invece si riferisce a dati storici elaborati
        :param pred: lista di booleani della stessa lunghezza del numero di righe di self.enabledcolumns
        :return: None
        """
        if self.filetype == NewFileEnum.NEW:
            self.original_df.insert(0, "predizione", pred)
        elif self.filetype == NewFileEnum.OLD:
            self.cleaned_df.insert(0, "predizione", pred)
        self.enabledcolumns.insert(0, "predizione", pred)

    def remove_predictions(self):
        """
        @PRE: è stata invocata la funzione attach_predictions
        Rimuove la colonna "predizione" seguendo la logica già esposta nella funzione attach_predictions
        :return:
        """
        if self.filetype == NewFileEnum.NEW:
            self.original_df.drop(columns="predizione", inplace=True)
        elif self.filetype == NewFileEnum.OLD:
            self.cleaned_df.drop(columns="predizione", inplace=True)
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        """
        @PRE: nessuna
        Esporta i dati del dataframe self.enabledcolumns su file csv nel percorso indicato
        :param export_file_path: percorso di salvataggio del file csv
        :return: None
        """
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)

    def export_full_to_csv(self, export_file_path):
        """
        @PRE: nessuna
        Esporta i dati del dataframe self.original_df o self.cleaned_df ( a seconda di self.filetype)
        su file csv nel percorso indicato
        :param export_file_path: percorso di salvataggio del file csv
        :return: None
        """
        if self.filetype == NewFileEnum.NEW:
            self.original_df.to_csv(export_file_path, index=None, header=True)
        elif self.filetype == NewFileEnum.OLD:
            self.cleaned_df.to_csv(export_file_path, index=None, header=True)

    def export_just_predictions_to_csv(self, export_file_path):
        """
        @PRE: è stata invocata la funzione self.attach_predictions
        Esporta la sola colonna predizione di self.enabledcolumns su file csv nel percorso indicato
        :param export_file_path: percorso di salvataggio del file csv
        :return: None
        """
        self.enabledcolumns["predizione"].to_csv(export_file_path, index=None, header=True)
