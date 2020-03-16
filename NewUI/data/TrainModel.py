from imblearn.under_sampling import RandomUnderSampler

from utility.funzioni import *
from data.AlgorithmPipeline import *
from utility.Enums import *


class TrainModel:
    """
    Contiene il dataframe di addestramento,
    espone metodo per ritornare AlgorithmPipeline: un modello addestrato solamente sulle colonne enabledcolumns
    """

    def __init__(self, type: PFPGEnum, enabledcolumns: pd.DataFrame, disabledcolumns: pd.DataFrame):

        # label sempre enabled
        self.type :PFPGEnum = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

        # Per addestramento
        self.scaler: ScalingEnum = ScalingEnum.NONE
        self.sampler: SamplingEnum = SamplingEnum.NONE
        self.classifier: ClassifierEnum= ClassifierEnum.LOGISTIC

        # colonne categoriche apparte label
        self._categoricalpf = ["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente"]
        self._categoricalpg = ["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente"]

    """---------------------------------------------------Funzioni Setter-------------------------------------------"""

    def set_scaler(self, scaler: ScalingEnum):
        self.scaler = scaler

    def set_sampler(self, sampler: SamplingEnum):
        self.sampler = sampler

    def set_classifier(self, classifier: ClassifierEnum):
        self.classifier = classifier

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
        print(list(self.enabledcolumns.columns.values))
        print(columns)
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

    """--------------------------------------------------Funzioni Business------------------------------------------"""

    def trainmodel(self) -> AlgorithmPipeline:
        """
        @PRE: nessuna
        Genera e ritorna un oggetto di tipo AlgorithmPipeline con le seguenti specifiche:
        Viene istanziato un classificatore a seconda del tipo specificato in self.classifier
        Il classificatore viene addestrato sui dati contenuti in self.enabledcolumns con sampling specificato in
            self.sampler. Se self.sampler non è SamplingEnum.NONE allora self.enabledcolumns viene aggiornato con i dati
            su cui è stato effettuato sampling
        Viene istanziato uno scaler a seconda del tipo specificato su self.scaler. Tale scaler, se self.scaler non è
            ScalerEnum.NONE viene addestrato ed applicato su self.enabledcolumns per le colonne non contenute in
            self.categorical_pf o self.categorical_pg a seconda di self.type
        Il classificatore viene addestrato sui dati post sampling e post scaling in modo da produrre un modello
            addestrato.
        AlgorithmScaler viene costruito con i parametri:
            classificatore addestrato
            scaler addestrato
            columnstoscale per indicare quali colonne devono essere elaborate dallo scaler
            columnlist contenente tutte le colonne utilizzate dal classificatore
            self.type per indicare il tipo di titoli trattati dal classificatore
        :return:
        """

        trainset = self.enabledcolumns.copy()

        # Sampling
        if self.sampler != SamplingEnum.NONE:
            if self.sampler == SamplingEnum.UNDER:
                # Undersampling randomico 50-50 label 1 e label 0
                X = trainset.drop(columns="label").values
                Y = trainset["label"].values
                rus = RandomUnderSampler(random_state=42)
                X_rus, Y_rus = rus.fit_resample(X, Y)
                # unisco X_rus e Y_rus di nuovo in trainset
                trainset = pd.DataFrame(X_rus, columns=trainset.drop(columns="label").columns)
                trainset["label"] = Y_rus
                # Aggiorno i dati in enabledcolumns per contenere il nuovo trainset con sampling
                self.enabledcolumns = trainset.copy()
            if self.sampler == SamplingEnum.SMOTE:
                # SMOTE oversampling
                X = trainset.drop(columns="label").values
                Y = trainset["label"].values
                sm = SMOTE(random_state=42)
                X_sm, Y_sm = sm.fit_sample(X, Y)
                # unisco X_sm e Y_sm di nuovo in trainset
                trainset = pd.DataFrame(X_sm, columns=trainset.drop(columns="label").columns)
                trainset["label"] = Y_sm
                # Aggiorno i dati in enabledcolumns per contenere il nuovo trainset con sampling
                self.enabledcolumns = trainset.copy()

        # Separazione label
        label_column = trainset["label"]
        trainset.drop(columns="label", inplace=True)

        # Salvataggio nomi di tutte le colonne che verranno utilizzate
        columnlist = list(self.enabledcolumns.columns.values)

        # Instanziazione scaler
        scaler = None
        columnstoscale = []
        if self.scaler != ScalingEnum.NONE:
            if self.scaler == ScalingEnum.STANDARD:
                scaler = StandardScaler()
            elif self.scaler == ScalingEnum.MINMAX:
                scaler = MinMaxScaler()
            # Individuazione colonne categoriche
            column_list = list(self.enabledcolumns.columns.values)
            if self.type == PFPGEnum.PF:
                notcategorical = list(set(column_list) - set(self._categoricalpf))
                categorical = list(set(column_list) - set(notcategorical))
            elif self.type == PFPGEnum.PG:
                notcategorical = list(set(column_list) - set(self._categoricalpg))
                categorical = list(set(column_list) - set(notcategorical))
            # Addestramento e applicazione scaler su colonne non categoriche
            categorical_trainset = trainset[categorical]
            trainset.drop(columns=categorical, inplace=True)
            # Variabile con le colonne da scalare
            columnstoscale = list(trainset.columns.values)
            # Fit e transform scaler
            scaler.fit(trainset.values)
            scaled_features_trainset = scaler.transform(trainset.values)
            # Ricostruzione trainset
            scaled_trainset = pd.DataFrame(scaled_features_trainset, index=trainset.index, columns=trainset.columns)
            trainset = pd.concat([scaled_trainset, categorical_trainset], axis=1, sort=False)

        # Instanziazione classificatore
        if self.classifier == ClassifierEnum.LOGISTIC:
            classifier = skl.linear_model.LogisticRegression(solver="lbfgs", max_iter=10000)
        elif self.classifier == ClassifierEnum.SVC:
            classifier = svm.SVC(kernel="rbf", gamma="scale")
        elif self.classifier == ClassifierEnum.TREE:
            classifier = skl.tree.DecisionTreeClassifier()
        elif self.classifier == ClassifierEnum.FOREST:
            classifier = RandomForestClassifier(n_estimators=100)
        elif self.classifier == ClassifierEnum.XGB:
            classifier = xgb.XGBClassifier()

        # Addestramento classificatore
        X = trainset.values
        Y = label_column.values
        classifier = classifier.fit(X, Y)

        # Ritorno pipeline
        return AlgorithmPipeline(classifier,scaler,columnstoscale,columnlist,self.type)

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
