#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 20:47:42 2021

Credit: Kenarapfaik
@author: Olohireme
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd

path = '/opt/homebrew/bin/chromedriver'

def get_jobs(keyword, num_jobs, verbose):
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()

    
    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    
    url = 'https://www.glassdoor.ca/Job/canada-data-scientist-jobs-SRCH_IL.0,6_IN3_KO7,21.htm'
    #url = 'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=&typedLocation=canada&locT=N&locId=3&jobType=&context=Jobs&sc.keyword=data+scientist&dropdown=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        
        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
        except NoSuchElementException:
            pass
        
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            print("here")
            
            try:
                job_button.click()  #You might 
            except:
                 try:
                     driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
                 except NoSuchElementException:
                     pass
                 
            time.sleep(1)
            #collected_successfully = False
            
            #while not collected_successfully:
            try:
                company_name = driver.find_element_by_xpath('.//div[@class="css-87uc0g e1tk4kwz1"]').text
                location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz5"]').text
                job_title = driver.find_element_by_xpath('.//div[@class= "css-1vg6q84 e1tk4kwz4"]').text
                job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').get_attribute("innerText")
       #         collected_successfully = True
            except:
                time.sleep(5)
            
          
            
            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Job Description: {}".format(job_description[:500]))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                
      
            
            jobs.append({"Job Title" : job_title,
            "Job Description" : job_description,
            "Company Name" : company_name,
            "Location" : location
            })
            
        print('should move to next page')    
        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="css-1yshuyv e1gri00l3"]//a').click()
            print('moved to next page')
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  

df = get_jobs('data scientist',1000, False)

df.to_csv('glassdoor_jobs.csv')