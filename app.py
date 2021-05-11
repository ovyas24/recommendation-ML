from flask import Flask,request
from flask import jsonify
from Recommendation import generateRecomendations
# import requests
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello"

@app.route('/recommend',methods=["POST","GET"])
def recommend():
    req = request.get_json()
    # print(req["movies"])
    return jsonify(generateRecomendations(req["movies"]))

if __name__ == '__main__':
    app.run(debug=True)