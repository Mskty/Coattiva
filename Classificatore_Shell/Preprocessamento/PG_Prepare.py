from Classificatore_Shell.funzioni import *


def prepare_pg(dfPG: pd.DataFrame):
    """
        Effettua diverse operazioni di preparazione sui dati puliti per estrarre ulteriori informazioni da utilizzare nella classificazione
        :param dfPG: dataframe di titoli aggregati riferiti a Persone Giuridiche con tracciato di colonne identico ai dati storici aggregati e puliti
        :return: dataframe contenente i dati preparati
        """
    # Copio il dataset per poi ritornarlo
    dfPF = dfPG.copy()

    # Colonna nuovo cliente
    # Strategia: viene aggiunta l'informazione, per ogni credito, se il contribuente corrispondente era nuovo al momento
    # della presa in carico del titolo oppure no, questa informazione può essere estratta controllando che, per il credito,
    # il valore dei campi NumeroTitoliAperti e NumeroTitoliSaldati sia esattamente zero.
    dfPF["NuovoContribuente"] = (dfPF["NumeroTitoliSaldati"] == 0) & (dfPF["NumeroTitoliAperti"] == 0)
    dfPF["NuovoContribuente"] = dfPF["NuovoContribuente"].astype("int64")

    # Recupero cap da indirizzo con espressione regolare
    dfPF["Cap"] = dfPF["IndirizzoResidenza"].str.findall(r'(\d{5})').str[-1]  # estrazione cap da indirizzo

    # Recupero la provincia dall'indirizzo con espressione regolare
    dfPF["Provincia"] = dfPF["IndirizzoResidenza"].str.split().str[-1]  # Errato quando c'è una stringa che finisce come ' X TV', prende ' X ' ma non TV

    # I crediti con nuovo_cap==0 o provincia=='EE' sono esteri, creo una nuova colonna per indicarlo
    # E fillo i cap nulli (tutti esteri) con il valore 0
    dfPF["Estero"] = 0
    dfPF.loc[(dfPF.Cap == '00000') | (dfPF.Provincia == 'EE'), "Estero"] = 1
    # Imposto il cap di tutti gli esteri a 00000
    dfPF.loc[(dfPF.Estero == 1), "Cap"] = '00000'
    # Imposto le rimanenti anomalie con cap nullo (indirizzo malformato) anche esse a '00000'
    dfPF[["Cap"]] = dfPF[["Cap"]].fillna('00000')
    # Imposto Cap come campo numerico intero in modo da poter essere utilizzato per l'elaborazione
    dfPF["Cap"] = dfPF["Cap"].astype("int64")

    # Nuova colonna: ImportoTitoliAperti/importoTitoliSaldati, vale 0 per i nuovi contribuenti
    # L'idea è che il valore del rapporto sia più alto per i contribuenti peggiori, se >1 allora ha più aperto che saldato
    dfPF["RapportoImporto"] = 0
    dfPF.loc[(dfPF.NuovoContribuente != 1), "RapportoImporto"] = dfPF.loc[(dfPF.NuovoContribuente != 1)].ImportoTitoliAperti / dfPF.loc[(dfPF.NuovoContribuente != 1)].ImportoTitoliSaldati
    inf = np.inf
    dfPF.loc[(dfPF.RapportoImporto == inf), "RapportoImporto"] = -1
    # Imposto tutti i contribuenti con rapporto infinito, ovvero ci sono titoli aperti e nessuno saldato ad un valore molto elevato
    max_rapporto = 1000
    dfPF.loc[(dfPF.RapportoImporto == -1), "RapportoImporto"] = max_rapporto

    # Importo Dovuto rispetto ad ancora da pagare dei titoli aperti dove presenti, varia da 0 a 1, dove è più basso è migliore (significa che ha già pagato tutto)
    # Nella gran parte dei casi sarà 1 (ovverto il contribuente deve ancora pagare tutto il dovuto)
    dfPF["RapportoDovutoAperti"] = 0
    dfPF.loc[(dfPF.NumeroTitoliAperti != 0), "RapportoDovutoAperti"] = dfPF.loc[(dfPF.NumeroTitoliAperti != 0)].ImportoTitoliAperti / dfPF.loc[(dfPF.NumeroTitoliAperti != 0)].DovutoTitoliAperti

    # Droppo le colonne che non verranno utilizzate nell'addestramento del modello
    # (eccetto DataCaricoTitolo che verrà utilizzato per definire training set e test set)
    dfPF.drop(columns=["IndirizzoResidenza", "Provincia"], inplace=True)

    # Ritorno il dataset preparato
    return dfPF
