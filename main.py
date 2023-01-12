import re
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def smooth_scroll(current_scroll_position = 0, iteration_multiplyer = 1):
    driver.execute_script("document.documentElement.style.setProperty('scroll-behavior', 'smooth');")    
    scroll_iteration = 60 #default 60
    for _ in range(int(scroll_iteration*iteration_multiplyer)):
        current_scroll_position += 100
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(0.1)
    return current_scroll_position

def export(data,name):
    df = pd.DataFrame(data)
    df.to_csv(f"output/{name}.csv", index=False, header=True)

def display(data):
    for item in data:
        print('========================')
        print(item[0])
        print(item[1])
        print()

def data_to_dictionary(data):
    data = [sublist[1] for sublist in data]
    data = ' '.join(data)
    data = re.split(r'[\s,.]', data)
    data = [x.lower() for x in data]
    data = list(set(data))
    data = sorted(data)
    export(data,'dictionary')
    return(data)

if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("detach", False)

    driver = webdriver.Chrome(options=options)
    driver.get("https://web.facebook.com/groups/306516256927109")

    try:
        data = []
        list_author = []
        print('loading...')
        time.sleep(2)
        current_scroll_position = 0
        feed = driver.find_elements(By.CSS_SELECTOR, "div[role='feed']")
        feed = feed[0]
        for _ in range(3):
            print('starting a new batch...')
            current_scroll_position = smooth_scroll(current_scroll_position)

            cards = feed.find_elements(By.CLASS_NAME, "x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z")
            for card in cards:
                author = card.find_elements(By.CLASS_NAME, "x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz.x1gslohp.x1yc453h")
                author = author[0].text
                post = card.find_elements(By.CLASS_NAME, "x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a")
                post = [p.text for p in post]
                post = '\n'.join(post)
                if not any(post in row for row in data) and author != '' and author != '\n':
                    data.append([author,post])

        display(data)
        export(data,'scraping_data')
        dictionary = data_to_dictionary(data)
        print(dictionary)

    except NoSuchElementException:
        print("Content not found")

    driver.quit()
