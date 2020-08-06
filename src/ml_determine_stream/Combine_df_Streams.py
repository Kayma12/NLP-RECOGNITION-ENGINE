# Clean and append dfs
'''

df1 content

map_of_streams_actual1 = {
    'Business Analysis': ['business analyst'], 'Business Intelligence': ['business intelligence', 'data analyst'],
    'Cloud Computing': ['cloud', 'azure'], 'Compliance and Risk': ['compliance and risk', 'risk analyst'],
    'Cyber Security': ['cyber security'], 'Development': ['software developer']}



'''
# get df1 with developer
import os
import pickle
from pathlib import Path

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df_cybersecurity'), 'rb') as fh:  # you need to use 'rb' to read
    df_cyber_Security = pickle.load(fh)

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df1_jd'), 'rb') as fh:  # you need to use 'rb' to read
    df1_with_Dev = pickle.load(fh)

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df_compliance_and_risk'),
          'rb') as fh:  # you need to use 'rb' to read
    df_cr = pickle.load(fh)

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df_pmo'), 'rb') as fh:  # you need to use 'rb' to read
    df_pmo = pickle.load(fh)

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df_information_security'),
          'rb') as fh:  # you need to use 'rb' to read
    df_is = pickle.load(fh)

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df_itsm'), 'rb') as fh:  # you need to use 'rb' to read
    df_itsm = pickle.load(fh)
# print(df_cyber_Security.info())
# print(df1_with_Dev['Stream'].unique())

# remove cyber and risk from df
df1 = df1_with_Dev[(df1_with_Dev.Stream != 'Cyber Security') & (df1_with_Dev.Stream != 'Compliance and Risk')]

with open(os.path.join(os.path.dirname(__file__), 'scraped files/df2_jd'), 'rb') as fh:  # you need to use 'rb' to read
    df2 = pickle.load(fh)

df2 = df2[(df2.Stream != 'Information Security Management') & (df2.Stream != 'IT Service Management')]

# combine test data
with open(os.path.join(os.path.dirname(__file__), 'scraped files/df_test'), 'rb') as fh:  # you need to use 'rb' to read
    df_test = pickle.load(fh)
df_test_data = df2.append(df_test, ignore_index=True, sort=False)

# Concat all
df = df_test_data.append([df_pmo, df_cr, df_is, df_cyber_Security], ignore_index=True, sort=False)
df = df.append(df1, ignore_index=True, sort=False)

# just need to concat ITSM
df = df.append(df_itsm, ignore_index=True, sort=False)
# print(df['Stream'].unique())
# print(df.info())
# Drop BA scrape with BI Titles
df2 = df[(df.Stream == 'Business Analysis') & (df.Title.str.contains("Business Intelligence"))].index

df.drop(df2, inplace=True)

df_dup = df[df.duplicated()]

print(df_dup[df_dup['Stream'] == 'Development'])











with open(Path(__file__).parent / 'df_final', 'wb') as fh:  # notice that you need the 'wb' for the dump
    pickle.dump(df, fh)
