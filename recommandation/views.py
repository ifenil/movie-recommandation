from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.

def movies(request):
    return render(request,'index.html')

def result(request):
	final_movie=[]
	try:
		df = pd.read_csv("movie_dataset.csv")

		features = ['keywords','cast','genres','director']

		for feature in features:
			df[feature] = df[feature].fillna('')
	
		def combine_features(row):
			return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
	
		df["combined_features"] = df.apply(combine_features,axis=1)

		cv = CountVectorizer()

		count_matrix = cv.fit_transform(df["combined_features"])


		cosine_sim = cosine_similarity(count_matrix) 

		movie_user_likes = request.POST["nam"].title()

		def get_index_from_title(title):
			return df.loc[df.title == title].index[0]

		movie_index = get_index_from_title(movie_user_likes)

		similar_movies =  list(enumerate(cosine_sim[movie_index]))


		sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

		def get_title_from_index(index):
			return df.loc[index, "title"]	

		i=0 
		for element in sorted_similar_movies:
			app=str(get_title_from_index(element[0])) 
			final_movie.append(app)
			i=i+1
			if i>10:
				break
	except:
		final_movie=["Sorry,NOT FOUND"]

	return render(request,"result.html",{ 'movie' : final_movie })


