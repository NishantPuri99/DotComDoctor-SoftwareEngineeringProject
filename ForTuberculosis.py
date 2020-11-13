import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

df_CC = pd.read_csv('training_data.csv')
df_CC.drop("Unnamed: 133",inplace=True,axis=1)
df_CC.loc[df_CC['prognosis']!="Tuberculosis","prognosis"] = "Not Tuberculosis"
X_train_CC = df_CC.drop('prognosis',axis=1).copy()
y_train_CC = df_CC['prognosis'].copy()

df_test_CC = pd.read_csv('test_data.csv')
df_test_CC.loc[df_test_CC['prognosis']!="Tuberculosis","prognosis"] = "Not Tuberculosis"
X_test_CC = df_test_CC.drop('prognosis',axis=1).copy()
y_test_CC = df_test_CC['prognosis']

clt_rf_CC = RandomForestClassifier()
clt_rf_CC.fit(X_train_CC,y_train_CC)
y_pred_CC = clt_rf_CC.predict(X_test_CC)
#print(accuracy_score( y_test_CC, y_pred_CC))
pickle.dump(clt_rf_CC,open("TB_pred.pkl","wb"))