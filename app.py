from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__, static_folder='static')

cred = credentials.Certificate('credentails.json')
firebase_admin.initialize_app(cred, {'databaseURL' : 'https://agri-genomics-default-rtdb.asia-southeast1.firebasedatabase.app'})
ref = db.reference('/Data')

def get_height():
    with open('height.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def get_subpopulation():
    with open("subpopulation.pkl", "rb") as f:
        model = pickle.load(f)
    return model

def get_yield():
    with open("yield.pkl", "rb") as f:
        model = pickle.load(f)
    return model

def get_accuracy():
    accuracy_score = 94
    return accuracy_score

def get_r2score():
    r2score = 94
    return r2score

def get_r2score_y():
    r2scorey = 86
    return r2scorey

def conversion(input_sequence):
    primary = pd.read_csv("Primary.csv")
    primary = np.array(primary)
    primary = primary.reshape(-1)

    #Conversion of string to float
    input_list = list(input_sequence)
    for i in range(len(input_sequence)):
        if input_sequence[i] == "N":
            input_list[i] = primary[i]
    final_sequence = ''.join(input_list)
    legend = {'A': 1, 'T': 2, 'C': 3, 'G': 4}
    string = ""
    for i in final_sequence:
        for j in i:
            string += str(legend[j])
    return int(string)

model_height = get_height()
model_subpopulation = get_subpopulation()
model_yield = get_yield()
accuracy = get_accuracy()
r2score = get_r2score()
r2scorey = get_r2score_y()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predictions')
def makepredictions():
    return render_template('predictions.html')

@app.route('/data')
def viewdata():
    return render_template('data.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        gene_sequence = request.form['gene_sequence']
        final_sequence = conversion(gene_sequence)


        predicted_height = model_height.predict([[final_sequence]])
        predicted_height = predicted_height[0]

        predicted_subpopulation = model_subpopulation.predict([[final_sequence]])
        predicted_subpopulation = predicted_subpopulation[0]

        predicted_yield = model_yield.predict([[final_sequence]])
        predicted_yield = predicted_yield[0]

        ref.push({
            'sequence': gene_sequence,
            'height':round(predicted_height, 2),
            'subpopulation':predicted_subpopulation,
            'yield':round(predicted_yield, 2),
        })
        return jsonify({'height': predicted_height, 'subpopulation' : predicted_subpopulation, 'sequence':gene_sequence, 'acc':accuracy, 'r2':r2score, 'yield':predicted_yield, 'r2y':r2scorey})

if __name__ == '__main__':
    app.run(host = "localhost", port = 9999, debug = True)
