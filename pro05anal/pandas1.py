# 고수준의 자료구조(Series, DataFrame)와 빠르고 쉬운 데이터 분석용 함수 제공
# 통합된 시계열 연산, 축약연삭, 누락 데이터 처리, SQL, 시각화 ... 등을 제공
# 데이터 랭글링(Data Wrangling), 데이터 먼징(Data Munging) 을 효율적으로 처리 가능

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# Series : 일련의 객체를 담을 수 있는데 1차원 배열과 겉운 자료구조로 색인(index)을 갖는다.
obj = pd.Series([3, 7, -5, 4])

# obj = pd.Series([3, 7, -5, '점심 뭐 먹지'])  # 요소값은 object type
# -> 숫자와 문자열이 섞이면 자료형이 object로 처리됨

# obj = pd.Series((3, 7, -5, 4))
# -> 리스트 대신 튜플로도 Series 생성 가능

# obj = pd.Series({3, 7, -5, 4}) # TypeError: 'set' type is unordered
# -> set은 순서가 없어서 Series 생성 시 오류 발생

print(obj, type(obj))
# -> obj의 값과 자료형 출력
# -> type(obj)는 pandas.core.series.Series 형태로 나옴

obj2 = pd.Series([3, 7, -5, 4], index=['a','b','c','d'])
# -> 값은 [3, 7, -5, 4]
# -> 인덱스는 기본 숫자 대신 a, b, c, d로 지정

print(obj2)
# -> 사용자 정의 인덱스를 가진 Series 출력

print(obj2.sum(), ' ', np.sum(obj2), ' ', sum(obj2))
# -> 세 가지 방식으로 합계 출력
# -> obj2.sum() : pandas 메서드
# -> np.sum(obj2) : numpy 함수
# -> sum(obj2) : 파이썬 내장 함수
# -> 결과는 모두 같은 합계가 나옴

print(obj2.std())
# -> 표준편차 출력
# -> 데이터가 평균으로부터 얼마나 퍼져 있는지 나타냄

print(obj2.values)
# -> Series의 값들만 numpy 배열 형태로 출력

print(obj2.index)
# -> Series의 인덱스 정보 출력
# -> Index(['a', 'b', 'c', 'd'], dtype='object') 형태로 나옴

print(obj2['a'])
# -> 인덱스가 'a'인 값 1개만 가져오기
# -> 결과는 스칼라 값(하나의 값)으로 출력됨

print(obj2[['a']])
# -> 인덱스가 'a'인 값을 리스트 형태로 지정해서 가져오기
# -> 결과는 Series 형태로 출력됨
# -> 대괄호를 한 번 더 쓰면 여러 개를 뽑는 방식과 같은 형태가 됨


print(obj2[['a']])
# -> 인덱스가 'a'인 값을 리스트 형태로 지정해서 가져오기
# -> 결과는 Series 형태로 출력됨
# -> 대괄호를 한 번 더 쓰면 여러 개를 뽑는 방식과 같은 형태가 됨

print(obj2[['a', 'b']])
print(obj2['a':'c'])
print(obj2[['a', 'b']])
# -> 인덱스가 'a', 'b'인 값들을 선택
# -> 여러 개를 가져오므로 결과는 Series 형태로 출력됨
# -> fancy indexing(리스트 인덱싱) 방식

print(obj2[['a', 'b']])
# -> 인덱스가 'a', 'b'인 값들을 선택
# -> 여러 개를 가져오므로 결과는 Series 형태로 출력됨
# -> fancy indexing(리스트 인덱싱) 방식

print(obj2['a':'c'])
# -> 인덱스 'a'부터 'c'까지 범위로 선택
# -> 슬라이싱이므로 결과는 Series 형태로 출력됨
# -> pandas의 라벨 슬라이싱은 끝값 'c'도 포함됨

print(obj2[2])      # 인덱스 사용
# -> 위치(순서) 기준으로 2번째가 아니라, 0부터 시작하므로 세 번째 값 가져오기
# -> 현재 obj2에서는 값 -5가 출력됨
# -> 정수 한 개를 넣으면 위치 기반으로 동작함

print(obj2.iloc[2])
# -> iloc는 위치 기반 인덱싱
# -> 0, 1, 2 ... 같은 순서 번호로 값 선택
# -> 세 번째 값인 -5가 출력됨

print(obj2[1:4])
# -> 위치 기준 슬라이싱
# -> 1번 위치부터 4번 직전 위치까지 선택
# -> 즉, 두 번째~네 번째 값 선택
# -> 결과는 Series 형태로 출력됨

print(obj2[[2, 1]])
# -> 위치 번호 리스트를 사용해 여러 값 선택
# -> 2번 위치 값, 1번 위치 값을 순서대로 가져옴
# -> 결과는 Series 형태로 출력됨

print(obj2.iloc[[2, 1]])
# -> iloc로 위치 기반 여러 값 선택
# -> 2번 위치, 1번 위치 값을 차례대로 가져옴
# -> 결과는 Series 형태로 출력됨
# -> 위의 obj2[[2, 1]]와 같은 결과

