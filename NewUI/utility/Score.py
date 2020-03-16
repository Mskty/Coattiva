class Score:
    """
    Classe per salvare cinque metriche in un unico oggetto per riportarle con facilità nella parte view di
    interfaccia grafica
    """
    def __init__(self, accuracy: float, precision: float, recall: float, f1: float, roc_auc: float):
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1 = f1
        self.roc_auc = roc_auc
