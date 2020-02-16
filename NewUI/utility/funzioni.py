import itertools
import random
import tkinter as tk

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn as skl
import numpy as np
import seaborn as sns
import time
import datetime
import xgboost as xgb

from tkinter import filedialog

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from joblib import dump, load
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, svm, model_selection
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV, \
    RandomizedSearchCV, cross_validate, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, pairwise, precision_recall_curve, precision_score, recall_score, f1_score, roc_auc_score
from sklearn import preprocessing
from sklearn import tree
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from Modellazione.Model_Trainer import separazione_label

"""
in questo script sono contenute le funzioni utilizzate genericamente durante lo svolgimento del progetto e gli import più generali.
solo alcune vengono utilizzate anche nell'applicazione Classificatore_Shell, ma vengono quì riportate tutte per completezza.
"""


"""--------------------------------------------------UTILITIES PER DATASET-----------------------------------------------------"""


def set_dataset_display_properties(width=1000, columns=200, rows=200):
    """
    Imposta i valori di visualizzazione dei dataset pandas sul terminale
    :param width:
    :param columns:
    :param rows:
    :return:
    """

    pd.set_option('display.width', width)
    pd.set_option('display.max_columns', columns)
    pd.set_option('display.max_rows', rows)


def load_raw_data(raw_data_path) -> pd.DataFrame:
    """
    ritorna un pandas Dataframe dal file csv specificato dal percorso
    :param raw_data_path:
    :return:
    """
    set_dataset_display_properties()
    data = pd.read_csv(raw_data_path)

    return data


def load_raw_data_excel(raw_data_path) -> pd.DataFrame:
    """
        ritorna un pandas Dataframe dal file excel specificato dal percorso
        :param raw_data_path:
        :return:
        """
    set_dataset_display_properties()
    data = pd.read_excel(raw_data_path,
                         sheetname=0,
                         header=0,
                         index_col=False,
                         keep_default_na=True)

    return data


def save_dataset(data: pd.DataFrame):
    """
    Mostra un'interfaccia grafica per salvare il dataset in formato csv nella posizione desiderata nel filesystem
    :param data: pandas Dataframe da salvare
    :return:
    """
    root = tk.Tk()
    canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue2', relief='raised')
    canvas1.pack()

    def exportCSV():
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        data.to_csv(export_file_path, index=None, header=True)

    saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white',
                                 font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=saveAsButton_CSV)

    root.mainloop()


def show_data_info(data: pd.DataFrame):
    """
    Stampa diverse informazioni per il DataFrame passato
    :param data: pandas Dataframe
    :return:
    """

    print("\n----------INIZIO DATASET---------- \n")
    print("Formato: \n")
    print(data.shape)
    print("\nInfo e tipi: \n")
    print(data.info())
    print("\nDescrizione: \n")
    print(data.describe())
    print("\nPrime 5 righe: \n")
    print(data.head())
    print("\n----------FINE DATASET---------- \n")


def divide_features_target(data: pd.DataFrame):
    """
    Divide il dataset in 2 numpy array, X=features e Y=label, Y deve essere l'ultima colonna del DataFrame
    :param data:
    :return:
    """

    X = data.drop(data.columns[len(data.columns) - 1], axis=1).to_numpy()
    Y = data[data.columns[len(data.columns) - 1]].to_numpy()
    return X, Y


def discrete_label_encoder(features, data: pd.DataFrame) -> pd.DataFrame:
    """
    Ritorna il DataFrame passato con le colonne selezionate in formato label discrete
    :param features:
    :param data:
    :return:
    """

    data = data.copy()
    encoder = LabelEncoder()
    for feature in features:
        data[feature] = encoder.fit_transform(data[feature])
    return data


"""-------------------------------------GRAFICI E VISUALIZZAZIONE------------------------------------------"""


def bar_plot(x_data, y_data, title="", x_label="", y_label=""):
    # visualizza a schermo un bar plot con seaborn

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x_data, y_data)
    plt.title(title)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)


def dist_plot(data, title="", x_label="", y_label=""):
    # visualizza a schermo un distribution plot con seaborn della feature passata con il parametro data
    # data deve essere un array monodimensionale
    plt.figure(figsize=(10, 5))
    sns.set_style("whitegrid")
    ax = sns.distplot(data)


