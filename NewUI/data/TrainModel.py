from utility.funzioni import *
from data.AlgorithmPipeline import *
from utility.Enums import *


class TrainModel:
    """
    Contiene il dataframe di addestramento,
    espone metodo per ritornare AlgorithmPipeline: un modello addestrato solamente sulle colonne enabledcolumns
    """

    def __init__(self, type: PFPGEnum, enabledcolumns: pd.DataFrame, disabledcolumns: pd.DataFrame):
        self.type = type
        self.enabledcolumns = enabledcolumns
        self.disabledcolumns = disabledcolumns

        # Per addestramento
        self.scaler: ScalingEnum = ScalingEnum.NONE
        self.sampler: SamplingEnum = SamplingEnum.NONE
        self.classifier: ClassifierEnum.LOGISTIC

        # colonne categoriche apparte label
        self._categoricalpf=["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente"]
        self._categoricalpg=["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente"]

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

    def get_undersamplingrows(self) -> int:
        return self.get_positive_label()

    def get_SMOTErows(self) -> int:
        return self.get_positive_label()*2

    def get_positive_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.enabledcolumns.loc[(self.enabledcolumns.label == 0)])

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.enabledcolumns.columns.values))):
            self.disabledcolumns = self.enabledcolumns[columns]
            self.enabledcolumns.drop(columns=columns)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns)
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



        # Separazione label
        label_column = trainset["label"]
        trainset.drop(coluumns="label", inplace=True)


        # Instanziazione scaler
        scaler = None
        if self.scaler != ScalingEnum.NONE:
            if self.scaler == ScalingEnum.STANDARD:
                scaler = StandardScaler()
            elif self.scaler == ScalingEnum.MINMAX:
                scaler= MinMaxScaler()
            # Individuazione colonne categoriche
            column_list=list(self.enabledcolumns.columns.values)
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