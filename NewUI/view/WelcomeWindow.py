# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WelcomeWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from view.GUI import *


class WelcomeWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        # Inizializzazione con parent mainwindow
        super().__init__()
        self.mainwindow = parent
        self.setupUi(self)
        self.error_dialog = QtWidgets.QErrorMessage(self)

    def openFileNameDialog(self):
        """
        PRE: nessuna
        Apre una finestra che permette all'utente di selezionare un file di tipo sav contenente un modello addestrato
        :return: nome del file selezionato dall'utente
        """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Carica il file contenente il modello addestrato per "
                                                        "utilizzarlo", "",
                                                  "Model Files (*.sav)", options=options)
        return filename

    """-------------------------Funzioni SLOTS di bottoni presenti all'inizializzazione---------------------------- """

    def onClickedButtonAddestramento(self):
        """
        @PRE: è stato premuto il pulsante button_addestramento
        Chiude la finestra e invoca la funzione del parent mainwindow che permette di visualizzare la finestra di primo
        accesso per la modalitò addestramento
        :return: None
        """
        self.close()
        self.mainwindow.openFirstWindow()

    def onClickedButtonUtilizza(self):
        """
        @PRE: è stato premuto il pulsante button_utilizza
        Ottiene il nome di un file dall'utente, se questo è valido invoca la funzione del modello algorithm_from_file per
        caricare nell'applicativo il modello addestrato contenuto in tale file.
        Se l'elaborazione ha successo allora invoca la funzione returnToMain
        :return: None
        """
        filename = self.openFileNameDialog()
        if filename:
            text = "Attendi mentre il modello viene caricato da file"
            dialog = WaitingDialog(self.mainwindow, text, self.mapToGlobal(self.rect().center()))
            dialog.show()
            try:
                self.mainwindow.model.algorithm_from_file(filename)
                # informo il dialog del successo
                dialog.success(True)
                # nessuna eccezione ritorno alla main
                self.mainwindow.useSetup()
                self.close()
                self.mainwindow.show()
            except Exception as e:
                # Informo il dialog del fallimento
                dialog.success(False)
                # Stampa eccezione
                self.error_dialog.showMessage(str(e))

    def setupUi(self, WelcomeWindow):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della WelcomeWindow predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param WelcomeWindow: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        WelcomeWindow.setObjectName("WelcomeWindow")
        WelcomeWindow.resize(882, 200)
        WelcomeWindow.setMinimumSize(QtCore.QSize(882, 200))
        WelcomeWindow.setMaximumSize(QtCore.QSize(882, 200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        WelcomeWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(WelcomeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_addestramento = QtWidgets.QPushButton(self.centralwidget)
        self.button_addestramento.setObjectName("button_addestramento")
        self.horizontalLayout.addWidget(self.button_addestramento)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.button_utilizzo = QtWidgets.QPushButton(self.centralwidget)
        self.button_utilizzo.setObjectName("button_utilizzo")
        self.horizontalLayout_2.addWidget(self.button_utilizzo)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        WelcomeWindow.setCentralWidget(self.centralwidget)

        #FONT PER BOTTONI
        font = QtGui.QFont()
        font.setBold(True)
        self.button_utilizzo.setFont(font)
        self.button_addestramento.setFont(font)

        # SLOTS
        self.button_addestramento.clicked.connect(lambda: self.onClickedButtonAddestramento())
        self.button_utilizzo.clicked.connect(lambda: self.onClickedButtonUtilizza())

        self.retranslateUi(WelcomeWindow)
        QtCore.QMetaObject.connectSlotsByName(WelcomeWindow)

    def retranslateUi(self, WelcomeWindow):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param WelcomeWindow: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        WelcomeWindow.setWindowTitle(_translate("WelcomeWindow", "Classificatore Coattiva"))
        self.label.setText(_translate("WelcomeWindow", "CLASSIFICATORE COATTIVA"))
        self.label_2.setText(_translate("WelcomeWindow", "Selezionare a quale modalità accedere*:"))
        self.label_3.setText(_translate("WelcomeWindow", "1) Modalità addestramento: "))
        self.label_5.setText(_translate("WelcomeWindow",
                                        "E\' possibile addestrare e utilizzare un modello di apprendimento partendo dai dati storici."))
        self.button_addestramento.setText(_translate("WelcomeWindow", "Entra"))
        self.label_4.setText(_translate("WelcomeWindow", "2 Modalità utilizzo:"))
        self.label_6.setText(_translate("WelcomeWindow",
                                        "E\' possibile caricare da file un modello già addestrato in precedenza e utilizzarlo su nuovi dati."))
        self.button_utilizzo.setText(_translate("WelcomeWindow", "Carica Modello"))
        self.label_7.setText(
            _translate("WelcomeWindow", "* sarà necessario riavviare l\'applicativo per passare all\'altra modalità."))
