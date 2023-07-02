import time
import csv
from selenium import webdriver
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

#headers fucntion
def get_random_user_agent():
    # setting up headers fucntion
    user_agent_list = [
        'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',

    ]
    return random.choice(user_agent_list)

try:

    # categories symbols
    def categoriesFF(symbol):
        if symbol == "b":
            category_name = "Business"
        elif symbol == "e":
            category_name = "Entertainment"
        elif symbol == "m":
            category_name = "Health"
        elif symbol == "t":
            category_name = "Sci/Tech"
        elif symbol == "s":
            category_name = "Sports"
        elif symbol == "h":
            category_name = "Top stories"

        return category_name


    # setting up proxies
    proxy_list = [
        {'ip': '115.144.102.39', 'port': 10080, 'protocol': 'HTTP'},
        # {'ip': '186.121.235.66', 'port': 8080, 'protocol': 'HTTP'},
        {'ip': '46.101.13.77', 'port': 80, 'protocol': 'HTTP'},
        {'ip': '202.40.177.69', 'port': 80, 'protocol': 'HTTP'},
        {'ip': '185.74.7.50', 'port': 3128, 'protocol': 'HTTP'},
        {'ip': '81.12.44.197', 'port': 3129, 'protocol': 'HTTP'},
        {'ip': '5.189.184.6', 'port': 80, 'protocol': 'HTTP'},
    ]

    # Shuffle the proxy list
    random.shuffle(proxy_list)
    option = webdriver.ChromeOptions()

    # Removes navigator.webdriver flag

    # For older ChromeDriver under version 79.0.3945.16
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    # For ChromeDriver version 79.0.3945.16 or over
    option.add_argument('--disable-blink-features=AutomationControlled')

    # Define a list of countries and categories
    countries = ['US', 'AR', 'AU', 'AT', 'BE', 'BR', 'CA', 'CL', 'CO', 'CZ', 'DK', 'EG', 'FI', 'FR', 'IN', 'IE',
                 'IT', 'MY', 'MX',
                 'NZ', 'PE', 'PH', 'PL', 'PT', 'ES', 'VN']

    categories = ['m', 'b', 'e', 't', 's', 'h']

    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    # option.add_argument("--headless")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")

    # Open the CSV file in write mode
    with open('trends.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Country', 'Category', 'Trend Title'])

        # Loop through countries and categories
        while True:

            for country in countries:
                for category in categories:
                    # Get a random user-agent header for each request
                    user_agent = get_random_user_agent()

                    # Set headers for requests
                    headers = {
                        'User-Agent': user_agent
                    }

                    # Create a new WebDriver instance
                    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=option)

                    try:
                        time.sleep(3)
                        driver.get(
                            f'https://trends.google.com/trends/trendingsearches/realtime?geo={country}&hl=en-US&category={category}')
                        accept_cookies = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//a[@class="cookieBarButton cookieBarConsentButton"]')))

                        if accept_cookies.is_displayed():
                            accept_cookies.click()

                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                        time.sleep(2)
                        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

                        while True:
                            try:
                                # check if Load More button is visible
                                load_more_button = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.XPATH, '//div[@class="feed-load-more-button"]')))
                                if load_more_button.is_displayed():
                                    load_more_button.click()
                                else:
                                    break
                            except TimeoutException:
                                break

                        find_trends_element = driver.find_elements(By.XPATH,
                                                                   '//div[@class="feed-item contracted-item"]')
                        print(len(find_trends_element))

                        for element in find_trends_element:
                            trend_title = element.find_element(By.XPATH, './/div[@class="title"]').text
                            trend_title = trend_title.replace('•', '')
                            print(trend_title, "\n")

                            # checking if title already exists in csv file
                            with open('trends.csv', 'r', encoding='utf-8') as file:
                                reader = csv.reader(file)
                                found = False
                                for row in reader:
                                    if trend_title in row:
                                        found = True
                                        break

                                if not found:
                                    get_category_name = categoriesFF(category)
                                    writer.writerow([country, get_category_name, trend_title])  # Write the row to CSV

                    finally:
                        driver.quit()
                        time.sleep(30)

except Exception as e:
    print(e)
