# importing required functions from libraries
from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL


# Setting up database
db = SQL("sqlite:///pokedex.db")
exceptions = ["index.html", "favourites.html"]

# Make sures the user is logged in
def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")

        return f(*args, **kwargs)
    return decorated_function


# Return an apology if something goes wrong
def apology(message, title):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", message=escape(message), title=title)


# Saving the color of the type
colorCode = {
    "Normal": "#999966",
    "Fire": "#FF6600",
    "Fighting": "#FF0000",
    "Ice": "#99FFFF",
    "Water": "#3399FF",
    "Flying": "#9999FF",
    "Grass": "#33FF00",
    "Poison": "#660099",
    "Electric": "#FFFF00",
    "Ground": "#FFCC33",
    "Psychic": "#FF3399",
    "Rock": "#CC9966",
    "Bug": "#669900",
    "Dragon": "#003399",
    "Dark": "#333333",
    "Ghost": "#9933FF",
    "Steel": "#999999",
    "Fairy": "#FF99FF",
}


# Saving Pokemon types with their corresponding values
typeCode = {
    1: "Normal",
    10: "Fire",
    2: "Fighting",
    15: "Ice",
    11: "Water",
    3: "Flying",
    12: "Grass",
    4: "Poison",
    13: "Electric",
    5: "Ground",
    14: "Psychic",
    6: "Rock",
    7: "Bug",
    16: "Dragon",
    17: "Dark",
    8: "Ghost",
    9: "Steel",
    18: "Fairy",
}


# Lookup for stuff while displaying
def lookup(key, value):

    # returns an empty list if user hasn't searched for anything
    if not value:
        return []

    # logs whatever the user had searched for
    log(f"User {session['name']} looked up for {value} from {key}")

    # runs the following if key is search
    if key == "search":
        # if the user searches by global ID it looks up pokemon with the same
        try:
            poke_id = int(value)
            return db.execute("SELECT id, name, type, url FROM dex WHERE id = :poke_id", poke_id=poke_id)

        # if the user had searched by name, an error would have occured in the previous step while converting it to int and this would be executed
        except:
            return db.execute('SELECT id, name, type, url FROM dex WHERE name LIKE ?', "%" + value + "%")

    # runs the following if key is type
    if key == "type":
        # if the user searches by type ID it looks up pokemon with the same
        try:
            Type = typeCode[int(value)]
            return db.execute('SELECT id, name, type, url FROM dex WHERE type LIKE ?', "%" + Type + "%")

        # if the user had searched by type name, an error would have occured in the previous step while converting it to int and this would be executed
        except:
            return db.execute('SELECT id, name, type, url FROM dex WHERE type LIKE ?', "%" + value + "%")

    # runs the following if key is move
    if key == "move":
        return db.execute('SELECT id, name, type, url FROM dex WHERE moves LIKE ?', "%" + value + "%")

    # runs the following if key is ability
    if key == "ability":
        return db.execute('SELECT id, name, type, url FROM dex WHERE ability LIKE ?', "%" + value + "%")


# Capitalize words when importing
def capitalize(word):

    output = ""
    word = word.split("-")

    for i in range(len(word)):
        try:
            if word[i + 1]:
                output += word[i].capitalize() + " "
        except:
            output += word[i].capitalize()

    return output


# function to add/remove/display favourites
def fav(key, ID = None):

    # selects all starred pokemons
    fav = [int(i) for i in db.execute("SELECT fav FROM users WHERE id = :user_id", user_id = session['user_id'])[0]['fav'].split()]

    # returns the list if key is list
    if key == "list":
        # logs that the user's list was selected
        return fav

    # runs the following if key is add
    if key == "add":
        # logs that the user starred a pokemon
        log(f"{session['name']} added {ID} to their favourites list")
        fav.append(int(ID))

    # runs this if key is rm i.e. remove
    if key == "rm":
        # logs that the user unstarred a pokemon
        log(f"{session['name']} removed {ID} from their favourites list")
        fav.pop(fav.index(int(ID)))

    # sorts the list of starred pokemons
    fav.sort()

    # converts the list back to string
    string = ""
    for i in fav:
        string += str(i) + " "

    # upadtes the database
    db.execute("UPDATE users SET fav = :fav WHERE id = :user_id", user_id = session['user_id'], fav = string)


# function to split types into a list
def TypeSplit(d):
    # converts string to list
    for i in range(len(d)):
        d[i]['type'] = d[i]['type'].split("|")[0]

    return(d)


# searches for a pokemon
def searchPoke(searchList, searchKey = None, pokes = None):
    if request.method == "POST":
        # sets the variable to the name of button that was clicked
        btn = list(request.form)[0]

        # runs this if user starred/unstarred a pokemon
        if (btn == "fav-add" or btn == "fav-rm"):
            fav(btn.split("-")[1], request.form.get(btn))
            pokes = session['page']

        # looks up for a pokemon if user searched for pokemon by their specifics
        elif btn == "input":
            searchList[0] += " - " + request.form.get("input")
            pokes = lookup(searchKey, request.form.get("input"))
            session['offset'] = 1
            session['page'] = pokes

        # updates page number
        elif btn == 'previous':
            if session['offset'] == 1:
                    pass
            else:
                session['offset'] -= 1

            if searchKey not in exceptions:
                pokes = session['page']

        # sets the page number
        elif btn == 'page':
            try:
                session['offset'] = int(request.form.get("page"))
            except:
                session['offset'] = session['offset']

        # updates page number
        elif btn == 'next':
            if searchKey not in exceptions:
                pokes = session['page']
                session['offset'] += 1
                offset = session['offset']
                if pokes[offset:offset+12] == []:
                    session['offset'] -= 1
            else:
                session['offset'] += 1

        # if user clicked a button from the pokemon profile, it searches for that
        else:
            btn = btn.split("|")
            searchList[0] += " - " + btn[1]

            pokes = lookup(btn[0], btn[1])
            session['offset'] = 1
            session['page'] = pokes

        log(f"User {session['name']} clicked {btn} with their search - {searchKey}")

    else:
        if searchKey not in exceptions:
            pokes = []
        session['offset'] = 1

    search = searchList


    if searchKey in exceptions:
        session['page'] = pokes
        return render_template(searchKey, pokes = TypeSplit(pokes), offset = (session['offset'] * 12) - 12, fav = fav("list"), color = colorCode, session = session)

    else:
        return render_template("search.html", pokes=TypeSplit(pokes), offset=(session['offset'] * 12) - 12, search=search, fav=fav("list"), color=colorCode)


# logging function
def log(debug):
    # opens the file and closes it after writing into it
    with open("log.txt", "a") as f:
        f.write(f"{debug}\n")