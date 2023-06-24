from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import sklearn

app = Flask(__name__, static_folder='static')

def load_model(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model

model_height = load_model('height.pkl')
model_subpopulation = load_model("subpopulation.pkl")
model_yield = load_model("yield.pkl")
accuracy = 94
r2score = 94
r2scorey = 86


def conversion(input_sequence):
    primary = pd.read_csv("Primary.csv")
    primary = np.array(primary).reshape(-1)

    #Conversion of string to float
    legend = {'A': 1, 'T': 2, 'C': 3, 'G': 4}
    final_sequence = [str(legend.get(base, primary[i])) for i, base in enumerate(input_sequence) if base != 'N']
    return int(''.join(final_sequence))


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

        input_array = np.array([[final_sequence]])
        predicted_height = model_height.predict(input_array)[0]
        predicted_subpopulation = model_subpopulation.predict(input_array)[0]
        predicted_yield = model_yield.predict(input_array)[0]


        return jsonify({'height': predicted_height, 'subpopulation' : predicted_subpopulation, 'sequence':gene_sequence, 'acc':accuracy, 'r2':r2score, 'yield':predicted_yield, 'r2y':r2scorey})

if __name__ == '__main__':
    app.run(host = "localhost", port = 9999, debug = True)
