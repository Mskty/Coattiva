class Score:
    """
    Classe per salvare cinque metriche in un unico oggetto per riportarle con facilità nella parte view di
    interfaccia grafica.
    PARAMETRI:
    self.accuracy: valore float che rappresenta la metrica di accuratezza
    self.precision: valore float che rappresenta la metrica di precisione
    self.recall: valore float che rappresenta la metrica recall
    self.f1: valore float che rappresenta la metrica f1_score o f_score
    self.roc_auc: valore float che rappresenta la metrica roc_auc_score
    """
    def __init__(self, accuracy: float, precision: float, recall: float, f1: float, roc_auc: float):
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1 = f1
        self.roc_auc = roc_auc
