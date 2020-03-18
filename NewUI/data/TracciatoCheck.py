import pandas as pd
from utility.Enums import *


class TracciatoCheck:
    def __init__(self, typepfpg: PFPGEnum, filetype: NewFileEnum, df: pd.DataFrame):
        self.df = df.copy()
        self.typepfpg = typepfpg
        self.filetype = filetype

        # Liste di controllo tracciato
        self.oldcolumns = ["idAnagrafica", "AnnoNascita", "TipoPersonalità", "Telefono", "IndirizzoResidenza", "Cap",
                           "CittadinanzaItaliana", "Deceduto", "DecedutoDataInfo", "Cessata", "CessataDataInfo", "PEC",
                           "DataCaricoTitolo", "DataEmissioneTitolo", "TipoCredito", "ValoreTitolo", "Pagato120Giorni",
                           "DataPrimaNotifica", "DataPagamentoTotale", "NumeroTitoliAperti", "DovutoTitoliAperti",
                           "ImportoTitoliAperti", "NumeroTitoliSaldati", "ImportoTitoliSaldati", "NumeroTitoliRecenti",
                           "TotaleTitoliRecenti", "DataNascita"]
        self.newPFcolumns = ["Telefono", "IndirizzoResidenza", "CittadinanzaItaliana", "Deceduto",
                             "ValoreTitolo", "NumeroTitoliAperti", "DovutoTitoliAperti", "ImportoTitoliAperti",
                             "NumeroTitoliSaldati", "ImportoTitoliSaldati", "NumeroTitoliRecenti",
                             "TotaleTitoliRecenti",
                             "Eta", "Vetusta", "TitoliCredito"]
        self.newPGcolumns = ["Telefono", "IndirizzoResidenza", "Cessata", "PEC",
                             "ValoreTitolo", "NumeroTitoliAperti", "DovutoTitoliAperti", "ImportoTitoliAperti",
                             "NumeroTitoliSaldati", "ImportoTitoliSaldati", "NumeroTitoliRecenti",
                             "TotaleTitoliRecenti",
                             "Vetusta", "TitoliCredito"]

    def checkcolumns(self):
        columns = list(self.df.columns.values)
        # Controllo che le colonne in columns siano esattamente quelle che devono essere

        # Per file di titoli storici:
        if self.filetype == NewFileEnum.OLD:
            # Controllo che tutte le colonne che devono esserci siano presenti, salvo in una lista quelle assenti
            assenti = list(set(self.oldcolumns) - set(columns))
            # Lancio errore con lista assenti se presenti
            if len(assenti) > 0:
                raise ValueError(
                    "Errore: \n Nel file caricato mancano le seguenti colonne: " + ', '.join(map(str, list(assenti))))
            # Controllo che non ci siano colonne aggiuntive
            aggiuntive = list(set(columns) - set(self.oldcolumns))
            # Lancio errore con lista aggiuntive se presenti
            if len(aggiuntive) > 0:
                raise ValueError("Errore: \n Nel file caricato è necessario rimuovere le seguenti colonne perchè non "
                                 "parte del tracciato: " + ', '.join(map(str, list(assenti))))
        # Per file di titoli recenti:
        if self.filetype == NewFileEnum.NEW:
            # DEBUG rimuovo label e DataCaricoTitolo dalla lista colonne perchè potrebbero essere presenti e funzionanti
            if 'label' in columns:
                columns.remove('label')
            if 'DataCaricoTitolo' in columns:
                columns.remove('DataCaricoTitolo')
            # Per persone fisiche
            if self.typepfpg == PFPGEnum.PF:
                assenti = list(set(self.newPFcolumns) - set(columns))
                # Lancio errore con lista assenti se presenti
                if len(assenti) > 0:
                    raise ValueError("Errore: \n Nel file caricato mancano le seguenti colonne: " + ', '.join(
                        map(str, list(assenti))))
                # Controllo che non ci siano colonne aggiuntive
                aggiuntive = list(set(columns) - set(self.newPFcolumns))
                # Lancio errore con lista aggiuntive se presenti
                if len(aggiuntive) > 0:
                    raise ValueError("Errore: \n Nel file caricato è necessario rimuovere le seguenti colonne perchè "
                                     "non "
                                     "parte del tracciato: " + ', '.join(map(str, list(assenti))))
            if self.typepfpg == PFPGEnum.PG:
                assenti = list(set(self.newPGcolumns) - set(columns))
                # Lancio errore con lista assenti se presenti
                if len(assenti) > 0:
                    raise ValueError("Errore: \n Nel file caricato mancano le seguenti colonne: " + ', '.join(
                        map(str, list(assenti))))
                # Controllo che non ci siano colonne aggiuntive
                aggiuntive = list(set(columns) - set(self.newPGcolumns))
                # Lancio errore con lista aggiuntive se presenti
                if len(aggiuntive) > 0:
                    raise ValueError("Errore \n Nel file caricato è necessario rimuovere le seguenti colonne perchè "
                                     "non "
                                     "parte del tracciato: " + ', '.join(map(str, list(assenti))))
