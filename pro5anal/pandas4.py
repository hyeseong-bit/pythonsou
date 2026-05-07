# DataFrame 재구조화 (열을 행으로, 행을 열로 이동)
import pandas as pd
import numpy as np

df = pd.DataFrame(1000 + np.arange(6).reshape(2,3), 
                index=['대전', '서울'], columns=['2020','2021','2022'])
print(df)

# stack , unstack
print()
df_row = df.stack() # 열을 행으로 변경
print(df_row)

df_col = df_row.unstack() # 행을 열로 이동
print(df_col)

print('\n범주화 -------------')
price = [10.3, 5.5, 7.8, 3.6]   # 연속형 숫자 데이터 리스트
cut = [3, 7, 9, 11]             # 구간 경계값 설정: (3,7], (7,9], (9,11]

result_cut = pd.cut(price, cut)  # price 값을 cut 기준으로 범주형 구간으로 나눔
print(result_cut)                # 각 값이 어느 구간에 속하는지 출력
# 결과 예:
# 10.3 -> (9, 11]
# 5.5  -> (3, 7]
# 7.8  -> (7, 9]
# 3.6  -> (3, 7]
# (a, b] 는 a < x <= b 의미

print(pd.Series(result_cut).value_counts())  # 각 구간별 데이터 개수 세기

print()  # 줄바꿈

datas = pd.Series(np.arange(1, 1001))  # 1부터 1000까지의 숫자를 Series로 생성
print(datas.head(3))                   # 앞에서 3개만 출력
print(datas.tail(2))                   # 뒤에서 2개만 출력

result_cut2 = pd.qcut(datas, 3)        # 데이터를 개수가 비슷하도록 3개의 구간으로 나눔
# qcut은 값의 크기 기준이 아니라 "데이터 개수 비율" 기준으로 구간을 나눔
# 즉, 각 구간에 비슷한 수의 데이터가 들어가게 함

print(result_cut2)                     # 각 데이터가 어느 분위수 구간에 속하는지 출력
print(pd.Series(result_cut2).value_counts())   # 각 구간별 데이터 개수 확인


print('\nagg 함수 : 범주의 그룹별 연산 ------------')
group_col = datas.groupby(result_cut2, observed=True)
# datas를 result_cut2 구간 기준으로 그룹화
# observed=True : 실제로 존재하는 구간만 보여줌

# print(group_col)
# groupby 객체 자체는 그룹 정보만 가진 상태라 바로 출력해도 내용 확인이 어려움

print(group_col.agg(['count', 'mean', 'std', 'min']))
# 각 그룹별로 여러 통계값을 한 번에 계산
# count : 데이터 개수
# mean  : 평균
# std   : 표준편차
# min   : 최소값

# agg 대신 사용자 함수를 작성
def summaryFunc(gr):
    # gr : 각 그룹에 해당하는 데이터 묶음
    return {
        'count': gr.count(),   # 그룹 데이터 개수
        'mean': gr.mean(),     # 그룹 평균
        'std': gr.std(),       # 그룹 표준편차
        'min': gr.min()        # 그룹 최소값
    }

print(group_col.apply(summaryFunc))
# 각 그룹에 summaryFunc를 적용
# apply : 그룹별로 함수를 실행하는 함수
# 결과는 그룹별 통계값이 딕셔너리 형태로 출력됨

print()
print(group_col.apply(summaryFunc).unstack())
# unstack() : 계층 구조로 된 결과를 표 형태로 펼쳐서 보기 좋게 변환

print('\nmerge : 데이터프레임 객체 병합')

df1 = pd.DataFrame({
    'data1': range(7),
    'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b']
})
# df1 생성
# key 열을 기준으로 나중에 다른 데이터프레임과 연결할 예정

print(df1)

df2 = pd.DataFrame({
    'key': ['a', 'b', 'd'],
    'data2': range(3)
})
# df2 생성
# key 값 a, b, d 에 대해 data2 값 연결

print(df2)

print(pd.merge(df1, df2, on='key'))  # 교집합(inner join)
# df1과 df2를 key 열 기준으로 병합
# on='key' : key 컬럼을 공통 기준으로 사용
# 기본 merge 방식은 inner join(교집합)
# 즉, 양쪽에 모두 존재하는 key만 합쳐짐
# 여기서는 a, b만 합쳐지고 c, d는 제외됨
print() 
print(pd.merge(df1, df2, on='key', how='inner'))  # 교집합(inner join)
print()
print(pd.merge(df1, df2, on='key', how='outer'))  #  full outer join
print()
print(pd.merge(df1, df2, on='key', how='left'))  #  left outer join
print()
print(pd.merge(df1, df2, on='key', how='right'))  #  right outer join

print()
# 공통 칼럼명이 없는경 : df1 vs df3
df3 = pd.DataFrame({'key2': ['a', 'b', 'd'], 'data2': range(3)})
# df3 생성
# key2 컬럼을 기준으로 나중에 df1과 병합할 예정
# data2는 0, 1, 2 값이 들어감

print(df3)
print(df1)

print(pd.merge(df1, df3, left_on='key', right_on='key2'))  # inner join
# df1의 key 컬럼과 df3의 key2 컬럼을 기준으로 병합
# left_on='key'   : 왼쪽(df1)의 기준 컬럼
# right_on='key2' : 오른쪽(df3)의 기준 컬럼
# 기본값은 inner join이므로 공통값만 합쳐짐
# 즉 a, b만 합쳐지고 c, d 중 공통 아닌 값은 제외됨

