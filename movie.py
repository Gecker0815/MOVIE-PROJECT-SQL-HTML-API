from movie_storage_sql import list_movies, list_users
import commands

def user_menu():
    while True:
        users = list_users()
        users_total = len(users) + 1

        print("\nWelcome to the movie APP! 🎬\n")
        print("Select user:")
        if len(users) != 0:
            for i, user in enumerate(users.values(), start=1):
                print(f"{i}. {user["name"]}")
        print(f"{users_total}. Create new user\n")

        try:
            choice = int(input(f"Enter choice: "))
        except ValueError:
            print(f"Invalid input. Please enter an integer 0-{len(users)}.")
            continue

        if choice == users_total:
            commands.command_create_user(users)
        elif 1 <= choice <= users_total:
            return list(users.items())[choice - 1]
        else:
            print("Pleas enter a valid number!")


def movie_menu(user):
    """Display an interactive menu and execute the corresponding movie management command."""
    menu = {
        "List movies": commands.command_list_movies,
        "List movies sorted": commands.command_sort_movies,
        "Add movie": commands.command_add_movie,
        "Delete movie": commands.command_delete_movie,
        "Update movie": commands.command_update_movie,
        "Stats": commands.command_show_stats,
        "Random movie": commands.command_random_movie,
        "Search movie": commands.command_search_movie,
        "Filter movies": commands.command_filter_movies,
        "Generate website": commands.command_generate_website,
        "Delete Account": commands.command_delete_account
    }
    menu_total = len(menu)

    while True:
        movies = list_movies(user)
        print(f"\nWelcome back, {user[1]["name"]}! 🎬\n")
        print("0. Exit")
        for i, label in enumerate(menu, start=1):
            print(f"{i}. {label}")
        print("")

        try:
            choice = int(input(f"Enter choice: "))
        except ValueError:
            print(f"Invalid input. Please enter an integer 0-{menu_total}.")
            continue

        if choice == 0:
            print("Bye!")
            break
        elif 1 <= choice <= len(menu):
            list(menu.values())[choice - 1](movies, user)
            if (choice == len(menu)):
                print("Bye!")
                break
        else:
            print("Invalid choice. Please choose a valid option.")


def main():
    user = user_menu()
    movie_menu(user)


if __name__ == "__main__":
    main()