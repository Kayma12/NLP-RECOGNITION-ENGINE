import os
import re

import pandas as pd

import cv_cleaning
import read_in_files
import skills.preliminary_skills as pre_skills

# get skills
file_for_skills = "skills/preliminary_skills.csv"
skills_list = pd.read_csv(file_for_skills)

# get local cv
# cv_file_loc = "dummy_cvs/Susan Campbell CV DOC test.doc"

#get cv from directory
cv_dir = "dummy_cvs/"
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
    # can return full name
    first_and_last_name = name_and_cv[0:2]
    df_name = pd.DataFrame({'Name': [first_and_last_name[0] + " " + first_and_last_name[1]]})
    return df_name


def skill_cv_comparison(file):
    all_skills = pre_skills.get_skills(skills_list)
    # just dev skills
    dev_skills = all_skills[0]
    # dev_skills = ['python']
    dev_dict = pre_skills.list_to_dict(dev_skills)
    clean_cv = cv_cleaning.clean_cv(read_in_files.read_in_doc_docx_file(file))

    # for word in clean_cv:
    #     if word in dev_dict:
    #         dev_dict[word] = dev_dict.get(word) + 1
    #     if re.search(r"^\w+\d+$", word):
    #         if word.isdigit():
    #             continue
    #         else:
    #             result = ''.join([char for char in word if not char.isdigit()])
    #             if result in dev_dict:
    #                 dev_dict[result] = dev_dict.get(result) + 1

    for word in clean_cv:
        if word in dev_dict:
            dev_dict[word] = dev_dict.get(word) + 1
        if re.search(r"^\w+\d+$", word):
            if word.isdigit():
                continue
            else:
                result = ''.join([char for char in word if not char.isdigit()])
                if result in dev_dict:
                    dev_dict[result] = dev_dict.get(result) + 1

    dev_map = {key: val for key, val in dev_dict.items() if val > 0}
    df = pd.DataFrame([dev_map], columns=dev_map.keys())
    df_name = get_candidate_name(file)
    df_with_name = pd.concat([df, df_name], axis=1)
    df_with_name.set_index('Name', inplace=True)
    return df_with_name


# print(skill_cv_comparison(cv_file_loc).to_string())

## Final dataframe with more than one cvs
final_candidates_df = pd.DataFrame()
index = 0
while index < len(cv_file):
    a_cv_file = cv_file[index]
    cv_data = skill_cv_comparison(a_cv_file)
    final_candidates_df = pd.concat([final_candidates_df, cv_data])
    final_candidates_df = final_candidates_df.fillna(0).astype(int)
    index += 1

# print(final_candidates_db.to_string())

# df to csv
# final_candidates_db.to_csv(r'/Users/kaykay/Downloads/list_of_candidates.csv')
