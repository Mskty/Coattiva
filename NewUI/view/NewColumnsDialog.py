from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

class NewColumnsDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # Inizializzazione con parent
        super().__init__(parent)
        self.setupUi(self)

    def setContent(self):
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(0, 0, QTableWidgetItem("NuovoContribuente"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Campo che vale 0 o 1 a seconda che il contribuente associato sia un nuovo soggetto per ABACO"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(1, 0, QTableWidgetItem("Cap"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("L'indirizzo di residenza testuale non è gestibile dal modello quindi è stato estrapolato il CAP"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(2, 0, QTableWidgetItem("Estero"))
        self.tableWidget.setItem(2, 1, QTableWidgetItem("Campo che vale 0 o 1 a seconda che il contribuente abbia un indirizzo di residenza estero"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(3, 0, QTableWidgetItem("RapportoImporto"))
        self.tableWidget.setItem(3, 1, QTableWidgetItem("Campo che contiene il rapporto tra il valore dei titoli ancora da pagare da parte del contribuente precedenti alla data del ruolo e il valore dei titoli che avava invece già interamente saldato ad ABACO"))
        self.tableWidget.insertRow(self.tableWidget.rowCount())
        self.tableWidget.setItem(4, 0, QTableWidgetItem("RapportoDovutoAperti"))
        self.tableWidget.setItem(4, 1, QTableWidgetItem("Campo che contiene il rapporto tra l'importo ancora da pagare da parte del contribuente e il loro valore originario prima dei pagamenti"))

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
        self.tableWidget.setColumnCount(2)
        # Setting header
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Colonna"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Significato"))

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.retranslateUi(MetricheDialog)
        QtCore.QMetaObject.connectSlotsByName(MetricheDialog)

        self.setContent()

    def retranslateUi(self, MetricheDialog):
        _translate = QtCore.QCoreApplication.translate
        MetricheDialog.setWindowTitle(_translate("MetricheDialog", "Informazioni sull'elaborazione'"))
        self.label.setText(_translate("MetricheDialog", "COLONNE GENERATE"))
        self.label_2.setText(_translate("MetricheDialog", "I titoli storici, una volta puliti ed aggregati per essere portati alla stesso tracciato dei titoli recenti su cui verrà utilizzato il modello addestrato, vengono ulteriormente elaborati per estrarre maggiori informazioni dati dati tramite nuove colonne e rendere le colonne testuali come IndirizzoResidenza numeriche. \n"
                                                          "A seguire è riportata una descrizione di tali proprietà:"))