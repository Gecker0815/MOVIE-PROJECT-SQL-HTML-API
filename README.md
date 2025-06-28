#  Movie Management System

## 🎬 Project Overview
A simple CLI- and web-based system to manage a collection of movies in a SQLite database.

**Features**
- Add, delete & update movies
- Search, filter & pick a random movie
- Show stats (average, median, best/worst)
- Generate a browsable HTML website

## ⚙️ Setup & Dependencies
To use the system, you need to install the following dependencies:

```bash
pip install sqlalchemy requests python-dotenv random statistics
```

- **Python 3.8 or higher** is required.
- **SQLAlchemy**: for database abstraction.
- **requests**: for HTTP requests to the OMDb API.
- **python-dotenv**: for handling environment variables.
- **random** to select a random movie.
- **statistics** to display the movie statistics

## 🗄️ Database Structure
The movies are stored in a SQLite database with the following schema:

```sql
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    rating REAL NOT NULL,
    poster TEXT UNIQUE NOT NULL
);
```

## 🕹️ Command-Line Interface (CLI)
The system provides an interactive CLI with the following functions:

1. **List Movies**: Display all movies in the database.
2. **Add Movie**: Add a new movie if it doesn't already exist.
3. **Delete Movie**: Remove a movie from the database.
4. **Update Movie**: Update the rating of an existing movie.
5. **Show Stats**: Display statistics like average rating, median, best movie (highest rating), and worst movie (lowest rating).
6. **Random Movie**: Select and display details of a random movie.
7. **Search Movie**: Search for movies whose titles contain a given substring (case-insensitive) and display them.
8. **Filter Movies**: Filter movies based on minimum rating, start year, and end year.
9. **Generate Website**: Create an HTML page listing all movies using a predefined template.

## 🌐 Web-based Visualization
The `command_generate_website` function generates an HTML file displaying all movies in a grid. The template is defined in `index_template.html` and styled with the CSS file `style.css`.

## ✅ Input Validation
To ensure inputs are correct, the system includes validation for:
- Movie titles: Must not be empty.
- Ratings: Must be between 1 and 10.
- Release years: Must be a four-digit number.

## 🚀 Usage
To use the system, run the following command in your terminal:

```bash
python3 movie.py
```

You will then see an interactive menu where you can select different functions. Here are some examples:
- To list movies: `0. List movies`
- To add a movie: `1. Add movie`
- To delete a movie: `2. Delete movie`
- To view statistics: `3. Stats`