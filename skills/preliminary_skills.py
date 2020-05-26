

# get skills
def get_skills(df):
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