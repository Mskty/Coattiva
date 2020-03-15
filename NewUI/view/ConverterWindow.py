# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConverterWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog

from view.WaitingDialog import *

import pandas as pd


class ConverterWindow(QDialog):

    def __init__(self, parent=None):
        # Inizializzazione con parent mainwindow
        super().__init__(parent)
        self.mainwindow = parent
        self.setupUi(self)

        # variabili di business
        self.xlsxfile = ""
        self.csvfile = ""

    def openFileNameDialog(self):
        """
        Apre una finestra che permette all'utente di selezionare un file di tipo xlsx
        :return: nome del file selezionato dall'utente
        """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Seleziona File xlsx", "",
                                                  "Excel Files (*.xlsx)", options=options)
        return filename

    def openSaveDialog(self):
        """
        Apre una finestra che permette all'utente di selezionare un percorso di salvataggio per un file di tipo csv
        :return: nome del percorso di salvataggio selezionato dall'utente
        """
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Percorso File csv", "",
                                                  "Csv Files (*.csv)", options=options)
        return filename

    def onClickedButtonLoad(self):
        """
        Ottiene il nome di un file dall'utente, se questo è valido ed è già stato selezionato il percorso di
        salvataggio permette all'utente di premere il pulsante di conversione a csv :return: None
        """
        # Salvo file da convertire e scrivo il nome
        filename = self.openFileNameDialog()
        if filename:
            self.xlsxfile = filename
            self.label_file.setText("File da convertire .xlsx: " + filename)
            # Se anche l'altro è stato selezionato abilito il bottone
            if self.csvfile:
                self.button_save.setEnabled(True)

    def onClickedButtonPath(self):
        """
        Ottiene il percorso di salvataggio dall'utente, se questo è valido ed è già stato selezionato il file da
        convertire permette all'utente di premere il pulsante di conversione e salvataggio :return:
        """
        filename = self.openSaveDialog()
        if filename:
            self.csvfile = filename
            self.label_percorso.setText("Percorso di salvataggio .csv: " + filename)
            # Se anche l'altro è stato selezionato abilito il bottone
            if self.xlsxfile:
                self.button_save.setEnabled(True)

    def onClickedButtonSave(self):
        """
        Converte il file selezionato dal formato xlsx a csv, se la conversione ha successo lo salva al percorso indicato
        infine chiude la finestra
        :return: None
        """
        # Converto, salvo il file csv e chiudo la finestra
        text = "Attendi mentre il file viene convertito al formato csv"
        dialog = WaitingDialog(self.mainwindow, text, self.mapToGlobal(self.rect().center()))
        dialog.show()
        QtWidgets.QApplication.processEvents()
        try:
            data = pd.read_excel(self.xlsxfile,
                                 sheet_name=0,
                                 header=0,
                                 index_col=False,
                                 keep_default_na=True)
            data.to_csv(self.csvfile, index=None, header=True)
            dialog.success(True)
            self.close()
        except Exception as e:
            # Informo il dialog del fallimento
            dialog.success(False)

    def setupUi(self, ConverterWindow):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della ConverterWindow predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param ConverterWindow: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        ConverterWindow.setObjectName("ConverterWindow")
        ConverterWindow.resize(500, 200)
        ConverterWindow.setMinimumSize(QtCore.QSize(500, 200))
        ConverterWindow.setMaximumSize(QtCore.QSize(500, 200))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        ConverterWindow.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(ConverterWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ConverterWindow)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(ConverterWindow)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.label_file = QtWidgets.QLabel(ConverterWindow)
        self.label_file.setObjectName("label_file")
        self.label_file.setWordWrap(True)
        self.verticalLayout.addWidget(self.label_file)
        self.label_percorso = QtWidgets.QLabel(ConverterWindow)
        self.label_percorso.setObjectName("label_percorso")
        self.verticalLayout.addWidget(self.label_percorso)
        self.label_percorso.setWordWrap(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_load = QtWidgets.QPushButton(ConverterWindow)
        self.button_load.setObjectName("button_load")
        self.horizontalLayout.addWidget(self.button_load)
        self.button_path = QtWidgets.QPushButton(ConverterWindow)
        self.button_path.setObjectName("button_path")
        self.horizontalLayout.addWidget(self.button_path)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_save = QtWidgets.QPushButton(ConverterWindow)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout_2.addWidget(self.button_save)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.button_save.setEnabled(False)

        # SLOTS
        self.button_load.clicked.connect(lambda: self.onClickedButtonLoad())
        self.button_path.clicked.connect(lambda: self.onClickedButtonPath())
        self.button_save.clicked.connect(lambda: self.onClickedButtonSave())

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.retranslateUi(ConverterWindow)
        QtCore.QMetaObject.connectSlotsByName(ConverterWindow)

    def retranslateUi(self, ConverterWindow):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param ConverterWindow: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        ConverterWindow.setWindowTitle(_translate("ConverterWindow", "Convertitore"))
        self.label.setText(_translate("ConverterWindow", "CONVERTITORE DA XLSX A CSV"))
        self.label_file.setText(_translate("ConverterWindow", "File da convertire .xlsx: nessuno"))
        self.label_percorso.setText(_translate("ConverterWindow", "Percorso di salvataggio .csv: nessuno"))
        self.button_load.setText(_translate("ConverterWindow", "Seleziona File"))
        self.button_path.setText(_translate("ConverterWindow", "Seleziona Percorso Salvataggio"))
        self.button_save.setText(_translate("ConverterWindow", "Converti e Salva"))
