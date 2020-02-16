import itertools
import random
import tkinter as tk

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import sklearn as skl
import numpy as np
import seaborn as sns
import time
import datetime
import xgboost as xgb

from tkinter import filedialog

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from joblib import dump, load
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, svm, model_selection
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV, \
    RandomizedSearchCV, cross_validate, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, pairwise, precision_recall_curve, \
    precision_score, recall_score, f1_score, roc_auc_score
from sklearn import preprocessing
from sklearn import tree
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
from Modellazione.Model_Trainer import separazione_label
from utility.Enums import *


class DataModel:

    def __init__(self, type: PFPGEnum, data: pd.DataFrame = None, filename: str = None):
        try:
            self.df: pd.DataFrame = pd.read_csv(filename)
        except Exception:
            print("no file passed")
        else:
            self.df: pd.DataFrame = data
        self.type = type
        self.enabledcolumns = self.df.copy()
        self.disabledcolumns = pd.DataFrame()

    # Getter functions

    def get_disabledcolumnsnames(self) ->list:
        return list(self.disabledcolumns.columns.values)

    def get_columnsnames(self) -> list:
        names = list(self.df.columns.values)
        names.remove("label")
        return names

    def get_rows(self) -> int:
        return len(self.df)

    def get_positive_label(self) -> int:
        return len(self.df.loc[(self.df.label == 1)])

    def get_negative_label(self) -> int:
        return len(self.df.query("label==0"))

    def clean(self):
        # TODO INVOCARE PULIZIA
        pass

    def preprocess(self):
        # TODO INVOCARE PREPROCESSAMENTO
        pass

    def train_test_splitter_possibilities(self):
        """
            Dato il dataframe dei dati storici preparati ritorna un nuovo dataframe dove ogni riga
            rappresenta la data di un ruolo presente nei dati storici. Ogni riga riporta, per quella data
            quanti crediti appartengono a quel ruolo e tutti i precedenti (nesempi), quanti di questi sono
            classificati come positivi (true), e quanti come negativi (false). L'idea è che ciascuna delle
            date dei ruoli può essere utilizzata per splittare i dati storici in training set e test set,
            vengono dunque riportate le possibili composizioni dei training set ad ogni data di ruolo scelta.
            """
        # Ricavo i ruoli
        ruoli = self.df.DataCaricoTitolo.unique()

        # Ordino in modo crescente le date dei ruoli
        dates = [datetime.datetime.strptime(ts, "%Y-%m-%d") for ts in ruoli]
        dates.sort()
        ruoli = list([datetime.datetime.strftime(ts, "%Y-%m-%d") for ts in dates])

        # creo un dataframe con le possibili date e numero di esempi contenuto in ogni possibile training set
        results = pd.DataFrame()
        results["ruolo"] = ruoli
        results["nesempi"] = 0
        results["true"] = 0
        results["false"] = 0
        count = 1
        for r in ruoli:
            results.loc[(results.ruolo == r), "nesempi"] = len(self.df.loc[
                                                                   self.df.DataCaricoTitolo.isin(ruoli[:count])])
            results.loc[(results.ruolo == r), "true"] = len(
                self.df.loc[(self.df.DataCaricoTitolo.isin(ruoli[:count])) & (self.df.label == 1)])
            results.loc[(results.ruolo == r), "false"] = len(
                self.df.loc[(self.df.DataCaricoTitolo.isin(ruoli[:count])) & (self.df.label == 0)])
            count = count + 1

        return results

    def train_test_splitter(self, dates):
        """
        Suddivide il dataframe dei dati storici aggregati e preparati in training set e test set, dove il training set
        sarà composto di tutti i titoli con campo DataCaricoTitolo uguale ad uno dei valori presenti nella lista dates
        :param dates: lista di date
        :return: oggetti TrainModel e TestModel
        """
        # copio per non modificare dataframe originale
        df = self.df.copy()

        # Divisione test out of sample e training in sample
        trainset = df.loc[(df.DataCaricoTitolo.isin(dates))]
        testset = df.loc[(~df.DataCaricoTitolo.isin(dates))]

        # Drop dell colonna DataCaricoTitolo una volta separati i due set
        trainset.drop(columns="DataCaricoTitolo", inplace=True)
        testset.drop(columns="DataCaricoTitolo", inplace=True)

        # Mescolo le righe del training set
        trainset = skl.utils.shuffle(trainset, random_state=42)

        # Ritorno train e test set
        # TODO RITORNA TRAINMODEL E TESTMODEL
        return trainset, testset

    def disablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.df.columns.values))):
            self.disabledcolumns = self.df[columns]
            self.enabledcolumns.drop(columns=columns)
        else:
            print("error: colonne non presenti")

    def enablecolumns(self, columns: list):
        if set(columns).issubset(set(list(self.disabledcolumns.columns.values))):
            self.enabledcolumns[columns] = self.disabledcolumns[columns]
            self.disabledcolumns.drop(columns)
        else:
            print("error: colonne non presenti")




