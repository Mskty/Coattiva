import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import plot_roc_curve
from sklearn.metrics import plot_confusion_matrix

from data import AlgorithmPipeline


class GraphBuilder:

    #def __init__(self, estimator: AlgorithmPipeline):

    def plot_roc_curve(self, data: pd.DataFrame):
        # fa comparire il grafico della roc_curve
        pass

    def plot_precision_recall(self, data: pd.DataFrame):
        # fa comparire il grafico della precision vs recall con threshold della decision function (default 0)
        pass

    def plot_confusion_matrix(self, data: pd.DataFrame):
        # da comparire il grafico della confusion matrix
        pass
