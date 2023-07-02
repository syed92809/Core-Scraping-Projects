import csv
import time
import datetime
import os
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random
from selenium.webdriver.common.by import By
from itertools import cycle
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
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

    # # Get a random proxy from the proxy_pool
    # proxy = next(proxy_pool)
    # print(proxy)
    # if proxy['protocol'] == 'HTTP':
    #     options.add_argument(f'--proxy-server=http://{proxy["ip"]}:{proxy["port"]}')
    # elif proxy['protocol'] == 'HTTPS':
    #     options.add_argument(f'--proxy-server=https://{proxy["ip"]}:{proxy["port"]}')

    if os.name == "nt":
        return webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    elif os.name == "posix":
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver = get_driver()


# todays date function
def get_todays_date():
    today = datetime.date.today()
    return today

# setting up different credentials for login
def login_credentials():
    emails = ['markematics13@gmail.com']
    password = ['Saqib@123']

    login_email = random.choice(emails)
    login_password = password

    return login_email, login_password


# login function
def login_code():
    driver.get('https://www.linkedin.com/?trk=seo-authwall-base_nav-header-logo')
    time.sleep(5)
    find_input_email = driver.find_element(By.XPATH, "//input[@name='session_key']")
    find_input_password = driver.find_element(By.XPATH, "//input[@name='session_password']")

    find_input_email.clear()
    find_input_password.clear()

    # calling credentials function
    email, password = login_credentials()

    find_input_email.send_keys(email)
    find_input_password.send_keys(password)
    time.sleep(3)

    # clicking on login button
    click_login = driver.find_element(By.XPATH, "//button[@type='submit']")
    time.sleep(1)
    click_login.click()
    time.sleep(20)


