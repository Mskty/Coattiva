from enum import Enum


class PFPGEnum(Enum):
    PF = 0
    PG = 1

class SamplingEnum(Enum):
    NONE = 0
    UNDER = 1
    SMOTE = 2

class ScalingEnum(Enum):
    NONE = 0
    UNDER = 1
    SMOTE = 2

class ClassifierEnum(Enum):
    LOGISTIC = 0
    SVC = 1
    TREE = 2
    FOREST = 3
    XGB = 4

class NewFileEnum(Enum):
    NEW = 0
    OLD = 1

