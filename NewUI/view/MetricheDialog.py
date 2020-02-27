# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MetricheDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

class MetricheDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # Inizializzazione con parent
        super().__init__(parent)
        self.setupUi(self)

    def setContent(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Accuratezza"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Indica la percentuale di esempi che il modello addestrato ha predetto correttamente"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Precisione"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(1, 2, QTableWidgetItem("Indica la precisione del modello sulle predizioni positive, ovvero quanti degli esempi predetti come positivi avevano anche label positiva e sono quindi corretti"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Recall"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(2, 2, QTableWidgetItem("Indica la percentuale di esempi con label postiva che il modello addestrato ha predetto correttamente come positivi"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(3, 0, QTableWidgetItem("F1 Score"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("0-100%"))
        self.tableWidget.setItem(3, 2, QTableWidgetItem("Si tratta della media armonica tra precisione e recall. Assume il valore 100 quando sia precisione che recall valgono 100 (indicando che il modello è perfetto) mentre assume il valore 0 quando precisione o recall valgono 0. Fornisce quindi una punteggio generale alle prestazioni del modello"))

        # Imposto la grandezza delle righe
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()

    def setupUi(self, MetricheDialog):
        MetricheDialog.setObjectName("MetricheDialog")
        MetricheDialog.resize(858, 400)
        MetricheDialog.setMinimumSize(QtCore.QSize(858, 400))
        font = QtGui.QFont()
        font.setFamily("Arial")
        MetricheDialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(MetricheDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MetricheDialog)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
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
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
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

        self.retranslateUi(MetricheDialog)
        QtCore.QMetaObject.connectSlotsByName(MetricheDialog)

        self.setContent()

    def retranslateUi(self, MetricheDialog):
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



