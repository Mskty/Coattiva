#!/usr/bin/env python
import PySimpleGUI as sg

from controller import *


# Esempio per mostrare dati csv in una tabella

def set_layout(filename: str, df: pd.DataFrame, checkbox: int):
    """
    Funzione utilizzata per refreshare il layout della view ogni volta che viene modificato il dataframe
    o viene caricato un file, questo perchè pysimplegui non permette di utilizzare layout dinamici, ma va
    creata una nuova finestra con un nuovo layout ad ogni cambiamento.
    :param filename:
    :param df:
    :param checkbox:
    :return:
    """
    # --- Creazione layout --- #

    # Uses the first row (which should be column names) as columns names
    header_list = df.columns.values.tolist()
    # Drops the first row in the table (otherwise the header names and the first row will be the same)
    data = df[0:].values.tolist()

    titolo = sg.Text("Classiciazione per esempi su file csv")
    carica = sg.Button("Carica file", key=1)
    # nome_file = sg.Text("Carica una tabella!")
    nome_file = sg.Text("File aperto: " + filename)
    seleziona_modello = sg.Text("Seleziona il modello di apprendimento da utilizzare:")

    # set current checkbox:
    if checkbox == 1:
        radio1 = sg.Radio('SVM', "MODEL", default=True, key=11)
        radio2 = sg.Radio('RNF', 'MODEL', key=12)
        radio3 = sg.Radio('NN', 'MODEL', key=13)
    elif checkbox == 2:
        radio1 = sg.Radio('SVM', "MODEL", key=11)
        radio2 = sg.Radio('RNF', 'MODEL', default=True, key=12)
        radio3 = sg.Radio('NN', 'MODEL', key=13)
    elif checkbox == 2:
        radio1 = sg.Radio('SVM', "MODEL", key=11)
        radio2 = sg.Radio('RNF', 'MODEL', key=12)
        radio3 = sg.Radio('NN', 'MODEL', default=True, key=13)
    else:
        radio1 = sg.Radio('SVM', "MODEL", default=True, key=11)
        radio2 = sg.Radio('RNF', 'MODEL', key=12)
        radio3 = sg.Radio('NN', 'MODEL', key=13)

    # set table and others
    dataset = sg.Table(values=data,
                       headings=header_list,
                       display_row_numbers=False,
                       auto_size_columns=False,
                       max_col_width=25,
                       justification="left",
                       vertical_scroll_only=False,
                       select_mode="extended",
                       num_rows=min(25, len(data)))
    clean = sg.Button("Clean", key=2)
    predict = sg.Button("Predict", key=3)
    export = sg.Button("Export file", key=4)
    layout = [
        [titolo],
        [carica, nome_file],
        [seleziona_modello],
        [radio1, radio2, radio3],
        [dataset],
        [clean, predict, export]
    ]

    return layout


def show_ui():
    """
    In questa funzione vengono gestite tutte le funzionalità della UI, inclusa la comunicazione con il controller
    quì istanziato.
    :return:
    """
    # Opzioni globali UI
    sg.set_options(auto_size_buttons=True)

    # variabili essenziali UI

    df = pd.DataFrame()
    controller = Controller()
    checkbox = 1
    filename = ''

    data = []
    header_list = []

    # CARICAMENTO FILE
    filename = sg.popup_get_file(
        'filename to open', no_window=True, file_types=(("CSV Files", "*.csv"),))

    # --- populate table with file contents --- #
    if filename == '':
        return

    # --- Carico il primo file --- #

    df = controller.load_data(filename)

    # --- Creazione layout --- #

    layout = set_layout(filename, df, checkbox)

    # --- Creazione finestra --- #

    window = sg.Window('Table', layout, grab_anywhere=False, element_padding=(5, 5))

    # --- Gestione eventi --- #

    while True:
        event, values = window.Read()
        print(event, values)

        # Evento non riconosciuto o uscita: chiudi la finestra
        if event is None or event == 'Exit':
            break

        # Evento 1: carico una nuova tabella
        if event == 1:  # load dataset
            filename = sg.popup_get_file(
                'filename to open', no_window=True, file_types=(("CSV Files", "*.csv"),))
            if filename is not None:
                try:
                    df = controller.load_data(filename)
                    layout_new = set_layout(filename, df, checkbox)
                    window_new = sg.Window('Table', layout_new, grab_anywhere=False, element_padding=(5, 5))
                    window.close()
                    window = window_new
                except Exception:
                    sg.popup_error('Errore nella apertura del file csv')

        # Evento 2: pulisco il dataset da valori mancanti
        if event == 2:  # clean dataset
            if filename == '':
                sg.popup("Devi prima caricare un file!")
            # TODO else: pulisci la tabella e mostrala pulita
            else:
                for column in df.columns:
                    df[column].fillna(df[column].mode()[0], inplace=True)
                layout_new = set_layout(filename, df, checkbox)
                window_new = sg.Window('Table', layout_new, grab_anywhere=False, element_padding=(5, 5))
                window.close()
                window = window_new

        # Evento 3: predico la classe per ogni riga del dataset, fa partire sia preprocessing che predizione
        #           con modello già pre-allenato.
        if event == 3:  # clean dataset
            if filename == '':
                sg.popup("Devi prima caricare un file!")
            # TODO else: predici le classi dei sample della tabella e mostra la predizione in prima colonna per sample

    # --- Chiusura finestra alla fine del ciclo di eventi --- #

    window.close()


# Chiamo la UI
show_ui()
