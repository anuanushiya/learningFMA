from fma import app
from fma.models import db_find_users, db_find_units, db_add_unit, db_update_unit
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
    units = db_find_units({});
    return jsonify( {"units" : units }), 200

@app.route("/newunit", methods=["POST"])
def new_unit():
    db_add_unit(request.get_json("data"));
    return jsonify( {} ), 200

@app.route("/updateunit", methods=["PUT"])
def update_unit():
    db_update_unit(request.get_json("data"))
    return jsonify({}), 200
