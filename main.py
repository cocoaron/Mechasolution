#0428 update

import re

from selenium import webdriver
from bs4 import BeautifulSoup
import time

def instaSearch(keyword):
    url = 'https://www.instagram.com/explore/tags/'+keyword
    return url

def getContent(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        content = soup.select('div.M0dxS')[0].text
    except:
        content = ''

    tags = re.findall(r'#[^\s#,\\]+', content)

    date = soup.select('time._1o9PC')[0]['datetime'][:10]

    try:
        like = soup.select('div._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll')[0].text
    except:
        like = 0

    try:
        place = soup.select('div.M30cS')[0].text
    except:
        place = ''

    data = [content, date, like, place, tags]

    print(data)

driver = webdriver.Chrome('c:/mydriver/chromedriver.exe')
url = 'http://www.instagram.com'
driver.get(url)
time.sleep(3)

driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')

ID = input('ID를 입력하세요: ')
inputid = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
inputid.clear()
inputid.send_keys(ID)

password = input('비밀번호를 입력하세요: ')
inputPw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
inputPw.clear()
inputPw.send_keys(password)

inputPw.submit()
time.sleep(2)

word = 'ootd'
url = instaSearch(word)
driver.get(url)

first = driver.find_element_by_css_selector('div._9AhH0')
first.click()
time.sleep(2)

getContent(driver)

word = 'art'
url = instaSearch(word)
driver.get(url)

first = driver.find_element_by_css_selector('div._9AhH0')
first.click()
time.sleep(2)

getContent(driver)

word = '협찬'
url = instaSearch(word)
driver.get(url)

first = driver.find_element_by_css_selector('div._9AhH0')
first.click()
time.sleep(2)

getContent(driver)

word = '광고'
url = instaSearch(word)
driver.get(url)

first = driver.find_element_by_css_selector('div._9AhH0')
first.click()
time.sleep(2)

getContent(driver)

second = driver.find_element_by_css_selector('div.QBdPU')
second.click()
time.sleep(2)

getContent(driver)


#getContent(first)
