import pandas as pd
import numpy as np
# pandas : 데이터 분석용 라이브러리
# numpy : 수치 계산용 라이브러리

# 1) 나이대별 생존자 수
df = pd.read_csv('titanic_data.csv')
# 타이타닉 csv 파일 읽기

bins = [1, 20, 35, 60, 150]
# 나이를 나눌 구간 설정

labels = ["소년", "청년", "장년", "노년"]
# 각 구간에 붙일 이름 설정

df['나이대'] = pd.cut(df['Age'], bins=bins, labels=labels)
# Age 컬럼을 bins 기준으로 구간화하여 '나이대' 컬럼 생성

result = df.groupby('나이대', observed=True)['Survived'].sum().reset_index()
# 나이대별로 그룹화한 후 Survived 값의 합계 계산
# Survived는 0=사망, 1=생존 이므로 합계 = 생존자 수
# reset_index() : 결과를 다시 일반 DataFrame 형태로 변환

result.columns = ['나이대', '생존자수']
# 결과 컬럼명을 보기 좋게 변경

print(result)
# 나이대별 생존자 수 출력
print()

# 2) 성별/객실등급별 생존율
pivot1 = df.pivot_table(
    values='Survived',
    index='Sex',
    columns='Pclass',
    aggfunc='mean'
)
# pivot_table 생성
# values='Survived' : 생존 여부를 기준으로 계산
# index='Sex' : 행 기준은 성별
# columns='Pclass' : 열 기준은 객실 등급
# aggfunc='mean' : 평균 계산
# Survived가 0,1 이므로 평균 = 생존율

print(pivot1)
# 성별/객실등급별 생존율 출력
print()

# 성별/나이대/객실등급별 생존율
pivot2 = df.pivot_table(
    values='Survived',
    index=['Sex', '나이대'],
    columns='Pclass',
    aggfunc='mean'
)
# 성별과 나이대를 기준으로 행 구성
# 객실등급을 열로 구성
# 생존율 평균 계산

pivot2 = (pivot2 * 100).round(2)
# 생존율을 퍼센트(%)로 바꾸고 소수점 둘째 자리까지 반올림

print(pivot2)
# 성별/나이대/객실등급별 생존율 출력

print()

# 3) human.csv
df2 = pd.read_csv(
    "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/human.csv",
    skipinitialspace=True
)
# human.csv 파일 읽기
# skipinitialspace=True : 구분자 뒤 공백 무시

df2.columns = df2.columns.str.strip()
# 컬럼명 앞뒤 공백 제거

df2 = df2.dropna(subset=["Group"])
# Group 컬럼이 결측치(NaN)인 행 삭제

print(df2[['Career', 'Score']])
# Career, Score 컬럼만 출력

print(df2[['Career', 'Score']].mean())
# Career, Score 컬럼의 평균 계산 후 출력

print()

# 4) tips.csv
df3 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tips.csv")
# tips.csv 파일 읽기

df3.info()
# 데이터의 전체 구조 확인
# 행 개수, 컬럼명, 자료형, 결측치 여부 등 출력

print(df3.head(3))
# 앞에서 3행만 출력

print(df3.describe())
# 숫자형 컬럼의 기초 통계량 출력
# count, mean, std, min, max 등 확인 가능

print(df3["smoker"].value_counts())
# smoker 컬럼 값의 빈도수 계산
# 예: Yes, No 각각 몇 명인지 확인

print(df3["day"].unique())
# day 컬럼의 중복 없는 고유값 출력
# 예: Thur, Fri, Sat, Sun