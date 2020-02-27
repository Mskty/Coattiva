from utility.funzioni import *
from utility.Enums import *


class RecentPreprocesser:

    def __init__(self, type: PFPGEnum, df: pd.DataFrame):
        self.__type = type
        self.__df = df.copy()

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

        # DROPPO LE COLONNE CHE NON  VERRANNO PIU UTILIZZATE
        df.drop(columns=["IndirizzoResidenza", "Provincia"], inplace=True)
        # tolgo label se presetnte (non dovrebbe)
        if "label" in list(df.columns.values):
            df.drop(columns="label", inplace=True)
        # tolgo datacaricotitolo se presente (non dovrebbe)
        if "DataCaricoTitolo" in list(df.columns.values):
            df.drop(columns="DataCaricoTitolo", inplace=True)

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
