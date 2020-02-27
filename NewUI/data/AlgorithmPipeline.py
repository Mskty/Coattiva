from utility.funzioni import *
from utility.Score import *

from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import plot_confusion_matrix


class AlgorithmPipeline:

    # Classificatore già addestrato su training set
    # Scaler già addestrato su training set

    def __init__(self, classifier, scaler=None, columnstoscale: list = None):
        self.classifier = classifier
        self.scaler = scaler
        self.columnstoscale = columnstoscale

    def predict(self, dataset: pd.DataFrame):
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
        accuracy = accuracy_score(dataset["label"].values, dataset["predizione"].values)
        precision = precision_score(dataset["label"].values, dataset["predizione"].values)
        recall = recall_score(dataset["label"].values, dataset["predizione"].values)
        f1 = f1_score(dataset["label"].values, dataset["predizione"].values)
        roc_auc = roc_auc_score(dataset["label"].values, dataset["predizione"].values)
        return Score(accuracy, precision, recall, f1, roc_auc)

    def plot_roc_curve(self, dataset: pd.DataFrame):
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
        ax.plot([0, 1], [0, 1], 'r--', label="Selezione Casuale (AUC = 0.5)")
        ax.plot([0, 0, 1], [0, 1, 1], 'g-.', label="Classificatore Perfetto (AUC = 1.0)")
        ax.legend(loc='lower right')

    def plot_precision_recall(self, dataset: pd.DataFrame):
        # fa comparire il grafico della precision vs recall con threshold della decision function (default 0)
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
        ax.plot([0, 1, 1], [1, 1, 0.5], 'g-.', label="Classificatore Perfetto (AP = 1.0)")
        ax.set(ylabel="Precisione",
               xlabel="Recall")
        ax.legend(loc='lower right')

    def plot_confusion_matrix(self, dataset: pd.DataFrame):
        # da comparire il grafico della confusion matrix
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
        class_labels=["Positivo", "Negativo"]
        skl.metrics.plot_confusion_matrix(self.classifier, X, Y, cmap=plt.cm.Blues, values_format="", display_labels=class_labels)
        ax = plt.gca()
        ax.set(ylabel="Risultati reali",
               xlabel="Risultati predetti")