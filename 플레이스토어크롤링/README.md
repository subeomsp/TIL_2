# 구글 플레이스토어 리뷰 크롤링

- 필립 코틀러는 마켓 4.0에서 소비자들이 정보를 얻는 창구로 기업의 일방적인 광고가 아닌 커뮤니티, SNS 등을 활용한다고 지적했습니다.

   이에 따라 소비자들이 서비스에 대한 의견을 적극 피력할 수 있는 구글 플레이스토어의 리뷰를 크롤링하고, 분석하는 것이 점차 가치있을 것이라 생각합니다. 

- 그러니 구글 플레이스토어 리뷰를 크롤링합시다.

  - 구글 플레이스토어의 경우, 하단의 더보기 버튼을 추가해야 새로운 리뷰 데이터를 불러올 수 있기 때문에 BeautifulSoup 뿐만 아니라 Selenium을 활용해야 합니다. 이게 우리 대신에 더보기 버튼을 클릭해줄 수 있을거에요.
  - Selenium 활용을 위해 사용자의 크롬 버전에 맞는 chrome driver 다운로드가 필요합니다.
    - url = https://chromedriver.chromium.org/downloads
  - 스크롤 횟수(scroll_cnt) 변수를 조절하여 불러오길 원하는 리뷰의 양을 조절할 수 있습니다.

  ### 주의사항

  - 하단의 link = '링---크' 에서 링--크 부분을 원하는 어플리케이션의 url로 변경하여 사용합니다.
  - 이때, 어플리케이션사 정보를 기준으로 고객의 리뷰와 어플리케이션사의 리뷰를 구분지었기 때문에 원하는 어플리케이션에 해당하는 기준점을 찾으셔야 할 겁니다.
    - 현재는 '(.+)\nRainist Co.' / 'Rainist Co., Ltd.' 가 기준점으로 되어있습니다.
    - 보다 좋은 방법을 찾아보겠습니다.



# 구글 플레이스토어 리뷰 분석

- 분석은 비교적 단순하게

  1. 어플리케이션사가 답변을 해준 비율, 그리고 이에 걸리는 시간
  2. 리뷰에서 자주 등장한 명사 기준 워드 클라우드, 해당 키워드가 포함된 리뷰 산출

    두 가지 방식으로 이루어졌습니다.

- 1번의 경우, 해당 어플리케이션사가 고객과의 커뮤니케이션에 얼마나 신경쓰고 있는지를 보여주는 지표가 될 수 있겠죠.

- 2번의 경우 추후 명사 뿐 아니라 다른 품사를 추가하고, 모델링을 통한 감성분석을 해볼 생각입니다.



