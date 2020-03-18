import itertools
import random
import matplotlib.pyplot as plt
import pandas as pd
import sklearn as skl
import numpy as np
import time
import datetime
import xgboost as xgb
from sklearn import datasets, svm, model_selection
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectFromModel
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, pairwise, precision_recall_curve, precision_score, \
    recall_score, f1_score, roc_auc_score
from sklearn import preprocessing
from sklearn import tree
from sklearn.preprocessing import StandardScaler, MinMaxScaler
