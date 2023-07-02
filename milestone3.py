import time
import csv
from selenium import webdriver
import nltk
from nltk.corpus import wordnet
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from telnetlib import EC
from selenium.webdriver.support.ui import WebDriverWait



# websites to get content form
websiteLinks=[
    'wikipedia.org',
    'stackexchange.com',
    'tumblr.com',
    'slate.com',
    'instagram.com',
    'thedailybeast.com',
    'huffpost.com',
    'bbc.com',
    'steemit.com',
    'techcrunch.com',
    'reddit.com'
]

# Content paraphrasing and spining function
def paraphrase_text(text, paraphrase_ratio=0.9):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)

    paraphrased_text = []
    words_spun = 0

    for word, pos in pos_tags:
        synonyms = []
        if pos.startswith('NN'):
            synonyms = wordnet.synsets(word, pos=wordnet.NOUN)
        elif pos.startswith('VB'):
            synonyms = wordnet.synsets(word, pos=wordnet.VERB)
        elif pos.startswith('JJ'):
            synonyms = wordnet.synsets(word, pos=wordnet.ADJ)
        elif pos.startswith('RB'):
            synonyms = wordnet.synsets(word, pos=wordnet.ADV)

        if synonyms:
            paraphrased_words = [syn.lemmas()[0].name() for syn in synonyms]
            num_paraphrases = max(1, min(round(len(paraphrased_words) * paraphrase_ratio), len(paraphrased_words)))
            paraphrased_words = random.sample(paraphrased_words, num_paraphrases)
            paraphrased_word = random.choice(paraphrased_words)
            paraphrased_text.append(paraphrased_word)
        else:
            paraphrased_text.append(word)

    return ' '.join(paraphrased_text)

def spin_large_text(original_text, target_word_count, paraphrase_ratio=0.9):
    spun_text = ''
    words_spun = 0

    while words_spun < target_word_count:
        remaining_words = target_word_count - words_spun
        text_to_spin = original_text if words_spun == 0 else spun_text
        paraphrased_text = paraphrase_text(text_to_spin, paraphrase_ratio)
        paraphrased_words = paraphrased_text.split()
        words_to_append = min(remaining_words, len(paraphrased_words))
        spun_text += ' '.join(paraphrased_words[:words_to_append]) + ' '
        words_spun += words_to_append

    return spun_text.strip()



website_content=[]

