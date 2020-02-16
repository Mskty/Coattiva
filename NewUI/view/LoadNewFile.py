# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadnewfile.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from view.GUI import MainWindow


class LoadNewFile(QtWidgets.QDialog):
    # inizializzazione

    def __init__(self, parent: MainWindow = None):
        # Inizializzazione con parent mainwindow
        super().__init__(parent)
        self.mainwindow = parent
        self.setupUi(self)
        self.error_dialog = QtWidgets.QErrorMessage(self)

        # Inizializzazione variabili proprie
        self.type = "NEW"
        self.filename = ""

    # funzioni setter

    def setType(self, type: str):
        self.type = type

    def setFileName(self, filename: str):
        self.filename = filename

    # funzioni di business

    def openFileNameDialog(self):
        # Apre finesta per recupero file e lo passa al modello se corretto
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;CSV Files (*.csv)", options=options)
        # DEBUG
        if fileName:
            print(fileName)

        """# Utilizzo tablemodel
            try:
                self.mainwindow.tablemodel.setType(self.type)
                self.mainwindow.tablemodel.loadDataFromFile(
                    fileName)  # SARA' LA FUNZIONE SU DATAOBJECT A LANCIARE ECCEZIONI
                # nessuna eccezione ritorno alla main
                self.returnToMain()
            except Exception as e:
                # Stampa eccezione
                self.error_dialog.showMessage(str(e))"""

    def returnToMain(self):
        self.close()
        self.mainwindow.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.verticalLayout_4.addWidget(self.label_6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.radio_recenti = QtWidgets.QRadioButton(Dialog)
        self.radio_recenti.setObjectName("radio_recenti")
        self.horizontalLayout.addWidget(self.radio_recenti)
        self.radio_storici = QtWidgets.QRadioButton(Dialog)
        self.radio_storici.setObjectName("radio_storici")
        self.horizontalLayout.addWidget(self.radio_storici)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_5)

        # SLOTS
        self.radio_storici.clicked.connect(lambda: self.setType("OLD"))
        self.radio_recenti.clicked.connect(lambda: self.setType("NEW"))
        self.loadfile.clicked.connect(lambda: self.openFileNameDialog())

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Caricamento File Utilizzo"))
        self.label_2.setText(_translate("Dialog", "CARICAMENTO FILE DI UTILIZZO"))
        self.label_4.setText(_translate("Dialog",
                                        "E\' possibile caricare un file .csv contenente i titoli di credito su cui si vuole ottenere predizioni da parte del modello addestrato."))
        self.label_5.setText(_translate("Dialog",
                                        "Il file deve seguire il tracciato utilizzato da questo applicativo per essere valido."))
        self.label.setText(_translate("Dialog",
                                      "E\' possibile caricare un file contenente dati storici col medesimo tracciato di quello utilizzato per l\'addestramento del modello oppure un file contenente solamente titoli recenti facenti parte dello stesso ruolo."))
        self.label_6.setText(_translate("Dialog", "Scegli il tipo di dati contenuti nel file da elaborare:"))
        self.radio_recenti.setText(_translate("Dialog", "Dati Recenti"))
        self.radio_storici.setText(_translate("Dialog", "Dati Storici"))
        self.label_3.setText(
            _translate("Dialog", "Permi per selezionare il file .csv contenente i dati sui titoli di credito:"))
        self.pushButton.setText(_translate("Dialog", "Carica File"))
