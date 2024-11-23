import os

from cs50 import SQL
from flask import Flask, flash, redirect, request, render_template, session,  url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import uuid
import os

from helpers import apology, login_required


# Configure Application
app = Flask(__name__)

# Uploads folder:
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Configure sesssion to use filesystem (instead of signed coockies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite-database
db = SQL("sqlite:///Nutzdaten.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Index-Page
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        meal = bool(request.form.get("meal"))
        bakery = bool(request.form.get("bakery"))
        desert = bool(request.form.get("desert"))
        vegie = bool(request.form.get("vegie"))
        vegan = bool(request.form.get("vegan"))
        glutenfree = bool(request.form.get("gluten"))
        lactosefree = bool(request.form.get("lactose"))

        rezepte = db.execute(
            "SELECT rezept.id AS rezept_id, rezept.title, rezept.userID, rezept.bild, rezept.bakery, rezept.meal, rezept.desert, rezept.vegie, rezept.vegan, rezept.gluten, rezept.lactose, users.id AS user_id, users.username FROM rezept JOIN users ON rezept.userID = users.id"
           )
        rezept_filter = []

        #filter wenn nicht Bakery
        if bakery == True:
            for rezept in rezepte:
                if bool(rezept['bakery']) == True:
                    rezept_filter.append(rezept)

        #filter wenn nicht meal
        if meal == True:
            for rezept in rezepte:
                if bool(rezept['meal']) == True:
                    rezept_filter.append(rezept)
        # print(rezepte)
        #filter wenn nicht desert
        if desert == True:
            for rezept in rezepte:
                if bool(rezept['desert']) == True:
                    rezept_filter.append(rezept)
        
        #filter wenn vegetarisch
        if vegie == True:
            for rezept in rezepte:
                if bool(rezept['vegie']) == False:
                    if rezept in rezept_filter:
                        rezept_filter.remove(rezept)
        
        #filter wenn vegan
        if vegan == True:
            for rezept in rezepte:
                if bool(rezept['vegan']) == False:
                    if rezept in rezept_filter:
                        rezept_filter.remove(rezept)
        
        #filter wenn lactosefree
        if lactosefree == True:
            for rezept in rezepte:
                if bool(rezept['lactose']) == True:
                    if rezept in rezept_filter:
                        rezept_filter.remove(rezept)
        
        #filter wenn glutenfree
        if glutenfree == True:
            for rezept in rezepte:
                if bool(rezept['gluten']) == True:
                    if rezept in rezept_filter:
                        rezept_filter.remove(rezept)


        return render_template("index.html", rezepte = rezept_filter)
    
    else:
        rezepte = db.execute(
            "SELECT rezept.id AS rezept_id, rezept.title, rezept.userID, rezept.bild, rezept.bakery, rezept.meal, rezept.desert, rezept.vegie, rezept.vegan, rezept.gluten, rezept.lactose, users.id AS user_id, users.username FROM rezept JOIN users ON rezept.userID = users.id"
        )

        return render_template("index.html", rezepte = rezepte)


# Show Recipe Page
@app.route('/recipe/<int:nummer>')
@login_required
def recipe(nummer):
    rows = db.execute(
        "SELECT * FROM rezept WHERE id = ?",nummer
    )
    rezept = rows[0]

    rows = db.execute(
        "SELECT zutat FROM zutaten WHERE rezeptID = ?", nummer
    )

    zutaten = rows

    rows = db.execute(
        "SELECT anweisung FROM anweisungen WHERE rezeptID=?", nummer
    )
    anweisungen = rows

    rows = db.execute(
        "SELECT id FROM favourites WHERE userID=? AND rezeptID=?", session["user_id"], nummer
    )

    favos =  len(rows)

    rows = db.execute(
        "SELECT username FROM users WHERE id = ?", rezept["userID"]
    )
    userdata = rows[0]

    return render_template("rezept.html", nummer=nummer, rezept = rezept, zutaten=zutaten, anweisungen=anweisungen, userdata=userdata, favos = favos)

# Show "My Recipes"
@app.route('/myRecipes')
@login_required
def myRecipes():
    rezepte = db.execute(
        "SELECT rezept.id AS rezept_id, rezept.title, rezept.userID, rezept.bild, rezept.bakery, rezept.meal, rezept.desert, rezept.vegie, rezept.vegan, rezept.gluten, rezept.lactose, users.id AS user_id, users.username FROM rezept JOIN users ON rezept.userID = users.id WHERE userID = ?", session["user_id"]
        #"SELECT * FROM rezept JOIN users ON rezept.userID = users.id WHERE userID = ?", session["user_id"]
    )
    return render_template("index_ohne.html", rezepte = rezepte)

# Show "Favourites"
@app.route('/myFavourites')
@login_required
def myFavourites():
    rezepte = db.execute(
        "SELECT favourites.id, favourites.rezeptID, favourites.userID, rezept.id AS rezept_id, rezept.title, rezept.userID, rezept.bild, rezept.bakery, rezept.meal, rezept.desert, rezept.vegie, rezept.vegan, rezept.gluten, rezept.lactose, users.id, users.username FROM favourites JOIN rezept ON favourites.rezeptID = rezept.id JOIN users ON rezept.userID = users.id WHERE favourites.userID = ?", session["user_id"]
    )
    print(rezepte)
    return render_template("index_ohne.html", rezepte = rezepte)


# add to favourites function
@app.route('/addFavos/<int:nummer>')
@login_required
def addToFavos(nummer):
    db.execute(
        "INSERT INTO favourites (rezeptID, userID) VALUES (?, ?)", nummer, session["user_id"]
    )
    return redirect(url_for('recipe', nummer = nummer))
# remove from favourites
@app.route('/removeFavos/<int:nummer>')
@login_required
def removeFromFavos(nummer):
    db.execute(
        "DELETE FROM favourites WHERE rezeptID = ? AND userID = ?", nummer, session["user_id"]
    )
    return redirect(url_for('recipe', nummer = nummer))

# Login-Page
@app.route('/login', methods=["GET", "POST"])
def login():
    # forget any user_id
    session.clear()

    # User reached route via POST (as submitting the form via POST)
    if request.method == "POST":
        #Ensure username was submitted
        if not request.form.get("username"):
            return apology("No username was submitted", 403)
        #Ensure password was submitted
        elif not request.form.get("password"):
            return apology("No password was submitted", 403)
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure userename exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology ("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        return redirect("/")
        
    # User reached route via GET (as by clicking link in navbar or redirect)
    else:
        return render_template("login.html")
    

#Register-Page
@app.route("/register", methods=["GET", "POST"])
def register():
    # User reached route via POST (as submitting the form via POST)
    if request.method == "POST":
        #setting variables
        web_username = request.form.get("username")
        web_password = request.form.get("password")
        web_confirmation = request.form.get("confirmation")

        #check cells are filled
        if not web_username or not web_password or not web_confirmation:
            return apology("Please fill the form", 400)
        #check password matches confirmation
        if web_password != web_confirmation:
            return apology("Confirmation doesn't match password...", 400)
        #check username is free
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", web_username
        )
        if len(rows) != 0:
            return apology("Username is already taken!", 400)
        
        #create hash from password
        web_hash = generate_password_hash(web_password)
        
        #create useraccount in database
        db.execute(
            "INSERT INTO users(username, hash) VALUES(?, ?)", web_username, web_hash
        )
        #get id for session[user_id]
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", web_username
        )
        #Remember which usere has logged in
        session["user_id"] = rows[0]["id"]
        #redirect user to home page
        return redirect("/")
    
    # User reached route via GET (as by clicking link in Login-Form or redirect)
    else:
        return render_template("register.html")
    

#Add Recipe-Page
class recipe:
    def __init__(self):
        self.title = "blank"
        self.creator = "blank"
        self.picture = "/static/images/meal_default.png"
        self.vegie = False
        self.vegan = False
        self.lactose = False
        self.gluten = False
        self.bakery = False
        self.meal = False
        self.desert = False
        self.ingridients = []
        self.preparation = []

    def cdTitle(self, newTitle):
        self.title = newTitle

    def addIngridient(self, ingridient):
        self.ingridients.append(ingridient)

    def addPreparation(self, preparation):
        self.preparation.append(preparation)
    
    def cdPic(self, pic):
        self.picture = "/static/images/" + pic

    def clearRecipe(self):
        self.title = "blank"
        self.creator = "blank"
        self.picture = "/static/images/meal_default.png"
        self.vegie = False
        self.vegan = False
        self.lactose = False
        self.gluten = False
        self.bakery = False
        self.meal = False
        self.desert = False
        self.ingridients = []
        self.preparation = []

rezept = recipe()


@app.route("/addRecipe", methods=["GET", "POST"])
@login_required
def addRecipe():
    # User reached route via POST (as submitting the form via POST)
    if request.method == "POST":
        #To Do
        return apology("Task's left open", 400)
    
    #User reached route via GET (as clicking link in Navbar)
    else:
        return render_template("addRecipe.html", rezept = rezept)
    
@app.route("/setName", methods=["POST"])
@login_required
def changeName():
    webTitle = request.form.get("recipeTitle")
    rezept.cdTitle(webTitle)
    desert = request.form.get("desert")
    meal = request.form.get("meal")
    bakery = request.form.get("bakery")
    desert = request.form.get("desert")
    vegie = request.form.get("vegie")
    vegan = request.form.get("vegan")
    gluten = request.form.get("gluten")
    lactose = request.form.get("lactose")
    if meal:
        rezept.meal= True
    if bakery:
        rezept.bakery = True
    if desert:
        rezept.desert = True
    if vegie:
        rezept.vegie = True
    if vegan:
        rezept.vegan = True
    if gluten:
        rezept.gluten = True
    if lactose:
        rezept.lactose = True

    rows = db.execute(
        "SELECT username FROM users WHERE id = ?", session["user_id"]
    )

    rezept.creator = rows[0]["username"]
    return render_template("addRecipe.html", rezept = rezept)

@app.route("/addIngridient", methods=["POST"])
@login_required
def addingIngri():
    ingridient = request.form.get("ingridientName")
    rezept.addIngridient(ingridient)
    return render_template("addRecipe.html", rezept = rezept)

@app.route("/addPreparation", methods=["POST"])
@login_required
def addingPrep():
    preparation = request.form.get("preparationName")
    rezept.addPreparation(preparation)
    return render_template("addRecipe.html", rezept = rezept)

@app.route("/changePic", methods=["POST"])
@login_required
def changePicture():
    if 'recipePic' not in request.files:
        flash("No file part")
        return redirect(request.url)
    web_picture = request.files['recipePic']
    web_picture_name = secure_filename(web_picture.filename)
    unique_picname = str(uuid.uuid1()) + "_" + web_picture_name
    web_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_picname))
    rezept.cdPic(unique_picname)
    return render_template("addRecipe.html", rezept = rezept)

