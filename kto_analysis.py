import time
import xlsxwriter

from selenium import webdriver
from bs4 import BeautifulSoup
from konlpy.tag import Kkma

driver = webdriver.Chrome('D:/python/workspace/chromedriver.exe')
#driver = webdriver.Chrome()

driver.get(
    'https://twitter.com/search?l=&q=from%3AKor_Visitkorea%20since%3A2015-01-01&src=typd')

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
id_and_date_and_body_list=[]
id_and_noun_list=[]

for li in li_list:
    id_num = id_num + 1
    kma = Kkma()

    #날짜 추출
    a = li.find(
        "a", {"class": "tweet-timestamp js-permalink js-nav js-tooltip"})
    date = a["title"]

    #트위터 본문
    div = li.find(
        "div",{"class": "js-tweet-text-container"})
    body = div.p.text 
    id_and_date_and_body =[id_num, date, body]
    id_and_date_and_body_list.append(id_and_date_and_body)
   
    #명사추출
    body_nouns = kma.nouns(body)
    for noun in body_nouns:
        id_and_noun = [id_num,noun]
        id_and_noun_list.append(id_and_noun)

print(id_and_date_and_body_list)
print(id_and_noun_list)

# 엑셀 저장
workbook = xlsxwriter.Workbook('구석구석데이터.xlsx')
worksheet_first = workbook.add_worksheet('body')
worksheet_second = workbook.add_worksheet('noun')

row=0
col=0

#시트1_아이디, 날짜, 본문
for id_num, date, body in id_and_date_and_body_list:
    worksheet_first.write(row, col, id_num)
    worksheet_first.write(row, col+1, date)
    worksheet_first.write(row, col+2, body)
    row = row+1

print('첫번째 시트 저장 완료')

row=0
col=0
#시트2_아이디, 명사
for id_num, noun in id_and_noun_list:
    worksheet_second.write(row, col, id_num)
    worksheet_second.write(row, col+1, noun)
    row = row+1

print('두번째 시트 저장 완료')

workbook.close()


'''
# 해쉬태그 추출
    a2 = d.find_all("a", {"class": "twitter-hashtag pretty-link js-nav"})
    for ah in a2:
        hashtag = ah.find("b").text  # "광주호석투어"
        row = [id_num,title, hashtag]
        date_and_hashtag_list.append(row)
       
# csv 쓰기
data = pandas.DataFrame(date_and_hashtag_list)
data.columns = ['date', 'hashTag']
data.to_csv('구석구석_전체.csv', encoding='UTF-8')
'''
