# JSON 자료 : XML에 비해 경량, 배열 개념만 있으면 처리 가능
# JSON은 데이터를 문자열 형태로 주고받기 쉬운 자료 형식
# 파이썬에서는 보통 dict, list 형태로 바꿔서 사용함

import json
# JSON 데이터를 인코딩/디코딩하기 위한 json 모듈 import

dict = {'name':'tom','age':25, "score":['90','80','88']}  # dict type
# 파이썬 딕셔너리 자료 생성
# name, age, score 정보를 key:value 형태로 저장

print(dict, type(dict))
# dict 내용과 자료형 출력
# 현재는 파이썬의 dict 타입

print('json 인코딩 : dict -> str ---')
# 딕셔너리를 JSON 문자열로 바꾸는 과정 안내

str_val = json.dumps(dict)
# dict 타입을 JSON 형식의 문자열(str)로 변환
# dumps = dump string 이라고 생각하면 됨

# str_val = json.dumps(dict, indent=4)
# indent=4를 사용하면 보기 좋게 들여쓰기 된 JSON 문자열로 변환 가능

print(str_val, type(str_val))     # <class 'str'>
# 변환된 JSON 문자열과 자료형 출력
# 즉 JSON은 파이썬 안에서는 문자열로 다뤄짐

# print(str_val['name'])  # TypeError: string indices must be integers, not 'str'
# str_val은 문자열이므로 딕셔너리처럼 key로 접근 불가
# 문자열은 인덱스 번호로만 접근 가능

print(str_val[0:20])   # 문자열 관련 함수만 사용 가능
# JSON 문자열의 앞 20글자 출력
# 문자열 슬라이싱 예시

print('json 디코딩 : str -> dict ----')
# JSON 문자열을 다시 파이썬 dict로 바꾸는 과정 안내

json_val = json.loads(str_val)
# JSON 문자열(str)을 파이썬 딕셔너리(dict)로 변환
# loads = load string 이라고 생각하면 됨

print(json_val, type(json_val))      # <class 'dict'>
# 디코딩 결과와 자료형 출력
# 다시 dict 타입이 되었는지 확인

print(json_val['name'])              # dict 관련 명령 사용 가능
# dict 타입이므로 key를 사용해 값 접근 가능

for k in json_val.keys():
    # 딕셔너리의 모든 key를 하나씩 반복

    print(k)
    # key 값 출력

for v in json_val.values():
    # 딕셔너리의 모든 value를 하나씩 반복

    print(v)
    # value 값 출력

print("\n서울시 제공 도서관 정보 JSON 샘플 자료(5개) 읽기 --- ")
# 줄바꿈 후 안내 문구 출력
# 서울시 OpenAPI에서 JSON 형식 데이터 읽기 시작

import urllib.request as req
# URL에 접속해서 데이터를 읽기 위한 urllib.request 모듈 import

url = "http://openapi.seoul.go.kr:8088/sample/json/SeoulLibraryTimeInfo/1/5/"
# 서울시 도서관 정보 JSON 샘플 API 주소
# 1번부터 5번까지 총 5개 데이터 요청

plainText = req.urlopen(url).read().decode()
# urlopen(url) : URL 접속
# read() : 응답 데이터 읽기
# decode() : 바이트 데이터를 문자열로 변환

# print(plainText, type(plainText))   # <class 'str'>
# 받아온 데이터는 JSON 모양이어도 현재는 문자열(str) 상태

jsonData = json.loads(plainText)
# JSON 문자열을 파이썬 dict 타입으로 변환
# XML은 BeautifulSoup로 태그 구조를 읽지만,
# JSON은 loads()를 사용해서 바로 dict/list 구조로 바꿔 처리함

print(jsonData, type(jsonData))       # <class 'dict'>
# 변환된 데이터와 자료형 출력
# 최상위 JSON 객체가 {} 형태라서 dict 타입으로 변환됨
print(jsonData["SeoulLibraryTimeInfo"]["row"][0]["LBRRY_NAME"])

# dict의 get() 사용
print()
libData = jsonData.get("SeoulLibraryTimeInfo").get("row")
# jsonData 딕셔너리에서 "SeoulLibraryTimeInfo" 키의 값을 가져오고
# 그 안에서 다시 "row" 키의 값을 가져옴
# row에는 도서관 정보 여러 건이 리스트 형태로 저장되어 있음

# print(libData)
# row 데이터 전체를 확인하고 싶을 때 사용하는 출력문

name = libData[0].get('LBRRY_NAME')
# row 리스트의 첫 번째 데이터에서
# 'LBRRY_NAME' 키에 해당하는 도서관명 값 가져오기

print(name)
# 첫 번째 도서관명 출력

print()
# 한 줄 공백 출력

datas = []
# 도서관명, 전화번호, 주소를 저장할 빈 리스트 생성

for ele in libData:
    # row 리스트에 있는 각 도서관 정보를 하나씩 반복

    name = ele.get('LBRRY_NAME')
    # 현재 도서관 정보에서 도서관명 가져오기

    tel = ele.get('TEL_NO')
    # 현재 도서관 정보에서 전화번호 가져오기

    addr = ele.get('ADRES')
    # 현재 도서관 정보에서 주소 가져오기

    print(name, ' ', tel, ' ', addr)
    # 도서관명, 전화번호, 주소 출력

    datas.append([name, tel, addr])
    # 도서관명, 전화번호, 주소를 리스트로 만들어 datas에 추가

import pandas as pd
# 데이터프레임 생성을 위한 pandas 모듈 import

df = pd.DataFrame(datas, columns=['도서관명','전화','주소'])
# datas 리스트를 DataFrame으로 변환
# 각 열 이름을 도서관명, 전화, 주소로 지정

print(df)
# 완성된 DataFrame 출력