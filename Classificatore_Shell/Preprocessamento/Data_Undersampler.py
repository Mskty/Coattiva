from Classificatore_Shell.funzioni import *

def data_undersample(df: DataFrame):
    """
    Effettua undersampling randomico sul dataset passato
    :param df: dataframe corrispondente al training set
    :return: Il dataset passato alla funzione con ugual presenza di esempi con label 1 e label 0 ottenuto mantenendo tutti quelli con label 1
             e scegliendo casualmente tra tutti gli esempi con label 0 un numero uguale a quelli con label 1
    """
    # copia su cui effettuare l'undersampling
    df = df.copy()
    # Undersampling randomico 50-50 label 1 e label 0
    one_indices = df[df.label == 1].index
    sample_size = sum(df.label == 1)  # Equivalent to len(data[data.Healthy == 0]), numero di titoli con label 1 3394
    zero_indices = df[df.label == 0].index
    random_indices = np.random.choice(zero_indices, sample_size, replace=False)
    # Unisco gli 1 e 0
    under_indices = one_indices.union(random_indices)
    undersampletrain = df.loc[under_indices]  # nuovo training set con 50/50 di classe 1 e 0
    return undersampletrain