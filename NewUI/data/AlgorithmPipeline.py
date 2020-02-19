from utility.funzioni import *
from utility.Score import *

class AlgorithmPipeline:

    # Classificatore già addestrato su training set
    # Scaler già addestrato su training set

    def __init__(self, classifier, scaler=None, columnstoscale: list= None):
        self.classifier = classifier
        self.scaler = scaler
        self.columnstoscale = columnstoscale

    def predict(self, dataset: pd.DataFrame):
        dataset = dataset.copy()

        #Applicazione scaler su colonne non categoriche (columnstoscale) se presente
        if self.scaler != None:
            dataset_to_scale=dataset[self.columnstoscale]
            dataset.drop(columns=dataset.columns.difference(self.columnstoscale), inplace=True)
            scaled_features_dataset = self.scaler.transform(dataset_to_scale.values)
            scaled_dataset = pd.DataFrame(scaled_features_dataset, index=dataset_to_scale.index, columns=dataset_to_scale.columns)
            dataset = pd.concat([scaled_dataset, dataset], axis=1, sort=False)

        # Separazione colonna label se presente
        if "label" in dataset.columns:
            X = dataset.drop(columns="label").to_numpy()
        else:
            X = dataset.to_numpy()

        # Ritorno predizioni
        return self.classifier.predict(X)

    def metrics(self, dataset: pd.DataFrame) -> Score:
        accuracy = accuracy_score(dataset["label"].values, dataset["predizione"].values)
        precision = precision_score(dataset["label"].values, dataset["predizione"].values)
        recall = recall_score(dataset["label"].values, dataset["predizione"].values)
        f1 = f1_score(dataset["label"].values, dataset["predizione"].values)
        roc_auc = roc_auc_score(dataset["label"].values, dataset["predizione"].values)
        return Score(accuracy,precision,recall,f1,roc_auc)

    def confusion_matrix(self, dataset:pd.DataFrame):
        # Ritorna np array 2x2
        return confusion_matrix(dataset["label"].values, dataset["predizione"].values)





