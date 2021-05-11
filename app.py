from flask import Flask,request
from flask import jsonify
from Recommendation import generateRecomendations,getAllMovies
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return "Hello"

@app.route('/getMoviesList')
def allMovies():
    return jsonify(getAllMovies())

@app.route('/recommend',methods=["POST"])
def recommend():
    req = request.get_json()
    # print(req["movies"])
    return jsonify(generateRecomendations(req["movies"]))

if __name__ == '__main__':
    app.run(debug=True)