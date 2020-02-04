from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
from xgboost import XGBClassifier

from funzioni import *

traindf=load_raw_data("datasets/train")

show_data_info(traindf)

#add the Title feature
traindf['Title'] = traindf['Name'].str.split(", ", expand=True)[1].str.split(".", expand=True)[0]
title_names = (traindf['Title'].value_counts() < 10)  #this will create a true false series with title name as index
traindf['Title'] = traindf['Title'].apply(lambda x: 'Misc' if title_names.loc[x] == True else x)
print(title_names)

#handle missing values
traindf.drop(columns=["Name","Ticket","Cabin","PassengerId"], inplace=True)
traindf.dropna(subset=["Embarked"], inplace=True)


age_imputer=SimpleImputer()
traindf["Age"]=age_imputer.fit_transform(traindf[["Age"]])

traindf: pd.DataFrame = traindf.sample(frac=1)

#separate target label
Y=traindf["Survived"].to_numpy()
traindf.drop(columns="Survived", inplace=True)

show_data_info(traindf)

#start preprocessing
cat_columns=["Sex","Embarked","Title"]
num_columns=["Age","Fare", "SibSp","Parch","Pclass"]

#onehot encoding
cat_dum=pd.get_dummies(traindf[cat_columns].astype(str))
traindf.drop(columns=["Sex","Embarked","Title"], inplace=True)
traindf=traindf.join(cat_dum)

#scaler per numerici
features = traindf[num_columns]

scaler = StandardScaler().fit(features.values)
features = scaler.transform(features.values)

traindf[num_columns] = features

show_data_info(traindf)

#select model

X=traindf.to_numpy()

correlation_heatmap(traindf)
plt.clf()
#plt.show()

clf=KNeighborsClassifier(n_neighbors=3)
cross_validation(clf,X,Y,5)

clf2=RandomForestClassifier(n_estimators=200, min_samples_leaf=3,n_jobs=-1)
cross_validation(clf2,X,Y,5)
#param_grid={'n_estimators': [200,300,400,500], 'min_samples_leaf': [1,2,3,4,5]}
#grid_search(param_grid,RandomForestClassifier(),X,Y)
#clf.fit(X,Y)
#print(confusion_matrix(Y,clf.predict(X)))
#print(classification_report(Y,clf.predict(X)))
#print(rf_feat_importance(clf,traindf)[:9])
"""
#precision recall curve
precision,recall,threshold=precision_recall_curve(Y,clf.predict_proba(X)[:,1])
plot_precision_recall_vs_threshold(precision,recall,threshold)
plt.show()
plt.clf()

#roc curve
tpr,fpr,_=roc_curve(Y,clf.predict_proba(X)[:,1])
score=roc_auc_score(Y,clf.predict_proba(X)[:,1])
plot_roc_curve(tpr,fpr,"area="+str(round(score,2)))
plt.show()
print (str(clf.get_params()))
"""