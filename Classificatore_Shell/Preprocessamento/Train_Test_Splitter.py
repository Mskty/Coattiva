from Classificatore_Shell.funzioni import *
from sklearn.utils import shuffle
import datetime
import random as random


def train_test_splitter_possibilities(df: pd.DataFrame):
    """
    Dato il dataframe dei dati storici preparati ritorna un nuovo dataframe dove ogni riga
    rappresenta la data di un ruolo presente nei dati storici. Ogni riga riporta, per quella data
    quanti crediti appartengono a quel ruolo e tutti i precedenti (nesempi), quanti di questi sono
    classificati come positivi (true), e quanti come negativi (false). L'idea è che ciascuna delle
    date dei ruoli può essere utilizzata per splittare i dati storici in training set e test set,
    vengono dunque riportate le possibili composizioni dei training set ad ogni data di ruolo scelta.

    :param df: dataframe contenente i titoli aggregati e preparati
    :return: dataframe da 4 colonne: ruolo, nesempi, true, false
    """
    # Ricavo i ruoli
    ruoli = df.DataCaricoTitolo.unique()

    # Ordino in modo crescente le date dei ruoli
    dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in ruoli]
    dates.sort()
    ruoli = list([datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates])

    # creo un dataframe con le possibili date e numero di esempi contenuto in ogni possibile training set
    results = pd.DataFrame()
    results["ruolo"] = ruoli
    results["nesempi"] = 0
    results["true"] = 0
    results["false"] = 0
    count = 1
    for r in ruoli:
        results.loc[(results.ruolo == r), "nesempi"] = len(df.loc[df.DataCaricoTitolo.isin(ruoli[:count])])
        results.loc[(results.ruolo == r), "true"] = len(df.loc[(df.DataCaricoTitolo.isin(ruoli[:count])) & (df.label == 1)])
        results.loc[(results.ruolo == r), "false"] = len(df.loc[(df.DataCaricoTitolo.isin(ruoli[:count])) & (df.label == 0)])
        count = count + 1

    return results


def train_test_splitter(df: pd.DataFrame, dates, type):
    """
    Suddivide il dataframe dei dati storici aggregati e preparati in training set e test set, dove il training set
    sarà composto di tutti i titoli con campo DataCaricoTitolo uguale ad uno dei valori presenti nella lista dates
    :param df: dataframe contenente i titoli aggregati e preparati
    :param dates: lista di date
    :param type: inutilizzato
    :return: dataframe trainset e testset
    """
    # copio per non modificare dataframe originale
    df = df.copy()

    # Divisione test out of sample e training in sample
    trainset = df.loc[(df.DataCaricoTitolo.isin(dates))]
    testset = df.loc[(~df.DataCaricoTitolo.isin(dates))]

    # Drop dell colonna DataCaricoTitolo una volta separati i due set
    trainset.drop(columns="DataCaricoTitolo", inplace=True)
    testset.drop(columns="DataCaricoTitolo", inplace=True)

    # Mescolo le righe del training set
    trainset = skl.utils.shuffle(trainset, random_state=42)

    # Ritorno train e test set
    return trainset, testset