def correlation_heatmap(df: pd.DataFrame):
    # visualizza a schermo una correlation heatmap, con seaborn, delle features del dataframe passato
    _, ax = plt.subplots(figsize=(10, 8))
    colormap = sns.diverging_palette(220, 10, as_cmap=True)

    _ = sns.heatmap(
        df.corr(),
        cmap=colormap,
        square=True,
        cbar_kws={'shrink': .9},
        ax=ax,
        annot=True,
        linewidths=0.1, vmax=1.0, linecolor='white',
        annot_kws={'fontsize': 12}
    )

    plt.title('Pearson Correlation of Features', y=1.05, size=15)


def scatter_plot_3d(x_data, y_data, z_data, class_label, title="", x_label="", y_label="", z_label=""):
    # genera una nuova figura 3d, da visualizzare poi a schermo con plt.show()

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')
    plt.colorbar(ax.scatter(x_data, y_data, z_data, c=class_label))
    plt.title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)


def scatter_plot_2d(x_data, y_data, class_label, title="", x_label="", y_label="", size: int = None):
    # genera una nuova figura 2d, da visualizzare poi a schermo con plt.show()

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    if size == None:
        plt.colorbar(ax.scatter(x_data, y_data, c=class_label))
    else:
        plt.colorbar(ax.scatter(x_data, y_data, c=class_label, s=size))
    plt.title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    Stampa in un grafico 2d la confusion matrix
    si può scegliere di normalizzare i risultati tra 0 e 1 passando True al parametro normalize.
    :param cm: confusion matrix
    :param classes:
    :param normalize:
    :param title:
    :param cmap:
    :return:
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=0)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        # print("Normalized confusion matrix")
    else:
        True  # print('Confusion matrix, without normalization')

    # print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


"""-------------------------------------UTILITY PER SELEZIONARE IL MODELLO------------------------------------------"""


def report(results, n_top=3):
    # Funzione di utilità per stampare a schermo i migliori score
    # results è un array di risultati

    for i in range(1, n_top + 1):
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                results['mean_test_score'][candidate],
                results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")


def grid_search(param_grid, classifier, X_train, y_train, fold=5, metric="f1"):
    # effettua una cross validation del modello con grid search sulla lista dei parametri passata
    # ritorna i migliori parametri e il miglior risultato, media su tutti i fold
    # usa lo scoring specificato dal parametro metric, di default f1 score

    grid_search_cv = GridSearchCV(classifier, param_grid, cv=fold, iid=False, scoring=metric)

    start = time.perf_counter()
    grid_search_cv.fit(X_train, y_train)
    print("Esecuzione terminata in: ", time.perf_counter() - start)

    print("Migliori parametri:", grid_search_cv.best_params_)
    print("Miglior modello:", grid_search_cv.best_estimator_)
    cvres = grid_search_cv.cv_results_
    print("Risultati: \n")
    report(grid_search_cv.cv_results_)

    return grid_search_cv.best_params_, grid_search_cv.best_score_


def random_search(param_distribution, num_iter, classifier, X_train, y_train, fold=5, metric="f1"):
    # effettua una cross validation del modello con random search sulla distribuzione dei parametri passata
    # ritorna i migliori parametri e il miglior risultato, media su tutti i fold
    # usa lo scoring specificato dal parametro metric, di default f1 score

    random_search_cv = RandomizedSearchCV(classifier, param_distribution, n_iter=num_iter, cv=fold, iid=False, scoring=metric)

    start = time.perf_counter()
    random_search_cv.fit(X_train, y_train)
    print("Esecuzione terminata in: ", time.perf_counter() - start)

    print("Migliori parametri:" + random_search_cv.best_params_)
    print("Miglior modello:" + random_search_cv.best_estimator_)
    cvres = random_search_cv.cv_results_
    print("Risultati: \n")
    report(random_search_cv.cv_results_)

    return random_search_cv.best_params_, random_search_cv.best_score_


def display_scores(scores):
    # funzione di utilità per mostrare a schernmo i risultati della cross validation
    # scores è un array di scores ritornato da cross validation score

    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())


def cross_validation(classifier, X_train, y_train, fold=5, metric="f1"):
    # usa lo scoring specificato in metric
    # ritorna il valore medio della cross validation

    scores = cross_val_score(classifier, X_train, y_train, cv=fold, scoring=metric)  # default è stratified
    display_scores(scores)
    return scores


def display_all_scores(scores):
    """
    Utilizza la dunzione display_scores per stampare l'array di risultati presenti in ogni key di scores
    :param scores: dictionary contenente array numerici di scores ritornati da un processo di cross_validation
    :return:
    """
    keys = scores.keys()
    for key in keys:
        print(key, ":")
        display_scores(scores[key])
        print("")  # Linea bianca


