import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
# from build import Hello
# from sim import Simulation

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'rb'))

######################################################################################################################
# CREATE DATA Base
# exec(open('create_table.py').read())
######################################################################################################################
#


@app.route('/')
def home():
    return render_template('index.html')


# @test
# nic
# tetst test

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    # features = [int(x) for x in request.form.values()]
    # final_features = [np.array(features)]
    # prediction = model.predict(final_features)

    features = [int(x) for x in request.form.values()]

    # prediction = model.suma(features)
    # prediction = Hello()
    prediction = [1, 2, 3, 4, 5]

    output = prediction
    # output = round(prediction[0], 1)

    return render_template('index.html', prediction_text=f'Your Rating is: {output}')


if __name__ == "__main__":
    app.run(debug=True)
