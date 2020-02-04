from model import *
from preprocesser import *

files = {
    1: "svm_file_path",
    2: "rnf_file_path",
    3: "nn_file_path"
}


class Controller:
    preprocessor: Preprocessor = None
    active_model: ModelloPredittivo = None
    selected_model: ModelType = None

    original_data: pd.DataFrame = None
    preprocessed_data: pd.DataFrame = None
    predicted_data: pd.DataFrame = None

    def __init__(self):
        """
        Modello di default: svm
        """
        self.selected_model = ModelType.SVM
        #TODO self.active_model = ModelloPredittivo(files[self.selected_model.value])
        self.preprocessor = Preprocessor()

    def load_data(self, csv_file: str) -> pd.DataFrame:
        """
        Carica su come Pandas Dataframe i dati dal file csv
        il dataframe sarà accessibile da original_data
        errore nel caso non venga scelto un file csv controllato dalla interfaccia
        :param csv_file:
        :return:
        """
        self.original_data = load_raw_data(csv_file)
        return self.original_data

    def change_model(self, new_model: ModelType):
        """
        Sostituisce il modello predittivo attualmente attivo con quello selezionato dall'utente
        caricandolo dall'apposito file

        :param new_model:
        :return:
        """
        self.selected_model = new_model
        self.active_model = ModelloPredittivo(files[self.selected_model])

    def predict(self) -> pd.DataFrame or bool:
        """
        Ritorna il Dataframe presente su original_data con aggiunta come prima colonna quella contenente i
        valori predetti
        :return:
        """
        if self.preprocessed_data is not None:
            predicted_values = self.active_model.predict(self.preprocessed_data.to_numpy())
            self.predicted_data = self.original_data.copy()
            self.predicted_data["Risultato"] = predicted_values
            # Riordino l'ordine delle colonne per mettere per prima la predizione
            cols = self.predicted_data.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            self.predicted_data = self.predicted_data[cols]
            return self.predicted_data
        else:
            # Non è stato preparato il dataset
            return False

    def export_prediction(self):
        """
        Apre una finestra per salvare il dataset originale contenente anche la colonna delle predizioni
        come file .csv
        :return:
        """
        if self.predicted_data is not None:
            save_dataset(self.predicted_data)
            return True
        else:
            return False

    def clean_dataset(self, removenan=False) -> pd.DataFrame:
        """
        Pulisce il dataset rimuovendo (removenan=True) o sostituendo i valori mancanti
        TODO Forse dovrebbe sostituire l'original dataset visto che in caso di rimozioni è su questo che si faranno
        TODO Magari salvare le righe che non si sono potute predire
        :param removenan:
        :return:
        """
        return self.preprocessor.clean(self.original_data)

    def preprocess_data(self) -> bool:
        """
        Prepara il dataset per essere utilizzato per ottenere le predizioni, salva il dataset preparato su
        preprocessed_data. Ritorna falso se non è ancora stato caricato il dataset
        :return:
        """
        if self.original_data is not None:
            self.preprocessed_data = self.preprocessor.preprocess(self.original_data)
            return True
        else:
            return False
