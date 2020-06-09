import os
import pickle

from flask import Blueprint

from database import db_consultant, db_skills
import skills.cleaning_skills as pre_skills
from model import Consultant


# get skills
with open(os.path.join(os.path.dirname(__file__), 'preliminary_skills'), 'rb') as fh:  # you need to use 'rb' to read
    skills_list = pickle.load(fh)

# to load the file do this
with open(os.path.join(os.path.dirname(__file__), 'candidates_df'), 'rb') as fh:  # you need to use 'rb' to read
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
    db_skills.delete_many({})
    skills = db_skills.insert_many([
        {"stream": "All Skills", "skills": skills_list}
    ])


# Retrieve stream skills from db
def get_skills(stream):
    document = db_skills.find_one({"stream": stream})
    return document.get('skills')


# Retrieve all skills from db
def get_all_skills():
    dict_skills = db_skills.find()
    list_skills = list()
    for x in dict_skills:
        for y in x.get('skills'):
            if y != 'nan': list_skills.append(y)

    return list_skills


# Returns the consultants that have at least one skill from the list
def query_skills(list_skills):
    dict_skills = dict()
    for l in list_skills:
        dict_skills.update({"skills." + l: {"$gt": 0}})
    query = {'$or': [dict_skills]}
    # print(query)
    consultants_cursor = db_consultant.find(query)
    consultants_list = list()
    for c in consultants_cursor:
        consultants_list.append(c)
    return consultants_list


mydoc = query_skills(['Java', 'Python'])


"""
        "streams": {
            "development": True,
            "business_analysis": False,
            "business_intelligence": False
        },
"""