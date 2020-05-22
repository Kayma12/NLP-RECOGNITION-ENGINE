import os
import re

import textract
from skills.Preliminary_Skills import Skills
import pandas as pd
import cv_cleaning

# get skills
file_for_skills = "skills/preliminary_skills.csv"
skills_list = pd.read_csv(file_for_skills)

# get local cv
cv = "dummy_cvs/Susan Campbell CV1.docx"


def read_in_file(file):
    text_file_repr = textract.process(file)
    text_file_repr = text_file_repr.decode('utf-8')
    return text_file_repr.lower()


# if all cv have atleast the first name of a candidate in title
def get_candidate_name(file_address):
    '''
    Basename returns the last part of the directory, which is the file itself name and extension.
    '/home/User/Documents/file.txt' === file.txt
    '''
    # based on only one cv
    filename = os.path.basename(file_address)  # Susan Campbell CV1.docx
    before_period = os.path.splitext(filename)[0]
    name_and_cv = before_period.split(" ")
    # can return first name
    first_name = name_and_cv[0]
    # can return full name
    first_and_last_name = name_and_cv[0:2]
    df_name = pd.DataFrame({'Name': [first_and_last_name[0] + " " + first_and_last_name[1]]})
    return df_name


# go through cv, add values to mop then turn it into a df, then add name to column

# this function should take a cv location so it process however many in the directory one at a time .. so for each cv in
#location put it through this function

def skill_cv_comparison():
    skills_table = Skills()
    all_skills = skills_table.get_skills(skills_list)
    # just dev skills
    dev_skills = all_skills[0]
    dev_map = skills_table.list_to_dict(dev_skills)
    clean_cv = cv_cleaning.clean_cv(read_in_file(cv))

    for word in clean_cv:

        if word in dev_map:
            regex = re.compile('\\b' + word + '\\b')
            if re.search(regex, word):
                dev_map[word] = dev_map.get(word) + 1

    dev_map = {key: val for key, val in dev_map.items() if val > 0}
    df = pd.DataFrame([dev_map], columns=dev_map.keys())
    df_name = get_candidate_name(cv)
    df_with_name = pd.concat([df, df_name], axis=1)
    df_with_name.set_index('Name', inplace=True, drop=True)

    return df_with_name


print(skill_cv_comparison())
