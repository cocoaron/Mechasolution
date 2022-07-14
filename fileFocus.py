import requests
from datetime import datetime
import json
import pandas as pd
from sqlalchemy import false


# 인스타그램의 API는 로그인 정보가 필요하므로
# 먼저 로그인을 진행한 후 사용
class Instagram:
    def __init__(self):
        self.csrf_token = ""
        self.session_id = ""
        self.headers = {}
        self.cookies = {}  # cookie : HTTP에서 사용자의 정보를 저장하는 데이터

        self.sess = None  # 로그인 유지를 위해 requests의 session 클래스를 사용

    def login(self, username, password):  # 인스타그램 로그인
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        self.sess = requests.session()

        time = int(datetime.now().timestamp())
        response = self.sess.get(link)
        csrf = response.cookies['csrftoken']

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        self.headers = {
            # "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            # 특정 User-Agent를 사용하지 않으면 에러를 반환
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = self.sess.post(login_url, data=payload, headers=self.headers)
        json_data = json.loads(login_response.text)

        print("**print login_response.status_code, login_response.text:**")
        print(login_response.status_code, login_response.text)

        # 토큰 등 로그인 정보를 받아온 후 cookies 변수에 저장
        if json_data["authenticated"]:
            self.cookies = login_response.cookies
        else:
            print("login failed ", login_response.text)

    def get_search_data_tag_name(self, tag_name):  # 해쉬태그를 검색하여 나오는 게시물 정보
        url = "https://i.instagram.com/api/v1/tags/web_info"

        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "tag_name": tag_name
            }
        )

        return r.json()["data"]

    def get_top_search_tag(self, tag_name):  # 인스타그램 검색창에 입력 시 실행되는 api, 추천 검색어를 반환함
        url = "https://www.instagram.com/web/search/topsearch/"

        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "context": "blended",
                "query": tag_name,
                "include_reel": "true"
            }
        )

        return r.json()["hashtags"]

    def get_user_info(self, user_id):  # 단일 계정에 대한 정보 반환
        url = "https://i.instagram.com/api/v1/users/web_profile_info"

        r = self.sess.get(
            url,
            headers=self.headers,
            cookies=self.cookies,
            params={
                "username": user_id
            }
        )

        return r.json()["data"]


username = 'hatie176'#"dadq176"#'osusu176' #
password = 'chamehchameh'#"mechamecha"#'akekemem' #

instagram = Instagram()
instagram.login(username, password)

# 리스트 선언
top_post = []
recent_post = []

# 해시태그 검색
tags = instagram.get_top_search_tag('#' + input("검색어를 입력하십시오: "))
hashtags = []
recommend_hashtag = []

for tag in tags:
    hashtags = tag["hashtag"]["name"]
    recommend_hashtag.append(hashtags)


try:
    temp_hash = pd.read_excel("reading_v01_2.xlsx")
    temp_hash.drop(['Unnamed: 0'], axis=1, inplace=True)

    tempy = pd.concat([temp_hash, pd.DataFrame(recommend_hashtag, columns=['hashtag'])])

except:
    tempy = pd.DataFrame(recommend_hashtag, columns=['hashtag'])

finally:
    tempy.to_excel("reading_v01_2.xlsx")