print('a' in obj2)
# -> 'a'가 obj2의 값에 있는지 보는 게 아니라 인덱스에 있는지 확인
# -> 인덱스 'a'가 있으므로 True

print('k' in obj2)
# -> 'k'가 obj2의 인덱스에 있는지 확인
# -> 인덱스 'k'는 없으므로 False

print('파이썬 dict 자료를 Series 객체로 생성')
names = {'mouse':5000, 'keyboard':25000, 'monitor':45000}
# -> 딕셔너리 생성
# -> key는 상품명, value는 가격
# -> {'이름':값} 형태로 저장됨

print(names)
# -> 딕셔너리 전체 출력

obj3 = Series(names)
# -> 딕셔너리를 Series로 변환
# -> 딕셔너리의 key는 인덱스(index)가 되고
# -> 딕셔너리의 value는 값(data)이 됨

print(obj3, ' ', type(obj3))
# -> Series로 변환된 결과와 자료형 출력
# -> type(obj3)는 pandas.core.series.Series 형태

obj3.index = ['마우스','키보드','모니터']
print(obj3, ' ', type(obj3))

obj3.name = "상품가격"
print(obj3)

print('\nDataFrame 객체 ---------')
obj3.index = ['마우스','키보드','모니터']
# -> 기존 Series의 인덱스 이름 변경
# -> 원래 mouse, keyboard, monitor 였던 인덱스를
# -> 한글인 마우스, 키보드, 모니터로 바꿈

print(obj3, ' ', type(obj3))
# -> 인덱스가 바뀐 obj3 출력
# -> 자료형도 함께 출력
# -> type(obj3)는 여전히 Series

obj3.name = "상품가격"
# -> Series 자체의 이름(name) 지정
# -> Series 출력 시 이름이 함께 표시될 수 있음
# -> DataFrame으로 바꿀 때 열 이름으로 사용될 수도 있음

print(obj3)
# -> 이름이 지정된 Series 출력

print('/nDataFrame 객체 ---------')

df = pd.DataFrame(obj3)
# -> Series를 DataFrame으로 변환
# -> 1차원 Series가 2차원 DataFrame 형태로 바뀜
# -> 보통 Series의 name이 열 이름이 됨

print(df, ' ', type(df))
# -> DataFrame으로 변환된 df 출력
# -> 자료형도 함께 출력
# -> type(df)는 pandas.core.frame.DataFrame

data = {
    'irum':['홍길동','한국인','신기해','공깃밥','한가해'],
    'juso':('역삼동','신당동','역삼동','역삼동','신시동'),
    'nai':[23,25,33,231,35],
}
# -> 딕셔너리 형태로 데이터 준비
# -> key는 열 이름(column)이 됨
# -> value는 각 열에 들어갈 데이터 목록
# -> irum : 이름
# -> juso : 주소
# -> nai : 나이

frame = pd.DataFrame(data)
# -> 딕셔너리를 DataFrame으로 변환
# -> 각 key가 컬럼명이 되고
# -> 각 value의 값들이 행 단위로 들어감

print(frame)
# -> 생성된 DataFrame 출력
# -> 표 형태로 보임

print()
print(frame['irum'])
# -> DataFrame에서 'irum' 열(column)만 선택
# -> 결과는 Series 형태로 출력됨
# -> 보통 컬럼명을 문자열로 지정해서 가져오는 기본 방식

print(frame.irum)
# -> 위와 같은 의미로 'irum' 열 선택
# -> 점(.)으로도 컬럼 접근 가능
# -> 단, 컬럼명이 공백이 있거나 특수문자면 이 방식은 사용하기 어려움

print(type(frame.irum))
# -> frame.irum으로 가져온 자료형 확인
# -> 결과는 pandas의 Series 자료형

print(DataFrame(data=data, columns=['juso','irum','nai']))
# -> data를 이용해 DataFrame 생성
# -> columns 순서를 직접 지정해서 출력
# -> 원래 딕셔너리 순서와 상관없이 juso, irum, nai 순서로 열이 배치됨

# NaN (결측치)
# -> NaN은 값이 비어 있는 상태를 의미함
# -> 없는 데이터, 누락된 데이터를 표시할 때 사용

frame2 = pd.DataFrame(data,columns=['irum','nai','juso','tel'],
                    index=['a','b','c','d','e'])
# -> data를 이용해 새로운 DataFrame 생성
# -> 열 순서를 irum, nai, juso, tel 순서로 지정
# -> index도 a, b, c, d, e 로 직접 지정
# -> 기존 data에는 'tel' 열이 없기 때문에 해당 열은 NaN으로 채워짐
# -> 행 개수는 각 데이터 개수에 맞춰 5개 생성됨

print(frame2)

frame2['tel'] = '111-1111'
# -> frame2의 'tel' 열 전체에 같은 값 저장
# -> 모든 행(a, b, c, d, e)에 '111-1111'이 들어감
# -> 하나의 값을 넣으면 전체 행에 동일하게 적용됨

