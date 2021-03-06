from numpy.lib.function_base import append
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_title_from_index(index):
	return df[df.index == index]["title"].values[0]

def get_formated_data_title(title):
    data = df[df.title == title][["title","id"]].values[0]
    data1 = {
        "id":data[1],
        "title":data[0]
    }
    return data1

def get_relevent_data(index):
    try:
        data =df[df.index == index][["id","title","genres"]].values[0]
        dataDict = {
            "id":data[0],
            "name":data[1],
            "genre":data[2]
        }
        return dataDict
    except Exception as e:
        print(e,"------error------")
        return {}

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

def getRecomendationList(movie):
    try:
        movie_index = get_index_from_title(movie)
        similer_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similer_movies = sorted(similer_movies, key=lambda x: x[1], reverse=True)

        i = 0
        moviesNames = []
        for movie in sorted_similer_movies:
            moviesNames.append(movie[0])
            i = i+1
            if i > 50:
                break
        return moviesNames
    except:
        return []

def getRecommendationFull(similer_movies):
    try:
        sorted_similer_movies = sorted(similer_movies, key=lambda x: x[1], reverse=True)
        i = 0
        moviesNames = []
        for movie in sorted_similer_movies:
            moviesNames.append(movie[0])
            i = i+1
            if i > 51:
                break
        return moviesNames
    except:
        return []

def createRecomendationList(movie):
    try:
        movie_index = get_index_from_title(movie)
        similer_movies = cosine_sim[movie_index]
        # print(similer_movies[0])
        return similer_movies
    except:
        return []

def mixRecommender(moviesLiked):
    lis = []
    for movie in moviesLiked:
        data = createRecomendationList(movie)
        lis.append(data)
    newLis = []
    for items in lis:
        for item in items:
            newLis.append(item)
    recommendationsID = getRecommendationFull(list(enumerate(newLis)))
    recommendations = [] 
    for index in recommendationsID:
        data = get_relevent_data(index)
        if(len(data)!=0):
            recommendations.append(data)
    newArr = []
    seen = set()
    if(len(recommendations) != 0):
        for ele in recommendations:
            if(len(ele) != 0):
                if ele["id"] not in seen:
                    newArr.append(ele)
                    seen.add(ele["id"])
    return newArr[1:51]

def generateRecomendations(moviesLiked):
    recomendationLists = []
    for movie in moviesLiked:
        data = getRecomendationList(movie)

        if(len(data)!=0):
            recomendationLists.append(data)

    oneDList = np.array(recomendationLists)
    recommendationsId = oneDList.ravel()
    seen = set()

    recommendations = [] 
    for index in recommendationsId:
        data = get_relevent_data(index)
        if(len(data)!=0):
            recommendations.append(data)
    newArr = []
    if(len(recommendations) != 0):
        for ele in recommendations:
            if(len(ele) != 0):
                if ele["id"] not in seen:
                    newArr.append(ele)
                    seen.add(ele["id"])
    return newArr[1:51]

def combined_features(row):
	try:
		return row['keywords'] + " " + row['cast']+" "+row['genres']+" "+row['director']
	except:
		print("Error: ", row)

def getAllMovies():
    moviesNames = df["title"]
    movies = []
    for movie in moviesNames:
        data = get_formated_data_title(movie)
        movies.append(data)

    all = { 
        "movies" :  movies
    }
    return all

df = pd.read_csv("movie_dataset.csv")
features = ['keywords', 'cast', 'genres', 'director']

for feature in features:
	df[feature] = df[feature].fillna('')



df["combined_features"] = df.apply(combined_features, axis=1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])

cosine_sim = cosine_similarity(count_matrix)