from utility.funzioni import *
from utility.Enums import *
from data.TrainModel import *
from data.TestModel import *
from data.StoricCleaner import *
from data.StoricPreprocesser import *


class DataModel:

    # La colonna DataCaricoTitolo e label è sempre abilitata

    def __init__(self, type: PFPGEnum, data: pd.DataFrame = None, filename: str = None):
        try:
            self.df: pd.DataFrame = pd.read_csv(filename)
        except Exception:
            print("no file passed")
        if data is not None:
            self.df: pd.DataFrame = data
        self.type: PFPGEnum = type

        # Pulizia dei dati
        cleaner = StoricCleaner(self.type, self.df)
        self.df = cleaner.clean()

        # Preparazione dei dati
        preprocesser = StoricPreprocesser(self.type, self.df)
        self.df = preprocesser.prepare()

        # Inizializzazione colonne abilitate e disabilitate
        self.enabledcolumns = self.df.copy()
        self.disabledcolumns = pd.DataFrame()

    # Getter functions

    def get_disabledcolumnsnames(self) -> list:
        return list(self.disabledcolumns.columns.values)

    def get_enabledcolumnsnames(self) -> list:
        return list(self.disabledcolumns.columns.values)

    def get_columnsnames(self) -> list:
        names = list(self.df.columns.values)
        # Rimuovo label e DataCaricoTitolo perchè non disattivabili (e sono due colonne sempre presenti)
        names.remove("label")
        names.remove("DataCaricoTitolo")
        return names

    def get_rows(self) -> int:
        return len(self.df)

    def get_positive_label(self) -> int:
        return len(self.df.loc[(self.df.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.df.query("label==0"))

    # Disabilita e abilita colonne

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.df.columns.values))):
            self.disabledcolumns[columns] = self.df[columns]
            self.enabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enableallcolumns(self):
        self.enabledcolumns = self.df
        self.disabledcolumns = pd.DataFrame()

    # Creazione oggetti TrainModel e TestModel

    def train_test_splitter_possibilities(self) -> pd.DataFrame:
        """
            Dato il dataframe dei dati storici preparati ritorna un nuovo dataframe dove ogni riga
            rappresenta la data di un ruolo presente nei dati storici. Ogni riga riporta, per quella data
            quanti crediti appartengono a quel ruolo e tutti i precedenti (nesempi), quanti di questi sono
            classificati come positivi (true), e quanti come negativi (false). L'idea è che ciascuna delle
            date dei ruoli può essere utilizzata per splittare i dati storici in training set e test set,
            vengono dunque riportate le possibili composizioni dei training set ad ogni data di ruolo scelta.
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
        trainenabled.drop(columns="DataCaricoTitolo", inplace=True)
        testenabled.drop(columns="DataCaricoTitolo", inplace=True)

        # Ritorno train e test set

        trainset = TrainModel(self.type, trainenabled, traindisabled)

        # Genero testset solo se non vuoto
        testset= None
        if testenabled.empty is not True:
            testset = TestModel(self.type, testenabled, testdisabled)

        return trainset, testset

    # Esportazione dati su csv
    def export_to_csv(self, export_file_path):
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)