def cross_validation_scores(classifiers, X_train, y_train, fold=5, metric="f1", sample="None"):
    """
    Esegue cross validation e stampa i risultati per tutti i classificatori passati all'interno di classifiers
    :param classifiers:
    :param X_train:
    :param y_train:
    :param fold:
    :param metric: se sample == "None" utilizza la o le metriche specificate nella cross_validate
    :param sample: indica che tecnica di sampling è utilizzata, default nessuna, altrimenti i valori sono "SMOTE" o "NearMiss"
    :return:
    """
    if sample == "None":
        for classifier in classifiers:
            print(classifier.__class__.__name__, ": ")
            print(" ")
            display_all_scores(cross_validate(classifier, X_train, y_train, cv=fold, scoring=metric))
            print("\n")
    elif sample == "SMOTE":
        for classifier in classifiers:
            print(classifier.__class__.__name__, ": ")
            print(" ")
            display_all_scores(smote_cross_validation(classifier, X_train, y_train))
            print("\n")
    elif sample == "NearMiss":
        for classifier in classifiers:
            print(classifier.__class__.__name__, ": ")
            print(" ")
            display_all_scores(nearmiss_cross_validation(classifier, X_train, y_train))
            print("\n")


def smote_cross_validation(classifier, X, y, fold=5):
    """
    Esegue cross validation applicando SMOTE oversampling sui training folds
    Ritorna 5 diverse scoring metrics sui test set
    :param classifier:
    :param X:
    :param y:
    :param fold:
    :return:
    """

    kf = StratifiedKFold(n_splits=fold)
    accuracy = np.array([])
    precision = np.array([])
    recall = np.array([])
    f1 = np.array([])
    roc_auc = np.array([])
    scores = {'No Results': np.zeros(1)}
    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        X_train_oversampled, y_train_oversampled = SMOTE(random_state=42).fit_sample(X_train, y_train)
        classifier.fit(X_train_oversampled, y_train_oversampled)
        y_pred = classifier.predict(X_test)
        accuracy = np.append(accuracy, accuracy_score(y_test, y_pred))
        precision = np.append(precision, precision_score(y_test, y_pred))
        recall = np.append(recall, recall_score(y_test, y_pred))
        f1 = np.append(f1, f1_score(y_test, y_pred))
        roc_auc = np.append(roc_auc, roc_auc_score(y_test, y_pred))
        scores = {'test_accuracy': accuracy,
                  'test_precision': precision,
                  'test_recall': recall,
                  'test_f1_score': f1,
                  'test_roc_auc': roc_auc}
    return scores


def nearmiss_cross_validation(classifier, X, y, fold=5):
    """
    Esegue cross validation applicando NearMiss oversampling sui training folds
    Ritorna 5 diverse scoring metrics sui test set
    :param classifier:
    :param X:
    :param y:
    :param fold:
    :return:
    """
    kf = StratifiedKFold(n_splits=fold)
    accuracy = np.array([])
    precision = np.array([])
    recall = np.array([])
    f1 = np.array([])
    roc_auc = np.array([])
    scores = {'No Results': np.zeros(1)}
    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        X_train_oversampled, y_train_oversampled = NearMiss(random_state=42).fit_sample(X_train, y_train)
        classifier.fit(X_train_oversampled, y_train_oversampled)
        y_pred = classifier.predict(X_test)
        accuracy = np.append(accuracy, accuracy_score(y_test, y_pred))
        precision = np.append(precision, precision_score(y_test, y_pred))
        recall = np.append(recall, recall_score(y_test, y_pred))
        f1 = np.append(f1, f1_score(y_test, y_pred))
        roc_auc = np.append(roc_auc, roc_auc_score(y_test, y_pred))
        scores = {'test_accuracy': accuracy,
                  'test_precision': precision,
                  'test_recall': recall,
                  'test_f1_score': f1,
                  'test_roc_auc': roc_auc}
    return scores


def multiple_confusion_matrix(classifiers, X_train, y_train, X_test, y_test):
    """
    Fitta ogni classificatore in classifiers e stampa la confusion matrix, calcolata su
    X_test e y_test, per ogni classificatore.
    :param classifiers: lista di classificatori non fittati
    :param X_train:
    :param y_train:
    :param X_test:
    :param y_test:
    :return:
    """
    for classifier in classifiers:
        print(classifier.__class__.__name__, ": ")
        classifier.fit(X_train, y_train)
        print(confusion_matrix(y_test, classifier.predict(X_test)))
        print(classification_report(y_test, classifier.predict(X_test)))
        print("\n")


