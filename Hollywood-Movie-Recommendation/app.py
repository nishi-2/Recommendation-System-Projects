#In this model deployment, streamlit library is used. So, all the necessary libraries are fetched at first
import streamlit as st
import pickle
import pandas as pd
import requests
import bz2
import os

# This will show the title of our app
st.title('Movie Recommendation System')

path = os.path.dirname(__file__)
my_file = path+'/movies_dict.pkl'

# The movies dataset is loaded, which is in the form of dictionary. So, it is changed into the dataframe.
movies_dict = pickle.load(open(my_file, 'rb'))
movies = pd.DataFrame(movies_dict)

my_file2 = path+"/similarity.pkl"

#similarity matrix, representing the distance is loaded as it is
similarity= bz2.BZ2File(my_file2,'rb')
similarity_matrix  = pickle.load(similarity)
similarity.close()


#this function is for getting the poster related to the movie id. This is done by using the API provided by the TMDB site.
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=4a502c7d2be3ae2d76c8418ec12b1962&language=en-US'.format(movie_id))
    data = response.json()
    if data['poster_path'] is None:
        temporary_pic = path+'/NOPIC.jpg'
        return temporary_pic
    else:
        return 'http://image.tmdb.org/t/p/w500/' + str(data['poster_path'])
        

#This is the recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:13]
    recommended = []
    posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
    return recommended, posters


#creating a drop down list on the app to select the movie
select_movie = st.selectbox(
'Which movie would you like to see?',
movies['title'].values)


#the names and the poster of the selected movies will be shown
if st.button('Recommend'):
    names, posters = recommend(select_movie)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col10, col11, col12 = st.columns(3)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    with col6:
        st.text(names[5])
        st.image(posters[5])
    with col7:
        st.text(names[6])
        st.image(posters[6])
    with col8:
        st.text(names[7])
        st.image(posters[7])
    with col9:
        st.text(names[8])
        st.image(posters[8])
    with col10:
        st.text(names[9])
        st.image(posters[9])
    with col11:
        st.text(names[10])
        st.image(posters[10])
    with col12:
        st.text(names[11])
        st.image(posters[11])

    


