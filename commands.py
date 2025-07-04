import statistics
import random
from movie_storage_sql import add_movie, list_movies, delete_movie, update_movie, add_user, delete_user
from input_validation import enter_string, enter_new_rating, enter_year
import requests
import os
from dotenv import load_dotenv


def command_delete_account(movies, user):
    """Delete a user"""
    delete_user(user)


def command_list_movies(movies, user):
    """Retrieve and display all movies from the database."""
    print("********** Movie List **********")
    print(f"[{len(movies)}] movies in total")
    print("")
    for index, (movie, details) in enumerate(movies.items()):
        print(f"{index+1}. {movie} ({details['year']}): {details['rating']}")
        print("")


def command_add_movie(movies, user):
    """Prompt for movie details and add the movie to storage if it doesn't already exist."""
    title = enter_string("Enter movie name: ")
    load_dotenv()

    params = {'t': title, 'apikey': os.getenv("API_KEY")}

    try:
        response = requests.get('http://www.omdbapi.com/', params=params, timeout=5)
        response.raise_for_status()
        movie = response.json()

        if movie.get("Response") == "True":
            title = movie['Title']
            year = movie['Year']
            rating = float(movie['Ratings'][0]['Value'][:-3])
            poster = movie['Poster']

            if title not in movies:
                add_movie(title, rating, year, poster, user)
            else:
                print(f"The movie '{title}' already exists.")
        else:
            print(f"Movie '{title}' not found. Error: {movie.get('Error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        print("Error while contacting the movie database:", str(e))


def command_delete_movie(movies, user):
    """Prompt for a movie title and remove the movie from storage if it exists."""
    title = enter_string("Enter movie name: ")

    if title in movies:
        delete_movie(title)
    else:
        print(f"The movie '{title}' does not exist.")


def command_update_movie(movies, user):
    """Update the rating of an existing movie. Prompts for a movie title and a new rating."""
    title = enter_string("Enter movie name: ")
    rating = enter_new_rating()

    if title in movies:
        update_movie(title, rating)
    else:
        print(f"The movie '{title}' does not exist.")


def command_show_stats(movies, user):
    """
    Calculate and display statistics:
    - Average rating
    - Median rating
    - The movie with the highest rating (best movie)
    - The movie with the lowest rating (worst movie)
    """
    total_rating = 0
    max_rating = -1
    min_rating = 11
    best_movie = ""
    worst_movie = ""

    for title, values in movies.items():
        rating = values['rating']
        total_rating += rating
        if rating > max_rating:
            max_rating = rating
            best_movie = title
        if rating < min_rating:
            min_rating = rating
            worst_movie = title

    ratings = [movie["rating"] for movie in movies.values()]

    print("********** Movies Stats **********")
    print("")
    print(f"Average rating: {total_rating / len(ratings):.2f}")
    print(f"Median rating: {statistics.median(ratings)}")
    print(f"Best movie: {best_movie}")
    print(f"Worst movie: {worst_movie}")
    print("")


def command_random_movie(movies, user):
    """Select and display the details of a random movie."""
    movie, details = random.choice(list(movies.items()))
    print("********** Random Movie **********")
    print("")
    print(f"Title: {movie}")
    print(f"Rating: {details['rating']}")
    print(f"Year: {details['year']}")
    print("")


def command_search_movie(movies, user):
    """Search for movies whose titles contain a given substring (case-insensitive) and display them."""
    print("********** Search Movies **********")
    search_query = input("Enter your search query: ")
    print("")

    for title, details in movies.items():
        if search_query.lower() in title.lower():
            print(f"{title}:")
            print(f"  Rating: {details['rating']}")
            print(f"  Release year: {details['year']}")
            print("")


def command_sort_movies(movies, user):
    """This function sorts and displays a movie list based on user choice."""

    while True:
        print("********** My sorted movie list **********")
        print("")
        print("Menu:")
        print("0. Exit")
        print("1. Listed in chronological order ascending")
        print("2. Listed in chronological order descending")
        print("3. Sorted by rating")
        print("")

        try:
            choice = int(input("Enter choice (0-4): "))
        except ValueError:
            print("Invalid input. Please enter a number 0-4.")
            continue

        sorted_movies = {}

        if choice == 0:
            break
        elif choice == 1:
            sorted_movies = dict(sorted(movies.items(), key=lambda item: item[1]['year'], reverse=True))
        elif choice == 2:
            sorted_movies = dict(sorted(movies.items(), key=lambda item: item[1]['year'], reverse=False))
        elif choice == 3:
            sorted_movies = dict(sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True))

        list_movies(sorted_movies)
        break


def command_filter_movies(movies, user):
    print("********** Filter movies **********")

    minimum_rating = enter_new_rating("Enter minimum rating: ", True)
    start_year = enter_year("Enter start year: ", True)
    end_year = enter_year("Enter end year: ", True)

    filter_movies = {
        movie: details
        for movie, details in movies.items()
        if (minimum_rating is None or details["rating"] > minimum_rating)
           and (start_year is None or details["year"] > start_year)
           and (end_year is None or details["year"] < end_year)
    }

    list_movies(filter_movies)


def command_generate_website(movies, user):
    """Generate an HTML page listing all movies using a predefined template."""
    html_template = ""
    movies_html = ""

    with open("index_template.html", "r") as fileobj:
        html_template = fileobj.read()

    for title, details in movies.items():
        movies_html += f"""<li>
            <div class="movie">
                <img class="movie-poster" src="{details['poster']}"/>
                <div class="movie-title">{title}</div>
                <div class="movie-year">{details['year']}</div>
            </div>
        </li>"""


    html_template = html_template.replace("__TEMPLATE_MOVIE_GRID__", movies_html)
    html_template = html_template.replace("__TEMPLATE_TITLE__", "Movie visualizer")

    with open("index.html", "w") as fileobj:
        fileobj.write(html_template)

    print("Website generated successfully!")


def command_create_user(users):
    """This command allows you to create a new user in the database."""
    print("")
    print("Create new user! 👤")
    username = enter_string("Enter your username: ")

    if username not in users:
        add_user(username)
    else:
        print(f"The user '{username}' already exists.")