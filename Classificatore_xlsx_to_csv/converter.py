from tkinter import filedialog as fd, Tk, filedialog
import pandas as pd
import sys
import warnings

"""
Questo script serve per convertire il file xlsx su cui effettuare delle predizioni in csv
in quanto il programma per addestramento e utilizzo dei modelli richiede tale formato
per funzionare correttamente.
"""


""" Funzioni di utilità"""


def load_raw_data_excel(raw_data_path) -> pd.DataFrame:
    """
        ritorna un pandas Dataframe dal file excel specificato dal percorso
        :param raw_data_path:
        :return:
        """
    data = pd.read_excel(raw_data_path,
                         sheetname=0,
                         header=0,
                         index_col=False,
                         keep_default_na=True)
    return data


# ignore all warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

print("Selezionare il file xlsx da convertire:")
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = fd.askopenfilename(initialdir="/", title="Seleziona csv", filetypes=(("xlxs files", "*.xlsx"), ("all files", "*.*")))
print("Conversione del file in corso...")
data = load_raw_data_excel(filename)
print("Selezionare la destinazione su cui salvare il file come csv:")
export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
data.to_csv(export_file_path, index=None, header=True)
