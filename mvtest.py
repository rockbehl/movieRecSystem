import requests

class Movie:
    def __init__(self, id, title, genres, director, actors, release_year, duration, rating):
        self.attributes = {'id': id,
                           'title': title,
                           'genres': genres,
                           'director': director,
                           'actors': actors,
                           'release_year': release_year,
                           'duration': duration,
                           'rating': rating}

    def getattribute(self, item):
        try:
            return self.attributes[item]
        except KeyError:
            print(f"Attribute {item} not found")
            return None

    def getMini(self):
        return self.getattribute('title') + " (" + self.getattribute('release_year') + ")"




class MovieDatabase:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def get_movie(self, movie_id):
        movie_url = f"{self.base_url}/movie/{movie_id}?api_key={self.api_key}&append_to_response=credits"
        response = requests.get(movie_url)
        data = response.json()

        if 'status_code' in data:
            return None

        genres = [genre['name'] for genre in data.get('genres', [])]
        director = self._get_director(data.get('credits', {}).get('crew', []))
        actors = [actor['name'] for actor in data.get('credits', {}).get('cast', [])][:5]  # top 5 actors
        return Movie(
            id=data.get('id'),
            title=data.get('title'),
            genres=genres,
            director=director,
            actors=actors,
            release_year=data.get('release_date')[:4],
            duration=data.get('runtime'),
            rating=data.get('vote_average'),
        )

    def get_movies_by_genre(self, genre_id, number):
        discover_url = f"{self.base_url}/discover/movie?include_adult=true&include_video=false&language=en-US&page=1&sort_by=vote_average.asc&with_genres={genre_id}&api_key={self.api_key}"
        response = requests.get(discover_url)
        results = response.json()['results']
        results = results[:number]
        returnString = []
        for mov in results:
            print(mov)
            returnString.append(f"{mov['title']} ({mov['release_date'][:4]}), {mov['vote_average']}/10")
        return returnString

    def _get_director(self, crew):
        for member in crew:
            if member.get('job') == 'Director':
                return member.get('name')
        return "Unknown"

# Example usage
api_key = "7f02faf097b1baa953f3dfa536c4a5f3"
mdb = MovieDatabase(api_key)
movie = mdb.get_movie(343611)  # Replace 550 with a valid movie ID
if movie:
    print(movie.getattribute('title'), movie.getattribute('release_year'))
