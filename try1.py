# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 00:39:57 2020

@author: yajat
"""

import smtplib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
from pathlib import Path
#import pandas as pd

chrome_options=Options()
chrome_options.add_argument("--headless")

date1='July 16, 2020' # start date of consideration
date2='July 17, 2020' # end date of consideration

email_text='' # initialization of email text

# creating array of dates in the target range
dates = []
tdel = datetime.datetime.strptime(date2,'%B %d, %Y')-datetime.datetime.strptime(date1,'%B %d, %Y')
tdelta = tdel.days 

for i in range(tdelta+1):
    day = datetime.datetime.strptime(date1,'%B %d, %Y')+timedelta(days = i)
    dates.append(day.strftime('%B %d, %Y').lstrip("0").replace(" 0", " ")) 
    # gotta replace 08 July to 8 July and so on for comparison with national parks websites
    
# the xpath of clicking the calender button
month_dropdown='//*[@id="page-body"]/div[2]/div/div/div[2]/div[1]/section/div/div[2]/div[1]/div/div/div[1]/button[1]'

# 2 separate driver windows for 2 campgrounds @ Glacier
driver1 = webdriver.Chrome("C:\\Users\yajat\Documents\courses\python3essentialLiL\WebScraping\chromedriver.exe",
                           options=chrome_options)
driver1.get("https://www.recreation.gov/camping/campgrounds/232493") # Fish creek campsite
driver1.find_element_by_xpath(month_dropdown).click()
soup1 = BeautifulSoup(driver1.page_source,features="lxml")
driver1.quit()

driver2 = webdriver.Chrome("C:\\Users\yajat\Documents\courses\python3essentialLiL\WebScraping\chromedriver.exe", 
                           options=chrome_options)
driver2.get("https://www.recreation.gov/camping/campgrounds/232492") # St. Mary campsite
driver2.find_element_by_xpath(month_dropdown).click()
soup2 = BeautifulSoup(driver2.page_source,features="lxml")
driver2.quit()

# comparing each date with avialability to each date in the target range, updating the email text likewise
for dats in dates:
    for tdd in soup2.findAll('td', {'aria-disabled':'false'}):
        if tdd["aria-label"].find(dats)>0:
            email_text+='Availability on '+dats+' at St. Mary\n'
    for td in soup1.findAll('td', {'aria-disabled':'false'}):
        if td["aria-label"].find(dats)>0:
            email_text+='Availability on '+dats+' at Fish Creek\n'
            
# finally sending the email to thy self
if email_text:
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
    
        smtp.login('YOUR_EMAIL_HERE','YOUR_PASSWORD_HERE')
    
        subject = 'Campsite availability for your trip, nigga'
        msg = f'Subject: {subject}\n\n{email_text}'
    
        smtp.sendmail('YOUR_EMAIL_HERE', 'YOUR_EMAIL_HERE', msg)

f = open(Path("C:\\Users\yajat\Documents\courses\python3essentialLiL\WebScraping") / "try1_log.txt",'a')
f.write(datetime.datetime.now().strftime('On %B %d, at %Y %H:%M:%S')+'\n')
f.close() 


