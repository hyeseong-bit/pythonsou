import requests
# 웹페이지에 접속해서 HTML 데이터를 가져오기 위한 requests 모듈 import

from bs4 import BeautifulSoup
# HTML 문서를 파싱해서 원하는 태그를 쉽게 찾기 위한 BeautifulSoup import

import sys
# 표준 입출력 관련 기능을 사용하기 위한 sys 모듈 import

import time
# 일정 시간마다 반복 실행하기 위해 time 모듈 import

sys.stdout.reconfigure(encoding="utf-8")
# 한글이 깨지지 않도록 표준 출력 인코딩을 utf-8로 재설정

ur1 = "https://finance.naver.com/marketindex/"
# 네이버 금융 시장지표 페이지 주소 저장

headers = {"User-Agent": "Mozilla/5.0"}
# 웹 브라우저로 접속한 것처럼 보이게 하기 위한 요청 헤더 설정

while True:
    # 무한 반복 실행
    # 아래 작업을 계속 반복하면서 일정 시간마다 환율 정보 읽기

    res = requests.get(url=ur1, headers=headers)
    # 지정한 URL에 GET 요청을 보내고 응답 결과를 res에 저장

    soup = BeautifulSoup(res.content, 'html.parser')
    # 응답받은 HTML 문서를 BeautifulSoup 객체로 변환

    nation = soup.select_one("h3.h_lst span.blind").get_text(strip=True)
    # h3 태그(class=h_lst) 안의 span 태그(class=blind) 1개 선택
    # 국가명/통화명 텍스트 추출
    # 예: 미국 USD

    # print(nation)    # 미국 USD
    # 국가명 확인용 출력문

    # 환율값
    price = soup.select_one(".value").get_text(strip=True)
    # class가 value인 태그를 선택해서 환율값 추출
    # 예: 1,508.80

    # print(price)     # 1,508.80
    # 환율값 확인용 출력문

    unit = soup.select_one(".txt_krw .blind").get_text(strip=True)
    # class가 txt_krw인 영역 안의 class=blind 태그를 선택해서 단위 추출
    # 예: 원

    # print(unit)
    # 단위 확인용 출력문

    change = soup.select_one(".change").get_text(strip=True)
    # class가 change인 태그를 선택해서 전일 대비 변동값 추출
    # 예: 2.00

    # print(change)
    # 변동값 확인용 출력문

    updown = soup.select(".head_info.point_up span.blind")[-1].get_text(strip=True)
    # class가 head_info point_up인 영역 안의 span 태그(class=blind)들을 모두 선택
    # 그중 마지막 값을 가져와 상승/하락 상태 텍스트 추출
    # 현재 코드는 상승(point_up)인 경우를 기준으로 작성됨

    # print(updown)
    # 상승/하락 상태 확인용 출력문

    print(f"{nation.replace(' ','')} {price}{unit} {updown} {change}")
    # 최종 결과를 한 줄로 출력
    # nation.replace(' ','') 는 국가명 사이 공백 제거
    # 예: 미국USD 1,508.80원 상승 2.00

    time.sleep(5)
    # 5초 동안 대기한 후 다시 반복