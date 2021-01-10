#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import re
import pandas as pd
import numpy as np
import requests
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import csv
from tqdm import tqdm
from datetime import datetime, timedelta


def get_trending_video():
    url = 'https://www.youtube.com/feed/trending'

    driver = webdriver.Chrome('./chromedriver') #크롬 드라이버 경로
    driver.get(url)

    time.sleep(5)
    
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
        time.sleep(5)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_page_height == last_page_height:
            break

        last_page_height = new_page_height

    
    load_box = driver.find_elements_by_css_selector('#grid-container ytd-video-renderer')
    
    info_dict = {'title' : [],
                'link' : [],
                'Youtuber' : [],
                'view' : [],
                'date' : []}
    
    for video in load_box:
        try: 
            #제목
            title = video.find_element_by_css_selector('#video-title').text
            #url
            link = video.find_element_by_css_selector('#video-title').get_attribute('href')
            #유튜버
            Youtuber = video.find_element_by_css_selector('#text a').text
            #조회수
            view = video.find_element_by_css_selector('#metadata-line span:nth-child(1)').text
            #날짜
            date = video.find_element_by_css_selector('#metadata-line span:nth-child(2)').text

            info_dict['title'].append(title)
            info_dict['link'].append(link)
            info_dict['Youtuber'].append(Youtuber)
            info_dict['view'].append(view)
            info_dict['date'].append(date)
        except:
            pass

    df = pd.DataFrame(info_dict)
    driver.close()
    return df

def check_df(today_df):
    today = datetime.now()
    today_df.to_pickle('TrendingVideoList_{}.pkl'.format(today.strftime('%Y%m%d')))
    
    #어제의 데이터 받아오기
    try:
        yesterday = today - timedelta(days=1)
        yesterday_df = pd.read_pickle('TrendingVideoList_{}.pkl'.format(yesterday.strftime('%Y%m%d')))

        #어제의 동영상 리스트 받아오기
        yesterday_titles = list(yesterday_df['title'])

        #어제의 동영상과 다른 리스트만을 추출
        indexes = []
        for idx, t in enumerate(today_df['title']):
            #어제의 동영상 제목과 겹치면 패스
            if t in yesterday_titles:
                pass
        else:
            indexes.append(idx)
        
        today_df = today_df.iloc[indexes]
        return today_df
    
    except: #어제의 크롤링이 안된 경우
        return today_df
    
def YoutubeCrawler(df):
    now = datetime.now().strftime('%Y%m%d') #크롤링 당일 날짜 지정
    f = open('TrendingVideo_{}.csv'.format(now), 'w', encoding='utf-8-sig', newline='')
    f.close()
    
    content = [] #댓글을 담을 리스트
    
    #시작 url 설정 - 사실 어느 사이트건 상관은 없다.
    start_url = 'https://www.youtube.com/'
    driver = webdriver.Chrome('./chromedriver') #크롬 드라이버 경로
    driver.get(start_url)
    
    link_list = list(df['link'])
    link_length = len(link_list)
    
    for j in tqdm(range(link_length)):
        try:
            print('{}번째 동영상'.format(j))

            #필요한 url 새창 띄우기
            driver.execute_script("window.open('{},_blank');".format(link_list[j]))
            driver.switch_to.window(driver.window_handles[-1]) #가장 최근에 연 창 조절

            time.sleep(5) #댓글창로딩

            start = time.time()

            #모든 댓글 불러오기 
            last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight)")
                time.sleep(7) #댓글창 로딩
                new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
                
                if new_page_height == last_page_height:
                    break
                else:
                    last_page_height = new_page_height

            check_point_1 = time.time()
            print('마지막까지 내리기 : {}'.format(check_point_1 - start))

            #대댓글 불러오기
            load_reply = driver.find_elements_by_css_selector('#contents #text')

            for load in load_reply:
                #답글을 남기는 '답글' 과 '답글 n개 보기' 중 'n개 보기' 필터링
                if '보기' in load.text: 
                    driver.execute_script('arguments[0].click();',load)
                    #load.click()의 경우 오류가 발생
                else:
                    pass

            check_point_2 = time.time()
            print('대댓글 불러오기 (1) : {}'.format(check_point_2 - check_point_1))

            #대댓글 더 불러오기
            while True:
                check_point = driver.find_elements_by_xpath('//*[@id="continuation"]/yt-next-continuation/paper-button/yt-formatted-string')

                if len(check_point):
                    #답글이 일정 수준을 넘기면 '답글 더보기'가 등장, 이를 클릭하기 위함
                    load_more_reply = driver.find_elements_by_xpath('//*[@id="continuation"]/yt-next-continuation/paper-button/yt-formatted-string')

                    for load in load_more_reply:
                        try:
                            driver.execute_script('arguments[0].click();',load)
                        except:
                            break
                else:
                    break

            check_point_3 = time.time()
            print('대댓글 불러오기 (2) : {}'.format(check_point_3 - check_point_2))

             #답글에도 자세히보기를 사용해야할경우가있기때문에 자세히보기 클릭은 답글을 다 연 다음에
            load_detail = driver.find_elements_by_xpath('//*[@id="more"]/span')

            for load in load_detail:
                if load.text == '자세히 보기':
                    driver.execute_script('arguments[0].click();',load)
                else:
                    pass

            check_point_4 = time.time()
            print('자세히 보기 : {}'.format(check_point_4 - check_point_3))
            
            load_content = driver.find_elements_by_xpath('//*[@id="main"]')        

            content_length = len(load_content)
            print('총 리뷰: {}'.format(content_length))

            for i in tqdm(range(content_length)):
                
                try: #Youtube Premium이 걸릴경우가 있다
                    #ID
                    author = load_content[i].find_element_by_css_selector('#author-text span').text
                    content.append(author)
                except:
                    content.append('None')

                try:    
                    #리뷰
                    review = load_content[i].find_element_by_css_selector('#content-text').text
                    content.append(review)
                except:
                    content.append('None')
                try:
                    #like
                    like = load_content[i].find_element_by_css_selector('#vote-count-middle').text
                    content.append(like)
                except:
                    content.append('None')

                with open('TrendingVideo_{}.csv'.format(now), 'a', encoding='utf-8-sig', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(content)

                content = []

            
            end = time.time()
            print('댓글 크롤링 : {}'.format(end - check_point_4))
            print('처음-끝 : {}'.format(end - start))
            print('{}번째 동영상 끝'.format(j))
            print('--------------------------------')
            
            #대책없이 새창 열고 이전 창에 대한 관리를 안하면 메모리 오류가 나면서 죽어버린다
            driver.close() # 기존 창 닫고
            driver.switch_to.window(driver.window_handles[0]) #첫번째 창으로 이동 & 연결
            
        except:
            pass
        
if __name__ == "__main__":
    today_df = get_trending_video()
    today_df = check_df(today_df)
    YoutubeCrawler(today_df)

