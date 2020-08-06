import os
import pickle

with open(os.path.join(os.path.dirname(__file__), 'df_final'), 'rb') as fh:  # you need to use 'rb' to read
    df = pickle.load(fh)


# Drop over laps in BA
'''
'Ref Data Architecture Business analyst And Project Manager',  >> ba. 
'Business Data Analyst â€“ Compliance',
>> IF IT CONTAINS DATA drop from BA
'''
df2 = df[(df.Stream == 'Business Analysis') & (df.Title.str.contains("Data"))].index
df.drop(df2, inplace=True)