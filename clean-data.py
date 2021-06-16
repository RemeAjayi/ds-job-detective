#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 20:16:43 2021

@author: olohireme
"""

import pandas as pd
import re

def split_province(x):
    sen = x.split(',')
    if len(sen) > 0:
        return sen[0]
    else:
        return x
    
def remove_rating(x):
    regex = re.compile('[-+]?[0-9]*\.[0-9]+$')
    if regex.search(x) is not None:
        return x[:-3]
    else:
        return x
        

df_1 = pd.read_csv('backups/indeed_2.csv', error_bad_lines=False)
df_2 = pd.read_csv('backups/indeed_1.csv')

#One is enough, but I ran the scraper on two  separate days in order to get new jobs
df_indeed = pd.concat([df_1, df_2], ignore_index=True, join="inner")

#remove all rows without Job Description
df_indeed = df_indeed[df_indeed["Job Description"] != "None"]
#only keep relevant columns
df_indeed = df_indeed[["Job Title","Company Name", "Job Description", "Location"]]
#remove duplicates, where Job Title and Company Name and Location are the same among rows
df_indeed = df_indeed.drop_duplicates(subset=['Job Title', 'Company Name', 'Location'], keep='first')

df_glass_1 = pd.read_csv('backups/glassdoor_1.csv')
df_glass_2 = pd.read_csv('backups/glassdoor_2.csv')
#One is enough, but I ran the scraper on two  separate days in order to get new jobs

df_glass = pd.concat([df_glass_1, df_glass_2],ignore_index=True, join="inner")
#remove redundant columns
df_glass = df_glass[["Job Title","Company Name", "Job Description", "Location"]]

#remove duplicates, where Job Title and Company Name and Location are the same among rows
df_glass = df_glass.drop_duplicates(subset=['Job Title', 'Company Name', 'Location'], keep='first')

#combine both df & and job board column
#Separate City & province
df_indeed["Location"] = df_indeed["Location"].apply(lambda x: split_province(x))
#use regex to remove rating from company name if rating exists
df_glass["Company Name"] = df_glass["Company Name"].apply(lambda x: remove_rating(x))
#Concat both dfs with Job Board Column
df_indeed["Job Board"] = "Indeed"
df_glass["Job Board"]= "Glassdoor"

df =  pd.concat([df_indeed, df_glass], ignore_index=True)
df = df.sample(frac = 1).reset_index(drop=True)
#run this only if you want to generate a dataset of jobs
#df.to_csv('outputs/data_science_jobs.csv')

