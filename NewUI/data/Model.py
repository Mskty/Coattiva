from utility.funzioni import *
from data.DataModel import *
from data.TrainModel import *
from data.TestModel import *
from data.NewDataModel import *
from data.AlgorithmPipeline import *


class Model:
    """
    Classe che rappresenta la logica di business dell'applicativo. Coordina le operazioni tra i modelli rappresentanti
    i dati originali caricati dall'utente (DataModel), il trainingset (TrainModel), il testset (TestModel) e i nuovi
    dati su cui produrre predizioni (NewDataModel). Espone metodi permettere all'utente di caricare o salvare daati,
    per modificare le proprietò di tali modelli, generare trainset e testset (attraverso DataModel), addestrare un
    classificatore predittivo con un oggetto di tipo AlgorithmPipeline(attraverso TrainModel) e utilizzarlo per ottenere
    predizioni e grafici, nonchè esportare i risultati su file. Fornisce un unico punto di accesso per le classi contenute
    nel package view per comunicare ed effettuare operazioni sui dati sottostanti salvati nei modelli sopra elencati.
    PARAMETRI:
    self.datafilename: valore stringa contenente il nome del file csv utilizzato per originare un oggetto di tipo DataModel
    self.use_datafilename: valore stringa contenente il nome del file csv utilizzato per originare un oggetto di tipo NewDataModel
    self.data: oggetto di tipo DataModel, è None alla creazione dell'oggetto
    self.train: oggetto di tipo TrainModel generato a partire da self.data. è None alla creazione dell'oggetto
    self.test: oggetto di tipo TestModel generato a partire da self.data. è None alla creazione dell'oggetto
    self.usedata: oggetto di tipo NewDataModel, è None alla creazione dell'oggetto
    self.columns: lista di stringhe contenente i nomi delle colonne/features abilitabili o disabilitabili dall'utente
                  per i dati presenti in self.data, self.train e self.test, è vuota alla creazione dell'oggetto
    self.traintestsplit: Oggetto di tipo pandas Dataframe contenente le informazioni su come splittare i dati contenuti
                         in self.data per generare un trainset e testset. Viene generato a partire da self.data,
                         è None alla creazione dell'oggetto
    self.workingalgorithm: oggetto di tipo AlgorithmPipeline, viene generato da self.train, è None alla creazione dell'oggetto
    """

    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self):

        self.datafilename: str = ""
        self.use_datafilename: str = ""

        self.data: DataModel = None
        self.train: TrainModel = None
        self.test: TestModel = None
        self.usedata: NewDataModel = None

        self.columns: list = []
        self.traintestsplit: pd.DataFrame = None
        self.workingalgorithm: AlgorithmPipeline = None

    """---------------------------------------------------Funzioni Setter-------------------------------------------"""

    def set_data(self, type: PFPGEnum, filename: str):
        """
        @PRE: nessuna
        Inizializza o resetta i parametri dell'oggetto Model a partire da un nuovo file di dati storici di tipo type
        e formato csv.
        Il percorso del file è contenuto nel parametro filename.
        :param type: enum di tipo (PF o PG) dei dati contenuti nel file
        :param filename: percorso di caricamento del file csv
        :return: None
        """

        """
        Questa funzione deve essere la prima ad essere invocata per utilizzare l'applicativo in modalità ADDESTRAMENTO
        """

        # Inzizializza o resetta i parametri del modello a partire da un nuovo file di dati storici
        self.data = DataModel(type, filename=filename)  # fa già pulizia e preparazione
        self.datafilename = filename
        # Ottengo i nomi delle colonne
        self.columns = self.data.get_columnsnames()
        # Ottengo i possibili split train e test
        self.traintestsplit = self.data.train_test_splitter_possibilities()
        # Reset parametri train test usedata e workingalgorithm
        self.train = None
        self.test = None
        self.usedata = None
        self.workingalgorithm = None

    def set_use_data(self, typefile: NewFileEnum, filename: str):
        """
        @PRE: è stato invocato self.train_algorithm o self.algorithm_from_file
        Inizializza l'oggetto self.usedata di tipo NewDataModel che conterrà i dati inseriti dall'utente che dovranno
        essere predetti dal  modello contenuto in self.workingalgorithm. Tale oggetto viene inizializzato
        a partire da un file di dati storici o recenti e in formato csv.
        Il percorso del file è contenuto nel parametro filename.
        :param typefile: enum di tipo (OLD o NEW) dei dati contenuti nel file
        :param filename: percorso di caricamento del file csv
        :return: None
        """
        # Inizializza i dati su cui si dovrà utilizzare il modello a partire da un file
        # Ottengo le colonne che saranno utilizzate dal workingalgorithm
        columns = self.workingalgorithm.columnlist
        # DEBUG per colonne mantenute dalla costruzione a partire da TrainModel
        if "predizione" in columns:
            columns.remove("predizione")
        if "label" in columns:
            columns.remove("label")
        # Costruisco l'oggetto NewDataModel
        self.usedata = NewDataModel(self.workingalgorithm.type, typefile, columns,
                                    filename)  # fa  già pulizia e preparazione
        # Salvo nome del file
        self.use_datafilename = filename

    def reset_settings(self):
        """
        @PRE: è stato invocato self.set_data
        Resetta self.use_datafilename, self.usedata, self.train, self.test e self.workingalgorithm come al momento
        della chiamata di self.set_data.
        Mantiene però il file di dati storici caricato da cui produrre successivamente il trainset e testset
        :return: None
        """
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
        """
        @PRE: è stato invocato self.set_data
        Genero self.train e self.test utilizzando la seguente strategia:
        Ho la data del ruolo (parametro date) da cui quelli precedenti e sè stesso faranno parte del training set
        Scorro finche non trovo la data desiderata aggiungendo le date precedenti a una lista
        una volta trovata la aggiungo la data desiderata e mi fermo.
        Una volta costruita la lista invoco la funzione di self.data train_test_splitter passando la lista di date per
        ottenere il trainset e il testset
        :param date: data in formato stringa dell'ultimo ruolo che sarà contenuto nel training set
        :return: None
        """
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

    """---------------------------------------------------Funzioni Getter-------------------------------------------"""

    # I dati vengono ritornati in formato gestibile dalla view allo scopo di visualizzazione

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
        return [self.train.get_rows(), self.train.get_positive_label(),
                self.train.get_negative_label()]

    def get_disabledcolumns(self) -> list:
        # Ottiene e ritorna la lista di colonne disattivate
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

    """---------------------------------------------------Funzioni Business-----------------------------------------"""

    def export_data(self, filepath: str):
        self.data.export_to_csv(filepath)

    def export_trainset(self, filepath: str):
        self.train.export_to_csv(filepath)

    def export_testset(self, filepath: str):
        self.test.export_to_csv(filepath)

    def export_usedata(self, filepath: str):
        self.usedata.export_full_to_csv(filepath)

    def enablecolumn(self, column: str):
        """
        @PRE: è stata invocata la funzione self.set_data, non è stata invocata la funzione self.train_algorithm
        Abilita una colonna in self.data e self.train, self.testset (se presenti)
        Viene ignorata la usedata poichè il modello è gia addestrato nel momento in cui sarà presente e pertanto
        non è più utile e possibile abilitare o disabilitare colonne
        :param column: nome stringa della colonna da abilitare
        :return: None
        """
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
        """
        @PRE: è stata invocata la funzione self.set_data, non è stata invocata la funzione self.train_algorithm
        disabilita una colonna in self.data e self.train, self.testset (se presenti)
        Viene ignorata la usedata poichè il modello è gia addestrato nel momento in cui sarà presente e pertanto
        non è più utile e possibile abilitare o disabilitare colonne
        :param column: nome stringa della colonna da disabilitare
        :return: None
        """
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
        """
        @PRE è stata invocata la funzione self.generate_train_test
        Genera un oggetto di tipo AlgorithmPipeline dalla funzione di self.train trainmodel.
        L'oggetto contiene il modello di classificazione addestrato sul trainset
        secondo le specifiche definite dall'utente e viene salvato all'interno del parametro self.workingalgorithm
        :return: None
        """
        self.workingalgorithm = self.train.trainmodel()

    def predict_train(self):
        """
        @PRE è stata invocata la funzione self.train_algorithm
        Calcola e aggiunge le predizioni al dataframe del trainset contenuto in self.train nel parametro enabledcolums
        :return: None
        """
        # Calcolo predizioni su trainset
        pred = self.workingalgorithm.predict(self.train.enabledcolumns)
        # Aggiungo predizioni al trainset
        self.train.attach_predictions(pred)

    def predict_test(self):
        """
        @PRE è stata invocata la funzione self.train_algorithm
        Calcola e aggiunge le predizioni al dataframe del test contenuto in self.test nel parametro enabledcolums
        :return: None
        """
        # Calcolo predizioni su testset
        pred = self.workingalgorithm.predict(self.test.enabledcolumns)
        # Aggiungo predizioni al testset
        self.test.attach_predictions(pred)

    def predict_use_data(self):
        """
        @PRE è stata invocata la funzione self.set_use_data
        Calcola e aggiunge le predizioni al dataframe del test contenuto in self.usedata nel parametro enabledcolums
        :return:
        """
        # Calcolo predizioni sui nuovi dati inseriti dall'utente
        pred = self.workingalgorithm.predict(self.usedata.enabledcolumns)
        # Aggiungo predizioni ai dati
        self.usedata.attach_predictions(pred)

    def is_test_present(self) -> bool:
        # Ritorna true se nell'oggetto Model è stato generato un test set, falso altrimenti
        if self.test is None:
            return False
        else:
            return True

    def serialize_algorithm(self, filename: str):
        """
        @PRE: è stata invocata la funzione self.train_algorithm
        Serializza l'oggetto contenuto in self.workingalgorithm sul file .sav indicato dal parametro filename
        :param filename: stringa che indica la posizione di salvataggio del file .sav su cui serializzare self.workingalgorithm
        :return: None
        """
        if filename:
            self.workingalgorithm.serialize(filename)

    def algorithm_from_file(self, filename: str):
        """
        @PRE: nessuna
        Carica un oggetto di tipo AlgorithmPipeline contennte un algoritmo addestrato da file .sav
        indicato dal parametro filename
        :param filename: stringa che indica la posizione del file .sav contenente il un oggetto AlgorithmPipeline serializzato
        :return: None
        """

        """
        Questa funzione deve essere la prima ad essere invocata per utilizzare l'applicativo in modalità UTILIZZO
        """

        if filename:
            # Genero oggetto AlgorithmPipeline vuoto
            self.workingalgorithm = AlgorithmPipeline()
            # Utilizzo la funzione di deserializzazione per caricare l'algoritmo addestrato da file
            self.workingalgorithm.deserialize(filename)

    """ -------------------------------------------------GRAFICI---------------------------------------------------- """

    def get_confusion_matrix_train(self):
        """
        @PRE: è stata invocata la funzione self.predict_train
        Genera e visualizza a schermo un grafico della confusion matrix per il trainset (self.train.enabledcolumns)
        :return: None
        """
        plt.close()
        self.workingalgorithm.plot_confusion_matrix(self.train.enabledcolumns)
        # Aggiungo titolo
        plt.title("Confusion Matrix per Training set")
        plt.show()

    def get_confusion_matrix_test(self):
        """
        @PRE: è stata invocata la funzione self.predict_test
        Genera e visualizza a schermo un grafico della confusion matrix per il testset (self.test.enabledcolumns)
        :return: None
        """
        plt.close()
        # Aggiungo titolo
        self.workingalgorithm.plot_confusion_matrix(self.test.enabledcolumns)
        plt.title("Confusion Matrix per Test set")
        plt.show()

    def get_auc_curve_train(self):
        """
        @PRE: è stata invocata la funzione self.predict_train
        Genera e visualizza a schermo un grafico della roc-auc curve per il trainset (self.train.enabledcolumns)
        :return: None
        """
        plt.close()
        # Aggiungo titolo
        self.workingalgorithm.plot_roc_curve(self.train.enabledcolumns)
        plt.title("Roc-Auc Curve per Training set")
        plt.show()

    def get_auc_curve_test(self):
        """
        @PRE: è stata invocata la funzione self.predict_test
        Genera e visualizza a schermo un grafico della roc-auc curve per il testset (self.test.enabledcolumns)
        :return: None
        """
        plt.close()
        # Aggiungo titolo
        self.workingalgorithm.plot_roc_curve(self.test.enabledcolumns)
        plt.title("Roc-Auc Curve per Test set")
        plt.show()

    def get_prc_curve_train(self):
        """
        @PRE: è stata invocata la funzione self.predict_train
        Genera e visualizza a schermo un grafico della precision-recall curve per il trainset (self.train.enabledcolumns)
        :return: None
        :return:
        """
        plt.close()
        # Aggiungo titolo
        self.workingalgorithm.plot_precision_recall(self.train.enabledcolumns)
        plt.title("Precision-Recall Curve per Training set")
        plt.show()

    def get_prc_curve_test(self):
        """
        @PRE: è stata invocata la funzione self.predict_test
        Genera e visualizza a schermo un grafico della precision-recall curve per il testset (self.test.enabledcolumns)
        :return: None
        """
        plt.close()
        # Aggiungo titolo
        self.workingalgorithm.plot_precision_recall(self.test.enabledcolumns)
        plt.title("Precision-Recall Curve per Test set")
        plt.show()
