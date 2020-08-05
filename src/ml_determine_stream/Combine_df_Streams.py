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

with open(os.path.join(os.path.dirname(__file__), 'df_cybersecurity'), 'rb') as fh:  # you need to use 'rb' to read
    df_cyber_Security = pickle.load(fh)


with open(os.path.join(os.path.dirname(__file__), 'df1_jd'), 'rb') as fh:  # you need to use 'rb' to read
    df1_with_Dev = pickle.load(fh)


#print(df_cyber_Security.info())
#print(df1_with_Dev['Stream'].unique())

# remove cyber and risk from df
df1_with_Dev = df1_with_Dev[(df1_with_Dev.Stream != 'Cyber Security') & (df1_with_Dev.Stream != 'Compliance and Risk')]
#print(df1_with_Dev['Stream'].unique())
#print(df1_with_Dev.info())

# combine risk and cybersecuirty with   >>> df1_with_Dev
# Technical support scrape






# drop itsm ism add test combine pmo






with open(os.path.join(os.path.dirname(__file__), 'df2_jd'), 'rb') as fh:  # you need to use 'rb' to read
    df2 = pickle.load(fh)


print(df2.info())
print(df2['Stream'].unique())