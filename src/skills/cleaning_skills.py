# get skills
def get_skills_from_df_to_list(df):
    # lower all string in df , strip space
    df = df.astype(str)
    df = df.apply(lambda x: x.astype(str).str.lower())
    df = df.apply(lambda x: x.astype(str).str.strip())

    # section off skills
    developer_skills = [word.rstrip('\n') for word in df['Developer'].dropna(axis=0)]
    bi_skills = [word.rstrip('\n') for word in df['Business_Intelligence'].dropna(axis=0)]
    ba_skills = [word.rstrip('\n') for word in df['Business_Analyst'].dropna(axis=0)]
    tester_skills = [word.rstrip('\n') for word in df['Tester'].dropna(axis=0)]

    return [developer_skills, bi_skills, ba_skills, tester_skills]


# dev_skills = get_skills(skills)[0] >> get dev skills example

def list_to_dict(skills_list):
    my_dict = {}
    for word in skills_list:
        my_dict[word] = 0
    return my_dict


def clean_list_of_skills(skills):
    skills_list = []
    for skill in skills:
        skill = skill.replace('\n', ' ')
        skill = skill.lower().strip()
        if skill != 'nan':
            skills_list.append(skill)
    return skills_list


# a = [x for x in lis for lis2 in lis]
def get_list_from_list(list_of_list):
    try:
        inner_list = []
        for outer_list in list_of_list:
            for inner_list_item in outer_list:
                inner_list.append(inner_list_item)

        return inner_list
    except:
        TypeError
        return list_of_list
