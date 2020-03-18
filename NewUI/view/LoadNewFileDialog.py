# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadnewfile.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from view.GUI import *
from view.WaitingDialog import *
from view.TracciatoDialog import *
from view.ConverterWindow import *


class LoadNewFile(QtWidgets.QDialog):
    """
    Finestra la cui apertura viene effettuata da un oggetto di classe MainWindow. Fornsice all'utente la possibilitò
    di caricare nel modello (oggetto di classe Model posseduto dall'oggetto MainWindow) un file .csv contenente i
    dati dei titoli di credito su cui ottenere predizioni da un classificatore addestrato nell'applicativo su dati
    storici precedentemente caricati. I dati caricabili possono essere dei dati recenti di titoli di credito aggregati
    la cui forma su file deve aderire al rispettivo tracciato, oppure dei dati storici di titoli di credito come da
    estrazione da database, seguendo le stesse regole elencate per il loro caricamento nelle classi MainFileWindow
    e FirstWindow. Il file caricato, se corretto. Il tipo di personalitò a cui sono riferiti i titoli di credito è
    passato all'apertura della finestra, e deve essere coerente con i dati su cui è stato precedentemente addestrato
    il classificatore all'interno dell'applicativo.
    Presenta la  possibilitò di indicare il tipo di file che si desidera utilizzare attraverso RadioButtons (dati recenti
    oppure dati storici) e poi caricare il file che, se corretto, permette di ritornare alla finestra MainWindow.
    Fornisce inoltre la possibilità attraerso l'apertura di due finestre aggiuntive di convertire un file da excel a .csv
    attraverso  una finestra di tipo ConverterWindow e di visualizzare informazioni sul tracciato che devono seguire
    i file caricabili attraverso una finestra di tipo TracciatoDialog.
    PARAMETRI:
    self.mainwindow: oggetto di tipo MainWindow da cui viene generata la finestra e che presenta il parametro
                     mainwindow.model da cui è possibile caricare ed elaborare il nuovo file .csv
    self.error_dialog: oggetto di tipo QtWidgets.QErrorMessage che si occupa di visualizzare una finestra che riporta
                       all'utente un messaggio di errore nel caso venga caricato un file errato, ovvero che non segua
                       il tracciato
    self.typepfpg: Valore di tipo PFPGEnum rappresentante il tipo dei titoli di credito che dovranno essere contenuti
                    nel file caricato dall'utente. Tale valore è fornito alla creazione della finestra
    self.type: Valore di tipo NewFileEnum rappresentante il tipo del file che dovrà essere caricato dall'utente.
               Il valore di default è NewFileEnum.NEW in quanto all'apertura della finestra
               è selezionato il bottone radio rappresentate il caricamento di un file riferito a titoli di credito
               recenti ed aggregati
    self.filename: Valore stringa che rappresenta il percorso di salvataggio del file .csv caricato, inzialmente
                   stringa vuota.
    """

    """
            @PRE nella descrizione dei metodi si riferisce alla precondizione che deve essere soddisfatta prima dell'invocazione
                 di tale metodo da parte dell'utente, tra le precondizioni è sempre considerata soddisfatta la creazione dell'oggetto
                 e l'invocazione di __init__
    """

    def __init__(self, typepfpg: PFPGEnum, parent = None):
        # Inizializzazione con parent mainwindow
        super().__init__(parent)
        self.mainwindow = parent
        self.setupUi(self)
        self.error_dialog = QtWidgets.QErrorMessage(self)

        # Inizializzazione variabili proprie
        self.typepfpg = typepfpg
        self.type: NewFileEnum = NewFileEnum.NEW
        self.filename = ""

    """------------------------------Funzioni Setter----------------------------------------------------------------"""

    def setType(self, type: NewFileEnum):
        self.type = type

    def setFileName(self, filename: str):
        self.filename = filename

    """----------------------------Funzioni di business-------------------------------------------------------------"""

    def openFileNameDialog(self):
        """
        @PRE: nessuna
        Apre una finestra che permette all'utente di selezionare un file di tipo csv
        :return: nome del file selezionato dall'utente
        """
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica File csv", "",
                                                  "CSV Files (*.csv)", options=options)
        return fileName

    def returnToMain(self):
        """
        @PRE: è stata invocata la funzione self.onClickedLoadFileButton
        Invoca sul parent mainwindow la funzione di setup per la seizone Utilizza una volta caricati ed elaborati i dati
        dell'utente dal modello, infine chiude la finestra.
        :return: None
        """
        self.mainwindow.useFileSetup()
        self.close()

    """-------------------------Funzioni SLOTS di bottoni presenti all'inizializzazione---------------------------- """

    def onClickedLoadFileButton(self):
        """
        @PRE: è stato premuto il pulsante loadfile
        Ottiene il nome di un file dall'utente, se questo è valido invoca la funzione del modello set_use_data per elaborare
        i dati contenuti in tale file. Se l'elaborazione ha successo allora invoca la funzione returnToMain
        :return: None
        """
        filename = self.openFileNameDialog()
        if filename:
            text = "Attendi mentre i dati contenuti sul file selezionato vengono elaborati"
            dialog=WaitingDialog(self.mainwindow,text,self.mapToGlobal(self.rect().center()))
            dialog.show()
            QtWidgets.QApplication.processEvents()
            try:
                # Può lanciare eccezione ValuError
                self.mainwindow.model.set_use_data(self.type, filename)

                # informo il dialog del successo
                dialog.success(True)
                # nessuna eccezione ritorno alla main
                self.returnToMain()
            except ValueError as e:
                # Informo il dialog del fallimento
                dialog.success(False)
                # Stampa eccezione
                self.error_dialog.showMessage(str(e))

    def onClickedConverterButton(self):
        """
        @PRE: è stato premuto il pulsante converter
        Apre la finestra di tipo ConverterWindow
        :return: None
        """
        converter = ConverterWindow(self)
        converter.exec_()

    def onClickedTracciatoButton(self):
        """
        @PRE: è stato premuto il pulsante tracciato
        Apre una finestra di tipo TracciatoDialog
        :return: None
        """
        tracciato= TracciatoDialog(type=self.typepfpg, parent=self, filetype=self.type)
        tracciato.exec_()

    def setupUi(self, Dialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della LoadNewFile predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param Dialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 400)
        # FONT DI BASE
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        Dialog.setFont(font)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(500, 400))
        Dialog.setMaximumSize(QtCore.QSize(500, 400))
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_6.setMinimumHeight(40)
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.radio_recenti = QtWidgets.QRadioButton(Dialog)
        self.radio_storici = QtWidgets.QRadioButton(Dialog)
        self.radio_recenti.setObjectName("radio_recenti")
        self.radio_recenti.setMinimumHeight(40)
        self.horizontalLayout.addWidget(self.radio_recenti)
        self.radio_recenti.setChecked(True)
        self.radio_storici.setObjectName("radio_storici")
        self.horizontalLayout.addWidget(self.radio_storici)
        self.radio_storici.setMinimumHeight(40)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setMinimumHeight(40)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.loadfile = QtWidgets.QPushButton(Dialog)
        self.loadfile.setObjectName("loadfile")
        self.horizontalLayout_2.addWidget(self.loadfile)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setObjectName("label_10")
        self.label_10.setMinimumHeight(40)
        self.horizontalLayout_4.addWidget(self.label_10)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.converter = QtWidgets.QPushButton(Dialog)
        self.converter.setObjectName("converter")
        self.horizontalLayout_4.addWidget(self.converter)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.label_7.setMinimumHeight(40)
        self.horizontalLayout_10.addWidget(self.label_7)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.tracciato = QtWidgets.QPushButton(Dialog)
        self.tracciato.setObjectName("tracciato")
        self.horizontalLayout_10.addWidget(self.tracciato)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.verticalLayout.addLayout(self.verticalLayout_5)

        # FONTS
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(12)
        self.label_2.setFont(font)
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_6.setFont(font)
        self.label_3.setFont(font)
        self.loadfile.setFont(font)

        # SLOTS
        self.radio_storici.clicked.connect(lambda: self.setType(NewFileEnum.OLD))
        self.radio_recenti.clicked.connect(lambda: self.setType(NewFileEnum.NEW))
        self.converter.clicked.connect(lambda: self.onClickedConverterButton())
        self.loadfile.clicked.connect(lambda: self.onClickedLoadFileButton())
        self.tracciato.clicked.connect(lambda: self.onClickedTracciatoButton())

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param Dialog: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Caricamento File Utilizzo"))
        self.label_2.setText(_translate("Dialog", "CARICAMENTO FILE DI UTILIZZO"))
        self.label_4.setText(_translate("Dialog",
                                        "E\' possibile caricare un file .csv contenente i titoli di credito su cui si "
                                        "vuole ottenere predizioni da parte del modello addestrato."))
        self.label_5.setText(_translate("Dialog",
                                        "Il file deve seguire il tracciato utilizzato da questo applicativo per "
                                        "essere valido."))
        self.label.setText(_translate("Dialog",
                                      "E\' possibile caricare un file contenente dati storici col medesimo tracciato "
                                      "di quello utilizzato per l\'addestramento del modello oppure un file "
                                      "contenente solamente titoli recenti facenti parte di uno stesso ruolo."))
        self.label_6.setText(_translate("Dialog", "Scegli il tipo di dati contenuti nel file da elaborare:"))
        self.radio_recenti.setText(_translate("Dialog", "Dati Recenti"))
        self.radio_storici.setText(_translate("Dialog", "Dati Storici"))
        self.label_3.setText(
            _translate("Dialog", "Permi per selezionare il file .csv contenente i dati sui titoli di credito:"))
        self.loadfile.setText(_translate("Dialog", "Carica File"))
        self.label_10.setText(
            _translate("Dialog", "Premi per convertire un file da excel a csv:"))
        self.converter.setText(_translate("Dialog", "Convertitore"))
        self.label_7.setText(_translate("Dialog", "Premi per visualizzare il tracciato richiesto per il file .csv:"))
        self.tracciato.setText(_translate("Dialog", "Tracciato"))


