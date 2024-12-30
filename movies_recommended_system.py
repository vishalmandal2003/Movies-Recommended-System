# -*- coding: utf-8 -*-
"""movies recommended system.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18QpoOsnpOtni5NLNHEGF6frlhNyXqhlE
"""

import pandas as pd
import numpy as np

movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')

movies.head(1)

credits.head(1)

movies.shape

movies=movies.merge(credits,on='title')

movies.head(1)

movies=movies[['id','title','overview','genres','keywords','cast','crew']]

movies.info()

movies.head(1)

#missing data
movies.isnull().sum()

#removing missing data
movies.dropna(inplace=True)

movies.head()

#is there dublicate data
movies.duplicated().sum()

#remove dublicates
movies.drop_duplicates(inplace=True)

movies.iloc[0].genres

def convert(obj):
     L=[]
     for i in ast.literal_eval(obj):
          L.append(i['name'])
          return L

import ast
ast.literal_eval('[{"id": 28, "name": "Action"}, {"id": 12, "name": "Adventure"}, {"id": 14, "name": "Fantasy"}, {"id": 878, "name": "Science Fiction"}]')

movies['genres']=movies['genres'].apply(convert)

movies.head()

movies['keywords']=movies['keywords'].apply(convert)

movies.head()

movies['cast'][0]

def convert3(obj):
     L=[]
     counter=0
     for i in ast.literal_eval(obj):

      if  counter!=3:
         L.append(i['name'])
         counter+=1
      else:
           break


     return L

movies['cast']=movies['cast'].apply(convert3)

movies.head()

movies.shape

movies['crew'][0]

def fetch_director(obj):
     L=[]

     for i in ast.literal_eval(obj):
      if i['job']=='Director':
          L.append(i['name'])
          break
          return L

# removind a colume
movies.drop('crew',axis=1,inplace=True)

movies.head()

# applying list to columns
movies['overview']=movies['overview'].apply(lambda x:x.split())

movies.head()

#removing spaces between words
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x]if x is not None else x)

movies.head()

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+ movies['cast']

movies.head()

new_df=movies[['id','title','tags']]

#converting list into string

new_df['tags']=new_df['tags'].astype(str)

new_df['tags'][0]

new_df.head()

new_df['tags']=new_df['tags'].apply(lambda x: x.lower())

new_df.head()

from sklearn.feature_extraction.text import CountVectorizer

# Example DataFrame
#new_df = pd.DataFrame({ 'title','tags'})
new_df=movies[['id','title','tags']]

# Remove any rows with empty or null 'tags'
new_df = new_df[new_df['tags'].notnull() & new_df['tags'].str.strip().astype(bool)]

# Ensure the column is of type string
new_df['tags'] = new_df['tags'].astype(str)

# Define custom stop words
custom_stop_words = [
    'ourselves', 'cant', 'third', 'since', 'system', 'find', 'fire', 'below',
    'top', 'else', 'except', 'themselves', 'here', 'wherever', 'back', 'whereby',
    'con', 'within', 'mill', 'anyhow', 'ltd', 'there', 'same', 'afterwards',
    'sometimes', 'their', 'beyond', 'would', 'whether', 'somewhere', 'sincere',
    'am', 'anyway', 'enough', 'further', 'whereas', 'fifty', 'sometime', 'out',
    'full', 'move', 'onto', 'once', 'became', 'put', 'almost', 'everywhere',
    'whole', 'namely', 'whoever', 'per', 'he', 'often', 'between', 'everyone',
    'anywhere', 'yours', 'take', 'are', 'more', 'something', 'some', 'others',
    'de', 'side', 'latterly', 'must', 'when', 'down', 'while', 'toward', 'be',
    'whereafter', 'no', 'another', 'part', 'ever', 'in', 'nevertheless', 'go',
    'thick', 'i', 'where', 'front', 'perhaps', 'up', 'thin', 'herself', 'mostly',
    'she', 'empty', 'hers', 'many', 'to', 'un', 'few', 'cannot', 'however', 'ten',
    'our', 'give', 'get', 'moreover', 'thereby', 'though', 'hence', 'may',
    'himself', 'noone', 'someone', 'across', 'her', 'hereupon', 'alone', 'by',
    'those', 'etc', 'already', 'becomes', 'who', 'you', 'keep', 'either',
    'elsewhere', 'well', 'a', 'can', 'mine', 'herein', 'because', 'me', 'becoming',
    'three', 'itself', 'towards', 'thence', 'thru', 'never', 'upon', 'bottom',
    'still', 'then', 'throughout', 'behind', 'amongst', 'that', 'former', ...
]

# Vectorization using the custom stop words list
cv = CountVectorizer(max_features=5000, stop_words=custom_stop_words)
vectors = cv.fit_transform(new_df['tags']).toarray()

print(vectors)

new_df.head()

import nltk

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
     y=[]
     for i in text.split():
          y.append(ps.stem(i))
     return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

new_df.head()

# Assuming cv is your CountVectorizer instance
feature_names = cv.get_feature_names_out()
print(feature_names)

from sklearn.metrics.pairwise import cosine_similarity

similarity= cosine_similarity(vectors)

sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

def recommend (movie):
  movie_index=new_df[new_df['title']==movie].index[0]
  distances=similarity[movie_index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  for i in movies_list:
    print(new_df.iloc[i[0]].title)

recommend('The Dark Knight Rises')

new_df.head()