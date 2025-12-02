import requests
import os
from dotenv import load_dotenv
load_dotenv()


OMDb_API = os.getenv('OMDb_API_KEY')


class Movie:

    def __init__(self,title,grade):
        self.title = title
        self.grade = grade


    def find_movie(self):
        movies = requests.get(f"http://www.omdbapi.com/?t={self.title}&apikey={OMDb_API}&plot=short")
        return movies.json()