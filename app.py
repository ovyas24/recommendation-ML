from logging import log
from flask import Flask,request
from flask import jsonify
from Recommendation import generateRecomendations,getAllMovies, mixRecommender
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r'/*': {"origins": '*'}})

@app.route('/')
def hello_world():
    return "Hello"

@app.route('/getMoviesList')
def allMovies():
    response = jsonify(getAllMovies())
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/recommend', methods=["POST"])
def recommend():
    req = request.get_json()
    print(req,"----------------------------req------------------------")
    response = jsonify(mixRecommender(req["movies"]))
    return response

@app.route('/test')
def test():
    return jsonify(mixRecommender(["Avatar","Guardians of the Galaxy"]))

if __name__ == '__main__':
    app.run(debug=True)