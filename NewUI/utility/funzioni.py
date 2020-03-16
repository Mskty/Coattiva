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
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, pairwise, precision_recall_curve, precision_score, recall_score, f1_score, roc_auc_score
from sklearn import preprocessing
from sklearn import tree
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler
