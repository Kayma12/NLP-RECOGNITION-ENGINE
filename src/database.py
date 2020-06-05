from pymongo import MongoClient

mdb_client = MongoClient(host="mongodb://localhost:27017", connect=False)
mdb = mdb_client["test_database"]
db_consultant = mdb['consultant']
db_skills = mdb['skill']
