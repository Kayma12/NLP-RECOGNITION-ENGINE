from pymongo import MongoClient

mdb_client = MongoClient(host="mongodb://localhost:27017", connect=False)
mdb = mdb_client["Consultants"]


# Populate db
def add_consultant():
    consultant = mdb.consultant.insert_one({
        "name": {
            "first_name": "Susan",
            "last_name": "Campbell"
        },
        "streams": {
            "development": True,
            "business_analysis": False,
            "business_intelligence": False
        },
        "skills": {
            "Java": 3,
            "Python": 9,
        }
    })
    print("user added successfully !!!")
