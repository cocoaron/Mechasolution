from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

import time
import re

from datetime import datetime


# Data crawling
def getUserContent(driver):

    html = driver.page_source
    # to access html tag for likes, content, hashtag, time, place
    soup = BeautifulSoup(html, 'html.parser')
    # to receive and store info using html tag

    currentDateTime = datetime.now()
    # current date when crawling

    # content(본문 내용)
    try:
        content_raw = soup.select('div.MOdxS')[0].text
        content_box = re.findall('[A-Za-z0-9가-힣!-@]+', content_raw)
        content = ' '.join(content_box)
        # access content by its html tag and if exists, says exists
    except:
        content = None
        # if there is no content

    # hashtag
    instagram_tags = []
    ## create a list for storing hashtag contents
    # (each hashtag is treated as individual components)

    try:
        data = driver.find_element_by_css_selector(".C7I1f.X7jCj")
        # access content by its html tag
        tag_raw = data.text
        # store them as text string
        tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
        # find hashtag symbol(#) in the text string

        tag = ''.join(tags).replace("#"," ")
        # Before storing the data, remove hashtag symbol(#)
        tag_data = tag.split()
        # acknowledge each component by space(빈 칸)

        for tag_one in tag_data:
            # for loop to store each hashtag content in the list
            instagram_tags.append(tag_one)
            # store them in the list
    except:
        pass
    #if there is no hashtag in the post

    # date
    try:
        date = soup.select('time._1o9PC')[0]['title']
        # access content by its html tag and store them as text string
    except:
        date = None
        # for exception handling

    # like
    try:
        like = soup.select('section.EDfFK.ygqzn')[0].findAll('span')[-1].text
        # access content by its html tag and store them as text string
    except:
        like = None
        # if the post did not receive any likes at current time

    # location
    try:
        place = soup.select('div.M30cS')[0].text
        # access content by its html tag and store them as text string
    except:
        place = None
        # if post does not specify the location

    name = soup.select('a.sqdOP.yWX7d._8A5w5.ZIAjV')[0].text
    # name of the poster

    post_data = [name, like, date, currentDateTime.strftime("%b %d, %Y"), content, place, instagram_tags]
    #store them in a list

    print(post_data)
    return post_data



# Data crawling
def getTagContent(driver, search_tag):

    html = driver.page_source
    # to access html tag for likes, content, hashtag, time, place
    soup = BeautifulSoup(html, 'html.parser')
    # to receive and store info using html tag

    currentDateTime = datetime.now()
    # current date when crawling

    # content(본문 내용)
    try:
        content_raw = soup.select('div.MOdxS')[0].text
        content_box = re.findall('[A-Za-z0-9가-힣!-@]+', content_raw)
        content = ' '.join(content_box)
        # access content by its html tag and if exists, says exists
    except:
        content = None
        # if there is no content

    # hashtag
    instagram_tags = []
    ## create a list for storing hashtag contents
    # (each hashtag is treated as individual components)

    try:
        data = driver.find_element_by_css_selector(".C7I1f.X7jCj")
        # access content by its html tag
        tag_raw = data.text
        # store them as text string
        tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
        # find hashtag symbol(#) in the text string

        tag = ''.join(tags).replace("#"," ")
        # Before storing the data, remove hashtag symbol(#)
        tag_data = tag.split()
        # acknowledge each component by space(빈 칸)

        for tag_one in tag_data:
            # for loop to store each hashtag content in the list
            instagram_tags.append(tag_one)
            # store them in the list
    except:
        pass
    #if there is no hashtag in the post

    # date
    try:
        date = soup.select('time._1o9PC')[0]['title']
        # access content by its html tag and store them as text string
    except:
        date = None
        # for exception handling

    # like
    try:
        like = soup.select('section.EDfFK.ygqzn')[0].findAll('span')[-1].text
        # access content by its html tag and store them as text string
    except:
        like = None
        # if the post did not receive any likes at current time

    # location
    try:
        place = soup.select('div.M30cS')[0].text
        # access content by its html tag and store them as text string
    except:
        place = None
        # if post does not specify the location

    name = soup.select('a.sqdOP.yWX7d._8A5w5.ZIAjV')[0].text
    # name of the poster

    post_data = [search_tag, name, like, date, currentDateTime.strftime("%b %d, %Y"), content, place, instagram_tags]
    #store them in a list

    print(post_data)
    return post_data


driver = webdriver.Chrome('c:/mydriver/chromedriver.exe')
## webdriver
url = "http://www.instagram.com/accounts/login/"
## url for accessing

driver.get(url)
## open the site

time.sleep(3)
## wait for the page to fully open


# Log in
ID = str('mehmehmehhhhhh')
Passwd = str('cocoahs153!')

inputid = driver.find_element_by_name('username')
#inputid = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
#inputid.clear()
##first method is to find ID component by how web named the input textfield
##second method(hidden) is to find ID component by html tag

