import pandas as pd
from tkinter import filedialog as fd, Tk

def load_csv():
    """
    permette di caricare il file csv contenente i dati su cui riportare successivamente le predizioni del modello
    :return: pandas dataframe contenente i dati del file csv
    """
    Tk().withdraw()  # non c'è bisogno di una GUI avanzata
    filename = fd.askopenfilename(initialdir="/", title="Seleziona csv", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    # crezione dataframe
    df = pd.read_csv(filename)
    return df