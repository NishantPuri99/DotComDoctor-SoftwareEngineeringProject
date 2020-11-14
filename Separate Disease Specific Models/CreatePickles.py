import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv('training_data.csv')
df.drop("Unnamed: 133",inplace=True,axis=1)
print(df['prognosis'].unique())
for i in df['prognosis'].unique():
    df_new = df.copy()
    df_new.loc[df_new['prognosis']!=i,"prognosis"] = f"Not {i}"
    X_train = df_new.drop('prognosis',axis=1).copy()
    y_train = df_new['prognosis'].copy()
    clt_rf = RandomForestClassifier()
    clt_rf.fit(X_train,y_train)
    pickle.dump(clt_rf,open(f"D:\PEC\THIRD YEAR\SEMESTER 5\AI+WebTech+SE Project\DotComDoctor-Main\PKLs\{i}_pred.pkl","wb"))
    del df_new
