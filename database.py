# name, release data, watched - what we will have in our table
# First step is to create the initial data

import datetime
import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="C0nf!gurat!0n",
    database="zoodb"
)

mycursor = connection.cursor()
# mycursor.execute("CREATE DATABASE zoodb")

CREATE_ANIMALS_TABLE = "CREATE TABLE IF NOT EXISTS animals (id INTEGER PRIMARY KEY, animal_name TEXT, release_timestamp REAL)"
CREATE_VISITORS_TABLE = "CREATE TABLE IF NOT EXISTS users (username VARCHAR(64) PRIMARY KEY);"
CREATE_VISIT_LOG_TABLE = "CREATE TABLE IF NOT EXISTS log (user_username VARCHAR(64), animal_id INTEGER, FOREIGN KEY(user_username) REFERENCES users(username), FOREIGN KEY(animal_id) REFERENCES animals(id));"

INSERT_ANIMALS = "INSERT INTO animals (id, animal_name, release_timestamp) VALUES (%s, %s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
DELETE_ANIMAL = "DELETE FROM animals WHERE animal_name = (%s);"
SELECT_ALL_ANIMALS = "SELECT * FROM animals"
SELECT_ALL_VISITORS = "SELECT * FROM users"
SELECT_UPCOMING_ANIMALS = "SELECT * FROM animals WHERE release_timestamp > %s;"
SELECT_WATCHED_ANIMALS = "SELECT animals.* FROM animals JOIN log on animals.id = log.animal_id JOIN users on users.username = log.user_username WHERE users.username = %s;"
INSERT_WATCHED_ANIMAL = "INSERT INTO log (user_username, animal_id) VALUES (%s, %s);"
SET_ANIMAL_WATCHED = "UPDATE animals SET log = 1 WHERE animal_name = (%s);"


def create_table():
    mycursor.execute(CREATE_ANIMALS_TABLE)
    mycursor.execute(CREATE_VISITORS_TABLE)
    mycursor.execute(CREATE_VISIT_LOG_TABLE)


def add_user(username):
    mycursor.execute(INSERT_USER, (username,))
    connection.commit()


def add_animal(id, animal_name, release_timestamp):
    mycursor.execute(INSERT_ANIMALS, (id, animal_name, release_timestamp))
    connection.commit()


def get_users():
    mycursor.execute(SELECT_ALL_VISITORS)
    return mycursor.fetchall()


def get_animals(upcoming=False):  # Assume it is always False

    mycursor = connection.cursor()
    if upcoming:  # Dealing with if upcoming is True
        today_timestamp = datetime.datetime.today().timestamp()
        mycursor.execute(SELECT_UPCOMING_ANIMALS, (today_timestamp,))
    else:
        mycursor.execute(SELECT_ALL_ANIMALS)
    return mycursor.fetchall()


def visit_animal(username, animal_id):
    # Delete animal from to watch table and move to WATCHED table
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mycursor.execute(INSERT_WATCHED_ANIMAL, (username, animal_id))
    connection.commit()


def get_visited_animals(username):
    mycursor.execute(SELECT_WATCHED_ANIMALS, (username,))
    return mycursor.fetchall()
