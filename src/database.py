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

def add_skills():
    skills = mdb.skills.insert_many([
        {"stream": "Developer", "skills": ["java", "python", "javascript", "css", "html"]},
        {"stream": "Tester", "skills": ["mockito", "tester", "test", "junit", "test develpment"]},
        {"stream": "BA", "skills": ["project management", "agile", "excel", "risk analysis", "process modelling"]},
        {"stream": "BI", "skills": ["tableau", "power bi", "qlik", "sql", "hadoop"]}
    ])

# Retrieve strem skills from db
def get_skills(stream):
    document = mdb.skills.find_one({"stream": stream})
    return document.get('skills')