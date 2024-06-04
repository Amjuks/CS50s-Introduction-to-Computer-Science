# importing library functions
from cs50 import SQL
import requests
from sys import exit
from pokeBackend import capitalize
import time

# settings up SQL database for queries
db = SQL("sqlite:///pokedex.db")
db.execute("DELETE FROM dex")

# get information from api
try:
    limit = input("How many pokemons do you want to import?\n")
    pokedex = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset=0")
    print(f"Response Error: {pokedex.raise_for_status()}")

# exit program if something goes wrong
except requests.RequestException:
    print("something went wrong")
    exit()

# import data into database
try:
    start = time.time()
    # convert the api data into json format
    dexInfo = pokedex.json()

    # get data for each pokemon
    for pokemon in dexInfo['results']:

        # get the api url for that pokemon
        try:
            pokeInfo = requests.get(pokemon['url'])
            pokeInfo.raise_for_status()

        # exit if something goes wrong
        except requests.RequestException:
            print("something went wrong")
            exit()

        insert = """INSERT INTO dex
        (id, name, type, atk, def, hp, sp_atk, sp_def, spd, weight, moves, ability, url)
        VALUES (:poke_id, :name, :poke_type, :atk, :poke_def, :hp, :sp_atk, :sp_def, :spd, :weight, :moves, :ability, :img)"""

        # importing data for each pokemon
        try:
            # convert data from api into json format
            pokeData = pokeInfo.json()

            # declarations
            types = ""
            moves = ""
            ability = ""

            # store image url
            if not pokeData['sprites']['front_default']:
                # if pokemon doesnt have a url, set it to /n
                img = "/n"

            else:
                img = pokeData['sprites']['front_default']

            # store the type of pokemons
            for t in pokeData['types']:
                # types.append(t['type']['name'])
                types = types + capitalize(t['type']['name']) + "|"

            # saving the pokemon name
            name = capitalize(pokeData['name'])

            # check if the pokemon has stats
            if not pokeData['stats']:
                # if it doesnt have stats set it to 0
                atk = 0
                poke_def = 0
                hp = 0
                sp_atk = 0
                sp_def = 0
                spd = 0

            else:
                # if it has stats set it to the value
                atk = int(pokeData['stats'][1]['base_stat'])
                poke_def = int(pokeData['stats'][2]['base_stat'])
                hp = int(pokeData['stats'][0]['base_stat'])
                sp_atk = int(pokeData['stats'][3]['base_stat'])
                sp_def = int(pokeData['stats'][4]['base_stat'])
                spd = int(pokeData['stats'][5]['base_stat'])

            # save the weight of pokemon
            weight = int(pokeData['weight'])

            # check if the pokemon has abilities
            if not pokeData['abilities']:
                # set it to /n if it doesnt have any abilities
                ability = "/n"

            else:
                # store every ability for the pokemon
                for Ability in pokeData['abilities']:
                    ability = ability + capitalize(Ability['ability']['name']) + "|"

            # check if the pokemon has moves
            if not pokeData['moves']:
                # if it doesnt have set it to /n
                moves = "/n"

            else:
                # if it has store every move
                for move in pokeData['moves']:
                    moves = moves + capitalize(move['move']['name']) + "|"

            # replacing hyphens with space and removing the last | from yhose
            types = types.replace("-", " ")[:-1]
            moves = moves.replace("-", " ")[:-1]
            ability = ability.replace("-", " ")[:-1]

            # print the info that will be imported for debugging reasons
            print(f"Pokemond id: {pokeData['id']}, Pokemon Name: {name}, Pokemon Type: {types}")
            print(f"Attack: {atk}, hp: {hp}, def: {poke_def}, sp_atk:{sp_atk}, sp_def:{sp_def}, spd:{spd}")
            print(f"Moves: {moves}")
            print(f"Abilities: {ability}")
            print(f"weight: {pokeData['weight']}")
            print(f"url: {img}")

            # import all those data into database
            db.execute(insert, poke_id = int(pokeData['id']), name = name, poke_type = types, atk = atk, poke_def = poke_def, hp = hp, sp_atk = sp_atk, sp_def = sp_def, spd = spd, weight = int(pokeData['weight']), moves = moves, ability = ability, img = img)


        # exit if there are any errors
        except (KeyError, TypeError, ValueError):
            print("something went wrong")
            exit()

    # prints how much time it took to import
    print(f"Took {round(time.time() - start, 3)} seconds to import")

# exit if there are any errors
except (KeyError, TypeError, ValueError):
    print("something went wrong")

"""
Table Structure-

CREATE TABLE dex (
    id INT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    atk INT NOT NULL,
    def INT NOT NULL,
    hp INT NOT NULL,
    sp_atk INT NOT NULL,
    sp_def INT NOT NULL,
    spd INT NOT NULL,
    weight INT NOT NULL,
    moves TEXT NOT NULL,
    ability TEXT NOT NULL,
    url TEXT NOT NULL
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hash TEXT NOT NULL,
    fav TEXT NOT NULL DEFAULT " "
);
"""