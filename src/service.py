import os
import pickle
from database import db_consultant, db_skills
import skills.preliminary_skills as pre_skills

# get skills
with open(os.path.join(os.path.dirname(__file__),'preliminary_skills'), 'rb') as fh:  # you need to use 'rb' to read
    skills_list = pickle.load(fh)

# to load the file do this
with open(os.path.join(os.path.dirname(__file__),'candidates_df'), 'rb') as fh:  # you need to use 'rb' to read
    df = pickle.load(fh)

# print(df)
# print(df.index)


# Populate db
def add_consultant():
    consultant = db_consultant.insert_one({
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


# def add_consultants_from_engine():
#     for index in df.index:
#         print(index)
#
#     pass

# adding to database
def add_skills():
    skills = db_skills.insert_many([
        {"stream": "Developer", "skills": pre_skills.get_skills(skills_list)[0]},
        {"stream": "Tester", "skills": ["mockito", "tester", "test", "junit", "test develpment"]},
        {"stream": "BA", "skills": ["project management", "agile", "excel", "risk analysis", "process modelling"]},
        {"stream": "BI", "skills": ["tableau", "power bi", "qlik", "sql", "hadoop"]}
    ])


# Retrieve stream skills from db
def get_skills(stream):
    document = db_skills.find_one({"stream": stream})
    return document.get('skills')


