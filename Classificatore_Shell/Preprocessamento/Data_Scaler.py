from sklearn.preprocessing import StandardScaler, MinMaxScaler

from Classificatore_Shell.funzioni import *


def feature_scaling(trainset: pd.DataFrame, testset: pd.DataFrame, minmax=False, tipo="PF"):
    """
    Utilizza lo scaler desiderato per normalzzare i dati, ritorna training set e test set normalizzati e lo scaler addestrato per un utilizzo futuro
    :param trainset: Dataset contenete i dati su cui deve essere addestrato ed applicato lo scaler
    :param testset: Dataset contenente i dati su cui si dovrà applicare lo scaler dopo l'applicazione e addestramento col parametro trainset, può essere un dataframe vuoto
    :param minmax: Tipo dello scaler: Standard se minamax=False (Default) o MinMax se minmax=True
    :param tipo: "PF" per indicare che i dataset fanno riferimento a persone fisiche (default), "PG" altrimenti
    :return: 3 parametri di ritorno: trainset scalato, testset scalato e scaler pronto per l'utilizzo
    """
    # copia dei dataset passati
    trainset = trainset.copy()
    testset = testset.copy()
    scaled_testset = testset # nel caso il testset sia vuoto lo ritorno vuoto
    # Rimozione features categoriche da non scalare
    if tipo == "PF":
        # persone fisiche
        categorical_trainset = trainset[["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente", "label"]]
        trainset.drop(columns=["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente", "label"], inplace=True)
        if not testset.empty:
            categorical_testset = testset[["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente", "label"]]
            testset.drop(columns=["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente", "label"], inplace=True)
    elif tipo == "PG":
        # persone giuridiche
        categorical_trainset = trainset[["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente", "label"]]
        trainset.drop(columns=["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente", "label"], inplace=True)
        if not testset.empty:
            categorical_testset = testset[["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente", "label"]]
            testset.drop(columns=["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente", "label"], inplace=True)
    # Instanziazione scaler desiderato
    if minmax == False:
        # StandardScaler
        scaler = StandardScaler()
    else:
        # MinMaxScaler
        scaler = MinMaxScaler()
    scaler.fit(trainset.values)
    # Scaling di training e test sets
    scaled_features_trainset = scaler.transform(trainset.values)
    if not testset.empty:
        scaled_features_testset = scaler.transform(testset.values)
    # Ricostruzione training e test set con categoriche
    scaled_trainset = pd.DataFrame(scaled_features_trainset, index=trainset.index, columns=trainset.columns)
    scaled_trainset = pd.concat([scaled_trainset, categorical_trainset], axis=1, sort=False)
    if not testset.empty:
        scaled_testset = pd.DataFrame(scaled_features_testset, index=testset.index, columns=testset.columns)
        scaled_testset = pd.concat([scaled_testset, categorical_testset], axis=1, sort=False)

    # Ritorno i due dataset scalati e lo scaler
    return scaled_trainset, scaled_testset, scaler


def use_scaler(dataset: pd.DataFrame, scaler, tipo="PF"):
    """
    Utilizza lo scaler pre-addestrato sul training set del modello di classificazione per normalizzare i parametri di un dataset da classificare
    :param dataset: dataframe contenente i dati da scalare, deve avere la stessa identica composizione del train set utilizzato dallo scaler
    :param scaler: scaler ritornato dal metodo feature_scaling
    :param tipo: "PF" (default) o "PG"
    :return:
    """
    # copia dei dataset passati
    trainset = dataset.copy()

    if tipo == "PF":
        # persone fisiche
        categorical_dataset = dataset[["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente"]]
        dataset.drop(columns=["Telefono", "Deceduto", "CittadinanzaItaliana", "Estero", "NuovoContribuente"], inplace=True)
    elif tipo == "PG":
        # persone giuridiche
        categorical_dataset = dataset[["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente"]]
        dataset.drop(columns=["Telefono", "Cessata", "PEC", "Estero", "NuovoContribuente"], inplace=True)
    # Scaling del dataset
    scaled_features_dataset = scaler.transform(dataset.values)

    # Ricostruzione con categoriche
    scaled_dataset = pd.DataFrame(scaled_features_dataset, index=dataset.index, columns=dataset.columns)
    scaled_dataset = pd.concat([scaled_dataset, categorical_dataset], axis=1, sort=False)

    return scaled_dataset
