from utility.funzioni import *
from utility.Enums import *
from data.TrainModel import *
from data.TestModel import *
from data.StoricCleaner import *
from data.StoricPreprocesser import *


class DataModel:

    def __init__(self, type: PFPGEnum, data: pd.DataFrame = None, filename: str = None):
        try:
            self.original_df: pd.DataFrame = pd.read_csv(filename, low_memory=False)
        except Exception:
            print("no file passed")
        if data is not None:
            self.original_df: pd.DataFrame = data
        self.type: PFPGEnum = type

        # Pulizia dei dati
        cleaner = StoricCleaner(self.type, self.original_df)
        self.cleaned_df = cleaner.clean()

        # Preparazione dei dati
        preprocesser = StoricPreprocesser(self.type, self.cleaned_df)
        self.df = preprocesser.prepare()

        # Inizializzazione colonne abilitate e disabilitate
        self.enabledcolumns = self.df.copy()
        self.enabledcolumns.drop(columns="DataCaricoTitolo", inplace=True)
        self.disabledcolumns = pd.DataFrame()
        self.disabledcolumns["DataCaricoTitolo"] = self.df["DataCaricoTitolo"].copy()

    """---------------------------------------------------Funzioni Getter-------------------------------------------"""

    def get_disabledcolumnsnames(self) -> list:
        return list(self.disabledcolumns.columns.values)

    def get_enabledcolumnsnames(self) -> list:
        return list(self.enabledcolumns.columns.values)

    def get_columnsnames(self) -> list:
        """
        @PRE: nessuna
        Ritorna la lista dei nomi delle colonne che sarà possibile disabilitare attraverso la funzione disablecolumns
        :return: names, lista dei nomi delle colonne che sarà possibile disabilitare
        """
        names = list(self.df.columns.values)
        # Rimuovo label e DataCaricoTitolo perchè non disattivabili (e sono due colonne sempre presenti
        # nell'elaborazione)
        names.remove("label")
        names.remove("DataCaricoTitolo")
        # Rimuovo ValoreTitolo in quanto è considerato il campo più importante e non può essere rimosso
        names.remove("ValoreTitolo")
        return names

    def get_rows(self) -> int:
        return len(self.df)

    def get_positive_label(self) -> int:
        return len(self.df.loc[(self.df.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.df.query("label==0"))

    """--------------------------------------------------Funzioni Setter per colonne--------------------------------"""

    def disablecolumns(self, columns: list):
        """
        @PRE nessuna
        Sposta da self.enabledcolumns a self.disabledcolumns le colonne il cui nome è contenuto nel parametro columns.
        :param columns: lista di nomi di colonne da spostare
        :return: None
        """
        if set(columns).issubset(set(list(self.df.columns.values))):
            self.disabledcolumns[columns] = self.enabledcolumns[columns]
            self.enabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        """
        @PRE nessuna
        Sposta da self.disabledcolumns a self.enabledcolumns le colonne il cui nome è contenuto nel parametro columns.
        :param columns: lista di nomi di colonne da spostare
        :return: None
        """
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enableallcolumns(self):
        """
        @PRE nessuna
        Resetta la situazione delle colonne all'inizializzazione dell'oggetto.
        Spsota tutte le colonne presenti in self.disabledcolumns in self.enabledcolumns eccetto DataCaricoTitolo
        :return: None
        """
        self.enabledcolumns = self.df.copy()
        self.enabledcolumns.drop(columns="DataCaricoTitolo", inplace=True)
        self.disabledcolumns = pd.DataFrame()
        self.disabledcolumns["DataCaricoTitolo"] = self.df["DataCaricoTitolo"].copy()

    """-------------------------------------------------Funzioni Business-------------------------------------------"""

    def train_test_splitter_possibilities(self) -> pd.DataFrame:
        """
        @PRE: nessuna
        Dato il dataframe dei dati storici preparati ritorna un nuovo dataframe dove ogni riga
        rappresenta la data di un ruolo presente nei dati storici. Ogni riga riporta, per quella data
        quanti crediti appartengono a quel ruolo e tutti i precedenti (nesempi), quanti di questi sono
        classificati come positivi (true), e quanti come negativi (false). L'idea è che ciascuna delle
        date dei ruoli può essere utilizzata per splittare i dati storici in training set e test set,
        vengono dunque riportate le possibili composizioni dei training set ad ogni data di ruolo scelta.
        :return: results, un dataframe contenenti numero titoli e label (positive e negative) per ogni data di ruolo
        """
        # Ricavo i ruoli
        ruoli = self.df.DataCaricoTitolo.unique()

        # Ordino in modo crescente le date dei ruoli
        dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in ruoli]
        dates.sort()
        ruoli = list([datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates])

        # creo un dataframe con le possibili date e numero di esempi contenuto in ogni possibile training set
        results = pd.DataFrame()
        results["ruolo"] = ruoli
        results["nesempi"] = 0
        results["true"] = 0
        results["false"] = 0
        count = 1
        for r in ruoli:
            results.loc[(results.ruolo == r), "nesempi"] = len(self.df.loc[
                                                                   self.df.DataCaricoTitolo.isin(ruoli[:count])])
            results.loc[(results.ruolo == r), "true"] = len(
                self.df.loc[(self.df.DataCaricoTitolo.isin(ruoli[:count])) & (self.df.label == 1)])
            results.loc[(results.ruolo == r), "false"] = len(
                self.df.loc[(self.df.DataCaricoTitolo.isin(ruoli[:count])) & (self.df.label == 0)])
            count = count + 1

        return results

    def train_test_splitter(self, dates):
        """
        @PRE: è stata invocata la funzione self.train_test_splitter_possibilities
        Suddivide il dataframe dei dati storici aggregati e preparati in training set e test set, dove il training set
        sarà composto di tutti i titoli con campo DataCaricoTitolo uguale ad uno dei valori presenti nella lista dates
        :param dates: lista di date
        :return: oggetti TrainModel e TestModel
        """

        # Divisione test out of sample e training in sample
        trainindex = list(self.df.loc[(self.df.DataCaricoTitolo.isin(dates))].index.values)
        testindex = list(self.df.loc[(~self.df.DataCaricoTitolo.isin(dates))].index.values)

        trainenabled = self.enabledcolumns[self.enabledcolumns.index.isin(trainindex)].copy()
        traindisabled = self.disabledcolumns[self.disabledcolumns.index.isin(trainindex)].copy()
        testenabled = self.enabledcolumns[self.enabledcolumns.index.isin(testindex)].copy()
        testdisabled = self.disabledcolumns[self.disabledcolumns.index.isin(testindex)].copy()

        # Drop della colonna DataCaricoTitolo una volta separati i due set
        traindisabled.drop(columns="DataCaricoTitolo", inplace=True)
        testdisabled.drop(columns="DataCaricoTitolo", inplace=True)

        # Ritorno train e test set

        trainset = TrainModel(self.type, trainenabled, traindisabled)

        # Genero testset solo se non vuoto
        testset= None
        if testenabled.empty is not True:
            testset = TestModel(self.type, testenabled, testdisabled)

        return trainset, testset

    def export_to_csv(self, export_file_path):
        """
        @PRE: nessuna
        Esporta i dati del dataframe elaborato self.df su file csv nel percorso indicato
        :param export_file_path: percorso di salvataggio del file csv
        :return: None
        """
        self.df.to_csv(export_file_path, index=None, header=True)