inputid.send_keys(ID)
print('sucess: id')

inputPw = driver.find_element_by_name('password')
#inputPw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
#inputPw.clear()
## first method is to find password component by how web named the input textfield
## second method(hidden) is to find password component by html tag

inputPw.send_keys(Passwd)
print('sucess: pw')

time.sleep(2)
## wait for the site to input given info

login_ok_button = driver.find_element_by_css_selector(".sqdOP.L3NKy.y3zKF     ")
## find the html tag for log in button

login_ok_button.click()
## take action on the button

time.sleep(3)
print('sucess: login')
## wait for the site to fully log in

## Find the keyword and crawl data
crawling_tag_data = []
# list to store each post's data

## Find the user and crawl data
follow_data = []
# list to store each influencer's follower number
crawling_user_data = []
# list to store each post's data


# Crawl until user wants to stop
while True:

    choice = str(input("Search for hashtag(1) or user(2) or end crawling(0): "))
    # search for user you'd want to find

    if choice == '0':
        break
        # if user wants to stop crawling, exit loop
    else:
        if choice == '1':
            tag = str(input("Search for the keyword: "))
            search_tag = 'https://www.instagram.com/explore/tags/' + str(tag)
            # find the user by altering url
            driver.get(search_tag)
            # open the user profile page
            time.sleep(7)
            # wait for the site to load

            first = driver.find_element_by_css_selector('.v1Nh3.kIKUG._bz0w')
            # access the first post on the profile by its html tag
            first.click()
            # click the given html tag
            time.sleep(3)
            # wait for the post to load

            for i in range(9):

                crawling_tag_data.append(getTagContent(driver, tag))
                # store current post's data

                right = driver.find_element_by_css_selector("div.l8mY4.feth3")
                # access the button to reach next post on the profile by its html tag
                right.click()
                time.sleep(3)
                # wait for the post to load

        if choice == '2':
            user = str(input("Search for the user: "))
            # search for user you'd want to find
            profile = "http://www.instagram.com/" + str(user)
            # find the user by altering url
            driver.get(profile)
            # open the user profile page
            time.sleep(7)
            # wait for the site to load

            html = driver.page_source
            # to access html tag for followers
            soup = BeautifulSoup(html, 'html.parser')
            # to receive and store info using html tag

            name = soup.select("h2._7UhW9.fKFbl.yUEEX.KV-D4.fDxYl")[0].text

            followers = soup.select("span.g47SY")[1]['title'][:10]
            # get follower data from the profile
            followings = soup.select("span.g47SY")[2].text
            # get following data from the profile

            try:
                bio_raw = soup.select("span._7UhW9.vy6Bb.qyrsm.KV-D4.se6yk.T0kll")[0].text
                bio_raw_box = re.findall('[A-Za-z0-9가-힣!-@]+', bio_raw)
                bio_raw1 = tag = ' '.join(bio_raw_box)
                bio = bio_raw1
            except:
                pass

            try:
                bio_raw = soup.select("div._7UhW9.vy6Bb.MMzan.KV-D4.uL8Hv.T0kll")[3].text
                bio_raw_box = re.findall('[A-Za-z0-9가-힣!-@]+', bio_raw)
                bio_raw2 = tag = ' '.join(bio_raw_box)
                bio = bio + ', ' + bio_raw2
            except:
                pass

            user_data = [name, followers, followings, bio]
            # to see the follower and following data of a profile
            print(user_data)

            follow_data.append(user_data)
            # store current user's data

            first = driver.find_element_by_css_selector('.v1Nh3.kIKUG._bz0w')
            # access the first post on the profile by its html tag
            first.click()
            # click the given html tag
            time.sleep(3)
            # wait for the post to load

            for i in range(9):
                crawling_user_data.append(getUserContent(driver))
                # store current post's data

                right = driver.find_element_by_css_selector("div.l8mY4.feth3")
                # access the button to reach next post on the profile by its html tag
                right.click()
                time.sleep(3)
                # wait for the post to load

data_output = pd.DataFrame(crawling_tag_data, columns = ['search tag', 'name', 'like', 'post date', 'current date', 'content', 'place', 'tags'])
# to handle large amount of data, use Dataframe supported by pandas
data_output.to_csv('./instagram_tag_crawling_post_data.csv')
# save the output data as csv file (can be accessed using excel or notepad)

follower_output = pd.DataFrame(follow_data, columns = ['name', 'followers', 'followings', 'bio'])
# to handle large amount of data, use Dataframe supported by pandas
follower_output.to_csv('./instagram_crawling_follower_data.csv')
# save the output data as csv file (can be accessed using excel or notepad)

data_output = pd.DataFrame(crawling_user_data, columns = ['name', 'like', 'post date', 'current date', 'content', 'place', 'tags'])
# to handle large amount of data, use Dataframe supported by pandas
data_output.to_csv('./instagram_crawling_post_data.csv')
# save the output data as csv file (can be accessed using excel or notepad)