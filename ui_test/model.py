from funzioni import *
from choose_model_enum import *


class ModelloPredittivo:
    actual_model = None

    def __init__(self, model_file_path: str):
        """
        crea un oggetto di tipo ModelloPredittivo con actual model contenente il
        classificatore passato come file
        :param model_file_path:
        """
        self.actual_model = load_model(model_file_path)

    def predict(self, values: np.array):
        """
        Ritorna in un array i valori predetti associati a values
        :param values:
        :return:
        """
        return self.actual_model.predict(values)