print('-- concat ---')

print(pd.concat([df1, df3], axis=0))  # 행단위
# concat : 데이터프레임 이어붙이기
# axis=0 : 아래로 붙이기(행 방향)
# 열 이름이 다르면 없는 값은 NaN으로 채워짐

print(pd.concat([df1, df3], axis=1))  # 열단위
# axis=1 : 옆으로 붙이기(열 방향)
# 같은 인덱스 번호끼리 옆으로 연결됨
# 행 개수가 다르면 없는 부분은 NaN 처리됨

print('\n\n pivot_table : pivot과 groupby 명령의 중간적 성격')
# pivot_table은 pivot처럼 표를 재구성하면서
# groupby처럼 집계 기능도 같이 할 수 있음

# pivot: 데이터 열 중에서 두 개의 열(key)을 사용해 데이터의 행열을 재구성
data = {
    'city': ['강남', '강북', '강남', '강북'],
    'year': [2000, 2001, 2002, 2002],
    'pop': [3.3, 2.5, 3.0, 2.0]
}
# 딕셔너리 형태의 원본 데이터
# city : 지역
# year : 연도
# pop  : 인구 수치

df = pd.DataFrame(data)
# 딕셔너리를 데이터프레임으로 변환

print(df)
print()

print(df.pivot(index='city', columns='year', values='pop'))
# city를 행 인덱스로, year를 열 이름으로 사용
# 각 위치에 pop 값을 배치
# 즉 도시별-연도별 pop 표를 만듦

print(df.pivot(index='year', columns='city', values='pop'))
# year를 행 인덱스로, city를 열 이름으로 사용
# 연도별-도시별 pop 표를 만듦

print()

print(df.set_index(['city', 'year']).unstack())
# set_index(['city','year']) : city와 year를 멀티인덱스로 설정
# unstack() : 안쪽 인덱스를 열 방향으로 펼침
# pivot과 비슷한 결과를 다른 방식으로 표현

print()

print(df['pop'].describe())
# pop 열에 대한 기초통계량 출력
# count, mean, std, min, 25%, 50%, 75%, max 확인 가능

print()

print(df)

print(df.pivot_table(index=['city']))
# city를 기준으로 그룹화한 뒤 평균값을 계산한 표 생성
# pivot_table은 기본적으로 숫자 데이터의 평균(mean)을 구함
# 여기서는 city별 pop 평균이 출력됨

print(df.pivot_table(index=['city'], aggfunc='mean'))
# city를 기준으로 그룹화한 뒤 평균(mean) 계산
# pivot_table의 기본 집계 함수도 평균이지만
# aggfunc='mean'을 직접 써서 평균 계산임을 명확히 한 것

print(df.pivot_table(index=['city', 'year'], aggfunc=[len, 'sum']))
# city와 year를 기준으로 그룹화
# aggfunc=[len, 'sum'] : 여러 집계 함수 동시 적용
# len  -> 각 그룹의 데이터 개수
# sum  -> 각 그룹의 합계
# 결과는 city- year별 개수와 합계를 함께 보여줌

print(df.pivot_table(values='pop', index='city'))
# values='pop' : pop 열만 대상으로 사용
# index='city' : city를 기준으로 그룹화
# 즉, city별 pop 평균을 구하는 표 생성
# values를 지정했기 때문에 pop 열만 계산됨

print(df.pivot_table(values='pop', index='city', aggfunc=len))
# city를 기준으로 pop 데이터 개수 세기
# values='pop' : pop 열만 대상으로 사용
# index='city' : city별로 그룹화
# aggfunc=len  : 각 city에 해당하는 데이터 개수 계산

print()

print(df.pivot_table(values='pop', index=['year'], columns=['city']))
# year를 행 인덱스로, city를 열 이름으로 사용
# 각 위치에 pop 값이 들어가는 표 생성
# 즉, 연도별-도시별 pop 표를 만듦

print(df.pivot_table(values='pop', index=['year'], columns=['city'], margins=True))
# 위 표에 margins=True를 추가
# margins=True : 행/열의 전체 합계 또는 전체 평균을 같이 보여줌
# 기본적으로 마지막에 All 행/열이 추가됨

print(df.pivot_table(values='pop', index=['year'], columns=['city'], margins=True, fill_value=0))
# margins=True : 전체값(All) 추가
# fill_value=0 : 값이 없는 곳(NaN)을 0으로 채움
# 데이터가 없는 연도-도시 조합도 0으로 표시됨

print()

hap = df.groupby(['city'])
# city를 기준으로 그룹화한 groupby 객체 생성
# 아직 계산은 하지 않고 그룹만 묶어둔 상태

print(hap)
# groupby 객체 정보 출력
# 실제 데이터 요약 결과가 아니라 그룹 객체 자체가 보임

print(hap.sum())
# city별로 숫자형 데이터 합계 계산
# 예: year, pop 컬럼의 합이 city별로 출력됨

print(df.groupby(['city']).sum())
# 위와 같은 의미
# city별 숫자형 데이터 합계 계산

print(df.groupby(['city']).mean())
# city별 숫자형 데이터 평균 계산
# 즉 city별 year 평균, pop 평균이 출력됨