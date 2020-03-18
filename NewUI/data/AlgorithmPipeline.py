import pickle

from utility.Imports import *
from utility.Score import *
from utility.Enums import *
from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import plot_confusion_matrix


class AlgorithmPipeline:
    """
    Classe che rappresenta un classificatore addestrato applicabile su dati preprocessati. Contiene un oggetto classificatore
    addestrato che si occupa di produrre predizioni sui dati di input e può contenere un oggetto scaler, se utilizzato
    durante l'addestramento del classificatore, che si occupa di normalizzare i valori delle features/colonne numeriche
    dei dati per cui bisogna fornire una predizione.
    PARAMETRI:
    self.classifier: oggetto derivato dalla classe sklearn.base.BaseEstimator, un classificatore su cui è stato invocato
                     il metodo .fit() per addestrarlo e che può quindi produrre predizioni su nuovi dati con .pred()
    self.scaler: oggetto di tipo sklearn.preprocessing.StandardScaler oppure sklearn.preprocessing.MinMaxScaler su cui
                 è stato invocato il metodo .fit() per determinare i parametri di normalizzazione e può quindi normalizzare
                 nuovi dati con .transform(). Può essere None
    self.columnstoscal: lista di stringhe contenente il nome delle colonne/features che dovranno essere normalizzare dallo
                        scaler. Può essere None
    self.columnlist: lista di stringhe contenente il nome di tutte le colonne/features che sono state utilizzate per addestrare
                     il classificatore.
    self.type: valore di tipo PFPGEnum rappresentante il tipo di dati su cui è stato addestrato il classificatore

    """

    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self, classifier=None, scaler=None, columnstoscale: list = None, columnlist: list = None,
                 type: PFPGEnum = None):
        self.classifier = classifier
        self.scaler = scaler
        self.columnstoscale = columnstoscale
        self.columnlist = columnlist
        self.type: PFPGEnum = type

    def predict(self, dataset: pd.DataFrame):
        """
        @PRE: self.classifier not None
        Effettua scaling (se scaler è presente) e predice i risultati di ogni riga di dataset con classifier.predict
        :param dataset: pandas Dataframe con features compatibili con classifier e scaler
        :return: numpy array a 1 dimensione con le predizioni per ogni riga di dataset
        """
        dataset = dataset.copy()

        # Applicazione scaler su colonne non categoriche (columnstoscale) se presente
        if self.scaler is not None:
            dataset_to_scale = dataset[self.columnstoscale]
            dataset.drop(columns=self.columnstoscale, inplace=True)
            scaled_features_dataset = self.scaler.transform(dataset_to_scale.values)
            scaled_dataset = pd.DataFrame(scaled_features_dataset, index=dataset_to_scale.index,
                                          columns=dataset_to_scale.columns)
            dataset = pd.concat([scaled_dataset, dataset], axis=1, sort=False)

        # Separazione colonna label se presente
        if "label" in dataset.columns:
            X = dataset.drop(columns="label").to_numpy()
        else:
            X = dataset.to_numpy()

        # Ritorno predizioni
        return self.classifier.predict(X)

    def metrics(self, dataset: pd.DataFrame) -> Score:
        """
        @PRE: nessuna
        calcola e ritorna 5 metriche dal dataset su cui sono state effettuate le predizioni e in cui erano presenti
        i valori reali (nella colonna label). I valori delle metriche vengono salvati in un oggetto di tipo Score
        :param dataset: pandas Dataframe contenente le colonne label e predizione
        :return: oggetto Score contenente le 5 metriche
        """
        accuracy = accuracy_score(dataset["label"].values, dataset["predizione"].values)
        precision = precision_score(dataset["label"].values, dataset["predizione"].values)
        recall = recall_score(dataset["label"].values, dataset["predizione"].values)
        f1 = f1_score(dataset["label"].values, dataset["predizione"].values)
        roc_auc = roc_auc_score(dataset["label"].values, dataset["predizione"].values)
        return Score(accuracy, precision, recall, f1, roc_auc)

    def plot_roc_curve(self, dataset: pd.DataFrame):
        """
        @PRE: self.classifier not None
        Genera una figura matplotlib contenente il grafico roc-auc curve per i risultati delle predizioni
        ottenute sui dati contenuti nel parametro dataset.
        Per visualizzare il grafico una volta lanciata la funzione occorre invocare la funzione plt.show()
        :return: None
        """
        # fa comparire il grafico della roc_curve
        dataset = dataset.copy()

        # Applicazione scaler su colonne non categoriche (columnstoscale) se presente
        if self.scaler != None:
            dataset_to_scale = dataset[self.columnstoscale]
            dataset.drop(columns=self.columnstoscale, inplace=True)
            scaled_features_dataset = self.scaler.transform(dataset_to_scale.values)
            scaled_dataset = pd.DataFrame(scaled_features_dataset, index=dataset_to_scale.index,
                                          columns=dataset_to_scale.columns)
            dataset = pd.concat([scaled_dataset, dataset], axis=1, sort=False)

        if "predizione" in dataset.columns:
            dataset.drop(columns="predizione", inplace=True)
        # Separazione colonna label
        Y = dataset["label"].to_numpy()
        X = dataset.drop(columns="label").to_numpy()

        # Generazione del grafico
        skl.metrics.plot_roc_curve(self.classifier, X, Y)
        ax = plt.gca()
        ax.plot([0, 1], [0, 1], 'r--', label="Selezione Casuale (AUC = 0.50)")
        ax.plot([0, 0, 1], [0, 1, 1], 'g-.', label="Classificatore Perfetto (AUC = 1.00)")
        ax.legend(loc='lower right')

    def plot_precision_recall(self, dataset: pd.DataFrame):
        """
        @PRE: self.classifier not None
        Genera una figura matplotlib contenente il grafico precision-recall curve per i risultati delle predizioni
        ottenute sui dati contenuti nel parametro dataset.
        Per visualizzare il grafico una volta lanciata la funzione occorre invocare la funzione plt.show()
        :param dataset: pandas Dataframe con features compatibili con classifier e scaler
        :return: None
        """
        dataset = dataset.copy()

        # Applicazione scaler su colonne non categoriche (columnstoscale) se presente
        if self.scaler != None:
            dataset_to_scale = dataset[self.columnstoscale]
            dataset.drop(columns=self.columnstoscale, inplace=True)
            scaled_features_dataset = self.scaler.transform(dataset_to_scale.values)
            scaled_dataset = pd.DataFrame(scaled_features_dataset, index=dataset_to_scale.index,
                                          columns=dataset_to_scale.columns)
            dataset = pd.concat([scaled_dataset, dataset], axis=1, sort=False)

        if "predizione" in dataset.columns:
            dataset.drop(columns="predizione", inplace=True)
        # Separazione colonna label
        Y = dataset["label"].to_numpy()
        X = dataset.drop(columns="label").to_numpy()

        # Generazione del grafico

        skl.metrics.plot_precision_recall_curve(self.classifier, X, Y)
        ax = plt.gca()
        ax.plot([0, 1, 1], [1, 1, 0.5], 'g-.', label="Classificatore Perfetto (AP = 1.00)")
        ax.set(ylabel="Precisione",
               xlabel="Recall")
        ax.legend(loc='lower right')

    def plot_confusion_matrix(self, dataset: pd.DataFrame):
        """
        @PRE: self.classifier not None
        Genera una figura matplotlib contenente il grafico confusion matrix per i risultati delle predizioni
        ottenute sui dati contenuti nel parametro dataset.
        Per visualizzare il grafico una volta lanciata la funzione occorre invocare la funzione plt.show()
        :param dataset: pandas Dataframe con features compatibili con classifier e scaler
        :return: None
        """
        dataset = dataset.copy()

        # Applicazione scaler su colonne non categoriche (columnstoscale) se presente
        if self.scaler != None:
            dataset_to_scale = dataset[self.columnstoscale]
            dataset.drop(columns=self.columnstoscale, inplace=True)
            scaled_features_dataset = self.scaler.transform(dataset_to_scale.values)
            scaled_dataset = pd.DataFrame(scaled_features_dataset, index=dataset_to_scale.index,
                                          columns=dataset_to_scale.columns)
            dataset = pd.concat([scaled_dataset, dataset], axis=1, sort=False)

        if "predizione" in dataset.columns:
            dataset.drop(columns="predizione", inplace=True)
        # Separazione colonna label
        Y = dataset["label"].to_numpy()
        X = dataset.drop(columns="label").to_numpy()

        # Generazione del grafico
        class_labels = ["Positivo", "Negativo"]
        skl.metrics.plot_confusion_matrix(self.classifier, X, Y, cmap=plt.cm.Blues, values_format="",
                                          display_labels=class_labels)
        ax = plt.gca()
        ax.set(ylabel="Risultati reali",
               xlabel="Risultati predetti")

    def serialize(self, filename=None):
        """
        @PRE: self.classifier not None, self.columnlist not None, self.type not None
        Serializza il modello salvandolo alla destinazione specificata su filename, che deve essere di tipo .sav
        :param filename: percorso di salvataggio .sav del modello
        :return: None
        """
        modlist = [self.classifier, self.scaler, self.columnstoscale, self.columnlist, self.type]
        s = pickle.dump(modlist, open(filename, 'wb'))

    def deserialize(self, filename=None):
        """
        @PRE: nessuna
        Carica un modello già addestrato dal file .sav specificato dal parametro filename.
        L'oggetto AlgorithmPipeline deve giò essere stato creato prima di invocare questo metodo
        :param filename: file .sav da cui caricare il modello
        :return:
        """
        modlist_loaded = pickle.load(open(filename, 'rb'))
        try:
            # Se viene sollevata un eccezione all'interno di queste operazioni vuol dire che il file passato
            # Non fa riferimento ad un classificatore precedentemente addestrato da questo applicativo
            self.classifier = modlist_loaded[0]
            self.scaler = modlist_loaded[1]
            self.columnstoscale = modlist_loaded[2]
            self.columnlist = modlist_loaded[3]
            self.type = modlist_loaded[4]
        except Exception:
            raise ValueError("Errore: \n Il file caricato non contiene un classificatore addestrato in questo "
                             "applicativo")
