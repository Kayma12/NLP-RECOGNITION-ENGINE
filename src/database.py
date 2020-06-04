from pymongo import MongoClient

mdb_client = MongoClient(host="mongodb://localhost:27017", connect=False)
mdb = mdb_client["Name of collection"]