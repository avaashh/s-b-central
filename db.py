import os, pymongo
from dotenv import load_dotenv

load_dotenv()

client = pymongo.MongoClient(os.getenv("MongoUrl"))
db = client["grinnell-discord"]


def InsertOne(collection, post):
    db[collection].insert_one(post)


def InsertMany(collection, posts):
    db[collection].insert_many(posts)


def DeleteOne(collection, criteria):
    db[collection].delete_one(criteria)


def UpdateOne(collection, criteria, post):
    db[collection].update_one(criteria, {"$set": post})


def IncrementOne(collection, criteria, post):
    db[collection].update_one(criteria, {"$inc": post})


def FindOne(collection, criteria):
    return db[collection].find_one(criteria)


def FindAll(collection, criteria):
    return db[collection].find(criteria)
