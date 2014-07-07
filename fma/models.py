import pymongo
from fma import app
from flask import g, jsonify 
from pymongo import MongoClient
from bson.objectid import ObjectId

######################### DB CODE ########################
def connect_db(url) :
    client = MongoClient(url);
    return client

def get_db():
    if not hasattr(g, "mongo"):
        g.mongo = connect_db(app.config["DATABASE_URL"])
        g.database = g.mongo[app.config["DATABASE_NAME"]]
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

def db_add_user(user):
    # make sure there is no exising user with the same email.
    found = db_find_users({ "email" : user["email"]});
    if found.count() == 0 :
        db = get_db()
        db.users.insert(user)

# query is the dictionary of property that is used to query the database. 
# empty query will just return all units.
def db_find_users(query):
    print("Finding users")
    print(query)
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
"""
    The purpose of this method is to trim away the irrelevant values before returning to the client or putting
    into the database. 

    unit : the dict object
    copyId : bool , if True, then the "_id" value will be copied as well, else it will not be copied
"""
def to_unit(unit, copyId=None) :
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
        try:
            u["price"] = int(unit["price"])
        except ValueError:
            u["price"] = 0
    if "num_rooms" in unit :
        try:
            u["num_rooms"] = int(unit["num_rooms"])
        except ValueError:
            u["num_rooms"] = 0
    if "num_bathrooms" in unit :
        try:
            u["num_bathrooms"] = int(unit["num_bathrooms"])
        except ValueError:
            u["num_bathrooms"] = 0
    if "sqft" in unit :
        u["sqft"] = unit["sqft"]
    if copyId and "_id" in unit :
        u["_id"] = str(unit["_id"])
    return u

def db_find_units(query):
    db = get_db()
    print("Finding units")
    print(query)
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

def db_add_unit(unitdata) :
    db = get_db()
    u = to_unit(unitdata, False)
    db.units.insert(u)

"""
Construct a query based on a specific syntax.
1. A single number : returns the number
2. <number><  : return { "$gt" : number }
3. <number>>  : return { "$lt" : number }
4. <min>-<max> : return { "$gte" : min , "$lte" : max}
5. other format : return None
"""
def get_range_query(query):
    print(query)
    if query[-1] is "<" :
        try:
            value = float(query[:-1])
            return { "$gt" : value }
        except ValueError:
            print("GTE")
            return None
    elif query[-1] is ">" :
        try :
            value = float(query[:-1])
            return { "$lt" : value}
        except ValueError:
            print("LTE")
            return None
    elif "-" in query:
        range = query.split("-")
        if len(range) is not 2:
            return None
        else :
            try:
                min = float(range[0])
                max = float(range[1])
                return { "$lte" : max , "$gte" : min}
            except ValueError:
                return None
    else:
        try:
            value = float(query)
            return value
        except ValueError:
            print("ELSE")
            return None

