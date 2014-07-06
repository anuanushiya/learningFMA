import os 
import sys
import pymongo
from bson.objectid import ObjectId
from flask import Flask
# from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response, jsonify
from pymongo import MongoClient
##########################################################


MONGO_URL = os.environ.get('MONGOHQ_URL')
MONGO_DB = os.environ.get('MONGOHQ_DBNAME')
if MONGO_URL == None:
    MONGO_URL = "mongodb://localhost:27017"  # for development environmnet, set it to local host
    print("Development environment, mongodb location at " + MONGO_URL)

if MONGO_DB == None:
    MONGO_DB = "main"
print("Using DB : " + MONGO_DB)

print("Mongo URL : " + MONGO_URL)

app = Flask(__name__);
app.config.from_object(__name__)

# change this from the dict() initializer to {} instead. Looks nicer.
# I don't like key value of a dict to be "non-string", looks like variable to me.
app.config.update({
    "DATABASE_URL" : MONGO_URL,
    "DATABASE_NAME" : MONGO_DB,
    "DEBUG" : True,
    "SECRET_KEY" : "Development Key",
    "USERNAME" : "admin",
    "PASSWORD" : "default",
    })

import fma.views
