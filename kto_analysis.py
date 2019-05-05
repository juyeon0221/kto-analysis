import time

import pandas
from bs4 import BeautifulSoup
from selenium import webdriver

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

contents = driver.page_source
driver.close()

html = BeautifulSoup(contents, 'html.parser')

li_list = html.find_all("li", {"class": "js-stream-item stream-item stream-item"})

id_num=0
date_and_hashtag_list = list()
for li in li_list:
    id_num = id_num + 1
    a = li.find(
        "a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})
    date = a["title"]  # "오전 12:16 - 2019년 3월 26일"

    div = li.find(
        "div",{"class": "js-tweet-text-container"})
    body = div.p.text #트위터 본문

    print(date, body)


'''
    a2 = d.find_all("a", {"class": "twitter-hashtag pretty-link js-nav"})
    for ah in a2:
        hashtag = ah.find("b").text  # "광주호석투어"
        row = [id_num,title, hashtag]
        date_and_hashtag_list.append(row)
       

# Write
data = pandas.DataFrame(date_and_hashtag_list)
data.columns = ['date', 'hashTag']
data.to_csv('구석구석_전체.csv', encoding='UTF-8')
'''