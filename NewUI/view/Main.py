# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testtable.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from model.TableModel import *
from utility.utility import *
from view.FirstWindow import *


class MainWindow(QMainWindow):
    # Funzioni proprie della mainui

    # Contiene la variabile self.table.model

    def __init__(self, tablemodel):
        # Inizializzazione con modello
        super().__init__()
        self.setupUi(self)
        self.tablemodel = tablemodel
        self.table.setModel(tablemodel)

    def openFirstWindow(self):
        # apertura schermata inziale
        self.hide()
        FirstWindow(self).show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableView(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(10, 11, 781, 531))
        self.table.setObjectName("table")
        self.sample = QtWidgets.QCheckBox(self.centralwidget)
        self.sample.setGeometry(QtCore.QRect(10, 550, 81, 17))
        self.sample.setObjectName("sample")
        self.normalize = QtWidgets.QCheckBox(self.centralwidget)
        self.normalize.setGeometry(QtCore.QRect(100, 550, 81, 17))
        self.normalize.setObjectName("normalize")
        self.restore = QtWidgets.QPushButton(self.centralwidget)
        self.restore.setGeometry(QtCore.QRect(710, 550, 75, 23))
        self.restore.setObjectName("restore")
        self.process = QtWidgets.QPushButton(self.centralwidget)
        self.process.setGeometry(QtCore.QRect(620, 550, 75, 23))
        self.process.setObjectName("process")

        self.process.clicked.connect(lambda: self.openFileNameDialog())


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sample.setText(_translate("MainWindow", "Downsample"))
        self.normalize.setText(_translate("MainWindow", "Normalize"))
        self.restore.setText(_translate("MainWindow", "Restore"))
        self.process.setText(_translate("MainWindow", "Process"))


if __name__ == "__main__":
    import sys
    import pandas as pd

    # test data
    df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                       'b': [100, 200, 300],
                       'c': ['a', 'b', 'c']})

    # Instanziazione app e mainwindow
    app = QtWidgets.QApplication(sys.argv)
    tablemodel = TableModel(df)
    mainwindow = MainWindow(tablemodel)

    # Visualizzazione mainwindow
    #mainwindow.show()

    #inizializzazione schermata inziale
    mainwindow.openFirstWindow()

    #altro...
    tablemodel.provastampa()

    #chiusura programma
    sys.exit(app.exec_())


