import xml.etree.ElementTree as etree
# XML 데이터를 처리하기 위한 ElementTree 모듈 import

xmlfile = etree.parse("my.xml")
# my.xml 파일을 읽어 XML 트리 객체로 생성

print(xmlfile, type(xmlfile))
# xmlfile 객체와 자료형 출력
# 보통 ElementTree 객체로 나옴

root = xmlfile.getroot()
# XML 문서의 최상위 루트(root) 요소 얻기

print(root.tag)
# 루트 요소의 태그명 출력

print(root[0].tag)   # root 요소의 0번째 요소명(노드명) 얻기
# 루트의 첫 번째 자식 요소 태그명 출력

print(root[0][0].tag)
# 루트의 첫 번째 자식의 첫 번째 자식 요소 태그명 출력

print()

myname = root.find("item").find("name").text
# 첫 번째 item 요소를 찾은 뒤,
# 그 안의 name 요소를 찾아 텍스트 값 추출

mytel = root.find("item").find("tel").text
# 첫 번째 item 요소 안의 tel 요소를 찾아 텍스트 값 추출

print(myname + " " + mytel)
# name과 tel 값을 공백으로 연결해 출력

print('\n--- 기상청 제공 XML 자료 읽기--------------')

import requests
# 웹에서 XML 자료를 가져오기 위한 requests 모듈 import

url = "https://www.kma.go.kr/XML/weather/sfc_web_map.xml"
# 기상청 XML 자료 주소

headers = {"User-Agent":"Mozilla/5.0"}
# 웹 요청 시 브라우저처럼 보이도록 User-Agent 설정

res = requests.get(url, headers=headers)
# 기상청 사이트에 GET 요청 보내기

res.raise_for_status()
# 요청 실패 시 예외 발생
# 정상 응답이면 그냥 다음 줄 실행

print(res.status_code)
print(res.text[:300], type(res.text))
# 응답 내용 일부와 자료형 출력
# XML 형태의 문자열(str)로 들어오는지 확인

root = etree.fromstring(res.text)
# 응답으로 받은 XML 문자열을 Element 객체로 변환

print(root)
# XML의 루트 요소 객체 출력

# {current} namespace 제거
for elem in root.iter():
    # 루트 이하의 모든 요소를 하나씩 반복
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]   # '}'를 기준으로 잘라 태그명 얻기

# {current}weather -> weather

weather = root.find('weather')
print(weather)
# weather 요소 찾기 확인

year = weather.get('year')    # 속성값 얻기
month = weather.get('month')  # 속성값 얻기
day = weather.get('day')      # 속성값 얻기
hour = weather.get('hour')    # 속성값 얻기

print(f"{year}년 {month}월 {day}일 {hour}시 현재 예보")
# 연, 월, 일, 시를 보기 좋게 출력

# 각 지역(local tag) 순회
for local in weather.findall("local"):
    name = local.text.strip() if local.text else ""   # 태그 안의 텍스트
    ta = local.get('ta')  # local 요소(엘리먼트)의 ta 속성
    print(f"{name} 지역 온도는 {ta}")