def wikipedia(search_query):

    driver.get(f'https://en.wikipedia.org/wiki/{search_query}')
    time.sleep(5)

    try:
        content_element = driver.find_element(By.XPATH, '//div[@class="mw-content-container"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(5)
        try:
            image_element = driver.find_element(By.XPATH, '//a[@class="image"]/img')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text=spin_large_text(content,750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")


def stackexchange(search_query):

    driver.get(f'https://stackexchange.com/search?q={search_query}')
    time.sleep(5)

    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="result-link"]')
        find_span=find_first_link.find_element(By.XPATH, './/span]')
        find_article_link =find_span.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//div[@class="inner-content clearfix"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        featured_image_url = "No featured image found"
        spun_text=spin_large_text(content,750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")


def slate(search_query):
    driver.get(f'https://slate.com/search?q={search_query}')
    time.sleep(5)

    try:

        find_first_link=driver.find_element(By.XPATH, '//div[@class="gs-title"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//div[@class="main l-container"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="lazyloaded"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"

        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")


def thedailybeast(search_query):
    driver.get(f'https://www.thedailybeast.com/search?q={search_query}')
    time.sleep(5)

    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="SearchPageArticleCard__content-wrapper"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a[@class="SearchPageArticleCard__link"]')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//div[@class="StorySidebarWrapper__content"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//picture/img')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()

    except:
        print("No content found")



def huffpost(search_query):
    driver.get(f'https://www.huffpost.com/topic/search?q={search_query}')
    time.sleep(5)

    try:

        find_first_link = driver.find_element(By.XPATH, '//div[@class="card__headlines"]')
        find_article_link = find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//div[@class="entry__content-list js-entry-content js-cet-subunit"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="img-sized__img landscape"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()

    except:
        print("No content found")


def BBC(search_query):
    driver.get(f'https://www.bbc.com/search?q={search_query}')
    time.sleep(5)

    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="ssrcss-1f3bvyz-Stack e1y4nx260"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH,
                                              '//div[@class="ssrcss-1o6nrwy-ContainerWithSidebarWrapper e1jl38b40"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="p_holding_image"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()

    except:
        print("No content found")


def steemit(search_query):
    driver.get(f'https://www.steemit.com/search?q={search_query}')
    time.sleep(5)

    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="articles__content-block articles__content-block--text"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH,
                                              '//div[@class="ssrcss-1o6nrwy-ContainerWithSidebarWrapper e1jl38b40"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="p_holding_image"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()

    except:
        print("No content found")


def techcrunch(search_query):
    driver.get(f'https://search.techcrunch.com/search;_ylc=-?p={search_query}&fr=techcrunch')
    time.sleep(5)
    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="d-tc"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//article[@class="article-container article--post"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH,
                                                '//img[@class="article_featured-image article_featured-image--block"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")


def reddit(search_query):
    driver.get(f'https://www.reddit.com/search/?q={search_query}')
    time.sleep(5)

    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="t3_13nr8ip nbO8VWsMIB-Mv-tIa37NF"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="uI_hDmU5GSiudtABRz_37 "]')))
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="_1dwExqTGJH2jnA-MYGkEL-"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")


def tmblr(search_query):

    driver.get(f'https://www.tumblr.com/search/{search_query}')
    time.sleep(5)
    try:
        content_element = driver.find_element(By.XPATH, '//div[@class="Qb2zX"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="RoN4R tPU70 xhGbM"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")



def dailymail(search_query):
    driver.get(f'https://www.dailymail.co.uk/home/search.html?offset=0&size=50&sel=site&searchPhrase={search_query}')
    time.sleep(5)
    try:
        find_first_link=driver.find_element(By.XPATH, '//div[@class="sch-res-title"]')
        find_article_link =find_first_link.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//article[@class="article-text wide  heading-tag-switch"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH,
                                                '//img[@id="i-69f1baa06b2f430d"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")



def theguardian(search_query):
    driver.get(f'https://www.theguardian.com/international/{search_query}')
    time.sleep(5)

    try:

        find_first_link=driver.find_element(By.XPATH, '//a[@class="u-faux-block-link__overlay js-headline-text"]')
        get_article_link=find_first_link.get_attribute('href')

        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//div[@class="dcr-re5y45"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            image_element = driver.find_element(By.XPATH,
                                                '//img[@class="dcr-my5zgw"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")


def asahi(search_query):
    driver.get(f'https://www.asahi.com/ajw/search/results/?keywords={search_query}')
    time.sleep(5)

    try:
        find_first_link = driver.find_element(By.XPATH, '//ul[@class="ListBlock"]')
        find_article_li = find_first_link.find_element(By.XPATH, './/li')
        find_article_link = find_article_li.find_element(By.XPATH, './/a')
        get_article_link = find_article_link.get_attribute('href')
        time.sleep(2)
        driver.get(get_article_link)
        time.sleep(2)

        content_element = driver.find_element(By.XPATH, '//div[@id="MainInner"]')
        content = content_element.text
        words = content.split()
        if len(words) > 750:
            content = ' '.join(words[:750])
        time.sleep(3)
        try:
            find_image_element = driver.find_element(By.XPATH,
                                                '//div[@class="Image"]')
            find_image_p=find_image_element.find_element(By.XPATH, './/p')
            image_element=find_image_p.find_element(By.XPATH, './/img')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url = "No featured image found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)
        driver.back()
    except:
        print("No content found")

def indiaTimes(search_query):
    driver.get(f'https://www.indiatimes.com/explainers/news/{search_query}-604975.html')
    time.sleep(5)


    content_element = driver.find_element(By.XPATH, '//div[@id="article-description-0"]')
    content = content_element.text
    words = content.split()
    if len(words) > 750:
        content = ' '.join(words[:750])
    time.sleep(3)
    try:
        find_image_element = driver.find_element(By.XPATH,
                                                 '//div[@class="article-image container"]')
        image_element = find_image_element.find_element(By.XPATH, './/img')
        featured_image_url = image_element.get_attribute('src')
    except:
        featured_image_url = "No featured image found"
    spun_text = spin_large_text(content, 750)
    website_content.append(spun_text)
    print(spun_text, "\n", featured_image_url)
    driver.back()


def google_search(search_query):
    driver.get(f'https://www.google.com/search?q={search_query}')
    time.sleep(5)

    try:
        content=driver.find_element(By.XPATH, '//div[@class="LGOjhe"]').text
        time.sleep(5)

        # Open Google Images Section
        driver.get(f'https://www.google.com/search?tbm=isch&q={search_query}')
        time.sleep(5)

        try:
            image_element = driver.find_element(By.XPATH, '//img[@class="rg_i Q4LuWd"]')
            featured_image_url = image_element.get_attribute('src')
        except:
            featured_image_url="No featured found"
        spun_text = spin_large_text(content, 750)
        website_content.append(spun_text)
        print(spun_text, "\n", featured_image_url)

    except:
        print("Element not found")


search_term ="renal diet"
def main_websearch_func():
    wikipedia(search_term)
    time.sleep(5)

    stackexchange(search_term)
    time.sleep(5)

    slate(search_term)
    time.sleep(5)

    thedailybeast(search_term)
    time.sleep(5)

    huffpost(search_term)
    time.sleep(5)

    BBC(search_term)
    time.sleep(5)

    steemit(search_term)
    time.sleep(5)

    techcrunch(search_term)
    time.sleep(5)

    reddit(search_term)
    time.sleep(5)

    tmblr(search_term)
    time.sleep(5)

    dailymail(search_term)
    time.sleep(5)

    theguardian(search_term)
    time.sleep(5)

    asahi(search_term)
    time.sleep(5)

    indiaTimes(search_term)
    time.sleep(5)

    google_search(search_term)

    print(website_content)




def get_random_user_agent():
    # Replace this with your own method of getting a random user-agent
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

# Setting up proxies
proxy_list = [
    {'ip': '115.144.102.39', 'port': 10080, 'protocol': 'HTTP'},
    {'ip': '186.121.235.66', 'port': 8080, 'protocol': 'HTTP'},
    {'ip': '46.101.13.77', 'port': 80, 'protocol': 'HTTP'},
    {'ip': '202.40.177.69', 'port': 80, 'protocol': 'HTTP'},
    {'ip': '185.74.7.50', 'port': 3128, 'protocol': 'HTTP'},
    {'ip': '81.12.44.197', 'port': 3129, 'protocol': 'HTTP'},
    {'ip': '5.189.184.6', 'port': 80, 'protocol': 'HTTP'},
]

# Shuffle the proxy list
random.shuffle(proxy_list)

option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option('useAutomationExtension', False)
option.add_argument('--disable-blink-features=AutomationControlled')
# option.add_argument("--headless")

# Open the CSV file in read mode
with open('trends.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)

    for row in reader:
        trend_title = row[2]

        user_agent = get_random_user_agent()
        headers = {'User-Agent': user_agent}

        driver = webdriver.Chrome(executable_path="chromedriver.exe", options=option)

        search_query = f'{trend_title}'
        driver.get(f'https://www.google.com/search?q={search_query}')

        page_count = 1

        # Open the CSV file in append mode for each iteration
        with open('search_results.csv', 'a', newline='', encoding='utf-8') as resultfile:
            writer = csv.writer(resultfile)

            # Write the header row if the file is empty
            if resultfile.tell() == 0:
                writer.writerow(['Search Query', 'Featured Image URL', 'Body copy(spun)','Website URL'])

            while page_count <= 10:
                # Scroll to the height
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

                search_results = driver.find_elements(By.XPATH, '//div[@class="yuRUbf"]')

                # Process each search result
                for result in search_results:
                    try:
                        url_element = result.find_element(By.XPATH, './/a')
                        url = url_element.get_attribute('href')
                        for link in websiteLinks:
                            if link in url:
                                print("Website link found for:", trend_title)
                                print(url)
                                get_spun_text, get_img_url = html_Structure(link, url)

                                # Write the search result to the result CSV file
                                writer.writerow([trend_title, get_img_url, get_spun_text,url])
                                break

                    except:
                        continue

                try:
                    # Go to the next page of search results
                    next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Next")]')
                    next_button.click()


                except:
                    try:
                        more_result_button = driver.find_element(By.XPATH, '//span[contains(text(), "More Results")]')
                        more_result_button.click()


                    except:
                        print("No More Results")
                        time.sleep(5)
                        break

                # Wait for the next page to load
                time.sleep(5)

            driver.quit()
            time.sleep(120)