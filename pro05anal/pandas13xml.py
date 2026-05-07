# BeautifulSoup 모듈로 XML 문서 처리
from bs4 import BeautifulSoup
# bs4 라이브러리에서 BeautifulSoup 클래스 import
# XML 문서를 읽고 태그 단위로 분석하기 위해 사용

with open('my.xml', mode='r', encoding='utf-8') as f:
    # my.xml 파일을 읽기 모드로 열기
    # encoding='utf-8'은 한글 깨짐 방지용

    xmlfile = f.read()
    # 파일 전체 내용을 문자열로 읽어 xmlfile 변수에 저장

    print(xmlfile, type(xmlfile))       # <class 'str'>
    # 읽어온 XML 원문과 자료형 출력
    # 파일 내용은 문자열(str) 형태로 읽힘

soup = BeautifulSoup(xmlfile, 'lxml')
# XML 문자열을 BeautifulSoup 객체로 변환
# lxml 파서를 사용하여 XML 문서를 분석

print(type(soup))      # <class 'bs4.BeautifulSoup'>
# soup 객체의 자료형 출력
# BeautifulSoup 객체인지 확인

itemTag = soup.find_all('item')
# XML 문서 안의 모든 item 태그를 찾아 리스트로 반환

print(itemTag[1])
# item 태그들 중 두 번째 item 태그 출력
# 인덱스는 0부터 시작하므로 [1]은 두 번째 요소

print()
# 한 줄 공백 출력

nameTag = soup.find_all('name')
# XML 문서 안의 모든 name 태그를 찾아 리스트로 반환

print(nameTag[0]['id'])
# 첫 번째 name 태그의 id 속성값 출력
# 예: <name id="1">홍길동</name> 이면 1 출력

print('-----------')
# 구분선 출력

for i in itemTag:
    # item 태그들을 하나씩 반복

    nameTag = i.find_all('name')
    # 현재 item 태그 안에 있는 모든 name 태그 찾기

    for j in nameTag:
        # 찾은 name 태그들을 하나씩 반복

        print("id:" + j["id"] + " name:" + j.string)
        # name 태그의 id 속성값과 문자열 내용 출력
        # j["id"] 는 id 속성값
        # j.string 은 태그 사이의 텍스트 내용

        tel = i.find("tel")
        # 현재 item 태그 안에서 첫 번째 tel 태그 찾기

        print("tel:", tel.string)
        # tel 태그 안의 문자열 출력
        # 예: 전화번호 출력

    for j in i.find_all('exam'):
    # 현재 item 태그(i) 안에 있는 모든 exam 태그를 하나씩 반복

        print("kor:" + j["kor"] + ", eng:" + j["eng"])
    # exam 태그의 kor 속성과 eng 속성값 출력
    # 예: <exam kor="90" eng="80"></exam> 이면 kor:90, eng:80 출력

print()
# item 하나의 exam 정보 출력이 끝난 뒤 한 줄 공백 출력

print("\n서울시 제공 도서관 정보 XML 샘플 자료(5개) 읽기 --- ")
# 줄바꿈 후 안내 문구 출력
# 서울 열린데이터광장에서 제공하는 XML 샘플 데이터 읽기 시작

import urllib.request as req
# 웹 주소로 요청을 보내고 데이터를 읽기 위한 urllib.request 모듈 import

import pandas as pd
# 표 형태 데이터 처리를 위한 pandas 모듈 import

url = "http://openapi.seoul.go.kr:8088/sample/xml/SeoulLibraryTimeInfo/1/5/"
# 서울시 도서관 정보 XML 샘플 API 주소
# 1부터 5까지 총 5개의 데이터 요청

plainText = req.urlopen(url).read().decode()
# urlopen(url) : 해당 URL에 접속
# read() : 응답받은 데이터 읽기
# decode() : 바이트 데이터를 문자열로 변환

# print(plainText)
# 받아온 XML 원문 전체를 확인하고 싶을 때 사용하는 출력문

xmlObj = BeautifulSoup(plainText, 'xml')
# XML 문자열을 BeautifulSoup 객체로 변환
# 이번에는 XML 문서이므로 'xml' 파서 사용

libData = xmlObj.select('row')
# XML 문서 안의 모든 row 태그 선택
# 각 row가 도서관 1건의 정보라고 보면 됨

# print(libData)
# row 태그 전체를 확인하고 싶을 때 사용하는 출력문

rows = []
# 도서관명과 주소를 딕셔너리 형태로 저장할 빈 리스트 생성

for data in libData:
    # row 태그들을 하나씩 반복

    name = data.find("LBRRY_NAME").string
    # 현재 row 안에서 LBRRY_NAME 태그를 찾아 도서관명 추출

    addr = data.find("ADRES").string
    # 현재 row 안에서 ADRES 태그를 찾아 주소 추출

    print('도서관명:', name)
    # 도서관명 출력

    print('주소:', addr)
    # 주소 출력

    print()
    # 각 도서관 정보 출력 후 한 줄 공백

    rows.append({"도서관명": name, "주소": addr})
    # 도서관명과 주소를 딕셔너리로 만들어 rows 리스트에 추가

df = pd.DataFrame(rows)
# rows 리스트를 DataFrame으로 변환
# 열 이름은 도서관명, 주소

print(df)
# DataFrame 전체 출력

print("건수 : ", len(df))
# DataFrame 행 개수 출력
# 현재 저장된 도서관 정보 건수 확인