# company profile page function
def scraping_company_details_code():
    # Open companies CSV file in read mode
    with open('LinkedIn Companies for Scraping.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            company_name = row[0]
            company_url = row[1]
            headcounts_array = []
            headcounts_columns=[]


            # Creating a directory for the company if it doesn't exist
            company_directory = f'{company_name}_data'
            os.makedirs(company_directory, exist_ok=True)

            # Open the CSV file in write mode for each company
            csv_file_path = os.path.join(company_directory, f'{company_name}_headcounts_data.csv')
            with open(csv_file_path, 'w', newline='', encoding='utf-8') as resultfile:
                writer = csv.writer(resultfile)

                # opening company profile page
                driver.get(f'{company_url}/people/')
                time.sleep(2)

                driver.execute_script("window.scrollBy(0,750);")
                time.sleep(5)

                # clicking on next button
                time.sleep(5)
                next_button = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Page 2']")))
                time.sleep(2)
                next_button.click()

                time.sleep(5)

                # gettig source code of company's profile page
                page_source = driver.page_source

                soup = BeautifulSoup(page_source, 'html.parser')

                # find ul of headcounts container
                ul = soup.find('ul', class_='artdeco-carousel__slider ember-view')

                # finding li of ul container
                for li in ul.find_all('li'):
                    print("--=====================")
                    # print(city.find_all('div', {'class' : 'insight-container'}))
                    detail_box = li.find_all('div', {'class': 'insight-container'})

                    for d2 in detail_box:
                        headcounts_array.append(d2.text)
                # appending relevant columns to an array
                headcounts_columns.append(headcounts_array[0])
                headcounts_columns.append(headcounts_array[2])

                # filtering the above array so that it only contains relevant information
                filtered_array = []
                for value in headcounts_columns:
                    cleaned_values = [v.strip() for v in value.split('\n') if
                                      v.strip() not in ['What they do', 'Where they live', 'Add', 'toggle off']]
                    cleaned_values = list(filter(None, cleaned_values))  # Remove empty elements
                    filtered_array.append(cleaned_values)

                # Removing null indexes from an array after filtering it
                filtered_array = [arr for arr in filtered_array if any(arr)]

                # separating counts and their headings
                counts_array = []
                headings_array = []

                # removing spaces and commas from countries and replacing them with underscore( _ )
                for sublist in filtered_array:
                    counts = []
                    headings = []
                    for item in sublist:
                        count = int(item.split()[0])
                        heading = '_'.join(item.split()[1:]).replace(',', '_').replace(' ', '_')
                        counts.append(count)
                        headings.append(heading)
                    counts_array.append(counts)
                    headings_array.append(headings)

                print(company_url)
                print(counts_array)

                print(headings_array)

                # saving data into csv file for each company
                Date = get_todays_date()

                # Write the header row
                writer.writerow(['Date', 'Company URL'] + headings_array[0] + headings_array[1])

                # Write the data rows
                writer.writerow([Date, company_url] + counts_array[0] + counts_array[1])

                # clearing headcounts array to remove previous companies data
                headcounts_columns.clear()


            # Find show more button
            # find_showmore_button = driver.find_element(By.XPATH,
            #                                            '//button[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]')
            # find_showmore_button.click()
            # time.sleep(2)

            # Scraping headcounts code starts here

            # # Creating a directory for the company if it doesn't exist
            # company_directory = f'{company_name}_data'
            # os.makedirs(company_directory, exist_ok=True)
            #
            # # Open the CSV file in write mode for each company
            # csv_file_path = os.path.join(company_directory, f'{company_name}_headcounts_data.csv')
            # with open(csv_file_path, 'w', newline='', encoding='utf-8') as resultfile:
            #     writer = csv.writer(resultfile)
            #
            #     # Scraping "where they live" column
            #     headcount_containers = driver.find_elements(By.XPATH, '//div[@class="insight-container"]')
            #     print(headcount_containers)
            #
            #     # Extracting individual headcounts and removing "toggle off" and "Add" lines
            #     where_headcounts = [count.replace('toggle off', '').replace('Add', '').strip() for count in
            #                         headcount_containers[0].text.split('\n') if count.strip()]
            #     # print(where_headcounts)
            #     # Extracting the headings and removing any empty headings
            #     where_headings = [heading.strip() for heading in where_headcounts[2::2] if heading.strip()]
            #
            #     # separating individual counts and their headings
            #     counts_array=[]
            #     headings_array=[]
            #
            #     for items in where_headings:
            #         count,heading =items.split(' ',1)
            #         counts_array.append(count)
            #         headings_array.append(heading)
            #
            #     # calling date function here
            #     Date = get_todays_date()
            #
            #     # Write the header row
            #     writer.writerow(['Date', 'Company URL'] + headings_array)
            #
            #     # Write the data rows
            #     writer.writerow([Date, company_url] + counts_array)
            #
            #     counts_array.clear()
            #     headings_array.clear()
            #
            #     time.sleep(5)
            #     # Clicking on the next button
            #     next_button = WebDriverWait(driver, 20).until(
            #         EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Next']")))
            #     time.sleep(2)
            #     next_button.click()

                # # Scraping "what they do" column
                # headcount_containers = driver.find_elements(By.XPATH, '//div[@class="insight-container"]')
                #
                # what_headcounts = [count.replace('toggle off', '').replace('Add', '').strip() for count in
                #                    headcount_containers[2].text.split('\n') if count.strip()]
                # print(what_headcounts)
                #
                # what_headings = [heading.strip() for heading in what_headcounts[2::2] if heading.strip()]
                #
                # # separating individual counts and their headings
                # counts_array = []
                # headings_array = []
                #
                # for items in what_headings:
                #     count, heading = items.split(' ', 1)
                #     counts_array.append(count)
                #     headings_array.append(heading)
                #
                # # calling date function here
                # Date = get_todays_date()
                #
                # # Write the header row
                # writer.writerow(['Date', 'Company URL'] + headings_array)
                #
                # # Write the data rows
                # writer.writerow([Date, company_url] + counts_array)
                #
                # counts_array.clear()
                # headings_array.clear()


def get_todays_date():
    today = datetime.date.today()
    return today


# main scraper function
def core_scraper():
    # calling login function here
    login_code()
    time.sleep(2)

    # calling company details function
    scraping_company_details_code()
    time.sleep(2)


    # Quit the driver
    driver.quit()



# calling core scraper function here
core_scraper()


