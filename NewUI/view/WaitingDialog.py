# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WaitingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class WaitingDialog(QtWidgets.QDialog):
    """
    Finestra che permette la visualizzazione all'utente di un messaggio d'attesa durante l'esecuzione di operazioni
    particolarmente onerose in termini di tempo come il caricamento di un file di dati storici che deve essere elaborato
    oppure l'addestramento di un classificatore predittivo su tali dati all'interno dell'applicativo. Fornisce
    la possibilità, una volta termianta l'operazione di invocare il metodo success per comunciare all'utente il successo
    o fallimento di tale operazione, permettendo di chiudere la finestra di dialogo.
    PARAMETRI:
    self.text: valore stringa rappresentante il testo da visualizzare nella finestra durante l'attesa che l'operazione
               onerosa termini la sua esecuzione. Tale valore è fornito alla creazione della finestra.
    """

    """
        @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
             di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
             e l'invocazione di __init__
        """

    def __init__(self, parent, text=None, position=None):
        # Inizializzazione con parent
        super().__init__(parent)
        self.setupUi(self)
        self.text = text
        if text is not None:
            self.label.setText(text)
        if position is not None:
            qr = self.frameGeometry()
            qr.moveCenter(position)
            self.move(qr.topLeft())

    def success(self, success: bool):
        """
        @PRE: nessuna
        Funzione da chiamare al termine dell'elaborazione.
        Modifica il testo della finestra a seconda del fallimento o successo dell'operazione, infine aggiunge un bottone
        per chiudere la finestra una volta informato l'utente dello stato dell'operazione.
        :param success: True se l'operazione è terminata con successo False altrimenti
        :return:
        """
        self.verticalLayout.removeWidget(self.label)
        self.label.setParent(None)
        if success:
            text = "Operazione terminata con successo"
        else:
            text = "Operazione fallita"
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(label)
        button = QtWidgets.QPushButton("Chiudi")
        button.clicked.connect(lambda: self.close())
        self.verticalLayout.addWidget(button)

    def setupUi(self, WaitingDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della WaitingDialog predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param WaitingDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        WaitingDialog.setObjectName("WaitingDialog")
        WaitingDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        WaitingDialog.resize(320, 100)
        WaitingDialog.setMinimumSize(QtCore.QSize(320, 100))
        WaitingDialog.setMaximumSize(QtCore.QSize(320, 100))
        # FONT DI BASE
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        WaitingDialog.setFont(font)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setWeight(75)
        WaitingDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(WaitingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(WaitingDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        self.retranslateUi(WaitingDialog)
        QtCore.QMetaObject.connectSlotsByName(WaitingDialog)

    def retranslateUi(self, WaitingDialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param WaitingDialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        WaitingDialog.setWindowTitle(_translate("WaitingDialog", "Attendi"))
        self.label.setText(_translate("WaitingDialog", "Attendi il completamento dell\'operazione sui dati..."))