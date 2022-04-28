from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml
import re
from bs4 import BeautifulSoup
import unicodedata
import time
import pandas as pd
import os
from tqdm.notebook import tqdm
import ipywidgets
import time
import requests
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import platform

def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    return url

def select_first(driver):
    first = driver.find_element_by_css_selector("div._9AhH0")
    first.click()
    time.sleep(3)

def move_next(driver):
    right = driver.find_element_by_css_selector ('a.coreSpriteRightPaginationArrow')
    right.click()
    time.sleep(3)


def get_content(driver):
    try:  # 게시글이 표시될때까지 대기. 최대 20초. 게시글이 표시 될 경우 즉시 이하의 코드를 실행
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "C4VMK"))
        )
    except:
        print('게시글이 로드되지 않았습니다. 다음 게시글로 넘어갑니다.',
              datetime.today().strftime("%Y/%m/%d %H:%M:%S"))  # 20초 동안 게시글이 표시 되지 않으면 다음으로 넘어감
        # 몇몇 게시글이 로드되지 않는 경우가 발생하고 이때 적절한 시간을 두지 않고 넘겨버리면 이후의 게시글도 로드가 되지 않는 문제를 방지하고
        # 인스타그램 서버에서 크롤링 계정을 차단 하는 것을 방지하기 위해 추가되었습니다.
    # ① 현재 페이지 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # ② 본문 내용 가져오기
    try:
        content = soup.select('div.C4VMK > span')[0].text
        content = unicodedata.normalize('NFC', content)
    except:
        content = ' '
    # ③ 본문 내용에서 해시태그 가져오기(정규식 활용)
    tags = re.findall(r'#[^\s#,\\]+', content)
    # ④ 작성일자 정보 가져오기
    date = soup.select('time._1o9PC.Nzb55')[0]['datetime'][:10]
    # ⑤ 좋아요 수 가져오기
    try:
        like = driver.find_element_by_xpath(
            "/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div/a/span").text  # 기존 코드는 제대로 동작하지 않아 셀레니움을 이용
    except:
        like = 0
    # ⑥ 위치정보 가져오기
    try:
        place = soup.select('div.M30cS')[0].text
        place = unicodedata.normalize('NFC', place)
    except:
        place = ''
    data = [content, date, like, place, tags]
    return data


