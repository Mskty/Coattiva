# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WaitingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class WaitingDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, text=None):
        # Inizializzazione con parent
        super().__init__(parent)
        self.setupUi(self)
        if text is not None:
            self.label.setText(text)

    def success(self, success: bool):
        # Operazione terminata lo scrivo e permetto di chiudere la finestra
        self.verticalLayout.removeWidget(self.label)
        self.label.setParent(None)
        self.verticalLayout.removeWidget(self.progressBar)
        self.progressBar.setParent(None)
        if success:
            text = "Operazione terminata con successo"
        else:
            text = "Operazione fallita"
        label=QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(label)
        button=QtWidgets.QPushButton("Chiudi")
        button.clicked.connect(lambda: self.close())
        self.verticalLayout.addWidget(button)
        #self.setWindowFlags(self.windowFlags() & QtCore.Qt.WindowCloseButtonHint)

    def setupUi(self, WaitingDialog):
        WaitingDialog.setObjectName("WaitingDialog")
        WaitingDialog.setWindowModality(QtCore.Qt.NonModal)
        WaitingDialog.resize(320, 100)
        WaitingDialog.setMinimumSize(QtCore.QSize(320, 100))
        WaitingDialog.setMaximumSize(QtCore.QSize(320, 100))
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
        self.progressBar = QtWidgets.QProgressBar(WaitingDialog)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        # Disable help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

        self.retranslateUi(WaitingDialog)
        QtCore.QMetaObject.connectSlotsByName(WaitingDialog)

    def retranslateUi(self, WaitingDialog):
        _translate = QtCore.QCoreApplication.translate
        WaitingDialog.setWindowTitle(_translate("WaitingDialog", "Attendi"))
        self.label.setText(_translate("WaitingDialog", "Attendi il completamento dell\'operazione sui dati..."))
        self.progressBar.setFormat(_translate("WaitingDialog", "%p%"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WaitingDialog = WaitingDialog()
    WaitingDialog.show()
    sys.exit(app.exec_())

