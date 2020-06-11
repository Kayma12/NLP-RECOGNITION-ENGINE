import os
import pickle
import re
import pandas as pd
from pathlib import Path

from cleaning_and_reading import cv_cleaning, read_in_files
from skills import cleaning_skills as pre_skills
from service import get_all_skills as db_skills

# get skills from csv then clean them
file_for_skills = Path(__file__).parent / "skills/preliminary_skills.csv"

skills_list = pd.read_csv(file_for_skills)
skills_list = pre_skills.get_skills_from_df_to_list(skills_list)
skills_list = pre_skills.get_list_from_list(skills_list)
skills_list = pre_skills.clean_list_of_skills(skills_list)
# print(skills_list)

# get cv from directory
cv_dir = Path(__file__).parent / "dummy_cvs/"
file_ext = [".doc", ".docx"]

cv_file = [os.path.join(cv_dir, file) for file in os.listdir(cv_dir) if file.endswith(tuple(file_ext))]


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

    # seperating last name because some may contain info on the type of cv
    last_name_cv_detail = "".join((char if char.isalpha() else " ") for char in name_and_cv[1]).split()
    last_name = last_name_cv_detail[0]
    df_name = pd.DataFrame({'Name': [first_name + " " + last_name]})
    return df_name


def get_stream(file):
    file = file.lower()
    if "java" and "mockito" in file:
        return "Development"
    # elif "spring" and "oop" in file:
    #     return "Development"
    elif "etl" in file:
        return "Business Intelligence"
    elif "istqb" in file:
        return "Tester"
    elif "business fundamentals" in file:
        return "Business Analysis"
    elif "prince 2" and "scrum master" in file:
        return "PMO"
    elif "regulation and compliance" and "kyc" in file:
        return "Risk Regulation & Compliance"
    elif "completed the analysis programme" and "bcs" in file:
        return "Analyst"
    elif "completed the project support office" in file:
        return "Project Support Officer"
    else:
        return ""


def skill_cv_comparison(file):
    db_skills_cleaned = pre_skills.clean_list_of_skills(db_skills())
    skills_dict = pre_skills.list_to_dict(db_skills_cleaned)

    cv_before_cleaning = read_in_files.read_in_doc_docx_file(file)
    # df = get_stream(cv_before_cleaning)
    clean_cv = cv_cleaning.clean_cv(cv_before_cleaning)

    for key in skills_dict.keys():
        clean_cv_str = ''.join(clean_cv)
        clean_cv_str = cv_cleaning.remove_alevel_gcse_section(clean_cv_str)
        if ' ' in key:
            find_key = re.findall('%s' % key, clean_cv_str)
            count_amount_of_key = len(find_key)
            skills_dict[key] = count_amount_of_key
        else:
            num = clean_cv_str.split().count(key)

            skills_dict[key] = num
    clean_cv_str = ''.join(clean_cv)
    clean_cv_version = re.split("\s+", clean_cv_str)

    for word in clean_cv_version:
        if re.search(r"^\w+\d+$", word):
            if word.isdigit():
                continue
            else:
                result = ''.join([char for char in word if not char.isdigit()])
                if result in skills_dict:
                    skills_dict[result] = skills_dict.get(result) + 1

    dev_map = {key: val for key, val in skills_dict.items() if val > 0}
    df = pd.DataFrame([dev_map], columns=dev_map.keys())
    df_name = get_candidate_name(file)
    df_with_name = pd.concat([df, df_name], axis=1)
    df_with_name.set_index('Name', inplace=True)
    return df_with_name


# get skill from cv

# print(skill_cv_comparison(cv_file_loc).to_string())

# Final dataframe with more than one cvs
final_candidates_df = pd.DataFrame()
df_stream = pd.DataFrame(columns=['Stream'])
index = 0
while index < len(cv_file):
    a_cv_file = cv_file[index]
    cv_before_cleaning = read_in_files.read_in_doc_docx_file(a_cv_file)
    stream = get_stream(cv_before_cleaning.lower())
    df_stream.loc[index] = stream
    cv_data = skill_cv_comparison(a_cv_file)
    final_candidates_df = pd.concat([final_candidates_df, cv_data])
    index += 1

final_candidates_df = final_candidates_df.join(df_stream.set_index(final_candidates_df.index))
final_candidates_df = final_candidates_df.fillna(0).drop_duplicates()
final_candidates_df = final_candidates_df.astype(int, errors='ignore')

#print(final_candidates_df)
# print(final_candidates_df.index)

# this will create a file called candidates_df that will store the data frame
with open(Path(__file__).parent / 'candidates_df', 'wb') as fh:  # notice that you need the 'wb' for the dump
    pickle.dump(final_candidates_df, fh)

# dump preliminary skills
with open(Path(__file__).parent / 'preliminary_skills', 'wb') as fh:  # notice that you need the 'wb' for the dump
    pickle.dump(skills_list, fh)

# df to csv
#final_candidates_df.to_csv(r'/Users/kaykay/Downloads/list_of_candidates_all_skills_30+.csv')
