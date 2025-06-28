from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """))

    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT UNIQUE NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """))

    connection.commit()


def list_users():
    """Retrieve all users from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        users = result.fetchall()

    return {
        row[0]: {
            "id": row[0],
            "name": row[1],
        }
        for row in users
    }


def add_user(name):
    """Add a new user to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("""
                INSERT INTO users (name)
                VALUES (:name)
            """), {
                "name": name,
            })
            connection.commit()
            print(f"User with the name '{name}' was added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_user(user):
    """Delete a user from the database by id."""
    user_id = user[1]["id"]

    delete_movies_by_user_id(user_id)

    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM users WHERE id = :user_id"), {"user_id": user_id})
            connection.commit()
            print(f"User deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def list_movies(user):
    """Retrieve all movies from the database for a specific user."""
    user_id = user[1]["id"]

    with engine.connect() as connection:
        result = connection.execute(text("""SELECT title, year, rating, poster FROM movies WHERE user_id = :user_id"""), {"user_id": user_id})
        movies = result.fetchall()

    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster": row[3]
        }
        for row in movies
    }


def add_movie(title, year, rating, poster, user):
    """Add a new movie to the database."""
    user_id = user[1]["id"]

    with engine.connect() as connection:
        try:
            connection.execute(text("""
                INSERT INTO movies (title, year, rating, poster, user_id)
                VALUES (:title, :year, :rating, :poster, :user_id)
            """), {
                "title": title,
                "year": year,
                "rating": rating,
                "poster": poster,
                "user_id": user_id
            })
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")



def delete_movies_by_user_id(user_id):
    """Delete a movie from the database by user_id."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE user_id = :user_id"), {"user_id": user_id})
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database by title."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating}
            )
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
