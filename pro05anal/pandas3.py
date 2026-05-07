# 연산
from pandas import Series,DataFrame
import numpy as np

s1 = Series([1,2,3], index=['a','b','c'])
s2 = Series([4,5,6,7], index=['a','b','d','c'])
print(s1)
print(s2)
print(s1 + s2)      # 같은 index끼리 연산, 불일치시 NaN을 반환
print(s1.add(s2))   # numpy 함수를 계승

print(s1.mul(s2))   # sub, div

print()
df1 = DataFrame(np.arange(9).reshape(3, 3), columns=list('kbs'),
                index=['서울','대전','부산'])
# -> 0부터 8까지의 숫자를 생성하고 3행 3열 형태로 변환
# -> 열 이름은 k, b, s
# -> 행 인덱스는 서울, 대전, 부산

df2 = DataFrame(np.arange(12).reshape(4, 3), columns=list('kbs'),
                index=['서울','대전','제주','광주'])
# -> 0부터 11까지의 숫자를 생성하고 4행 3열 형태로 변환
# -> 열 이름은 k, b, s
# -> 행 인덱스는 서울, 대전, 제주, 광주

print(df1)
# -> df1 출력

print(df2)
# -> df2 출력

print(df1 + df2)
# -> 같은 행 인덱스와 같은 열 이름끼리 더하기
# -> 공통 인덱스(서울, 대전)는 정상 계산됨
# -> 한쪽에만 있는 인덱스(부산, 제주, 광주)는 대응값이 없어서 NaN 발생
# -> DataFrame끼리 연산할 때는 위치가 아니라 인덱스와 컬럼명을 기준으로 계산함

print(df1.add(df2, fill_value=0))      #NaNdms 0으로 채운 후 연산에 참여
# -> add() 메서드로 더하기 수행
# -> 값이 없는 부분(NaN)은 0으로 채운 뒤 계산
# -> 그래서 공통되지 않는 행도 NaN 대신 계산 결과가 나옴
# -> 예: 부산은 df2에 없으므로 df2 값을 0으로 보고 계산

# sub, mul, div도 가능
# -> sub() : 빼기
# -> mul() : 곱하기
# -> div() : 나누기
# -> 이 메서드들도 fill_value 사용 가능

print('NaN(결측값) 처리 -------------')
# -> 결측값 처리 구간 안내 문구 출력

df = DataFrame([[1.4,np.nan], [7, -4.5], [np.nan, np.nan],[0.5, -1]],
            columns=['one','two'])
# -> 결측값(np.nan)이 포함된 DataFrame 생성
# -> 열 이름은 one, two

print(df)
# -> 결측값이 포함된 DataFrame 출력

print()
# -> 한 줄 띄우기

print(df.isnull())      # null 값 탐지
# -> 각 값이 결측값이면 True, 아니면 False 반환
# -> NaN 위치를 확인할 때 사용

print(df.notnull())     
# -> 각 값이 결측값이 아니면 True, 결측값이면 False 반환
# -> isnull()과 반대 결과

print(df.dropna())
# -> 결측값이 하나라도 있는 행 삭제
# -> 기본값이 how='any' 이므로 NaN이 1개라도 있으면 그 행 제거

print()
# -> 한 줄 띄우기

print(df.dropna(how='any'))
# -> 결측값이 하나라도 있는 행 삭제
# -> dropna()와 같은 의미

print()
# -> 한 줄 띄우기

print(df.dropna(how='all'))
# -> 모든 값이 NaN인 행만 삭제
# -> 일부라도 값이 있으면 그 행은 유지됨

print()
# -> 한 줄 띄우기

print(df.dropna(subset=['one']))  # 톡정 열에 NaN이 있는 행 삭제
# -> 'one' 열을 기준으로 결측값이 있는 행 삭제
# -> 즉, one 열이 NaN인 행만 제거
# -> two 열에 NaN이 있어도 one에 값이 있으면 삭제되지 않음
# -> 주석의 "톡정"은 아마 "특정" 오타로 보임

print()
# -> 한 줄 띄우기

print(df.dropna(subset=['two']))
# -> 'two' 열을 기준으로 결측값이 있는 행 삭제
# -> 즉, two 열이 NaN인 행만 제거
# -> one 열이 NaN이어도 two에 값이 있으면 남음

print()
# -> 한 줄 띄우기

print(df.dropna(axis='columns'))
# -> 열(column) 방향으로 결측값 검사
# -> NaN이 하나라도 있는 열은 삭제
# -> one, two 중 NaN이 포함된 열은 제거됨
# -> 따라서 결측값이 있는 열 전체를 없앨 때 사용

print()
print(df)
imsi = df.drop(1)   # 원본은 삭제 안됨. 삭제된 결과가 새로운 dataFrame으로 생성됨
print(imsi)
print(df)
print()
# df.drop(1, inplace=True)  # 원본 삭제 됨.
# print(df)

print()
# 계산 관련 메소드
print(df.sum())          # 열의 합 - NaN은 연산에서 제외
print(df.sum(axis=0, skipna=True))   

print(df.sum(axis=1))    # 행의 합

print()
print(df.describe())     # 요약 통계량 출력
print(df.info())

print()
words = Series(['봄','여름','가을','봄'])
print(words.describe())