@app.route("/wipeRecipe", methods=["POST"])
@login_required
def wipeRecipe():
    rezept.clearRecipe()
    return render_template("addRecipe.html", rezept = rezept)


@app.route("/saveRecipe", methods=["POST"])
@login_required
def saveRecipe():
    # Hier muss das recipe-Objekt in die Datenbank eingelesen werden
    db.execute(
        "INSERT INTO rezept(title, userID, bild, bakery, meal, desert, vegie, vegan, gluten, lactose) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rezept.title, session["user_id"], rezept.picture, rezept.bakery, rezept.meal, rezept.desert, rezept.vegie, rezept.vegan, rezept.gluten, rezept.lactose
    )
    rows = db.execute(
        "SELECT id FROM rezept WHERE title = ?", rezept.title
    )    
    
    
    rezeptNummer = rows[0]["id"]

    for t in rezept.ingridients:
        db.execute(
            "INSERT INTO zutaten(rezeptId, zutat) VALUES(?,?)", rezeptNummer, t
        )

    for y in rezept.preparation:
        db.execute(
            "INSERT INTO anweisungen(rezeptId, anweisung) VALUES(?,?)", rezeptNummer, y
        )
    
    rezept.clearRecipe()
    return redirect('/')
    #return render_template("index.html", rezept = rezept)