print(frame2)
# -> 'tel' 열이 모두 '111-1111'로 채워진 DataFrame 출력

val = pd.Series(['222-2222','333-3333','444-4444'], index=['b','c','e'])
# -> Series 생성
# -> 값은 전화번호 3개
# -> 인덱스는 b, c, e
# -> 즉, 특정 행에만 대응되는 데이터라고 볼 수 있음

print(val)
# -> 생성한 Series 출력
# -> b, c, e 인덱스에만 값이 들어 있음

frame2['tel'] = val
# -> frame2의 'tel' 열에 Series 대입
# -> 인덱스 기준으로 맞는 행에만 값이 들어감
# -> b, c, e 행에는 각각 전화번호가 들어가고
# -> a, d 행은 해당 인덱스가 없으므로 NaN이 됨

print(frame2)
# -> 인덱스 기준으로 반영된 최종 DataFrame 출력
# -> a, d는 NaN
# -> b, c, e는 val의 값으로 변경됨

print()
print(frame2.T)  # 전치

print()
print(frame2.values)   # 결과는 list type
print(frame2.values[0, 1]) 
# -> frame2의 값들만 numpy 배열 형태로 본 후
# -> [0, 1] 위치의 값 가져오기
# -> 0행 1열의 값 선택
# -> 보통 첫 번째 행, 두 번째 열 값이 출력됨

print(frame2.values[0:2]) 
# -> frame2의 값들만 numpy 배열 형태로 본 후
# -> 0행부터 1행까지 가져오기 (2행 직전까지)
# -> 즉, 앞의 두 행 데이터가 배열 형태로 출력됨

frame3 = frame2.drop('d')
# -> 인덱스가 'd'인 행 삭제
# -> 기본 axis=0 이므로 행 삭제 의미
# -> 원본 frame2는 그대로이고, 삭제 결과를 frame3에 저장

# print(frame3) = frame2.drop('d', axis=0)  # 행 삭제
# -> 같은 의미 설명
# -> axis=0은 행 방향 삭제

print(frame3)
# -> 'd' 행이 삭제된 결과 출력

frame4 = frame2.drop('tel', axis=1)  # 열 삭제
# -> 'tel' 열 삭제
# -> axis=1은 열 방향 삭제 의미
# -> 원본 frame2는 그대로이고, 결과를 frame4에 저장

print(frame4)
# -> 'tel' 열이 제거된 DataFrame 출력

print('--------------')
print(frame2)

print(frame2.sort_index(axis=0, ascending=False))   # 행 단위 정렬
# -> 행 인덱스를 기준으로 정렬
# -> axis=0 이므로 행 기준
# -> ascending=False 이므로 내림차순 정렬
# -> 예: e, d, c, b, a 순으로 출력

print(frame2.sort_index(axis=1, ascending=True))   # 열 단위 정렬
# -> 열 이름(column)을 기준으로 정렬
# -> axis=1 이므로 열 기준
# -> ascending=True 이므로 오름차순 정렬
# -> 컬럼명이 가나다/알파벳 순으로 정렬됨

print(frame2.rank(axis=0))  # 순위 매김
# -> 각 열(column)별로 값의 순위를 계산
# -> axis=0 이므로 세로 방향, 즉 열 단위 비교
# -> 숫자 데이터 기준으로 작은 값부터 순위가 매겨짐
# -> 문자열 열은 상황에 따라 순위 계산 대상에서 제외되거나 문자열 기준 순위 처리될 수 있음

counts = frame2['juso'].value_counts()
# -> 'juso' 열의 값별 개수 세기
# -> 같은 주소가 몇 번 나왔는지 빈도수 계산

print(counts)
# -> 주소별 등장 횟수 출력

# 문자열 자르기
data = {
    'juso':['강남구 역삼동','중구 신당동','강남구 대치동'],
    'inwon':[23, 25, 15]
}
# -> 새로운 딕셔너리 데이터 생성
# -> juso는 '구 동' 형태의 문자열
# -> inwon은 인원수

fr = pd.DataFrame(data)
# -> 딕셔너리를 DataFrame으로 변환

print(fr)
# -> 생성된 DataFrame 출력

result1 = Series([x.split()[0] for x in fr.juso]) 
# -> fr.juso의 각 문자열을 공백 기준으로 나눔
# -> split() 결과에서 [0]은 첫 번째 단어
# -> 즉, '강남구 역삼동' -> '강남구'
# -> 각 주소의 앞부분(구)만 모아서 Series 생성

result2 = Series([x.split()[1] for x in fr.juso])
# -> fr.juso의 각 문자열을 공백 기준으로 나눔
# -> split() 결과에서 [1]은 두 번째 단어
# -> 즉, '강남구 역삼동' -> '역삼동'
# -> 각 주소의 뒷부분(동)만 모아서 Series 생성

print(result1) 
print(result2)






