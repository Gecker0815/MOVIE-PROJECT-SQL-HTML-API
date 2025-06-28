def enter_string(prompt):
    """Prompt the user to enter a string and ensure it is not empty."""
    while True:
        input_string = input(prompt).strip()
        if not input_string:
            print("Input cannot be empty. Please enter a valid string.")
            continue
        return input_string


def enter_new_rating(text = "Enter movie rating between 1-10: ", allow_blank = False):
    """Prompt the user to enter a movie rating between 1 and 10, and validate the input."""
    while True:
        try:
            rating = float(input(text))
        except ValueError:
            if allow_blank:
                return None

            print("Invalid input. Please enter a number between 1 and 10.")
            continue

        if 1 <= rating <= 10:
            return rating
        else:
            print("Rating must be between 1 and 10.")


def enter_year(text = "Enter the release year of the movie: ", allow_blank = False):
    """Prompt the user to enter a four-digit release year and validate the input."""
    while True:
        year = input(text)

        if allow_blank and year == "":
            return None

        if not year.isdigit():
            print("Error: Input must be a number.")
            continue

        if len(year) != 4:
            print("Error: Year must be a four-digit number.")
            continue

        return int(year)