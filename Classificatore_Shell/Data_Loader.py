from Classificatore_Shell.funzioni import *
from tkinter import filedialog as fd, Tk


def load_storic_data():
    """
    permette di caricare il file contenente i dati storici dall'estrazione e li separa in PF e PG
    :return: i due dataframes PF e PG
    """
    Tk().withdraw()  # non c'è bisogno di una GUI avanzata
    filename = fd.askopenfilename(initialdir="/", title="Seleziona csv", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    # crezione dataframes
    df = load_raw_data(filename)
    dfPG = df[df.TipoPersonalità == "PG"].copy()  # Persone Giuridiche
    dfPF = df[df.TipoPersonalità == "PF"].copy()  # Persone Fisiche
    return dfPF, dfPG


def load_new_data():
    """
    permette di caricare il file csv contenente i dati su cui riportare successivamente le predizioni del modello
    :return: pandas dataframe contenente i dati del file csv
    """
    Tk().withdraw()  # non c'è bisogno di una GUI avanzata
    filename = fd.askopenfilename(initialdir="/", title="Seleziona csv", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    # crezione dataframe
    df = load_raw_data(filename)
    return df


def save_data(df: pd.DataFrame):
    """
    Permette di selezionare un percorso da file sistem e salvare il dataframe salvato come file csv su tale perscorso
    :param df: dataframe che si desidera salvare su file csv
    :return:
    """
    Tk().withdraw()  # non c'è bisogno di una GUI avanzata
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv(export_file_path, index=None, header=True)
