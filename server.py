from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pickle
import pandas as pd
import random
import json
import os
df = pd.read_csv('training_data.csv')
input_symptoms = {}
output_prediction = ""

df.drop(df[["Unnamed: 133"]],axis=1,inplace=True)
symptomsList = [x for x in df if x!='prognosis']

app = Flask(__name__)
app.secret_key = "abc"
CheckForJaundice = pickle.load(open('PKLs/Jaundice_pred.pkl','rb'))
CheckForDengue = pickle.load(open('PKLs/Dengue_pred.pkl','rb'))
# CheckForCC = pickle.load(open('PKLs/CC_pred.pkl','rb'))
# CheckForTB = pickle.load(open('PKLs/TB_pred.pkl','rb'))
# CheckForCPox = pickle.load(open('PKLs/ChickenPox_pred.pkl','rb'))
Pickles = []
for root,dirs,files in os.walk('D:\PEC\THIRD YEAR\SEMESTER 5\AI+WebTech+SE Project\DotComDoctor-Main\PKLs'):
    Pickles.append(files)
OpenedPickles = {}
for pickleFile in files:
        name = pickleFile[:-9]
        OpenedPickles[name] = pickle.load(open(f"D:\PEC\THIRD YEAR\SEMESTER 5\AI+WebTech+SE Project\DotComDoctor-Main\PKLs\{pickleFile}","rb"))
@app.route('/',methods=['GET','POST'])
def symptomGiver():
    if(request.method == 'POST'):
        chosen_symptoms = request.form.getlist('symptoms')
        for i in df.columns:
            if i in chosen_symptoms:
                input_symptoms[i] = 1
            else:
                input_symptoms[i] = 0
        test_x = pd.read_json(json.dumps([input_symptoms]))
        # print(test_x.head())
        # print(test_x.columns)
        #test_x.drop(df[["Unnamed: 133"]],axis=1,inplace=True)
        test_x.drop(df[["prognosis"]],axis=1,inplace=True)
        #test_x.drop(columns=['prognosis','Unnamed: 133'],axis=1,inplace = True)
        #forTB = {'Prediction':CheckForTB.predict(test_x)[0],'Probs':{'HasDisease':CheckForTB.predict_proba(test_x)[0][1],'NotDiseased':CheckForTB.predict_proba(test_x)[0][0]}}
        #forCC = {'Prediction':CheckForCC.predict(test_x)[0],'Probs':{'HasDisease':CheckForCC.predict_proba(test_x)[0][0],'NotDiseased':CheckForCC.predict_proba(test_x)[0][1]}}
        forJaundice = {'Prediction':CheckForJaundice.predict(test_x)[0],'Probs':{'HasDisease':CheckForJaundice.predict_proba(test_x)[0][0],'NotDiseased':CheckForJaundice.predict_proba(test_x)[0][1]}}
        forDengue = {'Prediction':CheckForDengue.predict(test_x)[0],'Probs':{'HasDisease':CheckForDengue.predict_proba(test_x)[0][0],'NotDiseased':CheckForDengue.predict_proba(test_x)[0][1]}}
        #forCPox = {'Prediction':CheckForCPox.predict(test_x)[0],'Probs':{'HasDisease':CheckForCPox.predict_proba(test_x)[0][0],'NotDiseased':CheckForCPox.predict_proba(test_x)[0][1]}}
        Results = []
        for k,v in OpenedPickles.items():
            print(f"\nDisease {k} ")
            Prediction = v.predict(test_x)[0]
            Probs = v.predict_proba(test_x)
            print(f"\tPrediction = {Prediction}\t\tProbs = {Probs}")
            DiseaseDict = {'Prediction':Prediction}
            ReversedProbsList = ['hepatitis A','Osteoarthristis','Paralysis (brain hemorrhage)','Peptic ulcer diseae','Pneumonia','Psoriasis','Tuberculosis','Typhoid','Urinary tract infection','Varicose veins']
            if k in ReversedProbsList:
                DiseaseDict['Probs'] = {'HasDisease':Probs[0][1],'NotDiseased':Probs[0][0]}
            else:
                DiseaseDict['Probs'] = {'HasDisease':Probs[0][0],'NotDiseased':Probs[0][1]}
            Results.append(DiseaseDict)
        # print(CheckForCC.predict(test_x))
        # print(CheckForJaundice.predict(test_x))
        # print(CheckForDengue.predict(test_x))
        # print(CheckForTB.predict(test_x))
        # print(CheckForCPox.predict(test_x))
        # print(CheckForCC.predict_proba(test_x))
        # print(CheckForJaundice.predict_proba(test_x))
        # print(CheckForDengue.predict_proba(test_x))
        # print(CheckForTB.predict_proba(test_x))
        # print(CheckForCPox.predict_proba(test_x))
        # print(forTB)
        # print(forCC)
        # print(forJaundice)
        # print(forDengue)
        # print(forCPox)
        #Results = [forDengue,forJaundice]
        Predicted_Diagnosis = []
        Predicted_Probability = []
        ActualPredictionAvailable = False
        for i in Results:
            if i['Prediction'][:3] != 'Not':
                Predicted_Diagnosis.append(i['Prediction'])
                Predicted_Probability.append(i['Probs']['HasDisease']*100)
                ActualPredictionAvailable = True
        if not Predicted_Diagnosis:
            for i in Results:
                if(i['Probs']['HasDisease'] != 0.0):
                    Predicted_Diagnosis.append(i['Prediction'][4:])
                    Predicted_Probability.append(i['Probs']['HasDisease']*100)
        #output_prediction = {'RFC-result':df.iloc[RFCoutput[0],-2],'DTC-result':df.iloc[DTCoutput[0],-2],}
        output_prediction = ""
        if ActualPredictionAvailable:
            output_prediction = (ActualPredictionAvailable,Predicted_Diagnosis[0],Predicted_Probability[0])
        else:
            output_prediction = (ActualPredictionAvailable,list(zip(Predicted_Diagnosis,Predicted_Probability)))
        session["diagnosis"] = output_prediction
        #print(output_prediction)
        return redirect(url_for('diagnosis'))
    return render_template('index.html',variable = symptomsList)
@app.route('/diagnosis')
def diagnosis():
    #print(session['diagnosis'])
    return render_template('diagnosis.html',variable=session['diagnosis'])
if __name__ == '__main__':
    app.run(port=5000,debug=True)