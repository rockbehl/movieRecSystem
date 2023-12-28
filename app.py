from flask import Flask, render_template, request
import mvtest

app = Flask(__name__)
mdb = mvtest.MovieDatabase("7f02faf097b1baa953f3dfa536c4a5f3")  # Replace with your actual API key


@app.route('/')
def index():
    return render_template('index.html')  # A simple form for user to input movie ID


@app.route('/movie_details')
def movie_details():
    movie_id = request.args.get('movie_id', type=int)
    if not movie_id:
        return "No movie ID provided", 400

    movie = mdb.get_movie(movie_id)
    if movie:
        return render_template('movie_details.html', movie=movie, mdb=mdb)
    else:
        return "Movie not found", 404


if __name__ == '__main__':
    app.run(debug=True)
