# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tracciato.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

from utility.Enums import *


class TracciatoDialog(QtWidgets.QDialog):

    def __init__(self, type: PFPGEnum, parent=None, filetype: NewFileEnum = None):
        # Inizializzazione con parent
        super().__init__(parent)
        self.typepfpg = type
        self.filetype = filetype
        self.setupUi(self)

    def setContent(self):
        """
        Imposta i contenuti del tableWidget a seconda dei parametri typepfpg e filetype.
        Verrà inserita una riga nel tableWidget per ogni colonna/feature con le releative informazioni.
        :return: None
        """
        titlelist = []
        desclist = []
        if not self.filetype or self.filetype == NewFileEnum.OLD:
            titlelist = ["idAnagrafica", "DataNascita", "TipoPersonalità", "Telefono", "IndirizzoResidenza", "Cap",
                         "CittadinanzaItaliana",
                         "Deceduto", "DecedutoDataInfo", "Cessata", "CessataDataInfo", "PEC", "DataCaricoTitolo",
                         "DataEmissioneTitolo", "TipoCredito", "ValoreTitolo", "Pagato120Giorni", "DataPrimaNotifica",
                         "DataPagamentoTotale", "NumeroTitoliAperti", "DovutoTitoliAperti", "ImportoTitoliAperti",
                         "NumeroTitoliSaldati", "ImportoTitoliSaldati", "NumeroTitoliRecenti", "TotaleTitoliRecenti"]
            desclist = [
                "Campo numerico intero contenente l’id per mascherare la combinazione codice fiscale e partita iva del contribuente. Questo campo va dunque ad identificare unicamente ogni contribuente",
                "Campo data in formato aaaa-mm-gg contenente la data di nascita del contribuente ricavata dal codice fiscale",
                "Campo stringa che assume valore “PF” se il titolo è associato ad una persona fisica e “PG” se è invece associato ad una persona giuridica (azienda)",
                "Campo numerico intero che assume valore 1 se il numero di telefono è presente per il contribuente, 0 altrimenti",
                "Campo stringa contenente l’indirizzo di residenza del contribuente",
                "Campo stringa contenente il CAP del contribuente",
                "Campo numerico intero che assume valore 1 se il contribuente ha cittadinanza italiana, 0 altrimenti. Ricavato dal codice fiscale",
                "Campo numerico intero che assume valore 1 se il contribuente è attualmente riportato nel database aziendale come deceduto, 0 altrimenti",
                "Campo data in formato aaaa-mm-gg contenente la data di registrazione nel database del decesso del contribuente nel caso in cui questo fosse avvenuto",
                "Campo numerico intero che assume valore 1 se l’utenza è attualmente riportata nel database aziendale come cessata, 0 altrimenti",
                "Campo data in formato aaaa-mm-gg contenente la data di registrazione nel database della cessazione dell’utenza nel caso in cui questo fosse avvenuto",
                "Campo numerico intero che assume valore 1 se la PEC è presente per il contribuente, 0 altrimenti",
                "Campo data contenente la data in cui ABACO ha ottenuto il titolo di credito. Titoli di credito con la stessa data di carico appartengono allo stesso ruolo proveniente dell’ente",
                "Campo data in formato aaaa-mm-gg contenente la data in cui il titolo è stato emesso verso il contribuente",
                "Campo stringa contenente il tipo del titolo di credito",
                "Campo numerico decimale contenente il valore monetario del titolo di credito",
                "Campo numerico decimale contenente la somma pagata dal debitore a 120 giorni dopo la data di primo sollecito (DataPrimaNotifica) per il titolo",
                "Campo data in formato aaaa-mm-gg contenente la data in cui il contribuente è stato per la prima volta sollecitato al pagamento da ABACO, il campo Pagato120Giorni conta i pagamenti effettuati dal contribuente a partire da questa data",
                "Campo data in formato aaaa-mm-gg contenente la data in cui è stata pagata la totalità della somma dovuta dal titolo",
                "Campo numerico intero contenente il numero di titoli non pagati dal contribuente alla data di carico del titolo di credito, includendo anche titoli non provenienti da ruoli dell’ente",
                "Campo numerico decimale contenente la somma dei valori monetari originali dei titoli aperti",
                "Campo numerico decimale contenente la somma in euro che il contribuente deve ancora versare relativa ai titoli aperti",
                "Campo numerico decimale contenente il numero di titoli completamente saldati dal contribuente alla data di carico del titolo di credito, includendo anche titoli non provenienti da ruoli dell’ente",
                "Campo numerico decimale contenente la somma dei valori monetari originali dei titoli saldati",
                "Campo numerico intero contenente il numero di titoli riferiti allo stesso contribuente con stessa data di carico del titolo. Non viene considerato il titolo stesso nel conteggio",
                "Campo numerico decimale contenente la somma del valore dei titoli riferiti allo stesso contribuente con stessa data di carico del titolo. Non viene considerato il titolo stesso nel conteggio"]

        else:
            if self.filetype == NewFileEnum.NEW:
                if self.typepfpg == PFPGEnum.PF:
                    titlelist = ["Telefono", "IndirizzoResidenza",
                                 "CittadinanzaItaliana",
                                 "Deceduto", "ValoreTitolo", "NumeroTitoliAperti", "DovutoTitoliAperti",
                                 "ImportoTitoliAperti", "NumeroTitoliSaldati", "ImportoTitoliSaldati",
                                 "NumeroTitoliRecenti", "TotaleTitoliRecenti", "Eta", "Vetusta", "TitoliCredito"]
                    desclist = [
                        "campo numerico che può contenere solo i valori 0 e 1. Assumerà il valore 1 se è presente un contatto telefonico per il contribuente associato all’aggregazione di titoli, deve assumere il valore 0 altrimenti",
                        "campo testuale contente l’indirizzo di residenza del contribuente, deve essere nel formato standard Indirizzo – CAP – Località – Provincia",
                        "campo numerico che può contenere solo i valori 0 e 1. Assumerà il valore 1 se il contribuente è in possesso della cittadinanza italiana, deve assumere il valore 0 altrimenti",
                        "campo numerico che può contenere solo i valori 0 e 1. Assumerà il valore 1 se il contribuente associato all’aggregazione di titoli è deceduto, deve assumere il valore 0 altrimenti",
                        "campo numerico contenente la somma dei valori in euro (senza simbolo) dei titoli che hanno composto l’aggregazione, l’aggregazione deve essere fatta a priori decidendo quali e quanti titoli di credito combinare all’interno di uno stesso ruolo e riferiti allo stesso contribuente",
                        "campo numerico contenente il numero di singoli titoli che risultano ancora aperti dal contribuente",
                        "campo numerico contenente la somma del valore in euro (senza simbolo) dei titoli che sono stati conteggiati nel campo NumeroTitoliAperti",
                        "campo numerico contenente la somma in euro (senza simbolo) delle somme che il contribuente deve ancora versare sul valore dei titoli che sono stati conteggiati nel campo NumeroTitoliAperti",
                        "campo numerico contenente il numero dei singoli titoli che risultano completamente saldati in passato dal contribuente",
                        "campo numerico contenente la somma del valore in euro (senza simbolo) dei titoli che sono stati conteggiati nel campo NumeroTitoliSaldati",
                        "campo numerico contenente il numero dei singoli titoli riferiti al contribuente associato all’aggregazione presenti all’interno del ruolo, includendo nel conteggio anche i titoli che fanno parte dell’aggregazione",
                        "campo numerico contenente la somma del valore in euro (senza simbolo) dei titoli che sono stati conteggiati nel campo NumeroTitoliRecenti",
                        "campo numerico contenente l’età in anni del contribuente",
                        "campo numerico contenente il valore di vetustà minima (numero di giorni trascorsi a partire dalla data di emissione del titolo) tra tutti i singoli titoli di credito che sono stati aggregati",
                        "campo numerico contenente il numero dei singoli titoli di credito che sono stati inclusi nell’aggregazione"]
                if self.typepfpg == PFPGEnum.PG:
                    titlelist = ["Telefono", "IndirizzoResidenza",
                                 "Cessata",
                                 "PEC", "ValoreTitolo", "NumeroTitoliAperti", "DovutoTitoliAperti",
                                 "ImportoTitoliAperti", "NumeroTitoliSaldati", "ImportoTitoliSaldati",
                                 "NumeroTitoliRecenti", "TotaleTitoliRecenti", "Eta", "Vetusta", "TitoliCredito"]

                    desclist = [
                        "campo numerico che può contenere solo i valori 0 e 1. Assumerà il valore 1 se è presente un contatto telefonico per il contribuente associato all’aggregazione di titoli, deve assumere il valore 0 altrimenti",
                        "campo testuale contente l’indirizzo di residenza del contribuente, deve essere nel formato standard Indirizzo – CAP – Località – Provincia",
                        "campo numerico che può contenere solo i valori 0 e 1. Assumerà il valore 1 se l’utenza associata all’aggregazione di titoli è cessata, deve assumere il valore 0 altrimenti",
                        "campo numerico che può contenere solo i valori 0 e 1. Assumerà il valore 1 se è presente una PEC valida per il contribuente associato all’aggregazione di titoli, deve assumere il valore 0 altrimenti",
                        "campo numerico contenente la somma dei valori in euro (senza simbolo) dei titoli che hanno composto l’aggregazione, l’aggregazione deve essere fatta a priori decidendo quali e quanti titoli di credito combinare all’interno di uno stesso ruolo e riferiti allo stesso contribuente",
                        "campo numerico contenente il numero di singoli titoli che risultano ancora aperti dal contribuente",
                        "campo numerico contenente la somma del valore in euro (senza simbolo) dei titoli che sono stati conteggiati nel campo NumeroTitoliAperti",
                        "campo numerico contenente la somma in euro (senza simbolo) delle somme che il contribuente deve ancora versare sul valore dei titoli che sono stati conteggiati nel campo NumeroTitoliAperti",
                        "campo numerico contenente il numero dei singoli titoli che risultano completamente saldati in passato dal contribuente",
                        "campo numerico contenente la somma del valore in euro (senza simbolo) dei titoli che sono stati conteggiati nel campo NumeroTitoliSaldati",
                        "campo numerico contenente il numero dei singoli titoli riferiti al contribuente associato all’aggregazione presenti all’interno del ruolo, includendo nel conteggio anche i titoli che fanno parte dell’aggregazione",
                        "campo numerico contenente la somma del valore in euro (senza simbolo) dei titoli che sono stati conteggiati nel campo NumeroTitoliRecenti",
                        "campo numerico contenente l’età in anni del contribuente",
                        "campo numerico contenente il valore di vetustà minima (numero di giorni trascorsi a partire dalla data di emissione del titolo) tra tutti i singoli titoli di credito che sono stati aggregati",
                        "campo numerico contenente il numero dei singoli titoli di credito che sono stati inclusi nell’aggregazione"]

        # Popolo la tabella
        count = 0
        for item in titlelist:
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            self.tableWidget.setItem(count, 0, QTableWidgetItem(item))
            count += 1
        count = 0
        for item in desclist:
            self.tableWidget.setItem(count, 1, QTableWidgetItem(item))
            count += 1

        # Imposto la grandezza delle righe
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

        # Imposto le labels:
        if not self.filetype or self.filetype == NewFileEnum.OLD:
            self.label_newold.setText("Contenuto del file: Titoli storici non aggregati")
        else:
            self.label_newold.setText("Contenuto del file: Titoli recenti appartenenti ad un ruolo aggregati")
        if self.typepfpg == PFPGEnum.PF:
            self.label_3.setText("Tipo di contribuenti: Persone Fisiche")
        else:
            self.label_3.setText("Tipo di contribuenti: Persone Giuridiche")

    def setupUi(self, TracciatoDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della TracciatoDialog predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param TracciatoDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        TracciatoDialog.setObjectName("TracciatoDialog")
        TracciatoDialog.resize(500, 400)
        TracciatoDialog.setMinimumSize(QtCore.QSize(500, 400))
        TracciatoDialog.setWindowModality(QtCore.Qt.NonModal)
        # FONT GENERALE
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        TracciatoDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(TracciatoDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(TracciatoDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(TracciatoDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_newold = QtWidgets.QLabel(TracciatoDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_newold.sizePolicy().hasHeightForWidth())
        self.label_newold.setSizePolicy(sizePolicy)
        self.label_newold.setObjectName("label_newold")
        self.verticalLayout.addWidget(self.label_newold)
        self.label_3 = QtWidgets.QLabel(TracciatoDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.tableWidget = QtWidgets.QTableWidget(TracciatoDialog)
        self.tableWidget.setMinimumSize(QtCore.QSize(482, 0))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidget)
        # Our tablewidget has 2 columns
        self.tableWidget.setColumnCount(2)
        # Setting header
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Nome Colonna"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Significato"))

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        # FONTs
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        self.label.setFont(font)
        font.setPointSize(9)
        self.tableWidget.horizontalHeader().setFont(font)

        self.retranslateUi(TracciatoDialog)
        QtCore.QMetaObject.connectSlotsByName(TracciatoDialog)

        # Set table content
        self.setContent()

    def retranslateUi(self, TracciatoDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param TracciatoDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        TracciatoDialog.setWindowTitle(_translate("TracciatoDialog", "Tracciato"))
        self.label.setText(_translate("TracciatoDialog", "TRACCIATO"))
        self.label_newold.setText(_translate("TracciatoDialog", "Tipo di contribuenti: "))
