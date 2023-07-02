import os
import re
import string
import time, urllib.request
import pandas as pd
import selenium.common
import tldextract
import csv
import postgrest
import supabase
from selenium import webdriver
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from selenium.common.exceptions import WebDriverException
from itertools import cycle
from geopy.geocoders import Nominatim
from dateutil import parser
from mtranslate import translate
from datetime import datetime, timedelta
from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import Chrome, ChromeOptions


# Function to get random user-agent header
def get_random_user_agent():
    # Replace this with your own method of getting a random user-agent
    # This is just a placeholder implementation
    user_agent_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36'

    ]
    return user_agent_list[0]

def get_proxies():
    proxy_list = [

        {'ip': '101.229.217.60', 'port': 8111, 'protocol': 'HTTPS'},
        {'ip': '102.165.51.172', 'port': 3128, 'protocol': 'HTTPS'},
        {'ip': '103.111.118.68', 'port': 8080, 'protocol': 'HTTP'},
        {'ip': '103.199.139.174', 'port': 80, 'protocol': 'HTTPS'},

    ]
    return proxy_list


proxy_pool = cycle(get_proxies())
header_pool = cycle(get_random_user_agent())


def get_driver():
    import os
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    # Get a random user-agent from the header_pool
    user_agent = next(header_pool)

    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument(f'user-agent={user_agent}')

    # Get a proxy from the proxy_pool
    # proxy = next(proxy_pool)
    # options.add_argument(f'--proxy-server={proxy["protocol"].lower()}://{proxy["ip"]}:{proxy["port"]}')

    if os.name == "nt":
        return webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    elif os.name == "posix":
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver = get_driver()

# setting up different credentials for login
def login_crdentials():
    emails = [  'syed92809@gmail.com'  ]
    password = ['faizan..12']

    login_email = random.choice(emails)
    login_password = random.choice(password)

    return login_email, login_password
# credentials function ends here


# login function
def login_code():
    driver.get('https://www.linkedin.com/?trk=seo-authwall-base_nav-header-logo')
    time.sleep(5)

    find_input_email = WebDriverWait(driver,10).until (EC.visibility_of_element_located((By.XPATH,
                                           "//input[@class='text-color-text font-sans text-md outline-0 bg-color-transparent grow']")))
    find_input_password = driver.find_element(By.XPATH, "//input[@name='session_password']")

    find_input_email.clear()
    find_input_password.clear()

    # calling credentials function
    email,password=login_crdentials()

    find_input_email.send_keys(email)
    find_input_password.send_keys(password)
    time.sleep(3)

    # clicking on login button
    click_login = driver.find_element(By.XPATH, "//button[@type='submit']")
    time.sleep(1)
    click_login.click()
    time.sleep(5)
# login function ends here


# company profile page fucntion
def companies_profile_code():


    driver.get('https://www.linkedin.com/company/bright-data/people/')
    driver.execute_script("window.scrollBy(0,500);")
    time.sleep(3)

    #find show more button
    find_showmore_button = driver.find_element(By.XPATH,'//button[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]')
    find_showmore_button.click()
    time.sleep(2)
# companies profile fucntion ends here


#scraping company details fucntion
def company_details_code():

    # getting insights
    time.sleep(3)
    find_element=WebDriverWait(driver,10).until(EC.visibility_of_element_located((
        By.XPATH('//div[@class="artdeco-carousel__content"]'))))
    get_data = find_element.text
    print(get_data)



# main scraper function
def core_scraper():


    #calling login function here
    login_code()
    time.sleep(2)

    #opening companies profile page
    companies_profile_code()
    time.sleep(2)

    #calling company details function
    company_details_code()


# core scraper function ends here


# calling core scraper function here
core_scraper()
