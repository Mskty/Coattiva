from enum import Enum


class PFPGEnum(Enum):
    # Enum per il tipo di titoli di credito:
    # PF= Persone Fisiche
    # PG= Persone Giuridiche
    PF = 0
    PG = 1


class SamplingEnum(Enum):
    # Enum per il tipo di sampling da usare sui dati di addestramento:
    # NONE= Nessun Sampling dei dati
    # UNDER= Random Undersampling
    # SMOTE= Smote Oversampling
    NONE = 0
    UNDER = 1
    SMOTE = 2


class ScalingEnum(Enum):
    # Enum per il tipo di scaling da usare sui dati per le colonne numeriche non categoriche:
    # NONE= Nessuno Scaler
    # STANDARD= Standard Scaler
    # MINMAX= Minmax Scaler
    NONE = 0
    STANDARD = 1
    MINMAX = 2


class ClassifierEnum(Enum):
    # Enum per il tipo di algoritmo da utilizzare per addestrare il modello predittivo di classificazione:
    # LOGISTIC = Logistic Regressior Classifier
    # SVC = Support Vector Machine Classifier
    # TREE = Decision Tree Classifier
    # FOREST = Random Forest Classifier
    LOGISTIC = 0
    SVC = 1
    TREE = 2
    FOREST = 3
    XGB = 4


class NewFileEnum(Enum):
    # Enum per il tipo di file caricato dall'utente al momento dell'utilizzo del modello addestrato:
    # NEW = File contenente titoli recenti già aggregati con il loro specifico tracciato
    # OLD = File contenente titoli storici non aggregati con il loro specifico tracciato
    NEW = 0
    OLD = 1
