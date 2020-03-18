from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE

from utility.Imports import *
from data.AlgorithmPipeline import *
from utility.Enums import *


class TrainModel:
    """
    Classe che rappresenta i dati del trainingset che verranno utilizzati come in-sample per addestrare un classificatore.
    I dati presenti sono gestiti utilizzando Dataframes della libreria pandas.
    Vengono esposti metodi per modificare la struttura dei DataFrames attraverso la rimozione e aggiunta di colonne
    , per produrre un oggetto AlgorithmPipeline rappresentante il classificatore addestrato sui dati del training set e
    infine metodi per aggiungere e rimuovere le predizioni effettuate sui dati ed esportare su file csv i risultati.
    PARAMETRI:
    self.type: Valore di tipo PFPGEnum rappresentante il tipo di dati contenuti in self.enabledcolumns e self.disabledcolumns
    self.enabledcolumns: oggetto di tipo pandas.Dataframe contenente le colonne/features dei dati che saranno utilizzate
                         dal classificatore addestrato per predire i dati contenuti nel testset
    self.enabledcolumns: oggetto di tipo pandas.Dataframe contenente le colonne/features dei dati che sono attualmente
                         disattivate e non verranno quindi utilizzate dal classificatore addestrato per predire i dati
                         ontenuti nel testset
    self.scaler: Valore di tipo ScalingEnum rappresentante il tipo di scaling dei dati utilizzato dal classificatore
    self.sampler: Valore di tipo SamplingEnum rappresentate il tipo di sampling che sarà utilizzato durante l'addestramento
                  del classificatore sui dati del trainingset
    self.classifier: Valore di tipo ClassifierEnum rappresentante il tipo di algoritmo di apprendimento utilizzato per
                     addestrare il classificatore
    self._categoricalpf: parametro preimpostato, lista di valori stringa contenente i nomi delle colonne/features categoriche
                         per dati appartenenti a PERSONE FISICHE i cui valori non dovranno quindi essere sottoposti
                         a normalizzazione dallo scaler
    self._categoricalpg: parametro preimpostato, lista di valori stringa contenente i nomi delle colonne/features categoriche
                         per dati appartenenti a PERSONE GIURIDICHE i cui valori non dovranno quindi essere sottoposti
                         a normalizzazione dallo scaler
    """

    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self, type: PFPGEnum, enabledcolumns: pd.DataFrame, disabledcolumns: pd.DataFrame):

        # label sempre enabled
        self.type: PFPGEnum = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

        # Per addestramento, valori di default
        self.scaler: ScalingEnum = ScalingEnum.NONE
        self.sampler: SamplingEnum = SamplingEnum.NONE
        self.classifier: ClassifierEnum = ClassifierEnum.LOGISTIC

        # colonne categoriche apparte label (che sarà già stata rimossa al momento dello scaling)
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

        # Instanziazione algoritmo di apprendimento (valori iperparametri ottimali ottenuti dallo studio con grid
        # search), gli iperparametri ottimali per alcuni algoritmi sono risultati differenti per titoli riferiti a
        # Persone Fisiche e Persone Giuridiche

        # PERSONE FISICHE
        if self.type == PFPGEnum.PF:
            if self.classifier == ClassifierEnum.LOGISTIC:
                classifier = skl.linear_model.LogisticRegression(C=100, class_weight='balanced', dual=False,
                                                                 fit_intercept=True, intercept_scaling=1, l1_ratio=None,
                                                                 max_iter=1000, multi_class='auto', n_jobs=None,
                                                                 penalty='l1',
                                                                 random_state=None, solver='liblinear', tol=0.0001,
                                                                 verbose=0,
                                                                 warm_start=False)
            elif self.classifier == ClassifierEnum.SVC:
                classifier = svm.SVC(C=1, break_ties=False, cache_size=200, class_weight='balanced', coef0=0.0,
                                     decision_function_shape='ovr', degree=3, gamma=0.1, kernel='rbf',
                                     max_iter=-1, probability=True, random_state=None, shrinking=True,
                                     tol=0.001, verbose=False)
            elif self.classifier == ClassifierEnum.TREE:
                classifier = skl.tree.DecisionTreeClassifier(ccp_alpha=0.0, class_weight='balanced', criterion='gini',
                                                             max_depth=10, max_features=None, max_leaf_nodes=100,
                                                             min_impurity_decrease=0.0, min_impurity_split=None,
                                                             min_samples_leaf=4, min_samples_split=8,
                                                             min_weight_fraction_leaf=0.0, presort='deprecated',
                                                             random_state=None, splitter='random')
            elif self.classifier == ClassifierEnum.FOREST:
                classifier = RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight='balanced',
                                                    criterion='entropy', max_depth=14, max_features='auto',
                                                    max_leaf_nodes=None, max_samples=None,
                                                    min_impurity_decrease=0.0, min_impurity_split=None,
                                                    min_samples_leaf=1, min_samples_split=2,
                                                    min_weight_fraction_leaf=0.0, n_estimators=500,
                                                    n_jobs=-1, oob_score=False, random_state=None, verbose=0,
                                                    warm_start=False)
            elif self.classifier == ClassifierEnum.XGB:
                classifier = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                                               colsample_bynode=1, colsample_bytree=0.4, gamma=1.0,
                                               learning_rate=0.1, max_delta_step=0, max_depth=4,
                                               min_child_weight=10, missing=None, n_estimators=100, n_jobs=1,
                                               nthread=None, objective='binary:logistic', random_state=0,
                                               reg_alpha=0, reg_lambda=1, scale_pos_weight=2, seed=None,
                                               silent=None, subsample=1, verbosity=1)
        # PERSONE GIURIDICHE
        elif self.type == PFPGEnum.PG:
            if self.classifier == ClassifierEnum.LOGISTIC:
                classifier = skl.linear_model.LogisticRegression(C=100, class_weight='balanced', dual=False,
                                                                 fit_intercept=True, intercept_scaling=1, l1_ratio=None,
                                                                 max_iter=1000, multi_class='auto', n_jobs=None,
                                                                 penalty='l2',
                                                                 random_state=None, solver='liblinear', tol=0.0001,
                                                                 verbose=0,
                                                                 warm_start=False)
            elif self.classifier == ClassifierEnum.SVC:
                classifier = svm.SVC(C=1, break_ties=False, cache_size=200, class_weight='balanced', coef0=0.0,
                                     decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
                                     max_iter=-1, probability=True, random_state=None, shrinking=True,
                                     tol=0.001, verbose=False)
            elif self.classifier == ClassifierEnum.TREE:
                classifier = skl.tree.DecisionTreeClassifier(ccp_alpha=0.0, class_weight='balanced', criterion='gini',
                                                             max_depth=14, max_features=None, max_leaf_nodes=10,
                                                             min_impurity_decrease=0.0, min_impurity_split=None,
                                                             min_samples_leaf=4, min_samples_split=4,
                                                             min_weight_fraction_leaf=0.0, presort='deprecated',
                                                             random_state=None, splitter='random')
            elif self.classifier == ClassifierEnum.FOREST:
                classifier = RandomForestClassifier(bootstrap=False, ccp_alpha=0.0, class_weight='balanced',
                                                    criterion='entropy', max_depth=10, max_features='sqrt',
                                                    max_leaf_nodes=None, max_samples=None,
                                                    min_impurity_decrease=0.0, min_impurity_split=None,
                                                    min_samples_leaf=1, min_samples_split=2,
                                                    min_weight_fraction_leaf=0.0, n_estimators=200,
                                                    n_jobs=-1, oob_score=False, random_state=None, verbose=0,
                                                    warm_start=False)
            elif self.classifier == ClassifierEnum.XGB:
                classifier = xgb.XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
                                               colsample_bynode=1, colsample_bytree=0.4, gamma=1.0,
                                               learning_rate=0.1, max_delta_step=0, max_depth=4,
                                               min_child_weight=10, missing=None, n_estimators=100, n_jobs=1,
                                               nthread=None, objective='binary:logistic', random_state=0,
                                               reg_alpha=0, reg_lambda=1, scale_pos_weight=2, seed=None,
                                               silent=None, subsample=1, verbosity=1)
        # Addestramento classificatore
        X = trainset.values
        Y = label_column.values
        classifier = classifier.fit(X, Y)

        # Ritorno pipeline
        return AlgorithmPipeline(classifier, scaler, columnstoscale, columnlist, self.type)

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
