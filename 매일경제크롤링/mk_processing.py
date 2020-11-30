#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
import re
import pickle

class mk_processing:
    def __init__(self, df):
        #Scrapy를 이용해 크롤링한 파일 불러오기
        self.df = df

    #매일경제 기사에도 연합뉴스 기사가 포함되어 있고, 형식이 다르다. 이를 구분짓기 위한 함수
    def seperate_article(self, df):
        yh_article = []
        mk_article = []
        etc_article = []
        for article in self.df['content']:
            if '연합뉴스' in article and '매일경제' not in article:
                yh_article.append(article)
            elif '매일경제' in article:
                mk_article.append(article)
            else:
                etc_article.append(article)
        return yh_article, mk_article

    #연합뉴스 기사 전처리 함수
    def yh_processing(self, articles):
        processed_article = []
        for article in articles:
            article = re.sub('\<script\>(.+?)\(', '', article)
            article = re.sub('\>(.+?)\<\/fig','', article)
            article = re.sub('\<.+?\>','', article)
            article = re.sub('googletag.+?\;', '', article)
            article = re.sub('연합뉴스+.+','', article)
            article = re.sub('\n', '', article)
            article = re.sub('\t', '', article )
            article = re.sub('\r', '', article.strip())
            article = re.sub('\s\s+', '', article.strip())
            article = re.sub('\s\.', '', article.strip())
            article = re.sub('▶ 여기를 누르시면 크게 보실 수 있습니다', '', article)
            article = re.sub('연합뉴스+.+','', article)
            article = re.sub('.... 원본사이즈 보기 ....', '', article)
            article = re.sub('.... 사진설명', '', article)
            article = re.sub('\.\.\.\.', '', article)
            article = re.sub('사진 출처', '', article)
            article = re.sub('사진 제공', '', article)
            article = re.sub('\[\"\"\)', '', article)
            processed_article.append(article.strip())        
        return processed_article

    #매일경제 기사 전처리 함수
    def mk_processing(self, articles):
        processed_article = []
        for article in articles:
            article = re.sub('\<script\>(.+?)\(', '', article)
            article = re.sub('\>(.+?)\<\/fig','', article)
            article = re.sub('\<.+?\>','', article)
            article = re.sub('googletag.+?\;', '', article)
            article = re.sub('\[\ⓒ.+?]', '',article)
            article = re.sub('\[[가-힣 ]+?\]', '', article)
            article = re.sub('\n', '', article)
            article = re.sub('\t', '', article )
            article = re.sub('\r', '', article.strip())
            article = re.sub('\s\s+', '', article.strip())
            article = re.sub('\s\.', '', article.strip())
            article = re.sub('▶ 여기를 누르시면 크게 보실 수 있습니다', '', article)
            article = re.sub('연합뉴스+.+','', article)
            article = re.sub('.... 원본사이즈 보기 ....', '', article)
            article = re.sub('.... 사진설명', '', article)
            article = re.sub('\.\.\.\.', '', article)
            article = re.sub('사진 출처', '', article)
            article = re.sub('사진 제공', '', article)
            article = re.sub('\[\"\"\)', '', article)
            article = re.sub('\"\"\)', '', article)
            processed_article.append(article.strip())        
        return processed_article

def saving(df):
    processing = mk_processing(df)
    yh_art, mk_art = processing.seperate_article(df)
    yh_pro = processing.yh_processing(yh_art) #연합뉴스 기사 전처리
    mk_pro = processing.mk_processing(mk_art) #매일경제 기사 전처리

    total_article = yh_pro + mk_pro #기사 병합

    processed_df = pd.DataFrame(total_article, columns = ['text'])
    processed_df.to_pickle('mk_processed.pkl') #기사 저장
    print('전처리 완료')
        
        
if __name__ == "__main__":
    mk = pd.read_csv('mk_crawl.csv')
    saving(mk)

