from utility.Imports import *
from utility.Enums import *


class StoricPreprocesser:
    """
    Classe che espone metodi per effettuare preoprocessamento su dati riferiti a titoli storici precedentemente puliti
    ed aggregati salvati poi su un oggetto di tipo Dataframe pandas.
    Lo scopo di tali operazioni è diestrarre ulteriori informazioni dai dati puliti da utilizzare nella classificazione.
    Espone metodi per trattare le diverse fasi del preprocessamento per tali dati,
    per effettuare l'intera operazione di preprocesamento in ordine è necessario invocare il metodo self.prepare().
    che ritornerà al chiamante il Dataframe contentente i dati preparati.
    PARAMETRI:
    self.__df: oggetto di tipo pandas.Dataframe conentene i dati puliti ed aggregati da processare
    self.__type: Valore di tipo PFPGEnum rappresentante il tipo di dati contenuti in self.__df
    """

    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self, type: PFPGEnum, df: pd.DataFrame):
        self.__df = df.copy()
        self.__type = type

    def NuovoContribuente(self, df: pd.DataFrame):
        # Colonna NuovoContribuente Strategia: viene aggiunta l'informazione, per ogni credito, se il contribuente
        # corrispondente era nuovo al momento della presa in carico del titolo oppure no, questa informazione può
        # essere estratta controllando che, per il credito, il valore dei campi NumeroTitoliAperti e
        # NumeroTitoliSaldati sia esattamente zero.
        df["NuovoContribuente"] = (df["NumeroTitoliSaldati"] == 0) & (df["NumeroTitoliAperti"] == 0)
        df["NuovoContribuente"] = df["NuovoContribuente"].astype("int64")

        return df

    def locationData(self, df: pd.DataFrame):
        # Recupero cap da indirizzo con espressione regolare
        df["Cap"] = df["IndirizzoResidenza"].str.findall(r'(\d{5})').str[-1]  # estrazione cap da indirizzo

        # Recupero la provincia dall'indirizzo con espressione regolare
        df["Provincia"] = df["IndirizzoResidenza"].str.split().str[-1]

        # I crediti con nuovo_cap==0 o provincia=='EE' sono esteri, creo una nuova colonna per indicarlo
        # E fillo i cap nulli (tutti esteri) con il valore 0
        df["Estero"] = 0
        df.loc[(df.Cap == '00000') | (df.Provincia == 'EE'), "Estero"] = 1
        # Imposto il cap di tutti gli esteri a 00000
        df.loc[(df.Estero == 1), "Cap"] = '00000'
        # Imposto le rimanenti anomalie con cap nullo (indirizzo malformato) anche esse a '00000'
        df[["Cap"]] = df[["Cap"]].fillna('00000')
        # Imposto Cap come campo numerico intero in modo da poter essere utilizzato per l'elaborazione
        df["Cap"] = df["Cap"].astype("int64")

        # Droppo le colonne riportanti informazioni testuali che non verranno utilizzate nell'addestramento del modello
        # (eccetto DataCaricoTitolo che verrà utilizzato per definire training set e test set)
        df.drop(columns=["IndirizzoResidenza", "Provincia"], inplace=True)

        return df

    def RapportoImporto(self, df: pd.DataFrame):
        # Nuova colonna: ImportoTitoliAperti/importoTitoliSaldati, vale 0 per i nuovi contribuenti. L'idea è che il
        # valore del rapporto sia più alto per i contribuenti peggiori, se >1 allora ha più aperto che saldato
        df["RapportoImporto"] = 0
        df.loc[(df.NuovoContribuente != 1), "RapportoImporto"] = df.loc[(
                df.NuovoContribuente != 1)].ImportoTitoliAperti / df.loc[(
                df.NuovoContribuente != 1)].ImportoTitoliSaldati
        inf = np.inf
        df.loc[(df.RapportoImporto == inf), "RapportoImporto"] = -1

        # Imposto tutti i contribuenti con rapporto infinito, ovvero ci sono titoli aperti e nessuno saldato ad un
        # valore molto elevato
        max_rapporto = 1000
        df.loc[(df.RapportoImporto == -1), "RapportoImporto"] = max_rapporto

        return df

    def RapportoDovutoAperti(self, df: pd.DataFrame):
        # Importo Dovuto rispetto ad ancora da pagare dei titoli aperti dove presenti, varia da 0 a 1, dove è più
        # basso è migliore (significa che ha già pagato tutto)
        # Nella gran parte dei casi sarà 1 (ovvero il contribuente deve ancora pagare tutto il dovuto)
        df["RapportoDovutoAperti"] = 0
        df.loc[(df.NumeroTitoliAperti != 0), "RapportoDovutoAperti"] = df.loc[(
                df.NumeroTitoliAperti != 0)].ImportoTitoliAperti / df.loc[(
                df.NumeroTitoliAperti != 0)].DovutoTitoliAperti

        return df

    def prepare(self):
        # Pipeline per la preparazione dei dati storici puliti all'utilizzo per l'addestramento di un modello preditivo
        if self.__type == PFPGEnum.PF:
            self.__df = self.NuovoContribuente(self.__df)
            self.__df = self.locationData(self.__df)
            self.__df = self.RapportoImporto(self.__df)
            self.__df = self.RapportoDovutoAperti(self.__df)
        elif self.__type == PFPGEnum.PG:
            self.__df = self.NuovoContribuente(self.__df)
            self.__df = self.locationData(self.__df)
            self.__df = self.RapportoImporto(self.__df)
            self.__df = self.RapportoDovutoAperti(self.__df)

        return self.__df