# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from data.Model import *
from model.TableModel import *
from view.FirstWindow import *
from view.MainFileDialog import *
from view.LoadNewFileDialog import *
from view.WaitingDialog import *
from view.MetricheDialog import *
from view.NewColumnsDialog import *
from view.WelcomeWindow import *


class MainWindow(QMainWindow):
    """
    Classe che racchiude la finestra principale per l'utilizzo della parte di interfaccia grafica dell'applicativo.
    Viene instanziata all'inizio dell'esecuzione e racchiude un parametro che permette di accedere ai metodi della
    parte di modello attraverso un oggetto di tipo Model (parametro self.model).
    Presenta funzionalità per l'apertura delle finestre di Benvenuto (WelcomeWindow), di caricamentro dei dati storici
    (self.FirstWindow alla prima apertura e self.MainFileWindow se si vuole cambiare il file caricato una volta che era
    già stato selezionato) e di caricamento del file su cui effettuare le predizioni una volta addestrato il classificatore
    (la finestra LoadNewFile), nonche alcune finestre informative per l'utente (NewColumnsDialog e MetricheDialog).
    Gestisce gran parte delle operazioni eseguibili dall'operativo, al di fuori del caricamento dei file.
    L'accesso dell'utente a questa finestra puà essere effettuato in due modalità a seconda di quanto scelto nella
    finestra di benvenuto:
    MODALITA' ADDESTRAMENTO
    In questa modalità la classe fornisce all'utente la possibilità, una volta caricato ed elaborato il file contenente
    i titoli di credito storici, di selezionare come partizionarlo in training set e test set e rimuovere alcune colonne
    /features dall'addestramento del classificatore. Una volta partizionati i dati inziali vengono abilitati i bottoni
    radio che permettono di selezioanre alcune specifiche per l'addestramento del classificatore tra cui l'utilizzo
    di sampling sui dati per equilibrare la presenza di esempi positivi e negativi, l'utilizzo di due diverse tipologie
    di scaler per normalizzare i valori dei dati durante l'addestramento e utilizzo del classificatore e infine
    selezionare uno tra cinque algoritmi di apprendimento per addestrare e generare il classificatore. Una volta selezionate
    tali specifiche è possibile addestrare il classificatore tramite l'apposito pulsante. Al termine dell'addestramento
    verrà sbloccata la Tab Risultati in cui l'utente può visualizzare un recap delle performance del classificatore su
    training set e test set, anche attraverso grafici, inoltre verrà aggiunta alle tabelle nelle sezioni Train e Test
    una nuova colonna 'Predizione' contentente l'output del classificatore per ogni riga presente nelle tabelle.
    (nel caso venga utilizzato nell'addestramento un algoritmo di sampling allora la tabella nella sezione di train verrà
    aggiornata rappresentando il nuovo training set che è stato utilizzato per addestrare il classificatore)
    Viene inoltre abilitata la Tab Utilizza che permette di caricare un nuovo file di dati su cui ottenere le predizioni
    da parte del classificatore addestrato, anche tali dati saranno visualizzabili su una tabella nella rispettiva sezione.
    Per ogni tabella presente è possibile esportare in file .csv i contenuti (incluse le predizioni se prodotte) tramite
    l'apposito pulsante sottostante.
    E' possibile premere il pulsante reset, oppure caricare un nuovo file per l'addestramento, se si vuole addestrare
    un classificatore con specifiche diverse.
    E' infine fornita la possibilitò di salvare il classificatore già addestrato in un file .sav premendo il pulsante
    apposito nella sezione Main della finestra.
    MODALITA' UTILIZZO
    In questa modalità la finestra espone unicamente le funzionalità presenti nella Tab Utilizza, come sono state descritte
    nella precedente modalità. Per accedere a questa modalità è necessario caricare un file .sav dalla finestra di Benvenuto
    contentente un classificatore già addestrato salvato precedentemente all'interno dell'applicativo.

    PRAMETRI:
    self.model: oggetto di classe Model che fornisce alla classe e a tutta la parte view la possibilità di eseguire
                operazioni sui dati gestiti dalle classi del package data. Viene inizializzato all'avvio dell'applicativo
    self.datatable: oggetto di classe TableModel che costituisce il modello che permette la gestione e la visualizzazione
                    dei dati all'interno del QTableView presente nella Tab Data  (self.table_data), inzialmente assume
                    il valore NONE in quanto i dati verranno caricati successivamente alla creazione dell'oggetto Mainwindow
    self.traintable: oggetto di classe TableModel che costituisce il modello che permette la gestione e la visualizzazione
                    dei dati all'interno del QTableView presente nella Tab Train  (self.table_train), inzialmente assume
                    il valore NONE in quanto i dati del training set verranno generati successivamente alla creazione
                    dell'oggetto Mainwindow
    self.testtable: oggetto di classe TableModel che costituisce il modello che permette la gestione e la visualizzazione
                    dei dati all'interno del QTableView presente nella Tab Test  (self.table_test), inzialmente assume
                    il valore NONE in quanto i dati del test set verranno generati successivamente alla creazione
                    dell'oggetto Mainwindow
    self.usetable: oggetto di classe TableModel che costituisce il modello che permette la gestione e la visualizzazione
                    dei dati all'interno del QTableView presente nella Tab Utilizza (self.table_use), inzialmente assume
                    il valore NONE in quanto i nuovi dati da predire verranno caricati successivamente alla creazione
                    dell'oggetto MainWindow
    self.splitwidgetsize: variabile utilizzata per la gestione della larghezza della ScrollArea self.mainlistsplit
                          che conterrà i bottoni radio per generare trainingset e testset. Inizialmente None perchè tali
                          bottoni verranno gennerati successivamente alla creazione dell'oggetto MainWindow
    self.columnswidgetsize: variabile utilizzata per la gestione della larghezza della ScrollArea self.mainlistcolumn
                            che conterrà le checkbox per escludere delle colonne/features dall'addestramento del
                            classificatore. Inizialmente None perchè tali
                            checkbox verranno gennerate successivamente alla creazione dell'oggetto MainWindow

    """

    def __init__(self):
        # Inizializzazione
        super().__init__()
        self.setupUi(self)

        # Modello di business
        self.model = Model()

        # Modelli vuoti delle tabelle
        self.datatable: TableModel = None
        self.traintable: TableModel = None
        self.testtable: TableModel = None
        self.usetable: TableModel = None

        # Variabile larghezza scrollareas
        self.splitwidgetsize = None
        self.columnwidgetsize = None

    """-------------------------------------------------SCROLLARES------------------------------------------------"""

    def clearScrollArea(self, layout: QtWidgets.QVBoxLayout):
        """
        @PRE: nessuna
        Elimina dal QVBoxLayout del parametro passato layout tutti i widget presenti, ripristinando il layout della
        ScrollArea allo stato iniziale vuoto.
        :param layout: layuout di una ScrollArea
        :return: None
        """
        # PER ELIMINARE I WIDGET DA UN LAYOUT NELLA SCROLLAREA
        for i in reversed(range(layout.count())):
            widgetToRemove = layout.itemAt(i).widget()
            # remove it from the layout list
            layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)

    def onClickedColumnCheckbox(self):
        """
        @PRE è stata cliccata una checkbox all'interno di self.main_list_columns_layout
        @PRE self.main_list_columns è abilitato
        Abilita o disabilita la colonna corrispondente al testo della checkbox cliccata dalle tabelle self.datatable e
        self.traintable, self.testable (se presenti) utilizzando i rispettivi metodi di self.model
        :return: None
        """
        # Abilita o disabilita la colonna nelle tabelle del model dopo aver premuto su una checkbox
        # Ottengo la checkbox che è stata cliccata
        checkbox = self.sender()
        if checkbox.isChecked():
            self.model.enablecolumn(checkbox.text())
        else:
            self.model.disablecolumn(checkbox.text())
        # Refresh modelli per visualizzare le modifiche
        self.datatable.updatemodel()
        print("update data")
        try:
            self.traintable.updatemodel()
            print("update train")
        except:
            pass
        try:
            self.testtable.updatemodel()
            print("update test")
        except:
            pass

    def add_checkbox_columns(self, column: str):
        """
        @PRE: è stata invocata la funzione self.firstSetup
        Aggiunge al layout della ScrollArea self.main_list_columns una checkbox checkata rappresentativa del nome della
        colonna passato attraverso il parametro column, inoltre connette tale checkbox alla funzione SLOT
        self.onClickedColumnCheckbox.
        :param column: nome di una colonna stringa
        :return: None
        """
        # Aggiunge checkbox al layout della scrollview main_list_columns
        checkbox = QtWidgets.QCheckBox(column)
        # Imposto la checkbox come checkata
        checkbox.setCheckState(QtCore.Qt.Checked)
        # Collego la funzione SLOT alla checkbox
        checkbox.toggled.connect(lambda: self.onClickedColumnCheckbox())
        self.main_list_columns_layout.addWidget(checkbox)

    def onClickedSplitRadio(self):
        """
        @PRE: è stato cliccato un RadioButton all'interno della ScrollArea self.columns.splits
        @PRE: self.main_list_splits è abilitato
        Fa generale al modello le partizioni del dataset train e test come selezionato dall'utente
        dopodichè le utilizza per creare ed  abilita tabelle self.traintable e self.testtable (se presente),
        creando i rispettivi TableModel e setta le label per quelle tabelle,
        inoltre abilita la parte sottostante di comandi nella schermata principale (Addestramento modello)
        :return: None
        """
        # Ottengo il RadioButton che è stato cliccato
        radio: QtWidgets.QRadioButton = self.sender()
        if radio.isChecked():
            date = radio.objectName()
            self.model.generate_train_test(date)

            # Ho generato train e test nel modello ora genero le tabelle

            # Genero traintable
            self.traintable = TableModel(self.model.train.enabledcolumns)
            self.table_train.setModel(self.traintable)
            # Inserisco il testo nelle tab di train
            traininfo = self.model.get_train_info()
            self.setlabelsTrain(traininfo[0], traininfo[1], traininfo[2])
            # Abilito la tab train
            self.enableTrain()

            # Controllo se è stato generato il testset altrimenti non genero la tabella testtable
            if self.model.is_test_present():
                # Abilito tab test
                self.testtable = TableModel(self.model.test.enabledcolumns)
                self.table_test.setModel(self.testtable)
                # Inserisco il testo nelle tab di test
                testinfo = self.model.get_test_info()
                self.setlabelsTest(testinfo[0], testinfo[1], testinfo[2])
                # Abilito la tab test
                self.enableTest()
            else:
                # disabilito tab test
                self.testtable = None
                self.disableTest()

            # Abilito radio e addestra modello
            self.enableradios()
            self.enableMainButtonTrain()

    def add_radio_split(self, ruolo: str, esempi: int):
        """
        @PRE: è stata invocata la funzione self.firstSetup
        Aggiunge al layout della ScrollArea self.main_list_splits un RadioButton non checkato rappresentativo dello
        split che si vuole selezionare tra trainset e testset, inoltre connette tale RadioButton alla funzione SLOT
        self.onClickedSplitRadio
        :param ruolo: stringa rappresentante la data di un ruolo
        :param esempi: intero rappresentante il numero di titoli di credito aggregati contenuti dalla prima data
                       presente nei dati storici fino a quella contenuta nel parametro ruolo
        :return: None
        """
        # Aggiunge radio button al layout della ScrollView main_list_columns
        totali = self.model.data.get_rows()
        train = esempi
        test = totali - esempi
        # Scrivo il testo che accompagna il RadioButton
        if test > 0:
            radio = QtWidgets.QRadioButton(
                "Fino a ruolo: " + ruolo + "\nEsempi per training: " + str(train) + "\nEsempi per test: " + str(test))
        else:
            radio = QtWidgets.QRadioButton(
                "Fino a ruolo: " + ruolo + "\nEsempi per training: " + str(train) + "\nTest set vuoto \n(migliori "
                                                                                    "performance)")
        # utilizzo l'objectname per salvare il dato del ruolo
        radio.setObjectName(ruolo)
        # Collego la funzione SLOT al RadioButton
        radio.toggled.connect(lambda: self.onClickedSplitRadio())
        self.main_list_split_layout.addWidget(radio)

    """-------------------------------------------------COMBOBOXES------------------------------------------------"""

    def setOnClickDataCombo(self):
        """
        @PRE: è stato selezionato un valore tra quelli presenti nella ComboBox self.combo_data
        In base al valore selezionato nella ComboBox imposta il parametro data di self.datatable per visualizzare nella
        tabella il corretto DataFrame presente in self.model.data
        :return: None
        """
        # Imposta il corretto modello di tabella dati quando viene cambiata la selezione
        text = self.combo_data.currentText()
        if text == "Dati Originali":
            self.datatable.data = self.model.data.original_df
        elif text == "Dati Aggregati":
            self.datatable.data = self.model.data.cleaned_df
        elif text == "Dati Preparati":
            self.datatable.data = self.model.data.enabledcolumns
        # Aggiorno tabella
        self.datatable.updatemodel()

    def setDataCombo(self):
        """
        @PRE: è stata invocata la funzione self.firstSetup
        Imposta i valori contenuti nella ComboBox self.combo_data e collega la collega alla funzione SLOT
        self.onClickDataCombo
        :return: None
        """
        # Imposta il contenuto e slots della combobox nella parte dati
        self.combo_data.clear()
        names = ["Dati Originali", "Dati Aggregati", "Dati Preparati"]
        self.combo_data.addItems(names)
        # Size
        self.combo_data.setMinimumWidth(102)
        # Imposto come default l'opzione preparati
        index = self.combo_data.findText("Dati Preparati")
        self.combo_data.setCurrentIndex(index)
        self.setOnClickDataCombo()
        # SLOT
        self.combo_data.activated.connect(lambda: self.setOnClickDataCombo())

    def setOnClickUseCombo(self):
        """
        @PRE: è stato selezionato un valore tra quelli presenti nella ComboBox self.combo_use
        In base al valore selezionato nella ComboBox imposta il parametro data di self.usetable per visualizzare nella
        tabella il corretto DataFrame presente in self.model.usedata
        :return: None
        """
        # Imposta il corretto modello di tabella utilizza quando viene cambiata la selezione
        text = self.combo_use.currentText()
        if text == "Dati Originali":
            self.usetable.data = self.model.usedata.original_df
        elif text == "Dati Aggregati":
            self.usetable.data = self.model.usedata.cleaned_df
        elif text == "Dati Preparati":
            self.usetable.data = self.model.usedata.enabledcolumns
        # Aggiorno tabella
        self.usetable.updatemodel()

    def setUseCombo(self):
        """
        @PRE: è stata invocata la funzione self.useFileSetup
        Imposta i valori contenuti nella ComboBox self.combo_use e collega la collega alla funzione SLOT
        self.onClickUseCombo
        :return: None
        """
        # Imposta il contenuto e slots della combobox nella parte utilizza
        self.combo_use.clear()
        # Controllo di che tipo sono i dati caricati
        oldnewtype = self.model.get_use_datafiletype()
        if oldnewtype == "Dati Storici":
            names = ["Dati Originali", "Dati Aggregati", "Dati Preparati"]
        elif oldnewtype == "Dati Recenti":
            names = ["Dati Originali", "Dati Preparati"]

        self.combo_use.addItems(names)
        # Size
        self.combo_use.setMinimumWidth(102)
        # Imposto come default l'opzione preparati
        index = self.combo_use.findText("Dati Preparati")
        self.combo_use.setCurrentIndex(index)
        self.setOnClickUseCombo()
        # SLOT
        self.combo_use.activated.connect(lambda: self.setOnClickUseCombo())

    """------------------------------------------GUI SETUPS--------------------------------------------------------"""

    def resetUI(self):
        """
        @PRE: è stata invocata la funzione self.firstSetup
        Resetta soltanto gli elementi della UI allo stato in cui dovrebbero essere all'apertura dell'applicazione
        in modalità addestramento lasciando inalterate le variabili di modello, chiamando varie funzioni
        per abilitarli o disabilitarli.
        :return: None
        """
        # Radios (prima operazione perchè setchecked da problemi chiamando il segnale)
        self.sampling1.setChecked(True)
        self.scaling1.setChecked(True)
        self.algorithm1.setChecked(True)
        self.disableradios()

        # scroll areas
        self.enablescrolls()
        # Tabs
        self.disableTrain()
        self.disableTest()
        self.disableRisultati()
        self.disableUtilizza()
        # Buttons
        self.disableMainButtonSave()
        self.disableMainButtonTrain()
        self.disableUseApply()
        self.disableUseExport()
        # Combobox
        self.disableUseCombo()
        self.combo_use.clear()

        # Reset contenuti tab Utilizza:
        self.table_use.setModel(None)
        self.setlabelUtilizzaFilename("nessuno")

    def firstSetup(self):
        """
        @PRE: è stata invocata la funzione self.openFirstWindow o self.openLoadMainFileWindow
        @PRE: è stato caricato un file contentente i titoli storici dall'utente attraverso la finestra FirstWindow
              e i dati contenuti sono stati caricati ed elaborati nell'oggetto Model contenuto in self.model
        Esegue il setup inziale della GUI una volta caricato il file di addestramento nella firstwindow avendo quindi
        già generato il dataset all'interno del modello (self.model).
        Crea quindi la tabella data con rispettivo TableModel nella view.
        Popola infine le scrollview con le checkbox per le colonne e i possibili split dei dati in train e test
        attraverso le relative funzioni
        Serve anche come reset nel caso venga caricato un nuovo file premento il pulsante 'Caricamento nuovo file'
        :return: None
        """

        """
        Questa funzione esegue il setup inziale dell'applicativo in modalità ADDESTRAMENTO
        """

        # Resetto le tab e i modelli nel caso siano popolati
        self.resetUI()
        self.datatable: TableModel = None
        self.traintable: TableModel = None
        self.testtable: TableModel = None
        self.usetable: TableModel = None

        # Setta le label prendendo dati dal modello
        type = self.model.get_traintype()
        self.setlabelMainType(type)
        filename = self.model.get_datafilename()
        self.setlabelMainFilename(filename)
        # Settaggio della label ratio
        datatext = self.model.get_data_info()
        total: int = datatext[0]
        positive_perc: float = (datatext[1] / total) * 100
        negative_perc: float = (datatext[2] / total) * 100
        self.setlabelFileLabelRatio(positive_perc, negative_perc)

        # TableModel e testo delle label per la tab Dati
        self.datatable = TableModel(self.model.data.enabledcolumns)
        self.table_data.setModel(self.datatable)
        datainfo = self.model.get_data_info()
        self.setlabelsData(datainfo[0], datainfo[1], datainfo[2])

        # Imposto la ComboBox nel Tab dati
        self.setDataCombo()

        # Impostazione lista colonne nella scroll area
        # Pulisco prima il layout
        self.clearScrollArea(self.main_list_columns_layout)
        # Popolo il layout
        columnlist = self.model.get_column_names()
        for i in columnlist:
            self.add_checkbox_columns(i)
        self.main_list_columns.widget().adjustSize()
        if self.columnwidgetsize is None:
            self.main_list_columns.setMinimumWidth(self.main_list_columns.widget().width() + 30)
            # Salvo larghezza iniziale widget per reset
            self.columnwidgetsize = self.main_list_columns.minimumWidth()
        else:
            self.main_list_columns.setMinimumWidth(self.columnwidgetsize)

        # impostazione lista split nella scroll area
        # Pulisco prima il layout
        self.clearScrollArea(self.main_list_split_layout)
        # Popolo il layout
        ruoli, nesempi = self.model.get_train_test_splits()  # Lunghi uguale per costruzione
        for i in range(len(ruoli)):
            self.add_radio_split(ruoli[i], nesempi[i])
        self.main_list_split.widget().adjustSize()
        if self.splitwidgetsize is None:
            self.main_list_split.setMinimumWidth(self.main_list_split.widget().width() + 30)
            # Salvo larghezza iniziale widget per reset
            self.splitwidgetsize = self.main_list_split.minimumWidth()
        else:
            self.main_list_split.setMinimumWidth(self.splitwidgetsize)

    def useSetup(self):
        """
        @PRE: è stato caricato un file contentente un classificare addestrato dall'utente attraverso la finestra WelcomeWindow
              e tale classificatore è stato deserializzato e caricato nell'oggetto Model self.model
        Esegue il setup inziale della GUI una volta caricato un file di classificatore nella WelcomeWindow avendo quindi
        già deserializzato un oggetto di tipo AlgorithmPipeline nel modello (self.model).
        Rende quindi utilizzabile solo la tab Utilizza disabilitando tutte le altre attraverso le rispettive funzioni
        :return: None
        """
        """
         Questa funzione esegue il setup inziale dell'applicativo in modalità UTILIZZA, quindi con classificatore già addestrato
        """
        # Disabilito tutte le tabs tranne utilizza
        self.disableMain()
        self.disableData()
        self.disableTrain()
        self.disableTest()
        self.disableRisultati()
        # Abilito utilizza
        self.enableUtilizza()
        # Disabilito i bottoni non ancora attivabili finchè non viene caricato un file
        self.disableUseApply()
        self.disableUseExport()
        # Disabilito la combobox finchè non viene caricato un file
        self.disableUseCombo()
        # Imposto Utilizza come tab corrente
        self.TabWidget.setCurrentIndex(5)
        # Imposto la label del tipo del modello
        self.setlabelUtilizzaType(self.model.get_algorithmtype())

    def useFileSetup(self):
        """
        @PRE: è stata invocata la funzione self.openLoadNewFileWindow
        @PRE: è stato caricato un file contentente i titoli storici o recenti dall'utente attraverso la finestra LoadNewFile
              e i dati contenuti sono stati caricati ed elaborati nell'oggetto Model contenuto in self.model
        Esegue il setup della tab Utilizza una volta caricato in self.model il file dall'utente tramite  la finestra
        LoadNewFile.
        Viene generata la tabella self.usetable su cui visualizzare i dati caricati dall'utente ed elaborati nel modello.
        Viene abilitata la possibilità di ottenere predizioni su tali dati ed esportarli in formato csv tramite
        gli appositi bottoni.
        Infine viene impostata la ComboBox per visualizzare il file caricato nei diversi stati dell'elaborazione.
        :return: None
        """
        # Imposto la tabella per la visualizzazione del file caricato, vengono considerate le solo colonne elaborate
        self.usetable = TableModel(self.model.usedata.enabledcolumns)
        self.table_use.setModel(self.usetable)
        # Imposto la label per nome file
        filename = self.model.get_use_datafilename()
        self.setlabelUtilizzaFilename(filename)
        # Abilito il bottone per esportare i dati caricati
        # Abilito il bottone per l'utilizzo del modello sui nuovi dati e la combobox
        self.enableUseApply()
        self.enableUseExport()
        # Inizializzo la combobox
        self.enableUseCombo()
        self.setUseCombo()

    """--------------------------------------------------APERTURA FINESTRE-------------------------------------------"""

    def openWelcomeWindow(self):
        """
        @PRE: nessuna
        Visualizza la schermata inziale di avvio applicativo WelcomeWindow
        :return: None
        """
        # apertura schermata di selezione modalità di utilizzo con passaggio della mainwindow come parent
        window = WelcomeWindow(self)
        self.hide()
        window.show()

    def openFirstWindow(self):
        """
        @PRE: è stato premuto il pulsante per accedere alla modalità ADDESTRAMENTO dalla WelcomeWindow
        Visualizza la schermata inziale di avvio applicativo in modalità ADDESTRAMENTO FirstWindow
        :return: None
        """
        # apertura schermata inziale di addestramento con passaggio della mainwindow come parent
        window = FirstWindow(self)
        self.hide()
        window.show()

    def openMainFileWindow(self):
        """
        @PRE: è stata invocata la funzione self.firstSetup oppure self.useSetup
        Visualizza la finestra MainFileWindow
        :return: None
        """
        # apertura schermata di caricamento di nuovo file con passaggio della mainwindow come parent
        dialog = MainFileWindow(self)
        dialog.exec_()

    def openLoadNewFileWindow(self):
        """
        @PRE: è stata invocata la funzione self.buttonTrainModel
        Visualizza la finestra LoadNewFile
        :return: None
        """
        # apertura schermata nuovo file per utilizzo
        dialog = LoadNewFile(self.model.workingalgorithm.type, self)
        dialog.exec_()

    def openSaveDialog(self):
        """
        @PRE: nessuna
        Apre una finestra che permette all'utente di selezionare un percorso di salvataggio per un file di tipo csv
        :return: nome del percorso di salvataggio selezionato dall'utente
        """
        # Apre un dialog per ottenere un percorso su cui salvare un file
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Crea/Salva File csv", "",
                                                  "Csv Files (*.csv)", options=options)
        return filename

    """----------------------------------------Abilita disabilita tabs-----------------------------------------------"""

    def enableMain(self):
        self.TabWidget.setTabEnabled(0, True)

    def disableMain(self):
        self.TabWidget.setTabEnabled(0, False)

    def enableData(self):
        self.TabWidget.setTabEnabled(1, True)

    def disableData(self):
        self.TabWidget.setTabEnabled(1, False)

    def enableTrain(self):
        self.TabWidget.setTabEnabled(2, True)

    def disableTrain(self):
        self.TabWidget.setTabEnabled(2, False)

    def enableTest(self):
        self.TabWidget.setTabEnabled(3, True)

    def disableTest(self):
        self.TabWidget.setTabEnabled(3, False)

    def enableRisultati(self):
        self.TabWidget.setTabEnabled(4, True)

    def disableRisultati(self):
        self.TabWidget.setTabEnabled(4, False)

    def enableUtilizza(self):
        self.TabWidget.setTabEnabled(5, True)

    def disableUtilizza(self):
        self.TabWidget.setTabEnabled(5, False)

    """ -------------------------------------Abilita disabilita radio nelle groupbox-------------------------------"""

    def enableradios(self):
        self.groupBox.setEnabled(True)
        self.groupBox_2.setEnabled(True)
        self.groupBox_3.setEnabled(True)

    def disableradios(self):
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(False)
        self.groupBox_3.setEnabled(False)

    """-------------------------Abilita disabilita contenuto delle scroll areas-------------------------------------"""

    def enablescrolls(self):
        self.main_list_columns.widget().setEnabled(True)
        self.main_list_split.widget().setEnabled(True)

    def disablescrolls(self):
        self.main_list_columns.widget().setEnabled(False)
        self.main_list_split.widget().setEnabled(False)

    """-------------------------Abilita disabilita contenuto delle combo boxes--------------------------------------"""

    def enableUseCombo(self):
        self.combo_use.setEnabled(True)

    def disableUseCombo(self):
        self.combo_use.setEnabled(False)

    """---------------------------------------Abilita disabilita bottoni--------------------------------------------"""

    def enableMainButtonTrain(self):
        self.main_button_train.setEnabled(True)

    def disableMainButtonTrain(self):
        self.main_button_train.setEnabled(False)

    def enableMainButtonSave(self):
        self.main_button_save.setEnabled(True)

    def disableMainButtonSave(self):
        self.main_button_save.setEnabled(False)

    def enableUseApply(self):
        self.use_apply.setEnabled(True)

    def disableUseApply(self):
        self.use_apply.setEnabled(False)

    def enableTestGraphButtons(self):
        self.button_test_matrix.setEnabled(True)
        self.button_test_auc.setEnabled(True)
        self.button_test_prc.setEnabled(True)

    def disableTestGraphButtons(self):
        self.button_test_matrix.setEnabled(False)
        self.button_test_auc.setEnabled(False)
        self.button_test_prc.setEnabled(False)

    def enableUseExport(self):
        self.use_export.setEnabled(True)

    def disableUseExport(self):
        self.use_export.setEnabled(False)

    """ ----------------------------------------------Set testi delle labels--------------------------------------- """

    # Tab Main
    def setlabelMainType(self, type: str):
        self.main_type.setText("Tipologia di titoli di credito: " + type)

    def setlabelMainFilename(self, filename: str):
        self.main_filename.setText("File aperto per l'addestramento: " + filename)

    def setlabelFileLabelRatio(self, positivelabel: float, negativelabel: float):
        self.filelabelratio.setText(
            "1) I titoli contenuti nel training set hanno label al {0:.2f}".format(positivelabel) +
            "% positiva e {0:.2f}".format(negativelabel) +
            "% negativa, è possibile selezionare un algoritmo di sampling per equilibrarli.")

    # Tab Data
    def setlabelsData(self, tot: int, pos: int, neg: int):
        self.label_data_total.setText(str(tot))
        self.label_data_positive.setText(str(pos))
        self.label_data_negative.setText(str(neg))

    # Tab Train
    def setlabelsTrain(self, tot: int, pos: int, neg: int):
        self.label_train_total.setText(str(tot))
        self.label_train_positive.setText(str(pos))
        self.label_train_negative.setText(str(neg))

    # Tab Test
    def setlabelsTest(self, tot: int, pos: int, neg: int):
        self.label_test_total.setText(str(tot))
        self.label_test_positive.setText(str(pos))
        self.label_test_negative.setText(str(neg))

    # Tab Risultati
    def setlabelsRisultati(self, type: str, totallable: int, positivelabel: float, negativelabel: float, sampling: str,
                           scaling: str, algorithm: str, ignoredcolumns: list):
        self.results_typep.setText("Tipologia di titoli di credito: " + type)
        self.results_number_examples.setText("Numero di esempi utilizzati nell'addestramento: " + str(totallable) +
                                             ", di cui {0:.2f}".format(
                                                 positivelabel) + "% con label positiva e {0:.2f}".format(
            negativelabel) + "% con label negativa")
        self.results_sampling.setText("Sampling: " + sampling)
        self.results_scaling.setText("Scaling: " + scaling)
        self.results_algorithm.setText("Algoritmo di apprendimento: " + algorithm)
        # stampa lista colonne ignorate
        self.results_ignored.setText("Proprietà o colonne ignorate: ")
        nessuna = " Nessuna"
        for item in ignoredcolumns:
            nessuna = ""
            self.results_ignored.setText(self.results_ignored.text() + item + ", ")
        self.results_ignored.setText(self.results_ignored.text() + nessuna)

    def setlabelsTrainMetrics(self, acc: float, prec: float, rec: float, f1: float):
        # punteggi passati in decimale
        acc = acc * 100
        prec = prec * 100
        rec = rec * 100
        f1 = f1 * 100
        self.train_accuracy.setText("{0:.2f}".format(acc) + "%")
        self.train_precision.setText("{0:.2f}".format(prec) + "%")
        self.train_recall.setText("{0:.2f}".format(rec) + "%")
        self.train_f1.setText("{0:.2f}".format(f1) + "%")

    def setlabelsTestMetrics(self, acc: float, prec: float, rec: float, f1: float):
        # punteggi passati in decimale
        acc = acc * 100
        prec = prec * 100
        rec = rec * 100
        f1 = f1 * 100
        self.test_accuracy.setText("{0:.2f}".format(acc) + "%")
        self.test_precision.setText("{0:.2f}".format(prec) + "%")
        self.test_recall.setText("{0:.2f}".format(rec) + "%")
        self.test_f1.setText("{0:.2f}".format(f1) + "%")

    # Tab Utilizza
    def setlabelUtilizzaType(self, type: str):
        self.use_type.setText("Tipologia di titoli di credito: " + type)

    def setlabelUtilizzaFilename(self, filename: str):
        self.use_filename.setText("File caricato: " + filename)

    """-------------------------Funzioni SLOTS di bottoni presenti all'inizializzazione---------------------------- """

    def buttonTrainModel(self):
        """
        @PRE: è stato cliccato il bottone self.main_button_train
        @PRE: è stato generato un trainset attraverso l'invocazione della funzione self.onClickedSplitRadio
        Addestra l'algoritmo sul training set chiamando il metodo del modello (self.model)
        Aggiunge la colonna predizioni sulle tabelle chiamando il modello e facendo l'update dei TableModel
        Aggiunge tutti i dati necessari sulla tab Risultati
        Le operazioni riguardanti il testset vengono fatte solo se questo è presente
        :return: None
        """

        # Apertura finestra di attesa
        text = "Attendi mentre il modello predittivo viene addestrato e testato sui dati storici"
        waitdialog = WaitingDialog(self, text, self.mapToGlobal(self.rect().center()))
        waitdialog.show()
        QtWidgets.QApplication.processEvents()

        # Addestramento modello e setup ui risultati
        self.model.train_algorithm()

        # Aggiunta predizioni trainset
        self.model.predict_train()
        # Reinizializzo il modello traintable dato che i dati potrebbero essere cambiati se utilizzato sampling
        self.traintable = TableModel(self.model.train.enabledcolumns)
        self.table_train.setModel(self.traintable)
        self.traintable.updatemodel()
        # Aggiorno le label nel caso ci sia stato undersampling o oversampling
        traininfo = self.model.get_train_info()
        self.setlabelsTrain(traininfo[0], traininfo[1], traininfo[2])

        # Labels fisse Tab risultati
        tipo = self.model.get_traintype()
        list_train = self.model.get_sampling_info()
        totallabel: int = list_train[0]
        positivelabel: float = (list_train[1] / totallabel) * 100
        negativelabel: float = (list_train[2] / totallabel) * 100
        sampling = self.model.get_sampling()
        scaling = self.model.get_scaling()
        algorithm = self.model.get_algorithm()
        disabledcolumns = self.model.get_disabledcolumns()
        self.setlabelsRisultati(tipo, totallabel, positivelabel, negativelabel, sampling, scaling, algorithm,
                                disabledcolumns)

        # Risultati trainset
        train_scores = self.model.get_train_scores()
        acc = train_scores[0]
        prec = train_scores[1]
        rec = train_scores[2]
        f1 = train_scores[3]
        self.setlabelsTrainMetrics(acc, prec, rec, f1)

        # Aggiunta predizioni e risultati testset se presente
        if self.testtable is not None:
            # Abilito grafici
            self.enableTestGraphButtons()
            # Aggiunta predizioni e risultati trainset
            self.model.predict_test()
            self.testtable.updatemodel()
            # Risultati trainset
            test_scores = self.model.get_test_scores()
            acc = test_scores[0]
            prec = test_scores[1]
            rec = test_scores[2]
            f1 = test_scores[3]
            self.setlabelsTestMetrics(acc, prec, rec, f1)
        else:
            # Disabilito grafici
            self.disableTestGraphButtons()
            # Reset risultati testset
            self.test_accuracy.setText("na")
            self.test_precision.setText("na")
            self.test_recall.setText("na")
            self.test_f1.setText("na")

        # Abilito tab risultati
        self.enableRisultati()

        # Abilito e setto label tipo per la parte utilizza
        self.enableUtilizza()
        self.setlabelUtilizzaType(self.model.get_traintype())

        # Disabilito bottone e comandi della main in quanto è richiesto il bottone reset per sbloccare
        self.disablescrolls()  # scroll areas
        self.disableradios()  # radio commands
        self.disableMainButtonTrain()  # self

        # Abilito la possibilità di salvare il modello nel main
        self.enableMainButtonSave()

        # Elaborazione terminata informo la schermata di attesa
        waitdialog.success(True)

    def buttonLoadNewTrainFile(self):
        """
        @PRE: è stato cliccato il bottone self.main_button_file
        apre la finestra MainFileWindow attraverso l'apposito metodo
        :return: None
        """
        # Chiama la mainfilewindow
        self.openMainFileWindow()

    def buttonReset(self):
        """
        @PRE: è stato cliccato il bottone self.main_button_reset
        Riporta l'applicativo in uno stato identico a quello in cui si trovata al termine dell'esecuzione della funzione
        self.firstSetup.
        per resettare il modello (self.model) invoca la sua funzione reset_settings
        :return: None
        """
        # Reset: abilita tutte le colonne, disabilita train e test set, blocca le box
        # Reset radio boxes ( prima cosa perchè il setchecked chiama il segnale)
        self.sampling1.setChecked(True)
        self.scaling1.setChecked(True)
        self.algorithm1.setChecked(True)
        self.disableradios()

        # Reset modello:
        self.model.reset_settings()

        # Reset variabili:
        self.datatable = TableModel(self.model.data.enabledcolumns)
        self.table_data.setModel(self.datatable)
        self.traintable: TableModel = None
        self.testtable: TableModel = None
        self.usetable: TableModel = None

        # Reset contenuti tab Utilizza:
        self.table_use.setModel(None)
        self.setlabelUtilizzaFilename("nessuno")

        # Reset tabs
        self.disableTrain()
        self.disableTest()
        self.disableRisultati()
        self.disableUtilizza()

        # Reset bottoni main page
        self.disableMainButtonSave()
        self.disableMainButtonTrain()

        # Reset combobox Dati
        self.setDataCombo()

        # Reset bottoni e combobox Utilizza
        self.disableUseApply()
        self.disableUseExport()
        self.disableUseCombo()
        self.combo_use.clear()

        # Abilito scroll areas con checkbox e bottoni
        self.enablescrolls()

        # Impostazione lista colonne nella scroll area
        # Pulisco prima il layout
        self.clearScrollArea(self.main_list_columns_layout)
        # Popolo il layout
        columnlist = self.model.get_column_names()
        for i in columnlist:
            self.add_checkbox_columns(i)
        self.main_list_columns.widget().adjustSize()
        self.main_list_columns.setMinimumWidth(self.columnwidgetsize)

        # impostazione lista split nella scroll area
        # Pulisco prima il layout
        self.clearScrollArea(self.main_list_split_layout)
        # Popolo il layout
        ruoli, nesempi = self.model.get_train_test_splits()  # Lunghi uguale per costruzione
        for i in range(len(ruoli)):
            self.add_radio_split(ruoli[i], nesempi[i])
        self.main_list_split.widget().adjustSize()
        self.main_list_split.setMinimumWidth(self.splitwidgetsize)

    def buttonSave(self):
        """
        @PRE: è stato cliccato il bottone self.main_button_save
        Permette all'utente di salvare il classificatore addestrato su file .sav.
        Apre un FileDialog per selezionare la posizione in cui salvare il file, se la posizione è valida allora invoca
        la funzione del modello per serializzare il classificatore addestrato e salvarlo alla posizione indicata.
        :return: None
        """
        # chiama un dialog di salvataggio per ottere il path di salvataggio poi invoca la funzione del modello
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Salvataggio del modello addestrato", "",
                                                  "Model Files (*.sav)", options=options)
        if filename:
            dialog = WaitingDialog(self, "Attendi il salvataggio del modello addestrato")
            dialog.show()
            QtWidgets.QApplication.processEvents()
            self.model.serialize_algorithm(filename)
            dialog.success(True)

    def buttonDataPreprocessInfo(self):
        """
        @PRE: è stato cliccato il bottone self.data_preprocess_info
        Visualizza una finestra informativa di tipo NewColumnsDialog
        :return: None
        """
        # chiama NewColumnsDialog per ottenere informazioni sulle colonne aggiunte
        dialog = NewColumnsDialog()
        dialog.exec_()

    def buttonDataExport(self):
        """
        @PRE: è stato cliccato il bottone self.data_export
        Permette all'utente di salvare su file csv i dati presenti nella tabella self.datatable
        chiama la funzione self.openSaveDialog per ottenere il percorso di salvataggio del file csv, poi invoca la
        funzione del modello (self.model) per generare il file csv con i dati
        :return: None
        """
        # chiama opensave dialog per ottere il path di salvataggio poi invoca la funzione del modello per salvare
        filepath = self.openSaveDialog()
        try:
            self.model.export_data(filepath)
        except:
            pass

    def buttonTrainExport(self):
        """
        @PRE: è stato cliccato il bottone self.train_export
        Permette all'utente di salvare su file csv i dati presenti nella tabella self.traintable
        chiama la funzione self.openSaveDialog per ottenere il percorso di salvataggio del file csv, poi invoca la
        funzione del modello (self.model) per generare il file csv con i dati
        :return: None
        """
        # chiama opensave dialog per ottere il path di salvataggio poi invoca la funzione del modello per salvare
        filepath = self.openSaveDialog()
        try:
            self.model.export_trainset(filepath)
        except:
            pass

    def buttonTestExport(self):
        """
        @PRE: è stato cliccato il bottone self.test_export
        Permette all'utente di salvare su file csv i dati presenti nella tabella self.testtable
        chiama la funzione self.openSaveDialog per ottenere il percorso di salvataggio del file csv, poi invoca la
        funzione del modello (self.model) per generare il file csv con i dati
        :return: None
        """
        # chiama opensave dialog per ottere il path di salvataggio poi invoca la funzione del modello per salvare
        filepath = self.openSaveDialog()
        try:
            self.model.export_testset(filepath)
        except:
            pass

    def buttonTrainMatrix(self):
        """
        @PRE: è stato cliccato il bottone self.button_train_matrix
        Visualizza a schermo il grafico della confusion matrix per il trainset utilizzando il rispettivo metodo del
        modello
        :return: None
        """
        # grafico conf matrix train
        self.model.get_confusion_matrix_train()

    def buttonTrainRoc(self):
        """
        @PRE: è stato cliccato il bottone self.button_train_auc
        Visualizza a schermo il grafico della curva roc-auc per il trainset utilizzando il rispettivo metodo del
        modello
        :return: None
        """
        # grafico roc train
        self.model.get_auc_curve_train()

    def buttonTrainPrc(self):
        """
        @PRE: è stato cliccato il bottone self.button_train_prc
        Visualizza a schermo il grafico della curva precision-recall per il trainset utilizzando il rispettivo metodo
        del modello
        :return: None
        """
        # grafico prc train
        self.model.get_prc_curve_train()

    def buttonTestMatrix(self):
        """
        @PRE: è stato cliccato il bottone self.button_test_matrix
        Visualizza a schermo il grafico della confusion matrix per il testset utilizzando il rispettivo metodo del
        modello
        :return: None
        """
        # grafico conf matrix train
        self.model.get_confusion_matrix_test()

    def buttonTestRoc(self):
        """
        @PRE: è stato cliccato il bottone self.button_test_auc
        Visualizza a schermo il grafico della curva roc-auc per il testset utilizzando il rispettivo metodo del
        modello
        :return: None
        """
        # grafico roc train
        self.model.get_auc_curve_test()

    def buttonTestPrc(self):
        """
        @PRE: è stato cliccato il bottone self.button_test_prc
        Visualizza a schermo il grafico della curva precision-recall per il testset utilizzando il rispettivo metodo del
        modello
        :return: None
        """
        # grafico prc train
        self.model.get_prc_curve_test()

    def buttonResultsInfo(self):
        """
        @PRE: è stato cliccato il bottone self.results_info
        Vissualizza una finestra informativa di tipo MetricheDialog
        :return: None
        """
        # Apertura scheda info metriche
        dialog = MetricheDialog()
        dialog.exec_()

    def buttonUseLoadFile(self):
        """
        @PRE: è stato cliccato il bottone self.use_loadfile
        Permette all'utente di caricare un file csv su cui ottenere predizioni dal classificatore addestrato attraverso
        la finestra visualizzata dalla funzione self.openLoadNewFileWindow
        :return: None
        """
        # apri finestra LoadNewFile
        self.openLoadNewFileWindow()

    def buttonUseApply(self):
        """
        @PRE: è stato cliccato il bottone self.use_apply
        Genera le predizioni e le aggiunge ai dati presenti nella tabella self.usetable utilizzando il classificatore
        addestrato attraverso i metodi del modello(self.model).
        :return: None
        """
        # Riporta i risultati del modello sulla tabella del file di utilizzo
        # Dialog di attesa
        text = "Attendi mentre il modello effettua predizioni sui dati inseriti"
        dialog = WaitingDialog(self, text, self.mapToGlobal(self.rect().center()))
        dialog.show()
        QtWidgets.QApplication.processEvents()
        # Ottieni predizioni
        self.model.predict_use_data()
        # Refresh del modello per visualizzarle
        self.usetable.updatemodel()
        # Informo il dialog del successo
        dialog.success(True)
        # Mi disabilito in quanto le predizioni sono già state aggiunte
        self.disableUseApply()

    def buttonUseExport(self):
        """
        @PRE: è stato cliccato il bottone self.use_export
        Permette all'utente di salvare su file csv i dati presenti nella tabella self.usetable
        chiama la funzione self.openSaveDialog per ottenere il percorso di salvataggio del file csv, poi invoca la
        funzione del modello (self.model) per generare il file csv con i dati
        :return: None
        """
        # chiama opensave dialog per ottere il path di salvataggio poi invoca la funzione del modello per salvare
        filepath = self.openSaveDialog()
        try:
            self.model.export_usedata(filepath)
        except:
            pass

    def setupUi(self, MainWindow):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza l'interfaccia grafica della MainWindow predisponendo tutti i widget e i gli elementi interattivi
        con cui può interagire l'utente.
        :param MainWindow: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 800))

        # FONT GENERALE
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.TabWidget.setObjectName("TabWidget")
        self.Main = QtWidgets.QWidget()
        self.Main.setObjectName("Main")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.Main)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.Main)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.line = QtWidgets.QFrame(self.Main)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.main_type = QtWidgets.QLabel(self.Main)
        self.main_type.setWordWrap(True)
        self.main_type.setObjectName("main_type")
        self.verticalLayout_7.addWidget(self.main_type)
        self.main_filename = QtWidgets.QLabel(self.Main)
        self.main_filename.setWordWrap(True)
        self.main_filename.setObjectName("main_filename")
        self.verticalLayout_7.addWidget(self.main_filename)
        self.verticalLayout_6.addLayout(self.verticalLayout_7)
        spacerItem = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self.Main)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_16.addWidget(self.label_4)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem2)
        self.verticalLayout_20.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem3)

        self.main_list_columns = QtWidgets.QScrollArea(self.Main)
        self.main_list_columns.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.main_list_columns.setWidgetResizable(True)
        self.main_list_columns.setObjectName("main_list_columns")
        self.main_list_columns_content = QtWidgets.QWidget()
        self.main_list_columns_content.setGeometry(QtCore.QRect(0, 0, 369, 189))
        self.main_list_columns_content.setObjectName("main_list_columns_content")
        self.main_list_columns_layout = QtWidgets.QVBoxLayout(self.main_list_columns_content)
        self.main_list_columns_layout.setObjectName("main_list_columns_layout")
        self.main_list_columns.setWidget(self.main_list_columns_content)

        self.horizontalLayout_18.addWidget(self.main_list_columns)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem4)
        self.verticalLayout_20.addLayout(self.horizontalLayout_18)
        self.label_8 = QtWidgets.QLabel(self.Main)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_20.addWidget(self.label_8)
        self.horizontalLayout_15.addLayout(self.verticalLayout_20)
        self.verticalLayout_21 = QtWidgets.QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem5)
        self.label_5 = QtWidgets.QLabel(self.Main)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_17.addWidget(self.label_5)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem6)
        self.verticalLayout_21.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem7)

        self.main_list_split = QtWidgets.QScrollArea(self.Main)
        self.main_list_split.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.main_list_split.setWidgetResizable(True)
        self.main_list_split.setObjectName("main_list_split")
        self.main_list_split_content = QtWidgets.QWidget()
        self.main_list_split_content.setGeometry(QtCore.QRect(0, 0, 369, 189))
        self.main_list_split_content.setObjectName("main_list_split_content")
        self.main_list_split_layout = QtWidgets.QVBoxLayout(self.main_list_split_content)
        self.main_list_split_layout.setObjectName("main_list_split_layout")
        self.main_list_split.setWidget(self.main_list_split_content)

        self.horizontalLayout_20.addWidget(self.main_list_split)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(spacerItem8)
        self.verticalLayout_21.addLayout(self.horizontalLayout_20)
        self.label_12 = QtWidgets.QLabel(self.Main)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setWordWrap(True)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_21.addWidget(self.label_12)
        self.horizontalLayout_15.addLayout(self.verticalLayout_21)
        self.verticalLayout_6.addLayout(self.horizontalLayout_15)
        spacerItem9 = QtWidgets.QSpacerItem(20, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_6.addItem(spacerItem9)
        self.label_3 = QtWidgets.QLabel(self.Main)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.label_3)
        self.line_3 = QtWidgets.QFrame(self.Main)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_6.addWidget(self.line_3)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label = QtWidgets.QLabel(self.Main)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout_9.addWidget(self.label)
        self.filelabelratio = QtWidgets.QLabel(self.Main)
        self.filelabelratio.setWordWrap(True)
        self.filelabelratio.setObjectName("filelabelratio")
        self.verticalLayout_9.addWidget(self.filelabelratio)
        self.label_2 = QtWidgets.QLabel(self.Main)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.label_6 = QtWidgets.QLabel(self.Main)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_9.addWidget(self.label_6)
        self.verticalLayout_6.addLayout(self.verticalLayout_9)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.groupBox_3 = QtWidgets.QGroupBox(self.Main)
        self.groupBox_3.setMinimumSize(QtCore.QSize(170, 0))
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.sampling1 = QtWidgets.QRadioButton(self.groupBox_3)
        self.sampling1.setChecked(True)
        self.sampling1.setObjectName("sampling1")
        self.verticalLayout_11.addWidget(self.sampling1)
        self.sampling2 = QtWidgets.QRadioButton(self.groupBox_3)
        self.sampling2.setObjectName("sampling2")
        self.verticalLayout_11.addWidget(self.sampling2)
        self.sampling3 = QtWidgets.QRadioButton(self.groupBox_3)
        self.sampling3.setObjectName("sampling3")
        self.verticalLayout_11.addWidget(self.sampling3)
        self.horizontalLayout_5.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.Main)
        self.groupBox.setMinimumSize(QtCore.QSize(170, 0))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.scaling1 = QtWidgets.QRadioButton(self.groupBox)
        self.scaling1.setChecked(True)
        self.scaling1.setObjectName("scaling1")
        self.verticalLayout_10.addWidget(self.scaling1)
        self.scaling2 = QtWidgets.QRadioButton(self.groupBox)
        self.scaling2.setObjectName("scaling2")
        self.verticalLayout_10.addWidget(self.scaling2)
        self.scaling3 = QtWidgets.QRadioButton(self.groupBox)
        self.scaling3.setObjectName("scaling3")
        self.verticalLayout_10.addWidget(self.scaling3)
        self.horizontalLayout_5.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.Main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(170, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.algorithm1 = QtWidgets.QRadioButton(self.groupBox_2)
        self.algorithm1.setChecked(True)
        self.algorithm1.setObjectName("algorithm1")
        self.verticalLayout_12.addWidget(self.algorithm1)
        self.algorithm2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.algorithm2.setObjectName("algorithm2")
        self.verticalLayout_12.addWidget(self.algorithm2)
        self.algorithm3 = QtWidgets.QRadioButton(self.groupBox_2)
        self.algorithm3.setObjectName("algorithm3")
        self.verticalLayout_12.addWidget(self.algorithm3)
        self.algorithm4 = QtWidgets.QRadioButton(self.groupBox_2)
        self.algorithm4.setObjectName("algorithm4")
        self.verticalLayout_12.addWidget(self.algorithm4)
        self.algorithm5 = QtWidgets.QRadioButton(self.groupBox_2)
        self.algorithm5.setObjectName("algorithm5")
        self.verticalLayout_12.addWidget(self.algorithm5)
        self.horizontalLayout_5.addWidget(self.groupBox_2)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.Main)
        self.label_10.setWordWrap(False)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem12)
        self.main_button_train = QtWidgets.QPushButton(self.Main)
        self.main_button_train.setObjectName("main_button_train")
        self.horizontalLayout_7.addWidget(self.main_button_train)
        self.main_button_reset = QtWidgets.QPushButton(self.Main)
        self.main_button_reset.setObjectName("main_button_reset")
        self.horizontalLayout_7.addWidget(self.main_button_reset)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_9 = QtWidgets.QLabel(self.Main)
        self.label_9.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_13.addWidget(self.label_9)
        self.label_11 = QtWidgets.QLabel(self.Main)
        self.label_11.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label_11.setWordWrap(True)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_13.addWidget(self.label_11)
        self.verticalLayout_6.addLayout(self.verticalLayout_13)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.main_button_save = QtWidgets.QPushButton(self.Main)
        self.main_button_save.setObjectName("main_button_save")
        self.horizontalLayout_6.addWidget(self.main_button_save)
        self.main_button_file = QtWidgets.QPushButton(self.Main)
        self.main_button_file.setObjectName("main_button_file")
        self.horizontalLayout_6.addWidget(self.main_button_file)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.TabWidget.addTab(self.Main, "")
        self.Data = QtWidgets.QWidget()
        self.Data.setObjectName("Data")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Data)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_13 = QtWidgets.QLabel(self.Data)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        self.line_2 = QtWidgets.QFrame(self.Data)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_2.addWidget(self.line_2)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_data_total = QtWidgets.QLabel(self.Data)
        self.label_data_total.setObjectName("label_data_total")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_data_total)
        self.label_14 = QtWidgets.QLabel(self.Data)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_16 = QtWidgets.QLabel(self.Data)
        self.label_16.setObjectName("label_16")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.label_data_positive = QtWidgets.QLabel(self.Data)
        self.label_data_positive.setObjectName("label_data_positive")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_data_positive)
        self.verticalLayout_2.addLayout(self.formLayout_3)

        self.horizontalLayout_box = QtWidgets.QHBoxLayout()
        self.horizontalLayout_box.setSpacing(0)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_18 = QtWidgets.QLabel(self.Data)
        self.label_18.setObjectName("label_18")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.label_data_negative = QtWidgets.QLabel(self.Data)
        self.label_data_negative.setObjectName("label_data_negative")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_data_negative)
        self.horizontalLayout_box.addLayout(self.formLayout_4)
        self.combo_data = QtWidgets.QComboBox(self.Data)
        spacerItem_data = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_box.addItem(spacerItem_data)
        self.combo_data_label = QtWidgets.QLabel(self.Data)
        self.combo_data_label.setObjectName("combo_data_label")
        self.horizontalLayout_box.addWidget(self.combo_data_label)
        self.combo_data.setObjectName("combo_data")
        self.horizontalLayout_box.addWidget(self.combo_data)

        self.verticalLayout_2.addLayout(self.horizontalLayout_box)

        self.table_data = QtWidgets.QTableView(self.Data)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_data.sizePolicy().hasHeightForWidth())
        self.table_data.setSizePolicy(sizePolicy)
        self.table_data.setObjectName("table_data")
        self.table_data.horizontalHeader().setResizeContentsPrecision(1)
        self.table_data.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalLayout_2.addWidget(self.table_data)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.data_preprocess_info = QtWidgets.QPushButton(self.Data)
        self.data_preprocess_info.setObjectName("data_preprocess_info")
        self.horizontalLayout.addWidget(self.data_preprocess_info)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem14)
        self.label_data_export=QtWidgets.QLabel(self.Data)
        self.label_data_export.setObjectName("label_data_export")
        self.horizontalLayout.addWidget(self.label_data_export)
        self.data_export = QtWidgets.QPushButton(self.Data)
        self.data_export.setObjectName("data_export")
        self.horizontalLayout.addWidget(self.data_export)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.TabWidget.addTab(self.Data, "")
        self.Train = QtWidgets.QWidget()
        self.Train.setObjectName("Train")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.Train)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_15 = QtWidgets.QLabel(self.Train)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_3.addWidget(self.label_15)
        self.line_4 = QtWidgets.QFrame(self.Train)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_3.addWidget(self.line_4)
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_20 = QtWidgets.QLabel(self.Train)
        self.label_20.setObjectName("label_20")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.label_train_total = QtWidgets.QLabel(self.Train)
        self.label_train_total.setObjectName("label_train_total")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_train_total)
        self.verticalLayout_3.addLayout(self.formLayout_6)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_17 = QtWidgets.QLabel(self.Train)
        self.label_17.setObjectName("label_17")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.label_train_positive = QtWidgets.QLabel(self.Train)
        self.label_train_positive.setObjectName("label_train_positive")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_train_positive)
        self.verticalLayout_3.addLayout(self.formLayout_5)
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_21 = QtWidgets.QLabel(self.Train)
        self.label_21.setObjectName("label_21")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.label_train_negative = QtWidgets.QLabel(self.Train)
        self.label_train_negative.setObjectName("label_train_negative")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_train_negative)
        self.verticalLayout_3.addLayout(self.formLayout_7)
        self.table_train = QtWidgets.QTableView(self.Train)
        self.table_train.setObjectName("table_train")
        self.table_train.horizontalHeader().setResizeContentsPrecision(1)
        self.table_train.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalLayout_3.addWidget(self.table_train)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem15)
        self.label_train_export = QtWidgets.QLabel(self.Train)
        self.label_train_export.setObjectName("label_train_export")
        self.horizontalLayout_2.addWidget(self.label_train_export)
        self.train_export = QtWidgets.QPushButton(self.Train)
        self.train_export.setObjectName("train_export")
        self.horizontalLayout_2.addWidget(self.train_export)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.TabWidget.addTab(self.Train, "")
        self.Test = QtWidgets.QWidget()
        self.Test.setObjectName("Test")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Test)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_27 = QtWidgets.QLabel(self.Test)
        self.label_27.setObjectName("label_27")
        self.verticalLayout_4.addWidget(self.label_27)
        self.line_5 = QtWidgets.QFrame(self.Test)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_4.addWidget(self.line_5)
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_test_total = QtWidgets.QLabel(self.Test)
        self.label_test_total.setObjectName("label_test_total")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_test_total)
        self.label_23 = QtWidgets.QLabel(self.Test)
        self.label_23.setObjectName("label_23")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_23)
        self.verticalLayout_4.addLayout(self.formLayout_8)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_24 = QtWidgets.QLabel(self.Test)
        self.label_24.setObjectName("label_24")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_24)
        self.label_test_positive = QtWidgets.QLabel(self.Test)
        self.label_test_positive.setObjectName("label_test_positive")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_test_positive)
        self.verticalLayout_4.addLayout(self.formLayout_9)
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_25 = QtWidgets.QLabel(self.Test)
        self.label_25.setObjectName("label_25")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_25)
        self.label_test_negative = QtWidgets.QLabel(self.Test)
        self.label_test_negative.setObjectName("label_test_negative")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_test_negative)
        self.verticalLayout_4.addLayout(self.formLayout_10)
        self.table_test = QtWidgets.QTableView(self.Test)
        self.table_test.setObjectName("table_test")
        self.table_test.horizontalHeader().setResizeContentsPrecision(1)
        self.table_test.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalLayout_4.addWidget(self.table_test)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem16)
        self.label_test_export = QtWidgets.QLabel(self.Test)
        self.label_test_export.setObjectName("label_test_export")
        self.horizontalLayout_3.addWidget(self.label_test_export)
        self.test_export = QtWidgets.QPushButton(self.Test)
        self.test_export.setObjectName("test_export")
        self.horizontalLayout_3.addWidget(self.test_export)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.TabWidget.addTab(self.Test, "")
        self.Risultati = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Risultati.sizePolicy().hasHeightForWidth())
        self.Risultati.setSizePolicy(sizePolicy)
        self.Risultati.setObjectName("Risultati")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.Risultati)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_29 = QtWidgets.QLabel(self.Risultati)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setObjectName("label_29")
        self.verticalLayout_14.addWidget(self.label_29)
        self.line_7 = QtWidgets.QFrame(self.Risultati)
        self.line_7.setEnabled(True)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_14.addWidget(self.line_7)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setSpacing(6)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_36 = QtWidgets.QLabel(self.Risultati)
        self.label_36.setAlignment(QtCore.Qt.AlignCenter)
        self.label_36.setObjectName("label_36")
        self.verticalLayout_15.addWidget(self.label_36)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.results_typep = QtWidgets.QLabel(self.Risultati)
        self.results_typep.setObjectName("results_typep")
        self.horizontalLayout_11.addWidget(self.results_typep)
        self.verticalLayout_15.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.results_number_examples = QtWidgets.QLabel(self.Risultati)
        self.results_number_examples.setObjectName("results_number_examples")
        self.horizontalLayout_9.addWidget(self.results_number_examples)
        self.verticalLayout_15.addLayout(self.horizontalLayout_9)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.results_sampling = QtWidgets.QLabel(self.Risultati)
        self.results_sampling.setObjectName("results_sampling")
        self.gridLayout_2.addWidget(self.results_sampling, 1, 0, 1, 1)
        self.results_algorithm = QtWidgets.QLabel(self.Risultati)
        self.results_algorithm.setObjectName("results_algorithm")
        self.gridLayout_2.addWidget(self.results_algorithm, 1, 4, 1, 1)
        self.results_scaling = QtWidgets.QLabel(self.Risultati)
        self.results_scaling.setObjectName("results_scaling")
        self.gridLayout_2.addWidget(self.results_scaling, 1, 2, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem17, 1, 5, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem18, 1, 1, 1, 1)
        spacerItem19 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem19, 1, 3, 1, 1)
        self.verticalLayout_15.addLayout(self.gridLayout_2)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.results_ignored = QtWidgets.QLabel(self.Risultati)
        self.results_ignored.setWordWrap(True)
        self.results_ignored.setObjectName("results_ignored")
        self.horizontalLayout_10.addWidget(self.results_ignored)
        self.verticalLayout_15.addLayout(self.horizontalLayout_10)
        self.verticalLayout_15.setStretch(0, 1)
        self.verticalLayout_15.setStretch(1, 1)
        self.verticalLayout_15.setStretch(2, 1)
        self.verticalLayout_15.setStretch(3, 1)
        self.verticalLayout_15.setStretch(4, 1)
        self.verticalLayout_14.addLayout(self.verticalLayout_15)
        spacerItem20 = QtWidgets.QSpacerItem(1, 15, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_14.addItem(spacerItem20)
        self.label_35 = QtWidgets.QLabel(self.Risultati)
        self.label_35.setObjectName("label_35")
        self.verticalLayout_14.addWidget(self.label_35)
        self.line_8 = QtWidgets.QFrame(self.Risultati)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_14.addWidget(self.line_8)
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label_37 = QtWidgets.QLabel(self.Risultati)
        self.label_37.setAlignment(QtCore.Qt.AlignCenter)
        self.label_37.setObjectName("label_37")
        self.verticalLayout_18.addWidget(self.label_37)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_34 = QtWidgets.QLabel(self.Risultati)
        self.label_34.setAlignment(QtCore.Qt.AlignCenter)
        self.label_34.setObjectName("label_34")
        self.gridLayout_3.addWidget(self.label_34, 0, 2, 1, 1)
        self.train_f1 = QtWidgets.QLabel(self.Risultati)
        self.train_f1.setAlignment(QtCore.Qt.AlignCenter)
        self.train_f1.setObjectName("train_f1")
        self.gridLayout_3.addWidget(self.train_f1, 1, 4, 1, 1)
        self.train_accuracy = QtWidgets.QLabel(self.Risultati)
        self.train_accuracy.setAlignment(QtCore.Qt.AlignCenter)
        self.train_accuracy.setObjectName("train_accuracy")
        self.gridLayout_3.addWidget(self.train_accuracy, 1, 1, 1, 1)
        self.train_recall = QtWidgets.QLabel(self.Risultati)
        self.train_recall.setAlignment(QtCore.Qt.AlignCenter)
        self.train_recall.setObjectName("train_recall")
        self.gridLayout_3.addWidget(self.train_recall, 1, 3, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem21, 0, 0, 1, 1)
        self.train_precision = QtWidgets.QLabel(self.Risultati)
        self.train_precision.setAlignment(QtCore.Qt.AlignCenter)
        self.train_precision.setObjectName("train_precision")
        self.gridLayout_3.addWidget(self.train_precision, 1, 2, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.Risultati)
        self.label_32.setAlignment(QtCore.Qt.AlignCenter)
        self.label_32.setObjectName("label_32")
        self.gridLayout_3.addWidget(self.label_32, 0, 1, 1, 1)
        self.label_47 = QtWidgets.QLabel(self.Risultati)
        self.label_47.setAlignment(QtCore.Qt.AlignCenter)
        self.label_47.setObjectName("label_47")
        self.gridLayout_3.addWidget(self.label_47, 0, 3, 1, 1)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem22, 1, 0, 1, 1)
        self.label_48 = QtWidgets.QLabel(self.Risultati)
        self.label_48.setAlignment(QtCore.Qt.AlignCenter)
        self.label_48.setObjectName("label_48")
        self.gridLayout_3.addWidget(self.label_48, 0, 4, 1, 1)
        spacerItem23 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem23, 0, 5, 1, 1)
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem24, 1, 5, 1, 1)
        self.verticalLayout_18.addLayout(self.gridLayout_3)
        self.verticalLayout_18.setStretch(0, 1)
        self.verticalLayout_18.setStretch(1, 2)
        self.verticalLayout_14.addLayout(self.verticalLayout_18)
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_30 = QtWidgets.QLabel(self.Risultati)
        self.label_30.setAlignment(QtCore.Qt.AlignCenter)
        self.label_30.setObjectName("label_30")
        self.verticalLayout_16.addWidget(self.label_30)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem25)
        self.button_train_matrix = QtWidgets.QPushButton(self.Risultati)
        self.button_train_matrix.setObjectName("button_train_matrix")
        self.horizontalLayout_12.addWidget(self.button_train_matrix)
        self.button_train_auc = QtWidgets.QPushButton(self.Risultati)
        self.button_train_auc.setObjectName("button_train_auc")
        self.horizontalLayout_12.addWidget(self.button_train_auc)
        self.button_train_prc = QtWidgets.QPushButton(self.Risultati)
        self.button_train_prc.setObjectName("button_train_prc")
        self.horizontalLayout_12.addWidget(self.button_train_prc)
        spacerItem26 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem26)
        self.verticalLayout_16.addLayout(self.horizontalLayout_12)
        self.verticalLayout_14.addLayout(self.verticalLayout_16)
        self.label_43 = QtWidgets.QLabel(self.Risultati)
        self.label_43.setObjectName("label_43")
        self.verticalLayout_14.addWidget(self.label_43)
        self.line_9 = QtWidgets.QFrame(self.Risultati)
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.verticalLayout_14.addWidget(self.line_9)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_44 = QtWidgets.QLabel(self.Risultati)
        self.label_44.setAlignment(QtCore.Qt.AlignCenter)
        self.label_44.setObjectName("label_44")
        self.verticalLayout_19.addWidget(self.label_44)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.test_precision = QtWidgets.QLabel(self.Risultati)
        self.test_precision.setAlignment(QtCore.Qt.AlignCenter)
        self.test_precision.setObjectName("test_precision")
        self.gridLayout_6.addWidget(self.test_precision, 1, 2, 1, 1)
        self.test_accuracy = QtWidgets.QLabel(self.Risultati)
        self.test_accuracy.setAlignment(QtCore.Qt.AlignCenter)
        self.test_accuracy.setObjectName("test_accuracy")
        self.gridLayout_6.addWidget(self.test_accuracy, 1, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.Risultati)
        self.label_31.setAlignment(QtCore.Qt.AlignCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout_6.addWidget(self.label_31, 0, 1, 1, 1)
        self.label_45 = QtWidgets.QLabel(self.Risultati)
        self.label_45.setAlignment(QtCore.Qt.AlignCenter)
        self.label_45.setObjectName("label_45")
        self.gridLayout_6.addWidget(self.label_45, 0, 2, 1, 1)
        self.test_f1 = QtWidgets.QLabel(self.Risultati)
        self.test_f1.setAlignment(QtCore.Qt.AlignCenter)
        self.test_f1.setObjectName("test_f1")
        self.gridLayout_6.addWidget(self.test_f1, 1, 4, 1, 1)
        self.label_50 = QtWidgets.QLabel(self.Risultati)
        self.label_50.setAlignment(QtCore.Qt.AlignCenter)
        self.label_50.setObjectName("label_50")
        self.gridLayout_6.addWidget(self.label_50, 0, 4, 1, 1)
        self.test_recall = QtWidgets.QLabel(self.Risultati)
        self.test_recall.setAlignment(QtCore.Qt.AlignCenter)
        self.test_recall.setObjectName("test_recall")
        self.gridLayout_6.addWidget(self.test_recall, 1, 3, 1, 1)
        self.label_49 = QtWidgets.QLabel(self.Risultati)
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setObjectName("label_49")
        self.gridLayout_6.addWidget(self.label_49, 0, 3, 1, 1)
        spacerItem27 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem27, 0, 0, 1, 1)
        spacerItem28 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem28, 1, 0, 1, 1)
        spacerItem29 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem29, 0, 5, 1, 1)
        spacerItem30 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem30, 1, 5, 1, 1)
        self.verticalLayout_19.addLayout(self.gridLayout_6)
        self.verticalLayout_19.setStretch(0, 1)
        self.verticalLayout_19.setStretch(1, 2)
        self.verticalLayout_14.addLayout(self.verticalLayout_19)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.label_46 = QtWidgets.QLabel(self.Risultati)
        self.label_46.setAlignment(QtCore.Qt.AlignCenter)
        self.label_46.setObjectName("label_46")
        self.verticalLayout_17.addWidget(self.label_46)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem31 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem31)
        self.button_test_matrix = QtWidgets.QPushButton(self.Risultati)
        self.button_test_matrix.setObjectName("button_test_matrix")
        self.horizontalLayout_13.addWidget(self.button_test_matrix)
        self.button_test_auc = QtWidgets.QPushButton(self.Risultati)
        self.button_test_auc.setObjectName("button_test_auc")
        self.horizontalLayout_13.addWidget(self.button_test_auc)
        self.button_test_prc = QtWidgets.QPushButton(self.Risultati)
        self.button_test_prc.setObjectName("button_test_prc")
        self.horizontalLayout_13.addWidget(self.button_test_prc)
        spacerItem32 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem32)
        self.verticalLayout_17.addLayout(self.horizontalLayout_13)
        self.verticalLayout_14.addLayout(self.verticalLayout_17)
        self.line_10 = QtWidgets.QFrame(self.Risultati)
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.verticalLayout_14.addWidget(self.line_10)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem33 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem33)
        self.results_info = QtWidgets.QPushButton(self.Risultati)
        self.results_info.setObjectName("results_info")
        self.horizontalLayout_14.addWidget(self.results_info)
        self.verticalLayout_14.addLayout(self.horizontalLayout_14)
        self.verticalLayout_14.setStretch(0, 1)
        self.verticalLayout_14.setStretch(2, 3)
        self.verticalLayout_14.setStretch(4, 1)
        self.verticalLayout_14.setStretch(6, 2)
        self.verticalLayout_14.setStretch(7, 2)
        self.verticalLayout_14.setStretch(8, 1)
        self.verticalLayout_14.setStretch(10, 2)
        self.verticalLayout_14.setStretch(11, 2)
        self.TabWidget.addTab(self.Risultati, "")
        self.Utilizza = QtWidgets.QWidget()
        self.Utilizza.setObjectName("Utilizza")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.Utilizza)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_22 = QtWidgets.QLabel(self.Utilizza)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_5.addWidget(self.label_22)
        self.line_6 = QtWidgets.QFrame(self.Utilizza)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_5.addWidget(self.line_6)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.use_type = QtWidgets.QLabel(self.Utilizza)
        self.use_type.setObjectName("use_type")
        self.verticalLayout_8.addWidget(self.use_type)
        self.use_filename = QtWidgets.QLabel(self.Utilizza)
        self.use_filename.setObjectName("use_filename")
        self.verticalLayout_8.addWidget(self.use_filename)
        self.verticalLayout_5.addLayout(self.verticalLayout_8)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.use_loadfile = QtWidgets.QPushButton(self.Utilizza)
        self.use_loadfile.setObjectName("use_loadfile")
        self.horizontalLayout_8.addWidget(self.use_loadfile)
        self.use_apply = QtWidgets.QPushButton(self.Utilizza)
        self.use_apply.setObjectName("use_apply")
        self.horizontalLayout_8.addWidget(self.use_apply)
        spacerItem34 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem34)
        self.combo_use_label = QtWidgets.QLabel(self.Utilizza)
        self.combo_use_label.setObjectName("combo_use_label")
        self.horizontalLayout_8.addWidget(self.combo_use_label)
        self.combo_use = QtWidgets.QComboBox(self.Utilizza)
        self.combo_use.setObjectName("combo_use")
        self.horizontalLayout_8.addWidget(self.combo_use)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.table_use = QtWidgets.QTableView(self.Utilizza)
        self.table_use.setObjectName("table_use")
        self.table_use.horizontalHeader().setResizeContentsPrecision(1)
        self.table_use.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalLayout_5.addWidget(self.table_use)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem35 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem35)
        self.label_use_export = QtWidgets.QLabel(self.Utilizza)
        self.label_use_export.setObjectName("label_use_export")
        self.horizontalLayout_4.addWidget(self.label_use_export)
        self.use_export = QtWidgets.QPushButton(self.Utilizza)
        self.use_export.setObjectName("use_export")
        self.horizontalLayout_4.addWidget(self.use_export)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.TabWidget.addTab(self.Utilizza, "")
        self.verticalLayout.addWidget(self.TabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        # FONTS per le label e tabelle

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        self.TabWidget.tabBar().setFont(font)

        # Tab Main
        self.label_7.setFont(font)
        self.label_5.setFont(font)
        self.label.setFont(font)
        self.label_10.setFont(font)
        self.label_3.setFont(font)
        self.main_button_reset.setFont(font)
        self.main_button_train.setFont(font)
        self.main_button_save.setFont(font)

        # Tabs Data Train Test
        self.label_13.setFont(font)
        self.label_15.setFont(font)
        self.label_27.setFont(font)
        self.label_data_total.setFont(font)
        self.label_data_positive.setFont(font)
        self.label_data_negative.setFont(font)
        self.label_train_total.setFont(font)
        self.label_train_positive.setFont(font)
        self.label_train_negative.setFont(font)
        self.label_test_total.setFont(font)
        self.label_test_positive.setFont(font)
        self.label_test_negative.setFont(font)

        # Tab Risultati
        self.label_29.setFont(font)
        self.label_36.setFont(font)
        self.label_37.setFont(font)
        self.label_32.setFont(font)
        self.label_34.setFont(font)
        self.label_47.setFont(font)
        self.label_48.setFont(font)
        self.label_30.setFont(font)
        self.label_44.setFont(font)
        self.label_31.setFont(font)
        self.label_45.setFont(font)
        self.label_49.setFont(font)
        self.label_50.setFont(font)
        self.label_46.setFont(font)

        # Tab Utilizza
        self.label_22.setFont(font)
        self.use_loadfile.setFont(font)
        self.use_apply.setFont(font)

        # Tabelle
        self.table_data.horizontalHeader().setFont(font)
        self.table_train.horizontalHeader().setFont(font)
        self.table_test.horizontalHeader().setFont(font)
        self.table_use.horizontalHeader().setFont(font)

        # RetranslateUi
        self.retranslateUi(MainWindow)

        # Set di base della tab da visualizzare una volta aperto l'applicativo
        self.TabWidget.setCurrentIndex(0)

        # Connessione SLOTS alle funzioni
        self.sampling1.toggled.connect(lambda: self.model.set_sampling(SamplingEnum.NONE))
        self.sampling2.toggled.connect(lambda: self.model.set_sampling(SamplingEnum.UNDER))
        self.sampling3.toggled.connect(lambda: self.model.set_sampling(SamplingEnum.SMOTE))
        self.scaling1.toggled.connect(lambda: self.model.set_scaling(ScalingEnum.NONE))
        self.scaling2.toggled.connect(lambda: self.model.set_scaling(ScalingEnum.STANDARD))
        self.scaling3.toggled.connect(lambda: self.model.set_scaling(ScalingEnum.MINMAX))
        self.algorithm1.toggled.connect(lambda: self.model.set_algorithm(ClassifierEnum.LOGISTIC))
        self.algorithm2.toggled.connect(lambda: self.model.set_algorithm(ClassifierEnum.SVC))
        self.algorithm3.toggled.connect(lambda: self.model.set_algorithm(ClassifierEnum.TREE))
        self.algorithm4.toggled.connect(lambda: self.model.set_algorithm(ClassifierEnum.FOREST))
        self.algorithm5.toggled.connect(lambda: self.model.set_algorithm(ClassifierEnum.XGB))
        self.main_button_train.clicked.connect(lambda: self.buttonTrainModel())
        self.main_button_file.clicked.connect(lambda: self.buttonLoadNewTrainFile())
        self.main_button_reset.clicked.connect(lambda: self.buttonReset())
        self.main_button_save.clicked.connect(lambda: self.buttonSave())
        self.data_preprocess_info.clicked.connect(lambda: self.buttonDataPreprocessInfo())
        self.data_export.clicked.connect(lambda: self.buttonDataExport())
        self.train_export.clicked.connect(lambda: self.buttonTrainExport())
        self.test_export.clicked.connect(lambda: self.buttonTestExport())
        self.button_train_matrix.clicked.connect(lambda: self.buttonTrainMatrix())
        self.button_train_auc.clicked.connect(lambda: self.buttonTrainRoc())
        self.button_train_prc.clicked.connect(lambda: self.buttonTrainPrc())
        self.button_test_matrix.clicked.connect(lambda: self.buttonTestMatrix())
        self.button_test_auc.clicked.connect(lambda: self.buttonTestRoc())
        self.button_test_prc.clicked.connect(lambda: self.buttonTestPrc())
        self.results_info.clicked.connect(lambda: self.buttonResultsInfo())
        self.use_loadfile.clicked.connect(lambda: self.buttonUseLoadFile())
        self.use_apply.clicked.connect(lambda: self.buttonUseApply())
        self.use_export.clicked.connect(lambda: self.buttonUseExport())

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Funzione autogenerata al momento della creazione della classe a partire dal file .ui di QtDesigner
        Inizializza il contenuto testuale di tutti gli elementi inizializzati in setupUI
        :param MainWindow: Oggetto contenitore degli elementi dell'interfaccia (self nel caso sia questa finestra)
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Classificatore Coattiva"))
        self.label_7.setText(_translate("MainWindow", "Gestione dati caricati da file"))
        self.main_type.setText(_translate("MainWindow", "Tipologia di titoli di credito:"))
        self.main_filename.setText(_translate("MainWindow", "File aperto per l\'addestramento:"))
        self.label_4.setText(_translate("MainWindow",
                                        "Eliminare il check dal nome della colonna che si desidera ignorare per l\'addestramento:"))
        self.label_8.setText(_translate("MainWindow",
                                        "Verranno utilizzate solamente le colonne rimaste selezionate."))
        self.label_5.setText(_translate("MainWindow",
                                        "Selezionare fino a quale ruolo genererà il training set:"))
        self.label_12.setText(_translate("MainWindow", "I ruoli successivi alla data scelta comporranno il test set"))
        self.label_3.setText(_translate("MainWindow", "Addestramento Modello"))
        self.label.setText(_translate("MainWindow", "PREFERENZE RIGUARDANTI L\'ADDESTRAMENTO DEL MODELLO PREDITTIVO"))
        self.filelabelratio.setText(_translate("MainWindow",
                                               "1) I titoli contenuti nel training set hanno label per % positiva e % negativa, è possibile utilizzare un algoritmo di sampling per equilibrarli."))
        self.label_2.setText(
            _translate("MainWindow", "2) Selezionare la tipologia di normalizzazione da applicare ai dati."))
        self.label_6.setText(_translate("MainWindow",
                                        "3) Selezionare l\'algoritmo di apprendimento con cui addestrare il modello predittivo per la classificazione."))
        self.groupBox_3.setTitle(_translate("MainWindow", "1)Sampling"))
        self.sampling1.setText(_translate("MainWindow", "Nessuno"))
        self.sampling2.setText(_translate("MainWindow", "Downsampling"))
        self.sampling3.setText(_translate("MainWindow", "SMOTE Oversampling"))
        self.groupBox.setTitle(_translate("MainWindow", "2)Scaling"))
        self.scaling1.setText(_translate("MainWindow", "Nessuno"))
        self.scaling2.setText(_translate("MainWindow", "Standard"))
        self.scaling3.setText(_translate("MainWindow", "MinMax"))
        self.groupBox_2.setTitle(_translate("MainWindow", "3)Algoritmo di apprendimento"))
        self.algorithm1.setText(_translate("MainWindow", "Logistic Regression"))
        self.algorithm2.setText(_translate("MainWindow", "Support Vector Machine"))
        self.algorithm3.setText(_translate("MainWindow", "Decision Tree Classifier"))
        self.algorithm4.setText(_translate("MainWindow", "Random Forest Classifier"))
        self.algorithm5.setText(_translate("MainWindow", "XGB Classifier"))
        self.label_10.setText(_translate("MainWindow",
                                         "Clicca 'Addestra Modello' per addestrare il modello preddittivo sui titoli contenuti nel training set:"))
        self.main_button_train.setText(_translate("MainWindow", "Addestra Modello"))
        self.label_9.setText(_translate("MainWindow",
                                        "Una volta addestrato saranno visualizzabili le predizioni su training e test set nella colonna 'predizione' aggiunta alle rispettive tabelle.\nLe metriche relative all\' efficacia del modello saranno visualizzabili nella sezione Risultati.\nSarà inoltre possibile utilizzare il modello addestrato nella sezione Utilizza."))
        self.label_11.setText(_translate("MainWindow",
                                         "E\' possibile addestrare un nuovo modello predittivo premendo il pulsante Reset e nuovamente il pulsante Addestra."))
        self.main_button_file.setText(_translate("MainWindow", "Caricamento nuovo file"))
        self.main_button_save.setText(_translate("MainWindow", "Salvataggio Modello Addestrato"))
        self.main_button_reset.setText(_translate("MainWindow", "Reset"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Main), _translate("MainWindow", "Main"))
        self.label_13.setText(_translate("MainWindow", "Informazioni sul file caricato:"))
        self.label_data_total.setText(_translate("MainWindow", "nessuno"))
        self.label_14.setText(_translate("MainWindow", "Numero di titoli presenti:"))
        self.label_16.setText(_translate("MainWindow", "Numero di titoli con label positiva:"))
        self.label_data_positive.setText(_translate("MainWindow", "nessuno"))
        self.label_18.setText(_translate("MainWindow", "Numero di titoli con label Negativa: "))
        self.label_data_negative.setText(_translate("MainWindow", "nessuno"))
        self.data_preprocess_info.setText(_translate("MainWindow", "Informazioni Colonne Aggiuntive"))
        self.label_data_export.setText(_translate("MainWindow", "Premi per esportare i dati Preparati in file .csv: "))
        self.data_export.setText(_translate("MainWindow", "Esporta"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Data), _translate("MainWindow", "Data"))
        self.label_15.setText(_translate("MainWindow", "Informazioni sui dati di addestramento in-sample:"))
        self.label_20.setText(_translate("MainWindow", "Numero di titoli presenti:"))
        self.label_train_total.setText(_translate("MainWindow", "nessuno"))
        self.label_17.setText(_translate("MainWindow", "Numero di titoli con label positiva:"))
        self.label_train_positive.setText(_translate("MainWindow", "nessuno"))
        self.label_21.setText(_translate("MainWindow", "Numero di titoli con label Negativa:"))
        self.label_train_negative.setText(_translate("MainWindow", "nessuno"))
        self.label_train_export.setText(_translate("MainWindow", "Premi per esportare i dati della tabella in file "
                                                                 ".csv: "))
        self.train_export.setText(_translate("MainWindow", "Esporta"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Train), _translate("MainWindow", "Train"))
        self.label_27.setText(_translate("MainWindow", "Informazioni sui dati di test out-of-sample:"))
        self.label_test_total.setText(_translate("MainWindow", "nessuno"))
        self.label_23.setText(_translate("MainWindow", "Numero di titoli presenti:"))
        self.label_24.setText(_translate("MainWindow", "Numero di titoli con label positiva:"))
        self.label_test_positive.setText(_translate("MainWindow", "nessuno"))
        self.label_25.setText(_translate("MainWindow", "Numero di titoli con label Negativa:"))
        self.label_test_negative.setText(_translate("MainWindow", "nessuno"))
        self.label_test_export.setText(
            _translate("MainWindow", "Premi per esportare i dati della tabella in file .csv: "))
        self.test_export.setText(_translate("MainWindow", "Esporta"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Test), _translate("MainWindow", "Test"))
        self.label_29.setText(
            _translate("MainWindow", "Risultati e metriche per valutare le performance del modello addestrato:"))
        self.label_36.setText(_translate("MainWindow", "INFORMAZIONI SUL MODELLO"))
        self.results_typep.setText(_translate("MainWindow", "Tipologia di titoli di credito: nessuna"))
        self.results_number_examples.setText(_translate("MainWindow",
                                                        "Numero di esempi utilizzati nell\'addestramento: nessuno, di cui % con label positiva e % con label negativa"))
        self.results_sampling.setText(_translate("MainWindow", "Sampling: nessuno"))
        self.results_algorithm.setText(_translate("MainWindow", "Algoritmo di apprendimento: nessuno"))
        self.results_scaling.setText(_translate("MainWindow", "Scaling: nessuno"))
        self.results_ignored.setText(_translate("MainWindow", "Proprietà o colonne ignorate: nessuna"))
        self.label_35.setText(_translate("MainWindow", "Training set:"))
        self.label_37.setText(_translate("MainWindow", "TABELLA DELLE METRICHE"))
        self.label_34.setText(_translate("MainWindow", "Precisione"))
        self.train_f1.setText(_translate("MainWindow", "na"))
        self.train_accuracy.setText(_translate("MainWindow", "na"))
        self.train_recall.setText(_translate("MainWindow", "na"))
        self.train_precision.setText(_translate("MainWindow", "na"))
        self.label_32.setText(_translate("MainWindow", "Accuratezza"))
        self.label_47.setText(_translate("MainWindow", "Recall"))
        self.label_48.setText(_translate("MainWindow", "F1 Score"))
        self.label_30.setText(_translate("MainWindow", "GRAFICI"))
        self.button_train_matrix.setText(_translate("MainWindow", "Confusion Matrix"))
        self.button_train_auc.setText(_translate("MainWindow", "Roc-Auc Curve"))
        self.button_train_prc.setText(_translate("MainWindow", "Precision-Recall Curve"))
        self.label_43.setText(_translate("MainWindow", "Test set:"))
        self.label_44.setText(_translate("MainWindow", "TABELLA DELLE METRICHE"))
        self.test_precision.setText(_translate("MainWindow", "na"))
        self.test_accuracy.setText(_translate("MainWindow", "na"))
        self.label_31.setText(_translate("MainWindow", "Accuratezza"))
        self.label_45.setText(_translate("MainWindow", "Precisione"))
        self.test_f1.setText(_translate("MainWindow", "na"))
        self.label_50.setText(_translate("MainWindow", "F1 Score"))
        self.test_recall.setText(_translate("MainWindow", "na"))
        self.label_49.setText(_translate("MainWindow", "Recall"))
        self.label_46.setText(_translate("MainWindow", "GRAFICI"))
        self.button_test_matrix.setText(_translate("MainWindow", "Confusion Matrix"))
        self.button_test_auc.setText(_translate("MainWindow", "Roc-Auc Curve"))
        self.button_test_prc.setText(_translate("MainWindow", "Precision-Recall Curve"))
        self.results_info.setText(_translate("MainWindow", "Info Metriche"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Risultati), _translate("MainWindow", "Risultati"))
        self.label_22.setText(_translate("MainWindow", "Utilizzo del modello addestrato:"))
        self.use_type.setText(_translate("MainWindow",
                                         "Tipologia di titoli di credito su cui è stato addestrato il modello: non è ancora stato addestrato nessun modello."))
        self.use_filename.setText(_translate("MainWindow", "File caricato: nessuno"))
        self.use_loadfile.setText(_translate("MainWindow", "Carica File"))
        self.use_apply.setText(_translate("MainWindow", "Elabora"))
        self.label_use_export.setText(
            _translate("MainWindow", "Premi per esportare i dati della tabella in file .csv: "))
        self.use_export.setText(_translate("MainWindow", "Esporta"))
        self.combo_data_label.setText(_translate("MainWindow", "Selezione quale versione dei dati visualizzare nella tabella: "))
        self.combo_use_label.setText(
            _translate("MainWindow", "Selezione quale versione dei dati visualizzare nella tabella: "))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Utilizza), _translate("MainWindow", "Utilizza"))


if __name__ == "__main__":
    import sys

    # Instanziazione app
    app = QtWidgets.QApplication(sys.argv)
    # Instanziazione oggetto MainWindow che funge da centro dell'interfaccia grafica da cui chiamare le altre finestre
    mainwindow = MainWindow()

    # Avvio esecuzione UI a partire dal metodo di mainwindow per aprire la schermata di benvenuto
    mainwindow.openWelcomeWindow()

    # chiusura programma
    sys.exit(app.exec_())
