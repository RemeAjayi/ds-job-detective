#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 20:20:47 2021
Credit: 
@author: olohireme
"""
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#specify driver path
DRIVER_PATH = '/opt/homebrew/bin/chromedriver'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)

driver.get('https://ca.indeed.com/jobs?l=Canada')

advanced_search = driver.find_element_by_xpath("//a[contains(text(),'Advanced Job Search')]")
advanced_search.click()

#search data science 
search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
search_job.send_keys(['data science'])
#set display limit of 30 results per page
display_limit = driver.find_element_by_xpath('//select[@id="limit"]//option[@value="50"]')
display_limit.click()
#sort by date
sort_option = driver.find_element_by_xpath('//select[@id="sort"]//option[@value="date"]')
sort_option.click()
search_button = driver.find_element_by_xpath('//*[@id="fj"]')
search_button.click()

close_popup = driver.find_element_by_xpath('//div[@id="popover-x"]/button')
close_popup.click()
#select only English jobs
lang_div = driver.find_element_by_xpath('//*[@id="filter-language"]/button')
lang_div.click()
filter_lang = driver.find_element_by_xpath('//ul[@id="filter-language-menu"]/li[1]')
filter_lang.click()

driver.implicitly_wait(3) 


links =[]
descriptions=[]
jobs = []


for i in range(0,11):
    
    job_card = driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')
    
    for job in job_card:
       
    #.  not all companies have review
        try:
            review = job.find_element_by_xpath('.//span[@class="ratingsContent"]').text
        except:
            review = "None"
   #.   not all positions have salary
        try:
            salary = job.find_element_by_xpath('.//span[@class="salaryText"]').text
        except:
            salary = "None"
    #.  tells only to look at the element       
        
        try:
            location = job.find_element_by_xpath('.//span[contains(@class,"location")]').text
        except:
            location = "None"
    #.  tells only to look at the element       
        
        try:
            title  = job.find_element_by_xpath('.//h2[@class="title"]//a').text
        except:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
        
        link = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
        company = job.find_element_by_xpath('.//span[@class="company"]').text
        
        jobs.append({"Job Title" : title,
            "Salary Estimate" : salary,
            "Job Description":link,
            "Review" : review,
            "Company Name" : company,
            "Location" : location
            })
    
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label={}]//span[@class="pn"]'.format(i+2))
        next_page.click()

    except:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
        next_page.click()
 
    print("Page: {}".format(str(i+2)))

descriptions=[]
for job in jobs:
    driver.get(job["Job Description"])
    jd = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    descriptions.append(jd)
    job["Job Description"] = jd


df_da=pd.DataFrame(jobs)

df_da.to_csv('indeed.csv')
    

