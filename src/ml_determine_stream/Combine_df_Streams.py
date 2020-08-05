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

with open(os.path.join(os.path.dirname(__file__), 'df1_jd'), 'rb') as fh:  # you need to use 'rb' to read
    df1_with_Dev = pickle.load(fh)


print(df1_with_Dev.info())
print(df1_with_Dev['Stream'].unique(

))