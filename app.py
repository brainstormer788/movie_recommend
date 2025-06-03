import streamlit as st
import pandas as pd
import pickle
import requests
import gzip
import numpy as np


# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        omdb_api_key = "a2817129"
        movie_title = movies.iloc[movies[movies['movie_id'] == movie_id].index[0]].title
        search_url = f"http://www.omdbapi.com/?apikey={omdb_api_key}&t={movie_title}&type=movie"
        response = requests.get(search_url)
        
        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=Error+Loading+Image"
            
        data = response.json()
        
        if data.get('Response') == 'True' and data.get('Poster') and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Found"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Loading+Image"


# Movie recommendation function
def recommend(movie):
    try:
        movie = movie.lower().strip()

        if movie not in movies['title'].str.lower().values:
            return ["Movie not found! Please enter a valid movie name."], []

        movie_index = movies[movies['title'].str.lower() == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            try:
                movie_id = movies.iloc[i[0]].movie_id
                recommended_movies.append(movies.iloc[i[0]].title)
                recommended_movies_posters.append(fetch_poster(movie_id))
            except Exception as e:
                recommended_movies.append("Error loading movie")
                recommended_movies_posters.append("https://via.placeholder.com/500x750?text=Error")

        return recommended_movies, recommended_movies_posters
    except Exception as e:
        return ["Error occurred while getting recommendations"], ["https://via.placeholder.com/500x750?text=Error"]


# Load movie data
try:
    with open('movie_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
except Exception as e:
    st.error(f"Error loading movie data: {str(e)}")
    st.stop()

# Streamlit UI
st.title("Movie Recommender System")

try:
    with gzip.open("similarity.pkl.gz", "rb") as f:
        similarity = pickle.load(f)
except Exception as e:
    st.error(f"Error loading similarity matrix: {str(e)}")
    st.stop()

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Show Recommendations"):
    with st.spinner('Getting movie recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

        # Create 5 columns dynamically
        cols = st.columns(5)

        # Display first 5 movies with posters
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

        # If there are more than 5 recommendations, create another row
        if len(recommended_movie_names) > 5:
            cols = st.columns(5)
            for i in range(5, len(recommended_movie_names)):
                with cols[i - 5]:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])
