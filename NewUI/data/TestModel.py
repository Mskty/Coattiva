from utility.funzioni import *
from utility.Enums import *


class TestModel:
    """
    Classe che rappresenta i dati del testset che verranno utilizzati come out-of-sample per valutare le performance del classificatore
    addestrato. I dati presenti sono gestiti utilizzando Dataframes della libreria pandas. Vengono esposti metodi per
    modificare la struttura dei DataFrames attraverso la rimozione e aggiunta di colonne e metodi per
    aggiungere e rimuovere le predizioni effettuate sui dati ed esportare su file csv i risultati.
    PARAMETRI:
    self.type: Valore di tipo PFPGEnum rappresentante il tipo di dati contenuti in self.enabledcolumns e self.disabledcolumns
    self.enabledcolumns: oggetto di tipo pandas.Dataframe contenente le colonne/features dei dati che saranno utilizzate
                         dal classificatore addestrato per predire i dati contenuti nel testset
    self.enabledcolumns: oggetto di tipo pandas.Dataframe contenente le colonne/features dei dati che sono attualmente
                         disattivate e non verranno quindi utilizzate dal classificatore addestrato per predire i dati
                         ontenuti nel testset
    """

    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self, type: PFPGEnum, enabledcolumns: pd.DataFrame, disabledcolumns: pd.DataFrame):
        self.type: PFPGEnum = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

    """---------------------------------------------------Funzioni Getter-------------------------------------------"""

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    def get_positive_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 0)])

    """--------------------------------------------------Funzioni Setter per colonne--------------------------------"""

    def disablecolumns(self, columns: list):
        """
        @PRE: nessuna
        Sposta da self.enabledcolumns a self.disabledcolumns le colonne il cui nome è contenuto nel parametro columns.
        :param columns: lista di nomi di colonne da spostare
        :return: None
        """
        if set(columns).issubset(set(list(self.enabledcolumns.columns.values))):
            self.disabledcolumns[columns] = self.enabledcolumns[columns]
            self.enabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        """
        @PRE: nessuna
        Sposta da self.disabledcolumns a self.enabledcolumns le colonne il cui nome è contenuto nel parametro columns.
        :param columns: lista di nomi di colonne da spostare
        :return: None
        """
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    """-------------------------------------------------Funzioni Business-------------------------------------------"""

    def attach_predictions(self, pred: list):
        """
        @PRE: nessuna
        Aggiunge la lista di predizioni contenute nel parametro pred a self.enabledcolumns tramite la nuova colonna
        "predizione"
        :param pred: lista di booleani della stessa lunghezza del numero di righe di self.enabledcolumns
        :return: None
        """
        self.enabledcolumns.insert(0, "predizione", pred)

    def remove_predictions(self):
        """
        @PRE: è stata invocata la funzione self.attach_predictions
        Rimuove la colonna "predizione" seguendo la logica già esposta nella funzione attach_predictions
        :return:
        """
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        """
        @PRE: nessuna
        Esporta i dati del dataframe self.enabledcolumns su file csv nel percorso indicato
        :param export_file_path: percorso di salvataggio del file csv
        :return: None
        """
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)

