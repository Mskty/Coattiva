from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


class NewColumnsDialog(QtWidgets.QDialog):
    """
        Finestra di dialogo la cui apertura viene effettuata da un oggetto di classe MainWindow durante l'utilizzo dell'
        applicativo in MODALITA' ADDESTRAMENTO. Fornisce all'utente la possibilità di visualizzare informazioni all'interno
        di una tabella sulle nuove colonne/features generate durante l'elaborazione dei dati dei titoli di credito storici
        una volta puliti ed aggregati per estrarre ulteriori informazioni dai dati originari e migliorare le performance
        del classificatore predittivo durante l'addestramento.
        PARAMETRI: nessuno
    """

    """
            @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
                 di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
                 e l'invocazione di __init__
    """

    def __init__(self, parent=None):
        # Inizializzazione con parent
        super().__init__(parent)
        self.setupUi(self)

    def setContent(self):
        """
        @PRE: nessuna
        Imposta il contenuto del tableWidget aggiungendo una riga per ogni colonna/feature contenente le relative informazioni
        :return: None
        """
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(0, 0, QTableWidgetItem("NuovoContribuente"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(
            "Campo che vale 0 o 1 a seconda che il contribuente associato sia un nuovo soggetto per ABACO"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Cap"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem(
            "L'indirizzo di residenza testuale non è gestibile dal modello quindi è stato estrapolato il CAP"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Estero"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem(
            "Campo che vale 0 o 1 a seconda che il contribuente abbia un indirizzo di residenza estero"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(3, 0, QTableWidgetItem("RapportoImporto"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem(
            "Campo che contiene il rapporto tra il valore dei titoli ancora da pagare da parte del contribuente precedenti alla data del ruolo e il valore dei titoli che avava invece già interamente saldato ad ABACO"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(4, 0, QTableWidgetItem("RapportoDovutoAperti"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem(
            "Campo che contiene il rapporto tra l'importo ancora da pagare da parte del contribuente e il loro valore originario prima dei pagamenti"))

        # Imposto la grandezza delle righe
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

    def setupUi(self, MetricheDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della NewColumnsDialog predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param MetricheDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        MetricheDialog.setObjectName("MetricheDialog")
        MetricheDialog.resize(858, 400)
        MetricheDialog.setMinimumSize(QtCore.QSize(858, 400))
        MetricheDialog.setWindowModality(QtCore.Qt.NonModal)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        MetricheDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(MetricheDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MetricheDialog)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(MetricheDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(MetricheDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.tableWidget = QtWidgets.QTableWidget(MetricheDialog)
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
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Colonna"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Significato"))

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        # FONTs
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(9)
        self.tableWidget.horizontalHeader().setFont(font)

        self.retranslateUi(MetricheDialog)
        QtCore.QMetaObject.connectSlotsByName(MetricheDialog)

        self.setContent()

    def retranslateUi(self, MetricheDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param MetricheDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        MetricheDialog.setWindowTitle(_translate("MetricheDialog", "Informazioni sull'elaborazione'"))
        self.label.setText(_translate("MetricheDialog", "COLONNE GENERATE"))
        self.label_2.setText(_translate("MetricheDialog",
                                        "I titoli storici, una volta puliti ed aggregati per essere portati alla stesso tracciato dei titoli recenti su cui verrà utilizzato il modello addestrato, vengono ulteriormente elaborati per estrarre maggiori informazioni dati dati tramite nuove colonne e rendere le colonne testuali come IndirizzoResidenza numeriche. \n"
                                        "A seguire è riportata una descrizione di tali proprietà:"))