#while True:
for hash_item in recommend_hashtag:
    # 해시태그 검색
    hash_string = str(hash_item)
    hashtag_search = instagram.get_search_data_tag_name(hash_string)

    if hash_string == 'end':
        break

    else:
        ## 해시태그 검색 페이지에서 데이터 크롤링(인기 게시글)
        try:
            for i in range(0, 3):
                for j in range(0, 3):

                    top_username = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["user"][
                        "username"]
                    top_like = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"]["like_count"]
                    top_comments = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"][
                        "comment_count"]
                    '''
                    try:
                        top_comments = hashtag_search["top"]["sections"][i]["layout_content"]["medias"][j]["media"][
                        "comment_count"]
                    except:
                        top_comments = -1
                    '''

                    hashtag_top_user = instagram.get_user_info(top_username)

                    top_follower = hashtag_top_user["user"]["edge_followed_by"]["count"]
                    top_following = hashtag_top_user["user"]["edge_follow"]["count"]
                    top_biography = hashtag_top_user["user"]["biography"]

                    top_user_like = 0
                    top_user_comments = 0

                    # 수정
                    media_list = hashtag_top_user["user"]["edge_owner_to_timeline_media"]["edges"]
                    for medium in media_list:
                        top_user_like += medium["node"]["edge_liked_by"]["count"]
                        top_user_comments += medium["node"]["edge_media_to_comment"]["count"]

                    top_avglike = top_user_like / 12
                    top_avgcomments = top_user_comments / 12

                    try:
                        top_ER = (top_avglike + top_avgcomments) / top_follower * 100
                    except ZeroDivisionError:
                        top_ER = -1

                    top_post.append([hash_string, top_username, top_like, top_comments,
                                     top_follower, top_following, top_biography,
                                     top_avglike, top_avgcomments, top_ER])

            print("***** 인기 게시글 정보 수집 완료 *****")
            print("----- top post -----")
            print(top_post)
            print("")

        except:
            print(
                "////////////////////////////////////" + hash_string +
                " 해시태그에 대해 에러가 발생했습니다. ////////////////////////////////////////////////")
            pass

        try:
            temp = pd.read_excel("top_post_9_v01_2.xlsx")
            ##temp.drop(['Unnamed: 0'], axis = 1, inplace = True)

            output_top = pd.concat([temp, pd.DataFrame(top_post,
                                                       columns=['hashtag', 'username', 'like', 'comments',
                                                                'follower',
                                                                'following', 'biography',
                                                                'likeAvg', 'commentsAvg', 'ER'])])
        except:
            output_top = pd.DataFrame(top_post,
                                      columns=['hashtag', 'username', 'like', 'comments', 'follower',
                                               'following', 'biography',
                                               'likeAvg', 'commentsAvg', 'ER'])
        finally:
            output_top.to_excel('top_post_9_v01_2.xlsx', index=False, encoding='utf-8')
            top_post.clear()

## CSV 파일 저장
('\n'
 '부연설명\n'
 'username : 계정명\n'
 'like : 해시태그 검색창에서의 인기/최근 게시글의 좋아요 수\n'
 'comments : 해시태그 검색창에서의 인기/최근 게시글의 좋아요 수\n'
 'biography : 계정의 소개글\n'
 'likeAvg : 해당 계정의 최근 12개 게시글에 대한 평균 좋아요 수\n'
 'commentsAvg : 해당 계정의 최근 12개 게시글에 대한 평균 댓글 수\n'
 'ER : 최근 12개 게시글에 대한 ER지수\n'
 '\n'
 '\n'
 '# 인기 게시글 파일로 누적 저장\n'
 'try:\n'
 '    temp = pd.read_excel("top_post_9_v01.xlsx")\n'
 '    ##temp.drop([\'Unnamed: 0\'], axis = 1, inplace = True)\n'
 '\n'
 '    output_top = pd.concat([temp, pd.DataFrame(top_post,\n'
 '                                               columns=[\'hashtag\', \'username\', \'like\', \'comments\', \'follower\',\n'
 '                                                        \'following\', \'biography\',\n'
 '                                                        \'likeAvg\', \'commentsAvg\', \'ER\'])])\n'
 'except:\n'
 '    output_top = pd.DataFrame(top_post,\n'
 '                              columns=[\'hashtag\', \'username\', \'like\', \'comments\', \'follower\', \'following\', \'biography\',\n'
 '                                       \'likeAvg\', \'commentsAvg\', \'ER\'])\n'
 'finally:\n'
 '    output_top.to_excel(\'top_post_9_v01.xlsx\', index=False, encoding=\'utf-8\')\n'
 '\n')