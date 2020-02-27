import os, sys
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.QtWidgets import QListView, QPushButton, QHBoxLayout, QDialog, QApplication, QVBoxLayout, QCheckBox
from testqitem import *
from model.ColumnsListModel import *


class ChecklistDialog(QDialog):
    def __init__(self, name, stringlist=None, checked=False, icon=None, parent=None):
        super(ChecklistDialog, self).__init__(parent)

        self.name = name
        self.icon = icon
        self.model = ColumnsListModel([])
        self.listView = QListView()

        self.columns=[]
        if stringlist is not None:
            for i in range(len(stringlist)):
                item = CheckableItem(stringlist[i])
                #item.setCheckState(QtCore.Qt.Checked)
                #self.model.appendRow(item)

                self.columns.append(item)

        self.model2=ColumnsListModel(self.columns)
        self.listView.setModel(self.model2)

        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.selectButton = QPushButton("Select All")
        self.unselectButton = QPushButton("Unselect All")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.selectButton)
        hbox.addWidget(self.unselectButton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.listView)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        #self.setLayout(layout)
        self.setWindowTitle(self.name)
        if self.icon is not None: self.setWindowIcon(self.icon)


    def reject(self):
        QDialog.reject(self)

    def accept(self):
        self.choices = []
        i = 0
        while self.model.item(i):
            if self.model.item(i).checkState():
                self.choices.append(self.model.item(i).text())
            i += 1
        QDialog.accept(self)

    def select(self):
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            if not item.checkState():
                item.setCheckState(True)
            i += 1

    def unselect(self):
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            item.setCheckState(False)
            i += 1

if __name__ == "__main__":
    fruits = ["Banana", "Apple", "Elderberry", "Clementine", "Fig",
        "Guava", "Mango", "Honeydew Melon", "Date", "Watermelon",
        "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi", "Lemon",
        "Nectarine", "Plum", "Raspberry", "Strawberry", "Orange"]
    app = QApplication(sys.argv)
    form = ChecklistDialog("Fruit", fruits, checked=True)
    if form.exec_():
        print("\n".join([str(s) for s in form.choices]))