def Crawl_Insta():
    print('시작시간', datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
    email = input('이메일을 입력하세요.')
    pw = input('비밀번호를 입력하세요. 결과 창에 비밀번호가 공개되는 것을 방지하려면 아무것도 입력하지 마세요. 생성된 크롬창에서 직접 비밀번호를 입력하세요.')

    # 인스타그램 페이지 연결
    driver = webdriver.Chrome('c:/mydriver/chromedriver.exe')
    driver.get('https://www.instagram.com')
    time.sleep(2)
    # 로그인
    input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
    input_id.clear()
    input_id.send_keys(email)
    input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
    input_pw.clear()
    input_pw.send_keys(pw)
    input_pw.submit()
    print('인스타그램 로그인 확인을 위한 15초 타이머 시작')
    for i in tqdm(range(15)):
        time.sleep(1)
    # time.sleep(15) #로그인 확인을 위한 여유시간 15초

    word = input('키워드를 입력해주세요')  # 검색어
    url = insta_searching(word)
    target = input('몇개의 게시글을 크롤링할까요? 숫자만 입력 가능합니다.')

    # ③ 검색페이지 접속하기
    driver.get(url)
    time.sleep(4)  # 대기시간

    # ④ 첫 번째 게시글 열기
    select_first(driver)

    # ⑤ 비어있는 변수(results)만들기
    results = []
    print('크롤링 시작', datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
    # ⑥→⑦→⑧ 여러 게시물 수집하기

    for i in tqdm(range(int(target))):
        # 게시글 수집에 오류 발생시(네트워크 문제 등의 이유로)  2초 대기 후, 다음 게시글로 넘어가도록 try, except 구문 활용
        try:
            data = get_content(driver)  # 게시글 정보 가져오기
            results.append(data)
            move_next(driver)
        except:
            time.sleep(2)
            move_next(driver)
    print('데이터 저장 시작', datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
    # 엑셀로 저장
    results_df = pd.DataFrame(results)
    results_df.columns = ['content', 'data', 'like', 'place', 'tags']
    results_df.drop_duplicates(subset='content', inplace=True)  # 중복 게시글 제거
    results_df.reset_index(drop=True, inplace=True)  # 인덱스 재설정
    if not os.path.exists('./files/' + word + '.xlsx'):
        with pd.ExcelWriter('./files/' + word + '.xlsx', mode='w', engine='openpyxl') as writer:  # 엑셀 파일 없으면 생성
            results_df.to_excel(writer, sheet_name=word)
    else:
        with pd.ExcelWriter('./files/' + word + '.xlsx', mode='w', engine='openpyxl') as writer:  # 엑셀 파일 있으면 덮어씌우기
            results_df.to_excel(writer, sheet_name=word)
    print('완료', datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
    driver.quit()

Crawl_Insta()


def location_C(file):
    raw_total = pd.read_excel('./files/' + file + '.xlsx')

    location_counts = raw_total['place'].value_counts()
    location_counts_df = pd.DataFrame(location_counts)
    location_counts_df.to_excel('./files/' + file + '위치정보빈도.xlsx')

    return location_counts_df


def find_places(searching, key):
    # ① 접속URL 만들기
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(searching)

    # ② headers 입력하기
    headers = {
        "Authorization": "KakaoAK " + key
    }

    # ③ API 요청&정보 받기
    places = requests.get(url, headers=headers).json()['documents']

    # ④ 필요한 정보 선택하기
    place = places[0]
    name = place['place_name']
    x = place['x']
    y = place['y']
    category = place['category_group_name']
    data = [name, x, y, searching, category]

    return data


def save_locations():
    locations = input('좌표를 구할 키워드를 입력해주세요')
    locations_index = location_C(locations).index
    key = input('카카오 api 키를 입력해주세요.')

    locations_inform = []
    for location_index in tqdm(locations_index):
        try:
            data = find_places(location_index, key)
            locations_inform.append(data)
            time.sleep(0.5)
        except:
            pass
    locations_inform

    locations_inform_df = pd.DataFrame(locations_inform)
    locations_inform_df.columns = ['정식명칭', '경도', '위도', '인스타위치명', '카테고리']
    locations_inform_df.to_excel('./files/' + locations + '위치.xlsx', index=False)

    location_counts_df = pd.read_excel('./files/' + locations + '위치정보빈도.xlsx', index_col=0)
    locations_inform_df = pd.read_excel('./files/' + locations + '위치.xlsx')
    location_data = pd.merge(locations_inform_df, location_counts_df,
                             how='inner', left_on='정식명칭', right_index=True)
    location_data['정식명칭'].value_counts()
    location_data = location_data.pivot_table(index=['정식명칭', '경도', '위도'], values='place', aggfunc='sum')
    location_data.to_excel('./files/' + locations + '지도시각화.xlsx')

save_locations()


def hash_tags(file):
    tags_total = []
    raw_total = pd.read_excel('./files/' + file + '.xlsx')

    for tags in raw_total['tags']:
        tags_list = tags[2:-2].split("', '")
        for tag in tags_list:
            tags_total.append(tag)

    # 예제 5-18 데이터 정제하기
    STOPWORDS = ['', '#남이섬', '#Nami-island', '#가평', '#가평일상', '#일상', '#NamiLife', '#백수의삶', '#소통',
                 '#맞팔']  # 불필요한 해시태그 정리하기
    tag_total_selected = []
    for tag in tags_total:
        if tag not in STOPWORDS:
            tag_total_selected.append(tag)

    tag_counts_selected = Counter(tag_total_selected)
    df_tag_counts_selected = pd.DataFrame(tag_total_selected)
    df_tag_counts_selected.to_excel('./files/' + file + '해시태그.xlsx')

    return tag_counts_selected
def word_cloud() :
    file = input("키워드를 입력해주세요")
    if platform.system() == 'Windows':   #윈도우의 경우
        font_path = "c:/Windows/Fonts/malgun.ttf" #폰트 경로 설정(바꾸면 폰트 변경 됨)
    elif platform.system() == "Darwin":   #Mac 의 경우
        font_path = "/Users/$USER/Library/Fonts/AppleGothic.ttf"
    tag_counts_selected = hash_tags(file)
    wordcloud = WordCloud(font_path= font_path,
                    background_color="white", #배경색상
                    max_words=100, #최대 표시 단어 개수
                    relative_scaling= 0.3, #상대적 크기
                    width = 800, #가로
                    height = 400 #세로
                    ).generate_from_frequencies(tag_counts_selected)
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig('./files/'+ file + '워드클라우드.png')

word_cloud() #실행코드