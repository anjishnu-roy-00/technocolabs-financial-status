from urllib import request
from flask import Flask,render_template,url_for,request
import pickle
import numpy as np
app = Flask(__name__)

app=Flask(__name__)
@app.route("/")

def index():
    return render_template("index.html")
 
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,9)
    loaded_model = pickle.load(open("./QDA.pkl","rb"))
    preds = loaded_model.predict(to_predict)
    # 0 : operating, 1 : closed
    pred = preds[0]
    if pred == 0:
        result = 'operating'
    elif pred == 1:
        loaded_model = pickle.load(open("./RF.pkl","rb"))
        preds = loaded_model.predict(to_predict)
    # 0 : operating, 1 : acquired, 2 : closed, 3 : ipo
        pred = preds[0]
        if pred == 0:
            result = 'operating'
        elif pred == 1:
            result = 'acquired'
        elif pred == 2:
            result = 'closed'
        elif pred == 3:
            result = 'ipo'

    return result
    
@app.route("/predict",methods = ["POST"])
def result():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)
        prediction = str(result)
        return render_template("predict.html",prediction=prediction)
 
if __name__ == "__main__":
    app.run(debug=True)