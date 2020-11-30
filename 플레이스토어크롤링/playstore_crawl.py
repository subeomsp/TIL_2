#!/usr/bin/env python
# coding: utf-8

# 구글 플레이스토어의 경우, 더보기 버튼을 클릭해야 새로운 리뷰 정보를 받아올 수 있는 구조기에 셀레니움을 통한 동적 크롤링이 필요

# In[33]:


import time
import re
import pandas as pd
import numpy as np
import requests
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver

def review_crawl(link):
    link = link
    
    #리뷰를 담을 딕셔너리 생성
    data_info = {
        '리뷰' : [],
        '날짜' : [],

         #고객 리뷰에 대한 답변 유무, 답변까지의 기간에 따라 회사의 고객 커뮤니케이션에 관심도를 파악할 수 있다고 생각
        '답여부' : [],
        '답변일' : [],
            }

    #스크롤 횟수
    scroll_cnt = 20

    #자신의 크롬 버전에 맞는 드라이버 다운
    driver = webdriver.Chrome('./chromedriver') #크롬 드라이버 경로
    driver.get(link)

    for i in range(scroll_cnt):
      driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
      #화면의 맨 아래로 이동 이후, 새로운 리뷰를 로딩할때까지
      time.sleep(10)

      try:
        #더보기 클릭으로 새로운 리뷰 불러오기
        load_more = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span').click()
      except:
        pass
    
    data = driver.find_elements_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div/div/div/div[2]')

    for d in data:
        #어플리케이션사의 답변이 있는 경우와 없는 경우를 날짜의 수를 통해 구분
        filt = len(re.findall('.+년 .+월 .+일', d.text))

        if filt == 1:
            data_info['리뷰'].append(d.text.split('\n')[-1])
            data_info['날짜'].append(re.findall('.+년 .+월 .+일', d.text)[0])
            data_info['답여부'].append('N')
            data_info['답변일'].append('N')

        elif filt == 2:
            data_info['리뷰'].append(re.findall('(.+)\nRainist Co., Ltd.', d.text)[0])
            data_info['날짜'].append(re.findall('.+년 .+월 .+일', d.text)[0])
            data_info['답여부'].append('Y')

            #고객 리뷰에 대한 답변 리뷰 시간
            gap = re.findall('.+년 .+월 .+일', d.text)[1]
            gap = re.sub('Rainist Co., Ltd.','', gap)
            data_info['답변일'].append(gap)

        banksalad = pd.DataFrame(data_info)
        banksalad.to_pickle('banksalad_review.pkl')
        
if __name__ == "__main__":
    link = 'https://play.google.com/store/apps/details?id=com.rainist.banksalad2&hl=ko&showAllReviews=true'
    review_crawl(link)

