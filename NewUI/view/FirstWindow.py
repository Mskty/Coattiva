# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from view.GUI import *
from view.WaitingDialog import *
from view.tracciato import *
from view.ConverterWindow import *


class FirstWindow(QtWidgets.QMainWindow):
    # inizializzazione

    def __init__(self, parent=None):
        # Inizializzazione con parent mainwindow
        super().__init__()
        self.mainwindow = parent
        self.setupUi(self)
        self.error_dialog = QtWidgets.QErrorMessage(self)

        # Inizializzazione variabili proprie
        self.type: PFPGEnum = PFPGEnum.PF
        self.filename = ""

    # funzioni setter

    def setType(self, type: PFPGEnum):
        self.type = type

    def setFileName(self, filename: str):
        self.filename = filename

    # funzioni di business

    def openFileNameDialog(self):
        # Apre finesta per recupero file e lo passa al modello se corretto
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Carica File csv", "",
                                                  "CSV Files (*.csv)", options=options)

        return fileName

    def returnToMain(self):
        # Mainwindow non visibile alla prima apertura dell'applicazione ma visibile una volta che era già stato aperto
        # un file
        self.mainwindow.firstSetup()
        self.close()
        self.mainwindow.show()

    # SLOTS

    def onClickedLoadFileButton(self):
        filename = self.openFileNameDialog()
        if filename:
            text = "Attendi mentre i titoli di credito storici vengono puliti, aggregati e preparati all'utilizzo"
            dialog = WaitingDialog(self, text)
            dialog.show()
            try:
                self.mainwindow.model.set_data(self.type, filename)
                # informo il dialog del successo
                dialog.success(True)
                # nessuna eccezione ritorno alla main
                self.returnToMain()
            except Exception as e:
                # Informo il dialog del fallimento
                dialog.success(False)
                # Stampa eccezione
                self.error_dialog.showMessage(str(e))

    def onClickedConverterButton(self):
        converter = ConverterWindow(self)
        converter.exec_()

    def onClickedTracciatoButton(self):
        tracciato = TracciatoDialog(type=self.type, parent=self)
        tracciato.exec_()

    def setupUi(self, Dialog):
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

        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.verticalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setMinimumHeight(40)
        self.verticalLayout_6.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.radio_pf = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_pf.setObjectName("radio_pf")
        self.radio_pf.setMinimumHeight(40)
        self.horizontalLayout.addWidget(self.radio_pf)
        self.radio_pf.setChecked(True)
        self.radio_pg = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_pg.setObjectName("radio_pg")
        self.radio_pf.setMinimumHeight(40)
        self.horizontalLayout.addWidget(self.radio_pg)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_3.setMinimumHeight(40)
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.loadfile = QtWidgets.QPushButton(self.centralwidget)
        self.loadfile.setObjectName("loadfile")
        self.horizontalLayout_3.addWidget(self.loadfile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.label_10.setMinimumHeight(40)
        self.horizontalLayout_4.addWidget(self.label_10)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.converter = QtWidgets.QPushButton(self.centralwidget)
        self.converter.setObjectName("converter")
        self.horizontalLayout_4.addWidget(self.converter)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.label_7.setMinimumHeight(40)
        self.horizontalLayout_2.addWidget(self.label_7)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.tracciato = QtWidgets.QPushButton(self.centralwidget)
        self.tracciato.setObjectName("tracciato")
        self.horizontalLayout_2.addWidget(self.tracciato)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout.addLayout(self.verticalLayout_2)

        Dialog.setCentralWidget(self.centralwidget)

        # FONTS
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        font.setPointSize(12)
        self.label.setFont(font)
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_2.setFont(font)
        self.label_3.setFont(font)
        self.loadfile.setFont(font)

        # SLOTS
        self.radio_pf.clicked.connect(lambda: self.setType(PFPGEnum.PF))
        self.radio_pg.clicked.connect(lambda: self.setType(PFPGEnum.PG))
        self.loadfile.clicked.connect(lambda: self.onClickedLoadFileButton())
        self.converter.clicked.connect(lambda: self.onClickedConverterButton())
        self.tracciato.clicked.connect(lambda: self.onClickedTracciatoButton())

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        # RetranslateUi
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Classificatore Coattiva Benvenuto"))
        self.label.setText(_translate("Dialog", "BENVENUTO"))
        self.label_4.setText(_translate("Dialog",
                                        "E\' possibile caricare un file .csv contenente i titoli di credito storici "
                                        "con cui addestrare un modello predittivo per la classificazione "
                                        "di nuovi titoli."))
        self.label_6.setText(_translate("Dialog",
                                        "Il file deve seguire il tracciato utilizzato da questo applicativo per "
                                        "essere valido."))
        self.label_5.setText(_translate("Dialog",
                                        "Se il file risulta valido allora verranno automaticamente applicate "
                                        "operazioni di pulizia e preparazione dei dati per renderli utilizzabili "
                                        "come base per l\'algoritmo di apprendimento."))
        self.label_2.setText(
            _translate("Dialog", "Scegli il tipo di contribuenti a cui sono riferiti i titoli di credito:"))
        self.radio_pf.setText(_translate("Dialog", "Persone Fisiche"))
        self.radio_pg.setText(_translate("Dialog", "Persone Giuridiche"))
        self.label_3.setText(
            _translate("Dialog", "Premi per selezionare il file contenente i titoli storici:"))
        self.loadfile.setText(_translate("Dialog", "Carica File"))
        self.label_10.setText(
            _translate("Dialog", "Premi per convertire un file da excel a csv:"))
        self.converter.setText(_translate("Dialog", "Convertitore"))
        self.label_7.setText(_translate("Dialog", "Premi per visualizzare il tracciato richiesto per il file .csv:"))
        self.tracciato.setText(_translate("Dialog", "Tracciato"))