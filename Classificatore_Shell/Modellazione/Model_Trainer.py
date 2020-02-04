from Classificatore_Shell.funzioni import *
"""
Quì sono contenute le funzioni riguardanti l'addestramento diretto del modello a partire da training set 
e la funzione per riportare i risultati su test set
"""


def separazione_label(trainset: pd.DataFrame, testset: pd.DataFrame = None, test=False):
    """
    Separa i dataframe trainset e testset nelle rispettive componenti input (features) e output (label)
    :param trainset:
    :param testset:
    :param test: se True ritorna anche la separazione per il testset
    :return: X_train, Y_train array numpy per l'addestramento, opzionalmente anche X_test, Y_test array numpy per l'out of sample
    """
    X_test, Y_test = None, None
    Y_train = trainset['label'].to_numpy()
    X_train = trainset.drop(columns="label").to_numpy()
    if test == True:
        Y_test = testset['label'].to_numpy()
        X_test = testset.drop(columns="label").to_numpy()
        return X_train, Y_train, X_test, Y_test
    return X_train, Y_train


def train(classifier, trainset: pd.DataFrame):
    """
    Addestra il classificatore sul training set passato e lo ritorna
    :param classifier:
    :param trainset:
    :return: il classificatore addestrato sul training set
    """
    X_train, Y_train = separazione_label(trainset)
    return classifier.fit(X_train, Y_train)


def report_test(classifier, testset: pd.DataFrame):
    """
    Stampa a schermo le metriche per i risultati del testset, ritorna le previsioni fatte
    :param classifier: classificatore addestrato
    :param testset: dataframe contente il test set non vuoto
    :return: array numpy contenente le previsioni per ogni titolo appartenente al test set
    """
    X_test, Y_test = separazione_label(testset)
    predictions = classifier.predict(X_test)
    print("Confusion matrix per il test set:\n"
          "-il numero degli esempi classificati correttamente si trova nella diagonale principale \n"
          "-il numero degli esempi classificati correttamente si trova nella diagonale secondaria \n ", confusion_matrix(Y_test, predictions))
    print("Rapporto contenente i punteggi nelle metriche di accuratezza, precisione, recall e F1 Score raggiunti dal classificatore sul test set: \n",
          classification_report(Y_test, predictions))
    return predictions
