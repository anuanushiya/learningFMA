import os 
import pymongo
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, jsonify
from pymongo import MongoClient

######################### DB CODE ########################
def connect_db(url) :
    client = MongoClient(url);
    return client

def get_db():
    if not hasattr(g, "mongo"):
        g.mongo = connect_db(app.config["DATABASE"])
        g.database = g.mongo.main
    return g.database

# @app.teardown_appcontext
def close_db(error):
    if hasattr(g, "mongo"):
        g.mongo.close();

######################### DAO ############################
### code for adding user and removing user.
# user :
#   id :
#   email
#   firstname
#   lastname

# unit :
# id
# address {
#     block_number
#     street_name
#     postal_code
#     city
#     country
#     coordinates 
# }
# price  // rental price per month
# num_rooms
# num_bathrooms
# sqft  // square footage of apartment

def add_user(user):
    # make sure there is no exising user with the same email.
    found = find_users({ "email" : user["email"]});
    if found.count() == 0 :
        db = get_db()
        db.users.insert(user)

# query is the dictionary of property that is used to query the database. 
# empty query will just return all units.
def find_users(query):
    db = get_db()
    found = db.users.find(query)
    return found


##########################################################

######
MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL == None :
    MONGO_URL = "mongodb://localhost:27017/" # for development environmnet, set it to local host
    print("Development environment, mongodb location at " + MONGO_URL)

app = Flask(__name__);
app.config.from_object(__name__)

# change this from the dict() initializer to {} instead. Looks nicer.
# I don't like key value of a dict to be "non-string", looks like variable to me.
app.config.update({
    "DATABASE" : MONGO_URL,
    "DEBUG" : True,
    "SECRET_KEY" : "Development Key",
    "USERNAME" : "admin",
    "PASSWORD" : "default",
    })

app.config.from_envvar("FLASKR_SETTINGS", silent=True)

@app.route("/", methods=["GET"])
def home():
    return make_response(open('templates/index.html').read())

@app.route("/userslist", methods=["GET"])
def users_list():
    result = find_users({});
    users = []
    for user in result :
        u = { "email" : "", "first_name" : "", "last_name" : ""}
        if "email" in user :
            u["email"] = user["email"]
        if "first_name" in user :
            u["first_name"] = user["first_name"]
        if "last_name" in user :
            u["last_name"] = user["last_name"]
        users.append(u)
    return jsonify( {'users' : users } ), 200

if __name__ == "__main__" :
    app.run()

