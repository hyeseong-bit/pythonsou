from bs4 import BeautifulSoup  # BeautifulSoup 클래스 불러오기

html_page = """
<html><body>
<h1>제목 태그</h1>
<p>웹문서 연습</p>
<p>원하는 자료 확인</p>
</body></html>
"""
# 연습용 HTML 문자열

print(type(html_page))  # html_page 자료형 출력(str)

soup = BeautifulSoup(html_page, 'html.parser')  # HTML 문자열을 파싱
print(type(soup))  # BeautifulSoup 객체 자료형 출력

print()

h1 = soup.html.body.h1  # html > body > h1 태그 선택
print("h1: ", h1.string)  # h1 태그의 문자열 출력

p1 = soup.html.body.p  # 첫 번째 p 태그 선택
print("p1: ", p1.string)  # 첫 번째 p 태그 내용 출력

p2 = p1.next_sibling.next_sibling  # 다음 형제 노드를 따라 두 번째 p 태그 선택
print("p2: ", p2.string)  # 두 번째 p 태그 내용 출력

print('\n-- find() method 사용 -----------')
html_page2 = """
<html><body>
<h1 id="title">제목 태그</h1>
<p>웹문서 연습</p>
<p id="my" class="our">원하는 자료 확인</p>
</body></html>
"""
# 속성이 포함된 두 번째 HTML 문자열

soup2 = BeautifulSoup(html_page2, 'html.parser')  # 두 번째 HTML도 파싱

# find(태그명, 속성, ...)
print(soup2.p, ' ', soup2.p.string)          # 첫 번째 p 태그 전체와 문자열 출력
print(soup2.find('p').string)                # 첫 번째 p 태그의 문자열 출력  # find(['p','h1'])
print(soup2.find('p', id="my").string)       # p 태그 중 id가 "my"인 태그의 문자열 출력
print(soup2.find(id="title").string)         # id가 "title"인 태그의 문자열 출력
print(soup2.find(id="my").string)            # id가 "my"인 태그를 찾아 문자열 출력
print(soup2.find(class_="our").string)       # class가 "our"인 태그를 찾아 문자열 출력
print(soup2.find(attrs={"class":"our"}).string)   # attrs 속성으로 class가 "our"인 태그를 찾아 문자열 출력
print(soup2.find(attrs={"id":"my"}).string)       # attrs 속성으로 id가 "my"인 태그를 찾아 문자열 출력
print()

print('\n-- find_all(), findAll() method 사용 -----------')
# 줄바꿈 후 안내 문구 출력
# find_all() / findAll() 메소드 사용 예제 시작

html_page3 = """
<html><body>
<h1 id="title">제목 태그</h1>
<p>웹문서 연습</p>
<p id="my" class="our">원하는 자료 확인</p>
<div>
    <a href="https://www.naver.com">naver</a><br/>
    <a href="https://www.daum.com">daum</a>
</div>
</body></html>
"""
# a 태그와 div 태그가 포함된 새로운 HTML 문자열 작성
# 링크 정보 추출 연습용 데이터

soup3 = BeautifulSoup(html_page3, 'html.parser')
# html_page3 문자열을 BeautifulSoup 객체로 변환

print(soup3.find_all(['a']))
# 문서 안의 모든 a 태그를 리스트 형태로 찾아 출력

print(soup3.find_all(['a','p']))
# 문서 안의 모든 a 태그와 p 태그를 리스트 형태로 찾아 출력

print()
# 한 줄 공백 출력

links = soup3.find_all('a')
# 모든 a 태그를 찾아 links 변수에 저장

# print(links)
# links 전체 내용을 보고 싶을 때 사용하는 출력문

for i in links:
    # links에 저장된 a 태그들을 하나씩 반복

    href = i.attrs["href"]
    # a 태그의 href 속성값 추출
    # 예: https://www.naver.com

    text = i.text
    # a 태그 사이의 문자열 추출
    # i.string으로도 가능

    print(href, " ", text)
    # 링크 주소와 링크 텍스트 출력

print('\n정규표현식 사용---')
# 줄바꿈 후 정규표현식 사용 예제 시작

import re
# 정규표현식 처리를 위한 re 모듈 import

links2 = soup3.find_all(href=re.compile(r'^https'))
# href 속성값이 https로 시작하는 모든 태그 찾기
# ^ 는 시작 의미
# 즉 https로 시작하는 링크만 검색

# print(links2)
# 조건에 맞는 태그 전체를 보고 싶을 때 사용하는 출력문

for k in links2:
    # 검색된 태그들을 하나씩 반복

    print(k.attrs['href'])
    # 각 태그의 href 속성값만 출력

print("--- bugs 사이트 음악 순위 읽기---------------")
# 실제 웹사이트에서 음악 순위 읽기 예제 시작

import requests
# 웹페이지 요청을 보내기 위한 requests 모듈 import

url = "https://music.bugs.co.kr/chart"
# 벅스 실시간 차트 페이지 주소 저장

response = requests.get(url)
# 해당 URL로 GET 요청을 보내고 응답 결과를 response에 저장

# print(response.text)
# 서버에서 받은 HTML 원문 전체를 보고 싶을 때 사용하는 출력문

bsoup = BeautifulSoup(response.text, 'html.parser')
# 응답받은 HTML 문서를 BeautifulSoup 객체로 변환

musics = bsoup.find_all("td", class_="check")
# td 태그 중 class가 "check"인 모든 태그 찾기
# 벅스 차트에서 곡 제목 정보가 들어 있는 부분을 선택

for idx, music in enumerate(musics):
    # musics 리스트를 하나씩 반복하면서
    # idx에는 순번, music에는 각 태그가 들어감

    print(f"{idx + 1}위) {music.input['title']}")
    # 각 곡의 input 태그에 있는 title 속성값 출력
    # idx + 1로 순위를 1위부터 표시 