# css 셀렉터를 이용
from bs4 import BeautifulSoup

html_page = """
<html>
<body>
<div id="hello">
    <a href="http://www.naver.com">naver</a><br>
    <span>
    <a href="http://www.daum.com">daum</a><br>
    </span>
    <ul class = "world">
        <li>안녕</li>
        <li>반가워</li>
    </ul>
</div>
<div id="hi" class="good">
    두번째 div
</div>
</body>
<html>
"""
# 연습용 HTML 문자열
# div, a, ul, li 태그를 이용해 CSS 선택자 연습용 구조 작성

soup = BeautifulSoup(html_page, 'html.parser')
# HTML 문자열을 BeautifulSoup 객체로 변환

# aa = soup.select_one("div")
# aa = soup.select_one("div#hello")
# aa = soup.select_one("div.good")
aa = soup.select_one("div#hello > a")
# id가 hello인 div 바로 아래에 있는 첫 번째 a 태그 1개 선택

print('aa : ', aa, ' ', aa.string)
# 선택한 a 태그 전체와 태그 안의 문자열 출력

print()
# 한 줄 공백 출력

# bb = soup.select("div")
# bb = soup.select("div#hello > ul.world")
# bb = soup.select("div#hello ul.world")
bb = soup.select("div#hello ul.world > li")
# id가 hello인 div 안에 있는 class가 world인 ul의
# 바로 아래 li 태그들을 모두 선택

print('bb : ', bb)
# 선택된 li 태그 목록 전체 출력

for i in bb:
    # li 태그들을 하나씩 반복

    print(i, ' ', i.text)
    # 각 li 태그 전체와 태그 안의 텍스트 출력

print("---위키백과 사이트에서 이순신으로 검색된 자료 읽기---------------")
import requests
# 웹페이지 요청을 보내기 위한 requests 모듈 import

url = "https://ko.wikipedia.org/wiki/이순신"
# 위키백과 이순신 문서 주소 저장

headers = {"User-Agent":"Mozilla/5.0"}
# 브라우저에서 접속한 것처럼 보이게 하기 위한 헤더 정보

wiki = requests.get(url=url, headers=headers)
# 해당 URL에 GET 요청을 보내고 응답 결과를 wiki 변수에 저장

# print(wiki.text[:100])
# 응답받은 HTML 문서 앞부분 100글자만 확인할 때 사용

soup = BeautifulSoup(wiki.text, 'html.parser')
# 위키백과에서 받은 HTML 문서를 BeautifulSoup 객체로 변환

result = soup.select("#mw-content-text p")
# CSS 선택자로 p 태그 중 id가 mwHw인 태그 선택
# 조건에 맞는 태그들을 리스트 형태로 반환

# print(result)
# 선택된 결과 전체를 확인할 때 사용

for s in result:
    # 선택된 p 태그들을 하나씩 반복

    for sup in s.find_all("sup"):
        # p 태그 안에 있는 모든 sup 태그 찾기
        # 보통 각주 번호가 sup 태그로 들어 있음

        sup.decompose()         # 태그 삭제

    print(s.get_text(strip=True))
    # 태그를 제외한 순수 텍스트만 출력

print("---교초치킨 사이트에서 메뉴,가격 자료 읽기------------")
import pandas as pd
url = "https://kyochon.com/menu/chicken.asp"
headers = {"User-Agent":"Mozilla/5.0"}
response = requests.get(url, headers=headers)
# print(response.text)

soup2 = BeautifulSoup(response.text, 'html.parser')
# 메뉴명 얻기
# names = soup2.select("dl.txt>dt")
# print(names)
names = [tag.text.strip() for tag in soup2.select("dl.txt>dt")]
# print(names)
prices =  [int(tag.text.strip().replace(',','')) for tag in soup2.select("p.money strong")]
# print(prices)

df = pd.DataFrame({"상품명":names, "가격": prices})
print(df.head(3))
print(f"가격 평균 : {df['가격'].mean():.2f}")
print(f"가격 표준편차 : {df['가격'].std():.2f}")
cv = df['가격'].std() / df['가격'].mean() * 100
print(f"가격 변동계수(CV)) : {cv:.2f}%")
# 해석 : 가격 변동계수(CV) : 28.31%이므로 평균 대비 적당히 퍼져 있는 편