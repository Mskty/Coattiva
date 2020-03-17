from utility.funzioni import *
from utility.Enums import *


class StoricCleaner:
    """
    Classe che espone metodi per effettuare la pulizia ed aggregazione di dati riferiti a titoli storici
    forniti da un utente a partire da file che rispetti il rispettivo tracciato e salvati poi su un oggetto
    di tipo Dataframe pandas.
    Lo scopo di tali operazioni è eliminare gli errori rilevati all'interno del file (prodotto da un estrazione da
    database). ciò viene fatto controllando
    la validità di diverse informazioni recuperate dall'estrazione riferite all'effettivo periodo in cui i titoli
    di credito erano attuali (ad esempio viene calcolata l'età corretta alla data di carico). Inoltre aggrega
    i titoli, risolvendo le problematiche di conflitti in dati anagrafici dati dalla duplicazione delle anagrafiche
    per stessi contribuenti nel database da cui sono stati estratti i dati. L'aggregazione dei titoli
    viene effettuata creano un unico titoli di credito da molti, nel caso dovessero esserci, con gli stessi valori nei campi
    idAnagrafica-DataCaricoTitolo-DataPrimaNotifica.
    Espone metodi per trattare le diverse fasi della pulizia per i dati storici, sia per persone fisiche che giuridiche,
    per effettuare l'intera operazione di pulzia in corretto ordine è necessario invocare il metodo self.clean(), che
    ritornerà al chiamante il Dataframe contenente i dati puliti ed aggregati.
    PARAMETRI:
    self.__df: oggetto di tipo pandas.Dataframe conentene i dati recenti da processare
    self.__type: Valore di tipo PFPGEnum rappresentante il tipo di dati contenuti in self.__df che dovranno essere
                 considerati per le operazioni di pulizia ed aggregazione
    """
    """
    @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
        di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
        e l'invocazione di __init__
    """

    def __init__(self, type: PFPGEnum, df: pd.DataFrame):
        self.__type = type
        # Mantengo solo i titoli riferiti al tipo di personalità passato
        if self.__type == PFPGEnum.PF:
            self.__df = df[df.TipoPersonalità == "PF"].copy()
        elif self.__type == PFPGEnum.PG:
            self.__df = df[df.TipoPersonalità == "PG"].copy()

    """----------------------------------------------Persone Fisiche-----------------------------------------------"""

    def pf_setUp(self, df: pd.DataFrame):
        # Droppo le colonne Cessata e CessataDataInfo che non riguardano le Persone Fisiche in questo dataset
        df.drop(columns=["Cessata", "CessataDataInfo"], inplace=True)

        # droppo la colonna AnnoNascita se presente per errore perchè inutile, utilizzo DataNascita
        if 'AnnoNascita' in df.columns:
            df.drop(columns="AnnoNascita", inplace=True)

        # droppo la colonna 'IDTitoloCredito se presente per errore perchè inutile
        if 'IDTitoloCredito' in df.columns:
            df.drop(columns="IDTitoloCredito", inplace=True)

        # imposto i valori nulli di DecedutoDataInfo ad 'assente'
        df[["DecedutoDataInfo"]] = df[["DecedutoDataInfo"]].fillna("assente")

        # Elimino i titoli con indirizzoresidenza sconosciuto
        df = df[~(df['IndirizzoResidenza'] == "SCONOSCIUTO ALL'ANAGRAFE SCONOSCIUTO ALL'ANAGRAFE")]

        # Imposto i valori mancanti nella colonna Cap a 0
        df[["Cap"]] = df[["Cap"]].fillna(0)

        # Imposto i valori di TipoCredito a 1 in quanto il campo verà utilizzato solo per l'aggregazione
        df[["TipoCredito"]] = 1
        df[["TipoCredito"]] = df[["TipoCredito"]].astype('int64')

        return df

    def DataPrimaNotificaNulla(self, df: pd.DataFrame):
        # STRATEGIA: Imposto I valori nulli di DataPrimaNotifica e DataPagamentoTotale ad 'assente'. Successivamente,
        # dove il valore di DataPrimaNotifica risulta 'assente', imposto il suo valore uguale a datacaricotitolo.
        # Successivamente controllo che DataPagamentoTotale, dove presente nei casi in cui ho impostato
        # datanotifica=datacarico, sia ad una distanza di giorni massima da datacarico/datanotifica di 120 giorni.
        # per i titoli in cui questa condizione è soddisfatta imposto pagato120giorni=valoretitolo
        df[["DataPrimaNotifica"]] = df[["DataPrimaNotifica"]].fillna("assente")
        df[["DataPagamentoTotale"]] = df[["DataPagamentoTotale"]].fillna("assente")

        # Imposto dove il valore risulta assente, DataPrimaNotifica a DataCaricoTitolo
        df.loc[(df.DataPrimaNotifica == 'assente'), 'DataPrimaNotifica'] = df.query(
            "DataPrimaNotifica=='assente'").DataCaricoTitolo

        # Creo nuova colonna per giorni differenza
        df["DifferenzaPagamento"] = 0

        # Dove il titolo risulta essere stato pagato completamente in futuro calcolo la differenza in giorni tra
        # DataPagamentoTotale e DataCaricoTitolo (diventata uguale a notifica nei casi selezionati ovviamente)
        differencecolumn = (pd.to_datetime(
            df.query("DataPagamentoTotale != 'assente' & DataCaricoTitolo==DataPrimaNotifica").DataPagamentoTotale) -
                            pd.to_datetime(df.query(
                                "DataPagamentoTotale != 'assente' & DataCaricoTitolo==DataPrimaNotifica").DataCaricoTitolo)).dt.days

        # Imposto la differenza calcolata nella colonna DifferenzaPagamento
        df.loc[((df.DataPagamentoTotale != 'assente') & (
                df.DataCaricoTitolo == df.DataPrimaNotifica)), 'DifferenzaPagamento'] = differencecolumn

        # Se la DifferenzaPagamento calcolata nei casi trattati è inferiore o uguale a 120 giorni imposto il campo
        # Pagato120Giorni all'intero valore del titolo, in quanto è stato risarcito interamnete a 120 giorni dalla
        # data di carico del titolo e dunque sicuramente anche a 120 giorni dalla data di notifica sconosciuta,
        # in quanto DataPrimaNotifica è sempre più recente di DataCaricoTitolo
        df.loc[((df.DifferenzaPagamento != 0) & (df.DifferenzaPagamento <= 120)), "Pagato120Giorni"] = \
            df.loc[((df.DifferenzaPagamento != 0) & (df.DifferenzaPagamento <= 120)), "ValoreTitolo"]

        # Ho impostato il dovuto pagato a 120 giorni al valore del titolo, Droppo la colonna temporanea utilizzata
        # per effettuare il calcolo:
        df.drop(columns="DifferenzaPagamento", inplace=True)

        return df

    def pf_AnagraficheDuplicate(self, df: pd.DataFrame):
        # GESTIONE DEI CASI IN CUI, PER ANAGRAFICHE DUPLICATE NEL DATABASE, UN UNICO DOCUMENTO DI CREDITO (OVVERO
        # FORMATO DA TITOLI CHE HANNO STESSO VALORE DI idAnagrafica, DataCaricoTitolo e DataPrimaNotifica) PRESENTI
        # DIFFERENTI VALORI NEI CAMPI Telefono, Deceduto, IndirizzoResidenza o Cap a causa di ANAGRAFICHE DUPLICATE
        # per lo stesso contribuente

        # Gestione campo Deceduto
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "Deceduto"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "Deceduto", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        decedutodiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo Telefono
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "Telefono"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "Telefono", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        telefonodiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo IndirizzoResidenza
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "IndirizzoResidenza"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "IndirizzoResidenza",
                                 "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        indirizzodiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo Cap
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "Cap"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "Cap", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        capdiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Lista con tutte le anagrafiche che presentano almeno un anomalie fra tutti i campi considerati
        anagraficadifferente = ((set(telefonodiverso).union(set(indirizzodiverso))).union(set(decedutodiverso))).union(
            set(capdiverso))

        # Raggruppando per credito (idAnagrafica, DataCaricoTitolo, DataPrimaNotifica) rendo omogenei i campi Cap,
        # IndirizzoResidenza e Telefono (il campo Deceduto verrà trattato successivamente), ovvero per ogni
        # raggruppamento dovrà esserci un valore unico per tutti i titoli che lo compongono
        grouploc = df.loc[(df.idAnagrafica.isin(anagraficadifferente))].groupby(
            ["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica"])

        # IndirizzoResidenza: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'IndirizzoResidenza')] = grouploc[
            "IndirizzoResidenza"].transform(lambda x: x.mode()[0])

        # Cap: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito) sarà comunque
        # da risistemare in una fase successiva perchè la moda quì scelta per il cap può essere riferito
        # all'indirizzo non scelto come moda precedentemente se i titoli dei 2 indirizzi nel gruppo erano nella
        # stessa quantità)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'Cap')] = grouploc["Cap"].transform(
            lambda x: x.mode()[0])

        # Telefono: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'Telefono')] = grouploc["Telefono"].transform(
            lambda x: x.mode()[0])

        # ORA TELEFONO-INDIRIZZO-CAP SONO OMOGENEI, DOPO AVER PROCEDUTO CON L'OMOGENIZZAZIONE DI DECEDUTO SI POTRANNO
        # AGGREGARE I CREDITI NEL CREDITO CHE LI INCLUDE

        return df

    def pf_DataDeceduto(self, df: pd.DataFrame):
        # GESTIONE DATE DI DECESSO, Campo Età e Deceduto al tempo del carico del titolo vanno cacolati
        # successivamente. Inizialmente imposto il campo deceduto a 1 su tutti i titoli appartenenti ad un anagrafica
        # di una persona deceduta Metto lo stesso valore di data di decesso su tutte le righe appartenenti alla
        # stessa anagrafica Gruppo per id, se un valore datadecesso diverso da "assente" è presente, lo assegno a
        # tutte le altre righe del gruppo Strategia: trasformo ogni data in numero intero, data più recente sarà un
        # numero pià grande. le date NaN saranno sostituite da un numero molto grande a simboleggiare l'infinito.
        # Dopo gruppo per idAnagrafica e imposto tutte le date al minimo con ['DataDeceduto'].transform(min) in
        # quanto la data meno recente corrisponde alla prima registrazione certa di decesso del contribuente. Una
        # volta impostato su tutti i titoli la data meno recente, ritrasformo il tipo intero in data.

        df["Deceduto"] = df.groupby(['idAnagrafica'])['Deceduto'].transform(max)

        # Avevo precedentemente sostituito i NaN con 'assente' in quanto il NaN di excel non è ricercabile tramite
        # query su Pandas Ora però devo sostituire tale valore con NaN nuovamente
        df["DataDeceduto"] = df.DecedutoDataInfo.replace('assente', np.NaN)
        # Numero token per infinito: 9999-99-99 con cui sostituire i NaN
        df[['DataDeceduto']] = df[['DataDeceduto']].fillna(value='9999-99-99')
        df['DataDeceduto'] = df['DataDeceduto'].astype(str)
        df['DataDeceduto'] = df['DataDeceduto'].str.replace('\D', '').astype(int)

        # Ora posso raggruppare e trovare la data di decesso meno recente per ogni idAnagrafico che risulta deceduto
        df['DataDeceduto'] = df.groupby(['idAnagrafica'])['DataDeceduto'].transform(
            min)  # Ora test non contiene più id
        df['DataDeceduto'] = pd.to_datetime(df['DataDeceduto'].astype(str), format='%Y%m%d',
                                            errors='coerce').dt.date

        # Ora DataDeceduto contiene le date di decesso corrette per le anagrafiche decedute, nel'caso l'anagrafica
        # non sia deceduta il valore assunto sara NaT. Rimangono alcuni casi in cui il contribuente risulta deceduto
        # ma non c'era nessuna registrazione della data di decesso in nessun titolo, questi casi verranno gestiti al
        # momento del calcolo del decesso.

        # E' possibile droppare la colonna DecedutoDataInfo in quanto la nuova colonna la sostituisce correttamente
        df.drop(columns="DecedutoDataInfo", inplace=True)

        # Metto ad 'assente' i NaT corrispondendi a non deceduti o in cui è assente completamnete la data di decesso
        df[["DataDeceduto"]] = df[["DataDeceduto"]].fillna('assente')

        # Imposto la data decesso per i deceduti senza mai data a 2000-01-01, considerandoli quindi deceduti da sempre
        df.loc[(df.Deceduto == 1) & (df.DataDeceduto == 'assente'), 'DataDeceduto'] = datetime.date(2000, 1, 1)

        return df

    def Vetusta(self, df: pd.DataFrame):
        # CALCOLO VETUSTA' TITOLO Strategia: sottrazione tra valore in DataCaricoTitolo e valore in
        # DataEmissioneTitolo Bisogna ignorare i titoli di tipo "oneri di esazione" che non hanno tale data Questi
        # saranno sostituiti in una fase successiva con la mediana di vetustà sul dataset se non sono stati aggregati

        df["Vetusta"] = -1
        df.loc[(df.TipoCredito != 'oneri di esazione'), "Vetusta"] = (
                pd.to_datetime(df.query("TipoCredito!='oneri di esazione'")['DataCaricoTitolo'])
                - pd.to_datetime(df.query("TipoCredito!='oneri di esazione'")['DataEmissioneTitolo'])).dt.days

        # Inserisco la mediana della vetustà come vetustà dei titoli che la hanno nulla
        df["Vetusta"] = df.Vetusta.replace(-1, np.NaN)
        df[["Vetusta"]] = df[["Vetusta"]].fillna(df["Vetusta"].median())

        # Setto colonna come intero invece che float
        df.Vetusta = df.Vetusta.astype('int64')

        return df

    def pf_Eta(self, df: pd.DataFrame):
        # CALCOLO ETA' CONTRIBUENTE NELLA COLONNA ETA
        # Strategia: sottrazione tra valore in DataCaricoTitolo e valore in DataNascita

        df["Eta"] = pd.to_datetime(df['DataCaricoTitolo']).dt.year - pd.to_datetime(df['DataNascita']).dt.year

        # Ora la colonna Eta contiene le età dei titoli associati ai contribuenti del titolo

        return df

    def pf_Deceduto(self, df: pd.DataFrame):
        # CALCOLO IL VALORE CORRETTO DI DECEDUTO NELLA COLONNA CESSATA (AL TEMPO DELLA DATA CARICO DEL TITOLO)
        # Strategia: ottengo giorni di differenza per sottrazione tra valore in DataCaricoTitolo e valore in
        # DataPrimaNotifica, perchè è possibile si sia venuti a conoscenza del decesso durante l'analisi del
        # contribuente, ma esso era comunque deceduto all'arrivo del ruolo (DataCaricoTitolo)

        df["DifferenzaDeceduto"] = -9999  # inizializzo a alto negativo che indica che sicuramente non è deceduto

        # In questo momento tutti i possibili deceduti hanno campo Deceduto con valore 1,
        # filtro tramite quel valore e calcolo la differenza:
        df.loc[(df.Deceduto == 1), 'DifferenzaDeceduto'] = (
                pd.to_datetime(df.query("Deceduto==1").DataPrimaNotifica)
                - pd.to_datetime(df.query("Deceduto==1").DataDeceduto)).dt.days

        # Ora dove la differenza è >=0 metto Deceduto a 1 altrimenti 0 (non deceduto al momento della notifica):
        df.loc[(df.DifferenzaDeceduto.astype(int) >= 0), "Deceduto"] = 1  # per chiarezza ma inutile
        df.loc[(df.DifferenzaDeceduto.astype(int) < 0), "Deceduto"] = 0

        # Realmente deceduti di cui si era conoscenza alla data di notifica del titolo:
        df.drop(columns="DifferenzaDeceduto", inplace=True)

        # ORA I DATI DEI TITOLI APPARTENENTI A PERSONE FISICHE SONO PRONTI PER L'AGGREGAZIONE IN CREDITI

        return df

    def pf_cleanUselessColumns(self, df: pd.DataFrame):
        # DROPPO LE COLONNE CHE NON VERRANNO PIU' UTILIZZATE PERCHE' NON RILEVANTI AI FINI DELLA CLASSIFICAZIONE:
        df.drop(
            columns=["DataNascita", "TipoPersonalità", "PEC", "DataEmissioneTitolo",
                     "DataPagamentoTotale", "DataDeceduto"],
            inplace=True)

        return df

    def pf_aggregateTitles(self, df: pd.DataFrame):
        # AGGREGAZIONE DEI TITOLI APPARTENENTI ALLO STESSO DOCUMENTO DI CREDITO (
        # =IDANAGRAFICA-DATACREDITO-DATAPRIMANOTIFICA)

        # Strategia: raggruppo i titoli per idAnagrafica, DataCaricoTitolo e DataPrimaNotifica,
        # e aggrego le colonne secondo i parametri scelti (ad esempio "sum" per ValoreTitolo e Pagato120Giorni)

        # Sistemo le colonne NumeroTitoliRecenti e TotaleTitoliRecenti, in modo che contengano il conteggio e la
        # somma dei titoli per lo stesso idAnagrafica alla stessa data di carico del titolo (Ruolo):
        df["NumeroTitoliRecenti"] += 1
        df["TotaleTitoliRecenti"] += df["ValoreTitolo"]

        # Rinomino il campo TipoCredito a TitoliCredito in quanto più esplicativo del significato in aggregazione
        df["TitoliCredito"] = df["TipoCredito"]
        df.drop(columns="TipoCredito", inplace=True)

        # Parametri di aggregazione: Dove come metodo di aggregazione è specificato 'max' in realtà si mantiene
        # l'unico valore di quella colonna presente nel gruppo, in quanto sono stati tutti resi uguali nella fase di
        # pulizia precedente. Vetustà è determinata dal minimo: titolo più vecchio del gruppo, i campi corrispondenti
        # al tipo del titolo vengono sommati per indicare quanti e per che tipo di titoli erano presenti all'interno
        # dello stesso documento di credito.
        aggprm = {'Telefono': 'max', 'IndirizzoResidenza': 'max', 'Cap': 'max', 'CittadinanzaItaliana': 'max',
                  'Deceduto': 'max',
                  'ValoreTitolo': 'sum', 'Pagato120Giorni': 'sum', 'NumeroTitoliAperti': 'max',
                  'DovutoTitoliAperti': 'max', 'ImportoTitoliAperti': 'max',
                  'NumeroTitoliSaldati': 'max', 'ImportoTitoliSaldati': 'max', 'NumeroTitoliRecenti': 'max',
                  'TotaleTitoliRecenti': 'max', 'Eta': 'max', 'Vetusta': 'max', 'TitoliCredito': 'sum'}

        # Procedo con l'aggregazione dei titoli appartenenti allo stesso documento/credito:
        df = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica"]).agg(aggprm)

        # Resetto gli index del raggruppamento, in modo da continuare a vedere idAnagrafica, DataCaricoTitolo e
        # DataPrimaNotifica come colonne e campi dei crediti:
        df = df.reset_index()

        return df

    def label(self, df: pd.DataFrame):
        # Calcolo la label di classe per ogni credito secondo le specifiche
        label = df['Pagato120Giorni'] / df["ValoreTitolo"] >= 0.20
        df.insert(0, "label", label)
        """df['label'] = df['Pagato120Giorni'] / df["ValoreTitolo"] >= 0.20
        df['label'] = df['label'].astype("int64")"""

        # Droppo le colonne che non verranno più utilizzate
        df.drop(columns=["idAnagrafica", "DataPrimaNotifica", "Pagato120Giorni"], inplace=True)

        # Elimino il cap dato che serviva per la pulizia ma verrà ricalcolato dall'indirizzo nelle fasi successive
        df.drop(columns="Cap", inplace=True)

        return df

    """----------------------------------------------Persone Giuridiche---------------------------------------------"""

    def pg_setUp(self, df: pd.DataFrame):
        # Droppo le colonne Deceduto, DecedutoDataInfo, AnnoNascita, DataNascita, CittadinanzaItaliana che non
        # riguardano le Persone Fisiche in questo dataset
        df.drop(columns=["Deceduto", "DecedutoDataInfo", "DataNascita", "CittadinanzaItaliana"],
                inplace=True)

        # droppo la colonna AnnoNascita se presente per errore perchè inutile
        if 'AnnoNascita' in df.columns:
            df.drop(columns="AnnoNascita", inplace=True)

        # droppo la colonna 'IDTitoloCredito se presente per errore perchè inutile
        if 'IDTitoloCredito' in df.columns:
            df.drop(columns="IDTitoloCredito", inplace=True)

        # imposto i valori nulli di DecedutoDataInfo ad 'assente'
        df[["CessataDataInfo"]] = df[["CessataDataInfo"]].fillna("assente")

        # Elimino i titoli con indirizzoresidenza sconosciuto
        df = df[~(df['IndirizzoResidenza'] == "SCONOSCIUTO ALL'ANAGRAFE SCONOSCIUTO ALL'ANAGRAFE")]

        # Imposto i valori mancanti nella colonna Cap a 0
        df[["Cap"]] = df[["Cap"]].fillna(0)

        # Imposto i valori di TipoCredito a 1 in quanto il campo verà utilizzato solo per l'aggregazione
        df[["TipoCredito"]] = 1
        df[["TipoCredito"]] = df[["TipoCredito"]].astype('int64')

        return df

    def pg_AnagraficheDuplicate(self, df: pd.DataFrame):
        # GESTIONE DEI CASI IN CUI, PER ANAGRAFICHE DUPLICATE NEL DATABASE, UN UNICO DOCUMENTO DI CREDITO (OVVERO
        # FORMATO DA TITOLI CHE HANNO STESSO VALORE DI idAnagrafica, DataCaricoTitolo e DataPrimaNotifica) PRESENTI
        # DIFFERENTI VALORI NEI CAMPI Telefono, Deceduto, IndirizzoResidenza o Cap a causa di ANAGRAFICHE DUPLICATE
        # per lo stesso contribuente

        # Gestione campo Cessata
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "Cessata"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "Cessata", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        cessatadiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo Telefono
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "Telefono"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "Telefono", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        telefonodiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo IndirizzoResidenza
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "IndirizzoResidenza"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "IndirizzoResidenza",
                                 "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        indirizzodiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo Cap
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "Cap"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "Cap", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        capdiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Gestione campo PEC
        grouped = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica", "PEC"])
        grouptitlesc = grouped.agg(['count'])
        groupcumcount = grouptitlesc.groupby(level=[0, 1, 2]).cumcount().to_frame()
        groupcumcount = groupcumcount.reset_index()
        groupcumcount.columns = ["idAnagrafica", "DataCaricoTitolo", "Dataprimanotifica", "PEC", "cumcount"]
        groupquery = groupcumcount.query("cumcount==1")
        PECdiverso = np.unique(groupquery["idAnagrafica"]).tolist()

        # Lista con tutte le anagrafiche che presentano almeno un anomalie fra tutti i campi considerati
        anagraficadifferente = (((set(telefonodiverso).union(set(indirizzodiverso))).union(set(cessatadiverso))).union(
            set(capdiverso))).union(set(PECdiverso))

        # Raggruppando per credito (idAnagrafica, DataCaricoTitolo, DataPrimaNotifica) rendo omogenei i campi Cap,
        # IndirizzoResidenza Telefono e PEC (il campo Cessata verrà trattato successivamente), ovvero per ogni
        # raggruppamento dovrà esserci un valore unico per tutti i titoli che lo compongono
        grouploc = df.loc[(df.idAnagrafica.isin(anagraficadifferente))].groupby(
            ["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica"])

        # IndirizzoResidenza: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'IndirizzoResidenza')] = grouploc[
            "IndirizzoResidenza"].transform(lambda x: x.mode()[0])

        # Cap: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito) sarà comunque
        # da risistemare in una fase successiva perchè la moda quì scelta per il cap può essere riferito
        # all'indirizzo non scelto come moda precedentemente se i titoli dei 2 indirizzi nel gruppo erano nella
        # stessa quantità)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'Cap')] = grouploc["Cap"].transform(
            lambda x: x.mode()[0])

        # Telefono: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'Telefono')] = grouploc["Telefono"].transform(
            lambda x: x.mode()[0])

        # PEC: scelgo il valore di MODA tra quelli assunti dai titoli appartenenti al gruppo (credito)
        df.loc[(df.idAnagrafica.isin(anagraficadifferente), 'PEC')] = grouploc["PEC"].transform(
            lambda x: x.mode()[0])

        # ORA TELEFONO-INDIRIZZO-CAP-PEC SONO OMOGENEI, DOPO AVER PROCEDUTO CON L'OMOGENIZZAZIONE DI CESSATA SI
        # POTRANNO AGGREGARE I CREDITI NEL CREDITO CHE LI INCLUDE

        return df

    def pg_DataCessata(self, df: pd.DataFrame):
        # GESTIONE DATE DI CESSAZIONE UTENZA, Deceduto al tempo del carico del titolo verà cacolato successivamente.
        # Inizialmente imposto il campo cessata a 1 su tutti i titoli appartenenti ad un anagrafica di una persona
        # deceduta Metto lo stesso valore di data di cessazione su tutte le righe appartenenti alla stessa anagrafica
        # Gruppo per id, se un valore datacessata diverso da "assente" è presente, lo assegno a tutte le altre righe
        # del gruppo Strategia: trasformo ogni data in numero intero, data più recente sarà un numero più grande. le
        # date NaN saranno sostituite da un numero molto grande a simboleggiare l'infinito. Dopo gruppo per
        # idAnagrafica e imposto tutte le date al minimo con ['DataCessata'].transform(min) in quanto la data meno
        # recente corrisponde alla prima registrazione certa di cessata attovotà del contribuente. Una volta
        # impostato su tutti i titoli la data meno recente, ritrasformo il tipo intero in data.

        df["Cessata"] = df.groupby(['idAnagrafica'])['Cessata'].transform(max)

        # Avevo precedentemente sostituito i NaN con 'assente' in quanto il NaN di excel non è ricercabile tramite
        # query su Pandas Ora però devo sostituire tale valore con NaN nuovamente
        df["DataCessata"] = df.CessataDataInfo.replace('assente', np.NaN)

        # Numero token per infinito: 9999-99-99 con cui sostituire i NaN
        df[['DataCessata']] = df[['DataCessata']].fillna(value='9999-99-99')
        df['DataCessata'] = df['DataCessata'].astype(str)
        df['DataCessata'] = df['DataCessata'].str.replace('\D', '').astype(int)

        # Ora posso raggruppare e trovare la data di cessata attività meno recente per ogni idAnagrafico che risulta
        # deceduto
        df['DataCessata'] = df.groupby(['idAnagrafica'])['DataCessata'].transform(
            min)  # Ora test non contiene più id
        df['DataCessata'] = pd.to_datetime(df['DataCessata'].astype(str), format='%Y%m%d', errors='coerce').dt.date

        # Ora DataCessata contiene le date di cessata attività corrette per le anagrafiche con utenza cessata,
        # nel'caso l'anagrafica non sia cessata il valore assunto sara NaT. Rimangono alcuni casi in cui il
        # contribuente risulta con utenza cessata ma non c'era nessuna registrazione della data di cessazione in
        # nessun titolo, questi casi verranno gestiti al momento del calcolo della cessazione.

        # E' possibile droppare la colonna CessataDataInfo in quanto la nuova colonna la sostituisce correttamente
        df.drop(columns="CessataDataInfo", inplace=True)

        # Metto ad 'assente' i NaT corrispondendi a non cessate o in cui è assente completamnete la data di cessata
        # attività
        df[["DataCessata"]] = df[["DataCessata"]].fillna('assente')

        # Imposto la data cessazione per le utenze cessata senza mai data a 2000-01-01, considerandole quindi cessate
        # da sempre
        df.loc[(df.Cessata == 1) & (df.DataCessata == 'assente'), 'DataCessata'] = datetime.date(2000, 1, 1)
        # non ci sono casi come questo presenti nelle persone giuridiche

        return df

    def pg_Cessata(self, df: pd.DataFrame):
        # CALCOLO IL VALORE CORRETTO DI CESSATA ATTIVITA' NELLA COLONNA CESSATA (AL TEMPO DELLA DATA CARICO DEL
        # TITOLO) Strategia: ottengo giorni di differenza per sottrazione tra valore in DataCaricoTitolo e valore in
        # DataPrimaNotifica, perchè è possibile si sia venuti a conoscenza della cessazione durante l'analisi del
        # contribuente, ma esso aveva comunque cessato l'attività all'arrivo del ruolo (DataCaricoTitolo)

        df["DifferenzaCessata"] = -9999  # inizializzo a alto negativo che indica che sicuramente non è cessata
        # In questo momento tutte le possibili cessate hanno campo Cessata con valore 1,
        # filtro tramite quel valore e calcolo la differenza:
        df.loc[(df.Cessata == 1), 'DifferenzaCessata'] = (pd.to_datetime(df.query("Cessata==1").DataPrimaNotifica)
                                                          - pd.to_datetime(df.query("Cessata==1").DataCessata)).dt.days

        # Ora dove la differenza è >=0 metto Cessata a 1 altrimenti 0 (non Cessata al momento della notifica):
        df.loc[(df.DifferenzaCessata.astype(int) >= 0), "Cessata"] = 1  # per chiarezza ma inutile
        df.loc[(df.DifferenzaCessata.astype(int) < 0), "Cessata"] = 0

        # Realmente cessate di cui si era conoscenza alla data di notifica del titolo:
        df.drop(columns="DifferenzaCessata", inplace=True)

        # ORA I DATI DEI TITOLI APPARTENENTI A PERSONE GIURIDICHE SONO PRONTI PER L'AGGREGAZIONE IN CREDITI

        return df

    def pg_cleanUselessColumns(self, df: pd.DataFrame):
        # DROPPO LE COLONNE CHE NON VERRANNO PIU' UTILIZZATE PERCHE' NON RILEVANTI AI FINI DELLA CLASSIFICAZIONE:
        df.drop(
            columns=["TipoPersonalità", "DataEmissioneTitolo", "DataPagamentoTotale", "DataCessata"],
            inplace=True)

        return df

    def pg_aggregateTitles(self, df: pd.DataFrame):
        # AGGREGAZIONE DEI TITOLI APPARTENENTI ALLO STESSO DOCUMENTO DI CREDITO (
        # =IDANAGRAFICA-DATACREDITO-DATAPRIMANOTIFICA)

        # Strategia: raggruppo i titoli per idAnagrafica, DataCaricoTitolo e DataPrimaNotifica,
        # e aggrego le colonne secondo i parametri scelti (ad esempio "sum" per ValoreTitolo e Pagato120Giorni)

        # Sistemo le colonne NumeroTitoliRecenti e TotaleTitoliRecenti, in modo che contengano il conteggio e la
        # somma dei titoli per lo stesso idAnagrafica alla stessa data di carico del titolo (Ruolo):
        df["NumeroTitoliRecenti"] += 1
        df["TotaleTitoliRecenti"] += df["ValoreTitolo"]

        # Rinomino il campo TipoCredito a TitoliCredito in quanto più esplicativo del significato in aggregazione
        df["TitoliCredito"] = df["TipoCredito"]
        df.drop(columns="TipoCredito", inplace=True)

        # Parametri di aggregazione: Dove come metodo di aggregazione è specificato 'max' in realtà si mantiene
        # l'unico valore di quella colonna presente nel gruppo, in quanto sono stati tutti resi uguali nella fase di
        # pulizia precedente. Vetustà è determinata dal minimo: titolo più vecchio del gruppo, i campi corrispondenti
        # al tipo del titolo vengono sommati per indicare quanti e per che tipo di titoli erano presenti all'interno
        # dello stesso documento di credito.
        aggprm = {'Telefono': 'max', 'IndirizzoResidenza': 'max', 'Cap': 'max', 'Cessata': 'max', 'PEC': 'max',
                  'ValoreTitolo': 'sum', 'Pagato120Giorni': 'sum', 'NumeroTitoliAperti': 'max',
                  'DovutoTitoliAperti': 'max', 'ImportoTitoliAperti': 'max',
                  'NumeroTitoliSaldati': 'max', 'ImportoTitoliSaldati': 'max', 'NumeroTitoliRecenti': 'max',
                  'TotaleTitoliRecenti': 'max', 'Vetusta': 'max', 'TitoliCredito': 'sum'}

        # Procedo con l'aggregazione dei titoli appartenenti allo stesso documento/credito:
        df = df.groupby(["idAnagrafica", "DataCaricoTitolo", "DataPrimaNotifica"]).agg(aggprm)

        # Resetto gli index del raggruppamento, in modo da continuare a vedere idAnagrafica, DataCaricoTitolo e
        # DataPrimaNotifica come colonne e campi dei crediti:
        df = df.reset_index()

        return df

    def clean(self) -> pd.DataFrame:
        # Pipeline per la pulizia dei dati a seconda del parametro type inizializzato assieme all'oggetto
        if self.__type == PFPGEnum.PF:
            self.__df = self.pf_setUp(self.__df)
            self.__df = self.DataPrimaNotificaNulla(self.__df)
            self.__df = self.pf_AnagraficheDuplicate(self.__df)
            self.__df = self.pf_DataDeceduto(self.__df)
            self.__df = self.Vetusta(self.__df)
            self.__df = self.pf_Eta(self.__df)
            self.__df = self.pf_Deceduto(self.__df)
            self.__df = self.pf_cleanUselessColumns(self.__df)
            self.__df = self.pf_aggregateTitles(self.__df)
            self.__df = self.label(self.__df)
        elif self.__type == PFPGEnum.PG:
            self.__df = self.pg_setUp(self.__df)
            self.__df = self.DataPrimaNotificaNulla(self.__df)
            self.__df = self.pg_AnagraficheDuplicate(self.__df)
            self.__df = self.pg_DataCessata(self.__df)
            self.__df = self.Vetusta(self.__df)
            self.__df = self.pg_Cessata(self.__df)
            self.__df = self.pg_cleanUselessColumns(self.__df)
            self.__df = self.pg_aggregateTitles(self.__df)
            self.__df = self.label(self.__df)

        return self.__df