def random_feature_selection(trainset: pd.DataFrame, testset: pd.DataFrame = None, test=False):
    """
    Ritorna X Y sia train che test senza un numero randomico di features
    :param trainset:
    :param testset:
    :param test: se True ritorna anche il test set, False utilizzato solo sul training (per cross validation)
    :return:
    """

    remove_n = random.randint(1, 10)
    columns = np.random.choice(trainset.drop(columns="label").columns.values, remove_n, replace=False)
    print("Feature rimosse:", columns)
    print("Feature rimaste:", trainset.drop(columns="label").drop(columns=columns).columns.values)
    if test == True:
        X_train, Y_train, X_test, Y_test = separazione_label(trainset.drop(columns=columns), testset.drop(columns=columns), test=True)
        return X_train, Y_train, X_test, Y_test
    else:
        X_train, Y_train = separazione_label(trainset.drop(columns=columns))
        return X_train, Y_train


def column_feature_selection(trainset: pd.DataFrame, columns, testset: pd.DataFrame = None, test=False):
    """
    Ritorna X Y sia train che test con le sole feature indicate + label
    :param trainset:
    :param testset:
    :param testset: array contenente i titoli delle colonne da mantenere
    :param test: se True ritorna anche il test set, False utilizzato solo sul training (per cross validation)
    :return:
    """
    columns = np.array(columns)
    columns = np.append(columns, 'label')
    print("Feature rimaste:", columns)
    if test == True:
        X_train, Y_train, X_test, Y_test = separazione_label(trainset[columns], testset[columns], test=True)
        return X_train, Y_train, X_test, Y_test
    else:
        X_train, Y_train = separazione_label(trainset[columns])
        return X_train, Y_train


def model_feature_selection(trainset: pd.DataFrame, model, testset: pd.DataFrame = None, test=False):
    """
    Valuta l'importanza delle feature secondo il modello passato, ritorna una lista delle colonne corrispondente alle features valutate più importanti
    :param trainset:
    :param testset:
    :param model: Modello che valuterà le features, deve supportare la funzionalità di feature_importance
    :param test:
    :return:
    """
    model_select = SelectFromModel(model, threshold='median')
    X_train, Y_train = separazione_label(trainset)
    X_trans = model_select.fit_transform(X_train, Y_train)
    print("We started with {0} features but retained only {1} of them!".format(X_train.shape[1], X_trans.shape[1]))
    columns_retained_FromMode = trainset.drop(columns="label").columns[model_select.get_support()].values
    return columns_retained_FromMode


"""-------------------------------------VISUALIZZAZIONE METRICHE DI CLASSIFICAZIONE------------------------------------------"""


def plot_roc_curve(true_positive, false_positive, label=None):
    # fa comparire il grafico della roc_curve
    # richiede fpr, tpr, thresholds = roc_curve(y_train_true, y_proba_scores)

    plt.plot(true_positive, false_positive, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--', label="coin toss")
    plt.axis([0, 1, 0, 1])
    plt.legend(loc="lower right")
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')


def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
    # fa comparire il grafico della precision vs recall con threshold della decision function (default 0)
    # precisions, recalls, thresholds = precision_recall_curve(y_train_true, y_proba_scores)

    plt.plot(thresholds, precisions[:-1], "b-", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.axis([0, 1, 0, 1])
    plt.xlabel("Threshold")
    plt.legend(loc="upper left")


def plot_precision_recall(precision, recall):
    # fa comparire il grafico della precision vs recall con threshold della decision function (default 0)
    # precisions, recalls, thresholds = precision_recall_curve(y_train_true, y_proba_scores)

    plt.plot(recall, precision, "b-", label="Precision")
    plt.axis([0, 1, 0, 1])
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.legend(loc="upper left")


"""-------------------------------------SALVARE E CARICARE MODELLI------------------------------------------"""


def save_model(classifier, filename):
    """
    Salva il modello fittato in un file dal nome indicato
    :param classifier:
    :param filename:
    :return:
    """
    dump(classifier, filename + ".joblib")


def load_model(filename):
    """
    Carica il modello fittato dal file con il percorso indicato
    :param filename:
    :return: classificatore di scikit-learn fittato
    """
    classifier = load(filename + ".joblib")
    return classifier
