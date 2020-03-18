# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MetricheDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


class MetricheDialog(QtWidgets.QDialog):
    """
    Finestra di dialogo la cui apertura viene effettuata da un oggetto di classe MainWindow durante l'utilizzo dell'
    applicativo in MODALITA' ADDESTRAMENTO. Fornisce all'utente la possibilità di visualizzare informazioni all'interno
    di una tabella sulle metriche utilizzate per valutare le performance di un classificatore adddestrato sui dati
    dei titoli di credito storici.
    PARAMETRI: nessuno
    """

    """
            @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
                 di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
                 e l'invocazione di __init__
    """

    def __init__(self, parent):
        # Inizializzazione con parent
        super().__init__(parent)
        self.setupUi(self)

    def setContent(self):
        """
        @PRE: nessuna
        Imposta il contenuto del tableWidget aggiungendo una riga per ogni metrica contenente le relative informazioni
        :return: None
        """
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Accuratezza"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem(
            "Indica la percentuale di esempi che il modello addestrato ha predetto correttamente"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Precisione"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(1, 2, QTableWidgetItem(
            "Indica la precisione del modello sulle predizioni positive, ovvero quanti degli esempi predetti come positivi avevano anche label positiva e sono quindi corretti"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Recall"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(2, 2, QTableWidgetItem(
            "Indica la percentuale di esempi con label postiva che il modello addestrato ha predetto correttamente come positivi"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(3, 0, QTableWidgetItem("F1 Score"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(3, 2, QTableWidgetItem(
            "Si tratta della media armonica tra precisione e recall. Assume il valore 100 quando sia precisione che recall valgono 100 (indicando che il modello è perfetto) mentre assume il valore 0 quando precisione o recall valgono 0. Fornisce quindi una punteggio generale alle prestazioni del modello"))

        # Imposto la grandezza delle righe
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

    def setupUi(self, MetricheDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della MetricheDialog predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param MetricheDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        MetricheDialog.setObjectName("MetricheDialog")
        MetricheDialog.resize(858, 400)
        MetricheDialog.setMinimumSize(QtCore.QSize(858, 400))
        MetricheDialog.setWindowModality(QtCore.Qt.NonModal)
        # FONT GENERICO
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
        font.setPointSize(12)
        font.setBold(True)
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
        self.tableWidget.setColumnCount(3)
        # Setting header
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Metrica"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Range Valori"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Significato"))

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
        MetricheDialog.setWindowTitle(_translate("MetricheDialog", "Informazioni sulle metriche"))
        self.label.setText(_translate("MetricheDialog", "INFORMAZIONI SULLE METRICHE"))
        self.label_2.setText(_translate("MetricheDialog", "Vengono riportate nella schermata i valori di quattro "
                                                          "metriche per valutare le performance dell\'algoritmo, "
                                                          "sia sulla parte di training che sulla parte di test nel "
                                                          "caso sia presente. \n "
                                                          "I risultati sulla parte di training sono riportati per correttezza tuttavia "
                                                          "non sono rappresentativi di un caso di "
                                                          "utilizzo reale come nel caso della parte di test."))
