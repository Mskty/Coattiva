# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firstwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from view.Main import *


class FirstWindow(QtWidgets.QDialog):
    # inizializzazione

    def __init__(self, parent: MainWindow = None):
        # Inizializzazione con parent mainwindow
        super().__init__(parent)
        self.mainwindow = parent
        self.setupUi(self)
        self.error_dialog = QtWidgets.QErrorMessage(self)

        # Inizializzazione variabili proprie
        self.type = ""
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
        Dialog.setMinimumSize(QtCore.QSize(500, 400))
        Dialog.setMaximumSize(QtCore.QSize(500, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(Dialog)
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
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.label_6 = QtWidgets.QLabel(Dialog)
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
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.radio_pf = QtWidgets.QRadioButton(Dialog)
        self.radio_pf.setObjectName("radio_pf")
        self.horizontalLayout.addWidget(self.radio_pf)
        self.radio_pg = QtWidgets.QRadioButton(Dialog)
        self.radio_pg.setObjectName("radio_pg")
        self.horizontalLayout.addWidget(self.radio_pg)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.loadfile = QtWidgets.QPushButton(Dialog)
        self.loadfile.setObjectName("loadfile")
        self.horizontalLayout_3.addWidget(self.loadfile)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        # SLOTS
        self.radio_pf.clicked.connect(lambda: self.setType("PF"))
        self.radio_pg.clicked.connect(lambda: self.setType("PG"))
        self.loadfile.clicked.connect(lambda: self.openFileNameDialog())

        # RetranslateUi
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Classificatore Coattiva Benvenuto"))
        self.label.setText(_translate("Dialog", "BENVENUTO"))
        self.label_4.setText(_translate("Dialog",
                                        "E\' possibile caricare un file .csv contenente i titoli di credito storici da cui partire ad addestrare un modello predittivo per la classificazione delle label."))
        self.label_6.setText(_translate("Dialog",
                                        "Il file deve seguire il tracciato utilizzato da questo applicativo per essere valido."))
        self.label_5.setText(_translate("Dialog",
                                        "Se il file risulta valido allora verranno automaticamente applicate operazioni di pulizia e preprocessamento dei dati per renderli utilizzabili come base per l\'algoritmo di apprendimento."))
        self.label_2.setText(
            _translate("Dialog", "Scegli il tipo di debitori a cui sono riferiti i titoli di credito:"))
        self.radio_pf.setText(_translate("Dialog", "Persone Fisiche"))
        self.radio_pg.setText(_translate("Dialog", "Persone Giuridiche"))
        self.label_3.setText(
            _translate("Dialog", "Premi per selezionare il file .csv contenente i dati storici sui titoli di credito:"))
        self.loadfile.setText(_translate("Dialog", "Carica File"))
