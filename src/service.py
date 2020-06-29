import os
import pickle
import json
from bson.objectid import ObjectId
from database import db_consultant, db_skills
import skills.cleaning_skills as pre_skills
from model import Consultant
from bson import Binary


# get skills
with open(os.path.join(os.path.dirname(__file__), 'preliminary_skills'), 'rb') as fh:  # you need to use 'rb' to read
    skills_list = pickle.load(fh)

# to load the file do this
with open(os.path.join(os.path.dirname(__file__), 'candidates_df'), 'rb') as fh:  # you need to use 'rb' to read
    df = pickle.load(fh)

#print(df[['java','Stream']])
# print(df)
# print(df.index)


def add_consultants():
    dict_consultant = {"name": {}, "stream": {}, "skills": {}, "consultant_cv": {}}
    for index in df.index:
        dict_consultant['_id'] = ObjectId()
        dict_consultant['name']['first_name'] = index.split()[0]
        dict_consultant['name']['last_name'] = index.split()[1]

        for col in df.columns:

            if (col != 'Stream' and col != 'Candidate_cv'and col != 'cv_path'):

                #print(index)
                #print(df.loc[index, col])
                dict_consultant['skills'][col] = int(df.loc[index, col])
            elif (col == 'Stream'):
                dict_consultant['stream'] = df.loc[index, col]
            elif (col == 'cv_path'):
                with open(df.loc[index, col], "rb") as f:
                    data = f.read()
                bi = Binary(data)
                dict_consultant['cv_file'] = bi
            else:
                dict_consultant['consultant_cv'] = df.loc[index, col]
        db_consultant.insert_one(dict_consultant)
        # print(dict_consultant)


# adding skills to database
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
        cons = Consultant(c['name']['first_name'], c['name']['last_name'], c.get('stream'), c.get('skills'))
        consultants_list.append(cons)
    return consultants_list

# Returns a list of consultants only with the skills from the list
def query_consultants_with_skills(list_skills):
    query = list()
    query.append('{ "$or": [')
    for l in list_skills:
        query.append('{"skills.' + str(l) + '": {"$gt": 0}}')
        query.append(',')
    query.pop()
    query.append('] }')
    query2 = ''.join(query)
    d = json.loads(query2)
    consultants_cursor = db_consultant.find(d)
    consultants_list = list()
    for c in consultants_cursor:
        cons = Consultant(c.get('_id'), c['name']['first_name'], c['name']['last_name'], c.get('stream'), c.get('skills'))
        cons = filter_skills_consultant(cons, list_skills)
        consultants_list.append(cons)
    return consultants_list

# Given a consultant and a list of skills, returns the consultant with given skills only
def filter_skills_consultant(cons, list_skills):
    skills_consultant = cons.skills
    result = dict()
    for l in list_skills:
        result.update({l : skills_consultant.get(l)})
    cons.skills = result
    return cons

# Given a consultant, returns the consultant with his 10 best skills
def filter_10_skills(cons):
    dict_skills = dict()
    for l in cons.skills:
        if(cons.skills.get(l) != 0): dict_skills.update({l: cons.skills.get(l)})
    sort_skills = sorted(dict_skills.items(), key=lambda x: x[1], reverse=True)[0:10]
    cons.skills = sort_skills
    return cons

# Return a Consulant with a given ID with (the 10 highest) skills that are not 0
def get_consultant(consultant_id):
    c = db_consultant.find_one({"_id": ObjectId(consultant_id)})
    # c = db_consultant.find_one({"name.last_name": consultant_id})
    consultant = Consultant(c.get('_id'), c['name']['first_name'], c['name']['last_name'], c.get('stream'), c.get('skills'))
    consultant = filter_10_skills(consultant)
    return consultant

# Given a Consultant ID returns the binary file of the consultant 
def get_binary(consultant_id):
    c = db_consultant.find_one({"_id": ObjectId(consultant_id)})
    binary = c.get('cv_file')
    return binary



# get_consultant('Wick')
mydoc = query_consultants_with_skills(['java', 'sql','python'])
# for c in mydoc:
#    print(c)

"""
        "streams": {
            "development": True,
            "business_analysis": False,
            "business_intelligence": False
        },
"""

# a_consultant = Consultant('Gertrude', 'Wilson', 'developer', {'Java' : 3, 'Python' : 9, 'HTML5' : 2, 'CSS3' : 2}, availability = True)
# print(a_consultant)

