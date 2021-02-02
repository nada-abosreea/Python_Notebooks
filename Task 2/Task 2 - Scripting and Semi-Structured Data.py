#!/usr/bin/env python
# coding: utf-8

# ### Problem Descripition 
# 
# In 2012, URL shortening service Bitly partnered with the US government website USA.gov to provide a feed of anonymous data gathered from users who shorten links ending with .gov or .mil.
# 
# The text file comes in JSON format and here are some keys and their description. They are only the most important ones for this task.

# |key| description |
# |---|-----------|
# | a|Denotes information about the web browser and operating system|
# | tz | time zone |
# | r | URL the user come from |
# | u | URL where the user headed to |
# | t | Timestamp when the user start using the website in UNIX format |
# | hc | Timestamp when user exit the website in UNIX format |
# | cy | City from which the request intiated |
# | ll | Longitude and Latitude |

# In the cell, I tried to provide some helper code for better understanding and clearer vision
# 
# -**HINT**- Those lines of code may be not helping at all with your task.

# In[30]:


import json 
import pandas as pd

records = [json.loads(line) for line in open('usa.gov_click_data.json')]
records_df = pd.DataFrame(records)
records_df.head()


# In[31]:


records_df = records_df[['a', 'r', 'u', 'cy', 'll', 'tz', 't', 'hc']]
records_df.shape


# In[32]:


records_df.isna().sum()


# In[33]:


records_df = records_df.dropna()


# In[34]:


records_df.isna().sum()


# In[35]:


def extract_os(a):
    a = str(a)
    from_i = a.find('(')
    if from_i == -1:
        return ''
    to_i = a.find(';', from_i)
    if to_i == -1:
        to_i = a.find(')', from_i)
    #print(to_i)
    os = a[from_i+1:to_i]
    return os



def Make_URL_Short(URL):
    URL = str(URL)
    from_i = URL.find('/')
    if from_i == -1:
        return URL
    to_i = URL.find('/', from_i+2)
    short_url = URL[from_i+2:to_i]
    return short_url


# In[36]:


Make_URL_Short('http://www.ncbi.nlm.nih.gov/pubmed/22415991	')


# In[37]:


#records_df.insert(0, 'web_browser', records_df['a'].apply(lambda x : str(x).split(' ')[0]))
#records_df.insert(1, 'operating_system', records_df['a'].apply(extract_os))

records_df['web_browser'] = records_df['a'].apply(lambda x : str(x).split(' ')[0])
records_df['operating_system'] = records_df['a'].apply(extract_os)

#records_df.drop(['a'], axis=1, inplace=True)

records_df['r'] = records_df['r'].apply(Make_URL_Short)
records_df['u'] = records_df['u'].apply(Make_URL_Short)
records_df.sample(5)


# In[38]:


def extract_longitude(ll):
    ll = ll.split(',')
    if len(ll)>0:
        return ll[0][1:]
    else:
        return ''

def extract_latitude(ll):
    ll = ll.split(',')
    if len(ll)>1:
        return ll[1][1:-1]
    else:
        return ''


# In[39]:


#records_df.fillna('', inplace=True)
#records_df['longitude'] = records_df['ll'].astype(str).apply(extract_longitude)
#records_df['latitude'] = records_df['ll'].astype(str).apply(extract_latitude)

records_df['longitude'] = records_df['ll'].astype(str).apply(lambda x : x.split(',')[0][1:] if x!='' else '')
records_df['latitude'] = records_df['ll'].astype(str).apply(lambda x : x.split(',')[1][1:-1] if x!='' else '')


# In[40]:


records_df['t'] = pd.to_datetime(records_df['t'], unit='s') 
records_df['hc'] = pd.to_datetime(records_df['hc'], unit='s') 


# In[41]:


import numpy as np
np.max(records_df['hc'] - records_df['t'])


# In[42]:


records_df.drop(['ll'], axis=1, inplace=True)
records_df.rename(columns={'r':'from_url', 'u':'to_url', 'cy':'city', 'tz':'time_zone', 't':'time_out', 'hc':'time_in'}, inplace=True)
records_df.sample(10)


# In[43]:


records_df.rename(columns={'r':'from_url', 'u':'to_url', 'cy':'city', 'tz':'time_zone', 't':'time_in', 'hc':'time_out'}, inplace=True)


# In[44]:


records_df.drop(['a'], axis=1, inplace=True)
records_df.head()


# In[45]:


records_df.to_csv('usa.gov_click_data_clean.csv', index=False)


# ## Required

# Write a script can transform the JSON files to a DataFrame and commit each file to a sparete CSV file in the target directory and consider the following:
# 
#         

# All CSV files must have the following columns
# - web_browser
#         The web browser that has requested the service
# - operating_sys
#         operating system that intiated this request
# - from_url
# 
#         The main URL the user came from
# 
#     **note**:
# 
#     If the retrived URL was in a long format `http://www.facebook.com/l/7AQEFzjSi/1.usa.gov/wfLQtf`
# 
#      make it appear in the file in a short format like this `www.facebook.com`
#      
#     
# - to_url
# 
#        The same applied like `to_url`
#    
# - city
# 
#         The city from which the the request was sent
#     
# - longitude
# 
#         The longitude where the request was sent
# - latitude
# 
#         The latitude where the request was sent
# 
# - time_zone
#         
#         The time zone that the city follow
#         
# - time_in
# 
#         Time when the request started
# - time_out
#         
#         Time when the request is ended
#         
#         
# **NOTE** :
# 
# Because that some instances of the file are incomplete, you may encouter some NaN values in your transforamtion. Make sure that the final dataframes have no NaNs at all.

# In[ ]:




