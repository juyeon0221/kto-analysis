from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

import time

import pandas as pd

driver = webdriver.Chrome()

driver.get(
    'https://twitter.com/search?l=&q=from%3AKor_Visitkorea%20since%3A2019-01-01&src=typd')

time.sleep(3)


driver.find_element_by_name(
    "session[username_or_email]").send_keys('01031406980')

driver.find_element_by_name("session[password]").send_keys('Jenny0221@')

driver.find_element_by_xpath(
    "//*[@class='EdgeButton EdgeButton--primary EdgeButton--medium submit js-submit']").click()

last_height = driver.execute_script("return document.body.scrollHeight")


while True:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(3)

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:

        break

    last_height = new_height


list = list()

con = driver.page_source

html = BeautifulSoup(con, 'html.parser')

div = html.find_all("li", {"class": "js-stream-item stream-item stream-item"})

for d in div:

    a1 = d.find(
        "a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})

    title = a1["title"]

    a2 = d.find_all("a", {"class": "twitter-hashtag pretty-link js-nav"})

    for ah in a2:

        hashtag = ah.find("b").text

        row = [title, hashtag]

        list.append(row)

print('list 수집 완료')

data = pd.DataFrame(list)

data.columns = ['date', 'hashTag']

data.to_csv('구석구석_전체.csv', encoding='UTF-8')


driver.close()
