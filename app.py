import pickle
import streamlit as st
import requests
import pandas as pd
import os
import gdown

# Google Drive file ID
file_id = "1KGjEwNUzMSpt71knKSwVSIqLrpL2HCVX"
file_url = f"https://drive.google.com/uc?id={file_id}"
file_name = "similarity.pkl"

# Check if file exists, if not, download it
if not os.path.exists(file_name):
    gdown.download(file_url, file_name, quiet=False)

# Load the similarity matrix
import pickle
similarity = pickle.load(open(file_name, 'rb'))


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Catch API errors
        data = response.json()

        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"  # Default placeholder

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"


# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies.iloc[i[0]]['movie_id']  # Ensure correct column
        poster_url = fetch_poster(movie_id)

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster_url)

    return recommended_movie_names, recommended_movie_posters


# Load movie data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Enter the Movie name:-',
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(len(recommended_movie_names)):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

st.markdown("---")  # Adds a horizontal line
st.markdown(
    "<p style='text-align: center; color: red;'>If you are in India or seeing an error in the API, please connect to a VPN.</p>",
    unsafe_allow_html=True
)
