import datetime
import database

# menu lets users pick from the options

menu = """Please select one of the following options:
1) Introduce an animal to the Zoo.
2) List animals that are coming soon to the Zoo
3) View all animals (coming and present) 
4) Record a visitor of an animal
5) All the animals a specific visitor has seen
6) Add a visitor to the guestbook
7) Show all visitors in the guestbook
8) Exit

Your selection: """
welcome = "Welcome to the Zoo guestbook app!"

print(welcome)
database.create_table()


def prompt_add_showcased_animal():
    animal_name = input("Animal name: ")
    id = input("ID: ")
    release_date = input("Processed date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    release_timestamp = parsed_date.timestamp()

    database.add_animal(id, animal_name, release_timestamp)
    print(f"{animal_name} has been added to the database")


def print_animals_list(heading, movies):
    print(f" -- Animals {heading} --")
    for _id, animal_name, release_date in movies:
        animal_date = datetime.datetime.fromtimestamp(release_date)
        human_date = animal_date.strftime("%b %d %Y")
        print(f"{_id}: {animal_name} (on {human_date})")
    print("---- \n")


def prompt_visit_animal():
    username = input("Visitor: ")
    animal_id = input("Animal ID: ")
    database.visit_animal(username, animal_id)


def prompt_show_visited_animals():
    username = input("Visitor: ")
    animals_visit = database.get_visited_animals(username)
    if animals_visit:
        print_animals_list(f"{username}'s Visited", animals_visit)
    else:
        print("User does not exist or has not visited any animals, yet!")


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


def prompt_show_visitors(visitors):
    visitors_list = []
    for username in visitors:
        visitors_list.append(username)
    print(visitors_list)

while (user_input := input(menu)) != "8":
    if user_input == "1":
        prompt_add_showcased_animal()
    elif user_input == "2":
        animals = database.get_animals(True)
        print_animals_list("Coming Soon", animals)
    elif user_input == "3":
        movies = database.get_animals()
        print_animals_list("in our database", movies)
    elif user_input == "4":
        prompt_visit_animal()
    elif user_input == "5":
        prompt_show_visited_animals()
    elif user_input == "6":
        prompt_add_user()
    elif user_input == "7":
        visitors = database.get_users()
        prompt_show_visitors(visitors)
    else:
        print("Invalid input, please try again!")