# Function editIngri
@app.route("/editIngri/<int:pos>", methods=["POST", "GET"])
def editIngri(pos):
    if request.method == "POST":
        # Änderung anwenden
        rezept.ingridients[pos] = request.form.get("editedIngridientName")
        return render_template("addRecipe.html", rezept = rezept, pos = pos)
    else:
        return render_template("addRecipe_editIngri.html", pos = pos, rezept=rezept)
  

# Funktion deleteIngri
@app.route("/deleteIngri/<int:pos>")
def deleteIngri(pos):
    rezept.ingridients.pop(pos)
    return render_template("addRecipe.html", rezept = rezept, pos = pos)

# Funktion editPrep
@app.route("/editPrep/<int:pos>", methods=["POST", "GET"])
def editPrep(pos):
    if request.method == "POST":
        # Änderung anwenden
        rezept.preparation[pos] = request.form.get("editedPreparationName")
        return render_template("addRecipe.html", rezept = rezept, pos = pos)
    else:
        return render_template("addRecipe_editPrep.html", pos = pos, rezept=rezept)
  

#Funktion deleteIngri
@app.route("/deletePrep/<int:pos>")
def deletePrep(pos):
    rezept.preparation.pop(pos)
    return render_template("addRecipe.html", rezept = rezept, pos = pos)
