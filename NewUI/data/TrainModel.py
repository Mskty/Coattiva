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
        self.type = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

        # Per addestramento
        self.scaler: ScalingEnum = ScalingEnum.NONE
        self.sampler: SamplingEnum = SamplingEnum.NONE
        self.classifier: ClassifierEnum= ClassifierEnum.LOGISTIC

        # colonne categoriche apparte label
        self._categoricalpf = ["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente"]
        self._categoricalpg = ["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente"]

    # Set functions

    def set_scaler(self, scaler: ScalingEnum):
        self.scaler = scaler

    def set_sampler(self, sampler: SamplingEnum):
        self.sampler = sampler

    def set_classifier(self, classifier: ClassifierEnum):
        self.classifier = classifier

    # Getter functions

    def get_rows(self) -> int:
        return len(self.enabledcolumns)

    def get_positive_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 0)])

    def get_sampling_rows(self) -> int:
        if self.sampler == SamplingEnum.NONE:
            return self.get_rows()
        elif self.sampler == SamplingEnum.UNDER:
            return self.get_positive_label() * 2
        elif self.sampler == SamplingEnum.SMOTE:
            return self.get_negative_label() * 2

    def get_sampling_positive_label(self) -> int:
        if self.sampler == SamplingEnum.NONE:
            return self.get_positive_label()
        elif self.sampler == SamplingEnum.UNDER:
            return self.get_positive_label()
        elif self.sampler == SamplingEnum.SMOTE:
            return self.get_negative_label()

    def get_sampling_negative_label(self) -> int:
        if self.sampler == SamplingEnum.NONE:
            return self.get_negative_label()
        elif self.sampler == SamplingEnum.UNDER:
            return self.get_positive_label()
        elif self.sampler == SamplingEnum.SMOTE:
            return self.get_negative_label()

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.enabledcolumns.columns.values))):
            self.disabledcolumns = self.enabledcolumns[columns]
            self.enabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns=columns, inplace=True)
        else:
            print("error: colonne non presenti")

    def trainmodel(self) -> AlgorithmPipeline:

        trainset = self.enabledcolumns.copy()

        # Sampling
        if self.sampler != SamplingEnum.NONE:
            if self.sampler == SamplingEnum.UNDER:
                # Undersampling randomico 50-50 label 1 e label 0
                one_indices = trainset[trainset.label == 1].index
                sample_size = sum(trainset.label == 1)  # Equivalent to len(trainset[trainset.label == 1])
                zero_indices = trainset[trainset.label == 0].index
                random_indices = np.random.choice(zero_indices, sample_size, replace=False)
                # Unisco gli 1 e 0
                under_indices = one_indices.union(random_indices)
                trainset = trainset.loc[under_indices]  # nuovo training set con 50/50 di classe 1 e 0
            if self.sampler == SamplingEnum.SMOTE:
                # SMOTE oversampling
                X = trainset.drop(columns="label").values
                Y = trainset["label"].values
                sm = SMOTE(random_state=42)
                X_sm, Y_sm = sm.fit_sample(X, Y)
                # unisco X_sm e Y_sm di nuovo in trainset
                trainset = pd.DataFrame(X_sm, columns=trainset.drop(columns="label").columns)
                trainset["label"] = Y_sm

        # Separazione label
        label_column = trainset["label"]
        trainset.drop(columns="label", inplace=True)

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
            # Fit e transform
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
        return AlgorithmPipeline(classifier,scaler,columnstoscale)

    def attach_predictions(self, pred: list):
        self.enabledcolumns["predizione"] = pred

    def remove_predictions(self):
        self.enabledcolumns.drop(columns="predizione", inplace=True)

    def export_to_csv(self, export_file_path):
        self.enabledcolumns.to_csv(export_file_path, index=None, header=True)
