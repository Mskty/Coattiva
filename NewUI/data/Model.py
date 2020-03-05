# LOGICA DI BUSINESS FUNZIONI INVOCATE DALLA VIEW
from sympy.strategies.core import switch

from utility.funzioni import *
from data.DataModel import *
from data.TrainModel import *
from data.TestModel import *
from data.NewDataModel import *
from data.AlgorithmPipeline import *


class Model:
    def __init__(self):

        # TODO GESTIONE STATI

        self.datafilename: str = ""
        self.use_datafilename: str = ""

        self.data: DataModel = None
        self.train: TrainModel = None
        self.test: TestModel = None
        self.usedata: NewDataModel = None

        self.columns: list = []
        self.traintestsplit: pd.DataFrame = None
        self.workingalgorithm: AlgorithmPipeline = None

    # business

    def export_data(self, filepath: str):
        self.data.export_to_csv(filepath)

    def export_trainset(self, filepath: str):
        self.train.export_to_csv(filepath)

    def export_testset(self, filepath: str):
        self.test.export_to_csv(filepath)

    def export_usedata(self, filepath: str):
        self.usedata.export_full_to_csv(filepath)

    def enablecolumn(self, column: str):
        # Abilita colonne in data, trainset e testset (se presenti)
        # Viene ignorata la usedata poichè il modello è gia addestrato nel momento in cui sarà presente
        # E non è possibile abiltiare o disabilitare colonne
        try:
            self.data.enablecolumns([column])
        except Exception:
            pass
        try:
            self.train.enablecolumns([column])
        except Exception:
            pass
        try:
            self.test.enablecolumns([column])
        except Exception:
            pass

    def disablecolumn(self, column: str):
        # Disabilita colonne in data, trainset e testset (se presenti)
        # Viene ignorata la usedata poichè il modello è gia addestrato nel momento in cui sarà presente
        # E non è possibile abiltiare o disabilitare colonne
        try:
            self.data.disablecolumns([column])
        except Exception:
            pass
        try:
            self.train.disablecolumns([column])
        except Exception:
            pass
        try:
            self.test.disablecolumns([column])
        except Exception:
            pass

    # Addestramento e utilizzo modello predittivo

    def train_algorithm(self):
        # Produce il modello addestrato a partire dal trainset selezionato
        self.workingalgorithm = self.train.trainmodel()

    def predict_train(self):
        # Aggiunge predizioni alla tabella del trainmodel
        pred = self.workingalgorithm.predict(self.train.enabledcolumns)
        self.train.attach_predictions(pred)

    def predict_test(self):
        # Aggiunge predizioni alla tabella del testmodel
        pred = self.workingalgorithm.predict(self.test.enabledcolumns)
        self.test.attach_predictions(pred)

    def predict_use_data(self):
        # Aggiunge predizioni alla tabella del usedatamodel
        pred = self.workingalgorithm.predict(self.usedata.enabledcolumns)
        self.usedata.attach_predictions(pred)

    def is_test_present(self) -> bool:
        # Ritorna true se nel modello è presente un test set
        if self.test is None:
            return False
        else:
            return True

    def serialize_algorithm(self, filename: str):
        # Serializza l'algoritmo sul file indicato
        if filename:
            self.workingalgorithm.serialize(filename)

    def algorithm_from_file(self, filename: str):
        # Crea un nuovo algoritmo dal file indicato
        if filename:
            self.workingalgorithm = AlgorithmPipeline()
            self.workingalgorithm.deserialize(filename)

    # Setter

    def set_data(self, type: PFPGEnum, filename: str):
        # Inzizializza o resetta i parametri del modello a partire da un nuovo file di dati storici
        self.data = DataModel(type, filename=filename)  # fa già pulizia e preparazione
        self.datafilename = filename
        # get columns
        self.columns = self.data.get_columnsnames()
        # get traintestsplit
        self.traintestsplit = self.data.train_test_splitter_possibilities()
        # Reset train test and use_data
        self.train = None
        self.test = None
        self.usedata = None
        self.workingalgorithm = None

    def set_use_data(self, typefile: NewFileEnum, filename: str):
        # Inizializza i dati su cui si dovrà utilizzare il modello a partire da un file
        columns = self.workingalgorithm.columnlist
        if "predizione" in columns:
            columns.remove("predizione")
        if "label" in columns:
            columns.remove("label")
        self.usedata = NewDataModel(self.workingalgorithm.type, typefile, columns,
                                    filename)  # fa  già pulizia e preparazione
        self.use_datafilename = filename

    def reset_settings(self):
        # Resetta train test, algoritmo, nuovo file di utilizzo e colonne selezionate
        # Mantenendo però il file di dati storici caricato da cui produrre trainset e testset

        # Attributi
        self.use_datafilename = ""
        self.usedata = None
        self.train = None
        self.test = None
        self.workingalgorithm = None

        # Data
        self.data.enableallcolumns()

    def generate_train_test(self, date: str):
        # Ho la data del ruolo da cui quelli precendeti e se stesso faranno parte del training set
        # Scorro finche non trovo la data desiderata aggiungendo le date a una lista,
        # una volta trovata la aggiungo e mi fermo
        dates = []
        for index, row in self.traintestsplit.iterrows():
            if row["ruolo"] == date:
                dates.append(row["ruolo"])
                break
            else:
                dates.append(row["ruolo"])
        self.train, self.test = self.data.train_test_splitter(dates)

    def set_sampling(self, sampling: SamplingEnum):
        self.train.sampler = sampling

    def set_scaling(self, scaling: ScalingEnum):
        self.train.scaler = scaling

    def set_algorithm(self, algorithm: ClassifierEnum):
        self.train.classifier = algorithm

    # Getter (ritorna in formato da visualizzare su view)

    def get_column_names(self):
        return self.columns

    def get_train_test_splits(self):
        # saranno visualizzati in formato fino a data: esempi:
        return list(self.traintestsplit["ruolo"].values), list(self.traintestsplit["nesempi"].values)

    def get_datafilename(self):
        return self.datafilename

    def get_use_datafiletype(self):
        if self.usedata.filetype == NewFileEnum.OLD:
            return "Dati Storici"
        elif self.usedata.filetype == NewFileEnum.NEW:
            return "Dati Recenti"

    def get_use_datafilename(self):
        return self.use_datafilename

    def get_traintype(self):
        if self.data.type == PFPGEnum.PF:
            return "Persone Fisiche"
        elif self.data.type == PFPGEnum.PG:
            return "Persone Giuridiche"

    def get_algorithmtype(self):
        if self.workingalgorithm.type == PFPGEnum.PF:
            return "Persone Fisiche"
        elif self.workingalgorithm.type == PFPGEnum.PG:
            return "Persone Giuridiche"

    def get_algorithm(self):
        if self.train.classifier == ClassifierEnum.LOGISTIC:
            return "Logistic Regression"
        elif self.train.classifier == ClassifierEnum.SVC:
            return "Support Vector Machine"
        elif self.train.classifier == ClassifierEnum.TREE:
            return "Decision Tree Classifier"
        elif self.train.classifier == ClassifierEnum.FOREST:
            return "Random Forest Classifier"
        elif self.train.classifier == ClassifierEnum.XGB:
            return "XGB Classifier"

    def get_data_info(self) -> list:
        return [self.data.get_rows(), self.data.get_positive_label(), self.data.get_negative_label()]

    def get_train_info(self) -> list:
        return [self.train.get_rows(), self.train.get_positive_label(), self.train.get_negative_label()]

    def get_test_info(self) -> list:
        return [self.test.get_rows(), self.test.get_positive_label(), self.test.get_negative_label()]

    def get_sampling_info(self) -> list:
        return [self.train.get_sampling_rows(), self.train.get_sampling_positive_label(),
                self.train.get_sampling_negative_label()]

    def get_disabledcolumns(self) -> list:
        # Ottiene la lista di colonne disattivate
        disabledcolumns = list(self.data.disabledcolumns.columns.values)
        disabledcolumns.remove("DataCaricoTitolo")
        return disabledcolumns

    def get_sampling(self):
        if self.train.sampler == SamplingEnum.NONE:
            return "Nessuno"
        elif self.train.sampler == SamplingEnum.UNDER:
            return "Downsampling"
        elif self.train.sampler == SamplingEnum.UNDER:
            return "SMOTE Oversampling"

    def get_scaling(self):
        if self.train.scaler == ScalingEnum.NONE:
            return "Nessuno"
        elif self.train.scaler == ScalingEnum.STANDARD:
            return "Standard"
        elif self.train.scaler == ScalingEnum.MINMAX:
            return "MinMax"

    def get_train_scores(self) -> list:
        scores = self.workingalgorithm.metrics(self.train.enabledcolumns)
        return [scores.accuracy, scores.precision, scores.recall, scores.f1]

    def get_test_scores(self) -> list:
        scores = self.workingalgorithm.metrics(self.test.enabledcolumns)
        return [scores.accuracy, scores.precision, scores.recall, scores.f1]

    """ -------------------------------------------------GRAFICI---------------------------------------------------- """

    def get_confusion_matrix_train(self):
        plt.close()
        self.workingalgorithm.plot_confusion_matrix(self.train.enabledcolumns)
        plt.title("Confusion Matrix per Training set")
        plt.show()

    def get_confusion_matrix_test(self):
        plt.close()
        self.workingalgorithm.plot_confusion_matrix(self.test.enabledcolumns)
        plt.title("Confusion Matrix per Test set")
        plt.show()

    def get_auc_curve_train(self):
        plt.close()
        self.workingalgorithm.plot_roc_curve(self.train.enabledcolumns)
        plt.title("Roc-Auc Curve per Training set")
        plt.show()

    def get_auc_curve_test(self):
        plt.close()
        self.workingalgorithm.plot_roc_curve(self.test.enabledcolumns)
        plt.title("Roc-Auc Curve per Test set")
        plt.show()

    def get_prc_curve_train(self):
        plt.close()
        self.workingalgorithm.plot_precision_recall(self.train.enabledcolumns)
        plt.title("Precision-Recall Curve per Training set")
        plt.show()

    def get_prc_curve_test(self):
        plt.close()
        self.workingalgorithm.plot_precision_recall(self.test.enabledcolumns)
        plt.title("Precision-Recall Curve per Test set")
        plt.show()

    """ ----------------------------------------------DEBUG FUNCTIONS----------------------------------------------- """

    def db_train_from_file(self, type: PFPGEnum = PFPGEnum.PF):
        filename = "C:/Users/squer/Desktop/Coattiva/Datasets/export_trainset_PF.csv"
        df = pd.read_csv(filename)
        self.train = TrainModel(type, df, pd.DataFrame())

    def db_test_from_file(self, type: PFPGEnum = PFPGEnum.PF):
        filename = "C:/Users/squer/Desktop/Coattiva/Datasets/export_testset_PF.csv"
        df = pd.read_csv(filename)
        self.test = TestModel(type, df, pd.DataFrame())

    def db_enablecolumn(self, column: str):
        try:
            print(column)
            self.train.enablecolumns([column])
        except Exception:
            print("no trainset")
        try:
            self.test.enablecolumns([column])
        except Exception:
            print("no testset")

    def db_disablecolumn(self, column: str):
        try:
            self.train.disablecolumns([column])
        except Exception:
            print("no trainset")
        try:
            self.test.disablecolumns([column])
        except Exception:
            print("no testset")

    def db_get_traintype(self):
        if self.train.type == PFPGEnum.PF:
            return "Persone Fisiche"
        elif self.train.type == PFPGEnum.PG:
            return "Persone Giuridiche"

    # Addestramento e utilizzo modello predittivo

    # Setter

    def db_set_data(self):
        self.db_train_from_file()
        self.db_test_from_file()
        # get columns
        self.columns = self.train.db_columnnames()
        # get traintestsplit
        # self.traintestsplit = self.data.train_test_splitter_possibilities()
        # Reset train test and use_data
        self.workingalgorithm = None

    def db_get_disabledcolumns(self) -> list:
        return self.train.disabledcolumns.columns.values
