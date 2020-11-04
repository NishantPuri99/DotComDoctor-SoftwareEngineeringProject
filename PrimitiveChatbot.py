from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
df = pd.read_csv('training_data.csv')
dis_list = list(set(df['prognosis']))
dis_dict = {}
j=0
for disease in dis_list:
    dis_dict[disease] =j
    j+=1
df['prognosis'] = df['prognosis'].map(dis_dict)
df.drop(df.filter(regex="Unnamed"),axis=1, inplace=True)
train_X = df.drop(columns='prognosis')
train_Y = df['prognosis']
#Decision Tree
DTC = DecisionTreeClassifier()
DTC.fit(train_X,train_Y)
#Random Forest
RFC =RandomForestClassifier()
RFC.fit(train_X,train_Y)

testDF = pd.read_csv('test_data.csv')
testDF['prognosis'] = testDF['prognosis'].map(dis_dict)
test_x = testDF.drop(columns='prognosis')
test_y = testDF['prognosis']
print(type(test_x))
test_predDTC = DTC.predict(test_x)
test_predRFC = RFC.predict(test_x)

DTCAccuracy = accuracy_score(test_y,test_predDTC)
RFCAccuracy = accuracy_score(test_y,test_predRFC)
class_probs = DTC.predict_proba(test_x)
print(class_probs)
print(DTCAccuracy)
print(RFCAccuracy)