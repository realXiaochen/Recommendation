#1/3/2017 xiaochen zhuo
#Data source: http://grouplens.org/datasets/movielens/100k/
#Activity: find similarity between movies
import pandas as pd
import numpy as np


# Get the userid, movie_name, movie_rating table
r_cols = ['user_id', 'movie_id', 'rating']
ratings = pd.read_csv('u.data', sep='\t', names=r_cols, usecols=range(3))

m_cols = ['movie_id','title']
movies = pd.read_csv('u.item', sep="|",names = m_cols, usecols=range(2))

ratings = pd.merge(movies,ratings)

movieRatings = ratings.pivot_table(index=['user_id'], columns =['title'], values='rating')


# Pick a random movie 
rMovie = movieRatings['Schindler\'s List (1993)']

# Filter the movie rating to get all the popular movies (100+ rating) 
movieStats = ratings.groupby('title').agg({'rating':[np.size,np.mean]})
popularIndexes = movieStats['rating']['size'] >= 100
popularMovies = movieStats[popularIndexes]
print popularMovies.sort_values([('rating', 'mean')], ascending=False)[:15]


# Get the similarity of other movies with the random movie
similarMovies = movieRatings.corrwith(rMovie).dropna()


# Get the top k similar movies
df = popularMovies.join(pd.DataFrame(similarMovies, columns=['similarity']))

print df.sort_values(['similarity'],ascending=False)[1:15]
