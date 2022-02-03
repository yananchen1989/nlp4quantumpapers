#!/usr/bin/env python
# coding: utf-8

# In[1]:


######################################
########## Library/Packages ##########
######################################

#!pip install feedparser

import pandas as pd
import urllib
import time
import feedparser


# In[2]:


######################################
########## Data Frame Prep  ##########
######################################

API_Output = pd.DataFrame(columns = ["URL", "Title", "Published", "Updated", "Author", "Abstract"])


# In[3]:


######################################
########## Calling from API ##########
######################################

# Base api query url
base_url = 'http://export.arxiv.org/api/query?';

# Search parameters
search_query = 'all:quantum%20computing'    # search for articles relating to quantum computing
start = 0                                   # start at the first result
total_results = 100                          # want # total results (suggested was 20)
results_per_iteration = 50                  # # of results at a time (suggested was 5)
wait_time = 3                               # number of seconds to wait beetween calls (suggested was 3)

print('Searching arXiv for: "%s" \n\n' % search_query)


#Looping Through Results
for i in range(start,total_results,results_per_iteration):    
    
    #Output Result #s
    print("Results %i - %i" % (i,i+results_per_iteration))
    
    #Query Term Using Inputs
    query = 'search_query=%s&start=%i&max_results=%i' % (search_query, i, results_per_iteration)
    
    #Request from ArXiv Using URL+Query to form request
    print('%s' % base_url+query)
    response = urllib.request.urlopen(base_url+query).read()
    
    #Parse the response using feedparser
    feed = feedparser.parse(response)

    # Run through each entry, and grab selected information
    for entry in feed.entries:
        API_Output = API_Output.append({"URL":entry.id,
                                        "Title":entry.title,
                                        "Published":entry.published[:10],
                                        "Updated":entry.updated[:10],
                                        "Author":entry.author, #Note: This is the FIRST Author only.
                                        "Abstract":entry.summary}, ignore_index=True)

    
    #Wait to re-call from API
    print('Wait %i Second(s)' % wait_time)
    time.sleep(wait_time)
    
# Exited For Loop
print("\n\nData Gathering Complete!")
display(API_Output.head(3))
display(API_Output.tail(3))

#Output into CSV
API_Output.to_csv('API_Output.csv',index=False)


# In[4]:





# In[ ]:



