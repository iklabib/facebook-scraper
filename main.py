import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def smooth_scroll(current_scroll_position = 0):
    driver.execute_script("document.documentElement.style.setProperty('scroll-behavior', 'smooth');")    
    scroll_iteration = 60 #default 60
    for _ in range(scroll_iteration):
        current_scroll_position += 100
        driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")
        time.sleep(0.1)
        new_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
    return current_scroll_position


#Initiate chrome driver
options = Options()
options.add_experimental_option("detach", False)

driver = webdriver.Chrome(options=options)

# Go to website
driver.get("https://web.facebook.com/groups/306516256927109")


try:
    title = driver.find_element(By.XPATH, '//title').get_attribute('innerHTML')
    print(title)
except NoSuchElementException:
    print("Title not found")

try:
    element = driver.find_element(By.XPATH, "//*[text()='Public group']")
    class_name = element.get_attribute("class")
    # print(class_name)
except NoSuchElementException:
    print("Class not found")

arr = [
    'x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r x126k92a'
    'x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a',
    'x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r x126k92a'
]
try:
    current_scroll_position = 0
    data = []
    for _ in range(5):
        print('starting a new batch...')
        current_scroll_position = smooth_scroll(current_scroll_position)
        elements = driver.find_elements(By.CLASS_NAME, "x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs.x126k92a")
        index = 1
        string = ''
        for element in elements:
            class_name = element.get_attribute("class")
            if 'xdj266r' in class_name:
                if string not in data and string != '' and string != '\n':
                    data.append(string)
                    string = ''
                string = element.text
                index+=1
            else:
                string += f'\n{element.text}'
            
    for index, text in enumerate(data): 
        print(f'{index}. {text}\n')

    df = pd.DataFrame({'data': data})
    df.to_csv("output/scraping.csv", index=False, header=True)

    
except NoSuchElementException:
    print("Content not found")

# Close the browser
driver.quit()
