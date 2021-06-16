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
from time import sleep
import random

path = '/opt/homebrew/bin/chromedriver'

def get_jobs(keyword, num_jobs, verbose):
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    
    url = 'https://ca.indeed.com/jobs?l=Canada'
    driver.get(url)
    
    advanced_search = driver.find_element_by_xpath("//a[contains(text(),'Advanced Job Search')]")
    advanced_search.click()
    
    #search data science 
    search_job = driver.find_element_by_xpath('//input[@id="as_and"]')
    search_job.send_keys(['data scientist'])
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

    jobs = []


    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        
        #Going through each job in this page
        job_buttons =  driver.find_elements_by_xpath('//div[contains(@class,"clickcard")]')
        
        try:
            driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
        except NoSuchElementException:
            pass
        
        for job_button in job_buttons:  

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            print("here")
            
              #be random to avoid CAPTCHA
            if len(jobs) % 15 == 0:
                try:
                    link = job_button.find_element_by_xpath('.//span[@class="caption"]//a').get_attribute(name="href")
                except:
                    link = "None"
              
            if len(jobs) % 25 == 0:
                inputElement = driver.find_element_by_id("alertemail")
                inputElement.send_keys('1')
                try:
                    link = job_button.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href")
                except:
                    link = "None"
            
            try:
                job_button.click()  #You might 
            except:
                 try:
                     driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
                 except NoSuchElementException:
                     pass
                 
            sleepTimes = [2.1, 2.8, 3.2]
            sleep(random.choice(sleepTimes))
            #collected_successfully = False
            
            #while not collected_successfully:
            print("here")
            try:
                company_name = driver.find_element_by_xpath('.//span[@id="vjs-cn"]').text
                print(company_name)
                location = driver.find_element_by_xpath('.//span[@id="vjs-loc"]').text
                print(location)
                job_title = driver.find_element_by_xpath('.//div[@id="vjs-jobtitle"]').text
                print(job_title)
                job_description = driver.find_element_by_xpath('.//div[@id="vjs-desc"]').text
                print(job_description[:30])
               # collected_successfully = True
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
            
        #Clicking on the "next page" button
        try:  
            next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
            next_page.click()       
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  

df = get_jobs('data science', 500, False)

df.to_csv('glassdoor_jobs.csv')