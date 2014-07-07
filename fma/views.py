from fma import app
from fma.models import db_find_users, db_find_units, db_add_unit, db_update_unit, to_unit, get_range_query
from flask import jsonify, request, render_template, url_for

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/userslist", methods=["GET"])
def users_list():
    users = db_find_users({});
    return jsonify( {'users' : users } ), 200

@app.route("/users/", methods=["GET"])
def users_search():
    searched_email = request.args.get("email")
    if searched_email.strip() == "" :
        return users_list()
    # this might be potentially dangerous
    users = db_find_users( {"email" : { "$regex" : searched_email} });
    return jsonify( {'users' : users} ), 200

@app.route("/unitslist", methods=["GET"])
def units_list():
    query = {}

    street_name = request.args.get("street_name")
    city = request.args.get("city")
    country = request.args.get("country")
    price = request.args.get("price")
    num_rooms = request.args.get("num_rooms")
    num_bathrooms = request.args.get("num_bathrooms")
    if price is not None:
        query["price"] = get_range_query(str(price))
    if city is not None:
        query["address.city"] = { "$regex" : city }
    if country is not None:
        query["address.country"] = { "$regex" : country }
    if street_name is not None:
        query["address.street_name"] = { "$regex" : street_name }
    if num_rooms is not None:
        query["num_rooms"] = get_range_query(str(num_rooms))
    if num_bathrooms is not None:
        query["num_bathrooms"] = get_range_query(str(num_bathrooms))
    print(query)
    units = db_find_units(query);
    return jsonify( {"units" : units }), 200

@app.route("/newunit", methods=["POST"])
def new_unit():
    db_add_unit(request.get_json("data"));
    return jsonify( {} ), 200

@app.route("/updateunit", methods=["PUT"])
def update_unit():
    db_update_unit(request.get_json("data"))
    return jsonify({}), 200
