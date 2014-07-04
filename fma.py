import os 
import pymongo
from bson.objectid import ObjectId
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
    result = db.users.find(query)
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
    return users

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
def to_unit(unit, copyId) :
    u = { "address" : { "block_number" : "", "street_name" : "", "postal_code" : "", "city" : "", "country" : "", "coordinates" : ""}, "price" : 0, "num_rooms" : 0, "num_bathrooms" : 0, "sqft" : 0}
    if copyId :
        u["_id"] = ""
    if "address" in unit :
        if "block_number" in unit["address"] :
            u["address"]["block_number"] = unit["address"]["block_number"]
        if "street_name" in unit["address"] :
            u["address"]["street_name"] = unit["address"]["street_name"]
        if "postal_code" in unit["address"] :
            u["address"]["postal_code"] = unit["address"]["postal_code"]
        if "city" in unit["address"] :
            u["address"]["city"] = unit["address"]["city"]
        if "country" in unit["address"] :
            u["address"]["country"] = unit["address"]["country"]
        if "coordinates" in unit["address"] :
            u["address"]["coordinates"] = unit["address"]["coordinates"]
    if "price" in unit :
        u["price"] = unit["price"] 
    if "num_rooms" in unit :
        u["num_rooms"] = unit["num_rooms"]
    if "num_bathrooms" in unit :
        u["num_bathrooms"] = unit["num_bathrooms"]
    if "sqft" in unit :
        u["sqft"] = unit["sqft"]
    if copyId and "_id" in unit :
        u["_id"] = str(unit["_id"])
    return u


def add_unit(unit):
    db = get_db()
    db.units.insert(unit)

def find_units(query):
    db = get_db()
    result = db.units.find(query)
    units = []
    for unit in result :
        u = to_unit(unit, True)
        units.append(u)
    return units

def db_update_unit(unitdata):
    db = get_db()
    if "_id" in unitdata :
        existing = db.units.find_one( { "_id" : ObjectId(unitdata["_id"]) })
        if existing is None :
            print("Not existing")
            return False
        u = to_unit(unitdata, False) # ensure that the "data" is cleansed 
        db.units.update( { "_id" : ObjectId(unitdata["_id"]) }, { "$set" : u }, upsert = False );
        return True;
    else :
        return False

##########################################################

######
MONGO_URL = os.environ.get('MONGOHQ_URL') # for heroku

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

@app.route("/", methods=["GET"])
def home():
    return make_response(open('templates/index.html').read())

@app.route("/userslist", methods=["GET"])
def users_list():
    users = find_users({});
    return jsonify( {'users' : users } ), 200

@app.route("/users/", methods=["GET"])
def users_search():
    searched_email = request.args.get("email")
    if searched_email.strip() == "" :
        return users_list()
    # this might be potentially dangerous
    users = find_users( {"email" : { "$regex" : searched_email} });
    return jsonify( {'users' : users} ), 200

@app.route("/unitslist", methods=["GET"])
def units_list():
    units = find_units({});
    return jsonify( {"units" : units }), 200

@app.route("/newunit", methods=["POST"])
def new_unit():
    print(request.data)
    return jsonify( {} ), 200

@app.route("/updateunit", methods=["PUT"])
def update_unit():
    db_update_unit(request.get_json("data"))
    return jsonify({}), 200


if __name__ == "__main__" :
    app.run()

