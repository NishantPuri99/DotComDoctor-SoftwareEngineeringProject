from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pickle
import pandas as pd
import random
import json
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
df = pd.read_csv('training_data.csv')
input_symptoms = {}
df.drop(df[["Unnamed: 133"]],axis=1,inplace=True)
symptomsList = [x for x in df if x!='prognosis']
for i in df.columns:
    input_symptoms[i] = 0
output_prediction = ""

english_bot = ChatBot('Bot',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
],
trainer='chatterbot.trainers.ListTrainer')

english_bot.set_trainer(ListTrainer)

app = Flask(__name__)
app.secret_key = "abc"
Pickles = []
for root,dirs,files in os.walk('D:\PEC\THIRD YEAR\SEMESTER 5\AI+WebTech+SE Project\DotComDoctor-Main\PKLs'):
    Pickles.append(files)
OpenedPickles = {}
for pickleFile in files:
        name = pickleFile[:-9]
        OpenedPickles[name] = pickle.load(open(f"D:\PEC\THIRD YEAR\SEMESTER 5\AI+WebTech+SE Project\DotComDoctor-Main\PKLs\{pickleFile}","rb"))
@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/chatbot")
def chatbot_main():
    return render_template("mainbot.html")



@app.route("/map")
def map_function():
    return render_template('map2.html', title='Map')

@app.route("/examples")
def examples():
    return render_template("examples.html")

filenumber=int(os.listdir('saved_conversations')[-1])
filenumber=filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))
    response_list = response.split('|')
    session["symptoms"] = response_list
    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()
    return response

@app.route('/symptom-selector',methods=['GET','POST'])
def symptomGiver():
    if(request.method == 'POST'):
        chosen_symptoms = request.form.getlist('symptoms')
        for i in chosen_symptoms:
            if i in df.columns:
                input_symptoms[i] = 1
        return "Symptoms Added, Please close this page and continue."
    else:
        return render_template('sym-sel.html',variable=session["symptoms"])
@app.route('/diagnosis')
def diagnosis():
    test_x = pd.read_json(json.dumps([input_symptoms]))
    test_x.drop(df[["prognosis"]],axis=1,inplace=True)
    Results = []
    for k,v in OpenedPickles.items():
        Prediction = v.predict(test_x)[0]
        Probs = v.predict_proba(test_x)
        # # Use ths 2 statements below for checking purposes (Uncomment these 3 lines)
        # print(f"\nDisease {k} ")
        # print(f"\tPrediction = {Prediction}\t\tProbs = {Probs}")
        DiseaseDict = {'Prediction':Prediction}
        ReversedProbsList = ['hepatitis A','Osteoarthristis','Paralysis (brain hemorrhage)','Peptic ulcer diseae','Pneumonia','Psoriasis','Tuberculosis','Typhoid','Urinary tract infection','Varicose veins']
        if k in ReversedProbsList:
            DiseaseDict['Probs'] = {'HasDisease':Probs[0][1],'NotDiseased':Probs[0][0]}
        else:
            DiseaseDict['Probs'] = {'HasDisease':Probs[0][0],'NotDiseased':Probs[0][1]}
        Results.append(DiseaseDict)
    Predicted_Diagnosis = []
    Predicted_Probability = []
    ActualPredictionAvailable = False
    for i in Results:
        if i['Prediction'][:3] != 'Not':
            Predicted_Diagnosis.append(i['Prediction'])
            Predicted_Probability.append(round(i['Probs']['HasDisease']*100))
            ActualPredictionAvailable = True
    if not Predicted_Diagnosis:
        for i in Results:
            if(i['Probs']['HasDisease'] > 0.0):
                Predicted_Diagnosis.append(i['Prediction'][4:])
                Predicted_Probability.append(round(i['Probs']['HasDisease']*100))
    output_prediction = ""
    if ActualPredictionAvailable:
        output_prediction = (ActualPredictionAvailable,Predicted_Diagnosis[0],Predicted_Probability[0])
    else:
        output_prediction = (ActualPredictionAvailable,list(zip(Predicted_Diagnosis,Predicted_Probability)))
    session["diagnosis"] = output_prediction
    return render_template('diagnosis.html',variable=session['diagnosis'])
if __name__ == '__main__':
    app.run(port=5000)