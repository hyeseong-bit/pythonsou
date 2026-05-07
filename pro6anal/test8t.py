# 단일 모집단의 평균에 대한 가설검정(one samples t test)
# 실습 예제1
# A 중학교 1 학년 1반 학생들의 시험결과 담긴 파일을 읽어 처리
# 국어 점수 평균검정(80) student csv

# 귀무: 학생들의 국어점수 평균은 80이다.
# 대립: 학생들의 국어점수 평균은 80이 아니다.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import wilcoxon

pd.set_option('display.max_columns', None)
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/student.csv")
print(data.head())
print(data.describe())
print(data['국어'].mean())   # 72.9
print(len(data))    # 20    30행이 넘으면 중심극한정리에 의해 정규성을 따른다고 가정
# 30개가 넘지 않으므로 정규성 검정 실시
# Shapiro-Wilk 검정은 가설검정의 방법으로 데이터가 정규분포를 가지는 지에 대해 검정하는
# p값은 alpha 0.05 보다 커야 정규성을 따른다고 할 수 있다.
print(stats.shapiro(data['국어']))   # pvalue=0.012959
# alpha 0.05 > pvalue=0.012959 정규성을 만족하지 않음

# 정규성을 검정하지 못한 경우 대안 (Wilcoxon)
# Wilcoxon 비모수 검정 방법으로 정규성이 없을 때 적절한 선택이 될 수 있다.
wilcoxon_result = wilcoxon(data['국어'] - 80)
print("wilcoxon_result : ", wilcoxon_result)
# wilcoxon_result : WilcoxonResult=74.0, pvalue=0.3977762
# alpha 0.05 < pvalue=0.3977762 이므로 귀무가설 채택

result = stats.ttest_1samp(data['국어'], popmean=80)
print("result: ", result)
# result:statistic=-1.332180166, pvalue=0.19856051
# alpha 0.05 > pvalue=0.19856051 이므로 귀무가설 채택

# 결론 : 정규성은 부족하나 귀무가설 채택이라는 동일 결론을 얻음
# 표본 수가 크다면 그냥 ttest_1samp을 써도 된다.
# 보고서 작성 시에는 shapiro-wilk 검정결과 정규성 가정이 다소 위배 되었으나 
# 비모수검정(wilcoxon) 결과도 동일하므로 ttest_1samp 결과를 신뢰할 수 있다" 라고 명시한다.

print('--------------------')
# 실습 예제2 
# 여야신생아 몸무게의 평균 검정 수행 babyboom.csv
# 여야신생아의 몸무게는 평균이 2800(g)으로 알려져 왔으나 이보다 더 크다는 주장이 나왔다.
# 표본으료 여야 18 명을 뽑아 체중을 측정하였다고 할 때 새로운 주장이 맞는지 검정해 보자

# 귀무 : 여야신생아의 몸무게는 평균이 2800(g) 이다.
# 대립 : 여야신생아의 몸무게는 평균이 2800(g) 보다 크다.
data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/babyboom.csv")
print(data2.head(3))
print(data2.describe())
print()
fdata = data2[data2.gender == 1]  # 여아:1, 남아:2
print(fdata,' ', len(fdata))    # 18
print('여아 몸무게 평균 : ', np.mean(fdata.weight))         #  3132.4444
# 2800과 3132는 평균에 차이가 있는가?
print('여아 몸무게 표준편차 : ', np.std(fdata['weight']))   #  613.7878951616052

# One-sample t-test
result2 = stats.ttest_1samp(fdata['weight'], popmean=2800)
print("result2: ", result2)
# result2: statistic=2.23318766, pvalue=0.0392684417 , df= 17
# 해석1 (p값) :alpha 0.05 > pvalue=0.0392684417 이므로 귀무가설 기각
# 해석2 (t분포표): t값 2.23318766, df= 17, alpha 0.05, cv(임계값)? 1.740
#                 t값이 cv 값 오른쪽(귀무 기각영역)에 있으므로 귀무가설 기각

print("~~~~~~~~~~~~~~~~~~~~~~")
# 선행조건인 정규성 검정을 한 경우
print(stats.shapiro(fdata['weight']))   #  pvalue=0.017984789
# alpha 0.05 > pvalue=0.017984789 정규성을 만족하지 않음

# 정규성을 만족여부 시각화
sns.histplot(fdata['weight'], kde=True)  # 왜곡된 데이터 분포를 확인
plt.show()

# 정규성을 만족여부 시각화 2 Quantile-Quantile plot
stats.probplot(fdata['weight'], plot=plt) # Q-Q plot상에서 잔차가 정규성을 만족하지 못함
plt.show()

# 정규성 만족 못해 wilcoxon 비모수 검정
result3 = wilcoxon(fdata['weight'] - 2800)
print(result3)
# statistic=37.0, pvalue=0.03423309 이므로 귀무가설 
# 해석3(p값) : alpha 0.05 > pvalue=0.03423309 이므로 귀무가설 기각


print("---------------------------------------")
# [one-sample t 검정 : 문제1]  
# 영사기( 프로젝터 )에 사용되는 구형 백열전구의 수명은 250 시간이라고 알려졌다. 
# 한국 연구소에서 수명이 50 시간 더 긴 새로운 백열전구를 개발하였다고 발표하였다. 
# 연구소의 발표결과가 맞는지 새로 개발된 백열전구를 임의로 수집하여 수명 시간 관련 자료를 얻었다. 
# 한국 연구소의 발표가 맞는지 새로운 백열전구의 수명을 분석하라.
# 수집된 자료 :  305 280 296 313 287 240 259 266 318 280 325 295 315 278

# 귀무: 영사기( 프로젝터 )에 사용되는 구형 백열전구의 수명은 250 시간이라고 알려졌다.
# 대립: 한국 연구소에서 수명이 50 시간 더 긴 새로운 백열전구를 개발하였다고 발표하였다.

# 표본 데이터
data3 = [305, 280, 296, 313, 287, 240, 259, 266, 318, 280, 325, 295, 315, 278]

# 데이터와 표본 크기 출력
print(data3, ' ', len(data3))

# 표본의 평균 계산
print('평균 : ', np.mean(data3))

# 표본의 표준편차 계산(ddof=1 -> 표본표준편차)
print('표준편차 : ', np.std(data3, ddof=1))

# 단일표본 t검정 수행
# H0 : 모집단 평균은 250이다
# H1 : 모집단 평균은 250이 아니다
result4 = stats.ttest_1samp(data3, popmean=250)

# 검정 결과 출력
print("result4: ", result4)

# p-value를 소수점 10자리까지 출력
print(f"p값 : {result4.pvalue:.10f}")

# 해석:
# p-value = 0.0000401691 < 0.05 이므로 귀무가설을 기각한다.
# 즉, 모집단의 평균은 250과 통계적으로 유의한 차이가 있다.

# one-sample t 검정 : 문제2] 
# 국내에서 생산된 대다수의 노트북 평균 사용 시간이 5.2 시간으로 파악되었다. A회사에서 생산된 노트북 평균시간과 차이가 있는지를 검정하기 위해서 A회사 노트북 150대를 랜덤하게 선정하여 검정을 실시한다.  
# 실습 파일 : one_sample.csv
# 참고 : time에 공백을 제거할 땐 ***.time.replace("     ", ""),

#  null인 관찰값은 제거.
# 귀무가설: A회사 노트북 평균 사용시간은 5.2시간이다.
# 대립가설: A회사 노트북 평균 사용시간은 5.2시간과 차이가 있다.
print("----------------------------------------------")
# 1. 출력 시 모든 열이 보이도록 설정
pd.set_option('display.max_columns', None)

# 2. CSV 파일 읽기
tdata = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/one_sample.csv")

# 3. 컬럼명 좌우 공백 제거
tdata.columns = tdata.columns.str.strip()

# 4. 분석에 사용할 변수들을 숫자형으로 변환
tdata['time'] = pd.to_numeric(tdata['time'], errors='coerce')
tdata['gender'] = pd.to_numeric(tdata['gender'], errors='coerce')

# 5. gender가 1인 데이터만 추출
tdata = tdata[tdata['gender'] == 1]

# 6. 기초 통계량 확인
print('평균 :', tdata['time'].mean())
print('표준편차 :', tdata['time'].std())

# 7. 결측값 제거
stime = tdata['time'].dropna()

# 8. 단일표본 t검정 수행
#    H0 : 평균 사용 시간은 5.2이다
#    H1 : 평균 사용 시간은 5.2가 아니다
result5 = stats.ttest_1samp(stime, popmean=5.2)
print("result5: ", result5)
# result5: statistic=3.42936616, pvalue=0.001178725, df=53
# 해석1 (p값) :alpha 0.05 > pvalue=0.001178725 이므로 귀무가설 기각



# [one-sample t 검정 : 문제3] 
# https://www.price.go.kr/tprice/portal/main/main.do 에서 
# 메뉴 중  가격동향 -> 개인서비스요금 -> 조회유형:지역별, 품목:미용 자료(엑셀)를 파일로 받아 미용 요금을 얻도록 하자. 
# 정부에서는 전국 평균 미용 요금이 15000원이라고 발표하였다. 이 발표가 맞는지 검정하시오. (월별)

# [one-sample t 검정 : 문제3] 
# https://www.price.go.kr/tprice/portal/main/main.do 에서 
# 메뉴 중  가격동향 -> 개인서비스요금 -> 조회유형:지역별, 품목:미용 자료(엑셀)를 파일로 받아 미용 요금을 얻도록 하자. 
# 정부에서는 전국 평균 미용 요금이 15000원이라고 발표하였다. 이 발표가 맞는지 검정하시오. (월별)

# 문제 : 정부의 전국 평균 미용 요금 15,000원이 실제 데이터와 차이가 있는지 검정
# 귀무 : 전국 평균 미용 요금은 15,000원이다. (발표가 맞다.)
# 대립 : 전국 평균 미용 요금은 15,000원이 아니다. (발표가 틀리다.)

# 1. 엑셀 파일 읽기
# pip install xlrd
data3 = pd.read_excel('2026.02_data.xls')

# 2. 지역별 미용 요금 데이터 추출
#    첫 번째 행(0행), 세 번째 열(인덱스 2)부터 끝까지 선택
data4 = data3.iloc[0, 2:]

# 3. 숫자형으로 변환하고 결측값 제거
data4 = pd.to_numeric(data4, errors='coerce')
data4 = data4.dropna()

# 4. 기초 통계량 확인
print('표본 평균 미용 요금 :', data4.mean()) # 표본 평균 미용 요금 : 8995.875
print('표본 크기 :', len(data4))  # 표본 크기 : 16

# 5. 정규성 검정 수행
#    H0 : 표본은 정규분포를 따른다
result3 = stats.shapiro(data4)
print('정규성 검정 결과 :', result3)

# 6. 단일표본 t검정 수행
#    H0 : 전국 평균 미용 요금은 15000원이다
#    H1 : 전국 평균 미용 요금은 15000원이 아니다
t_result3 = stats.ttest_1samp(data4, popmean=15000)
print('단일표본 t검정 결과 :', t_result3)

# 7. 검정 결과 해석
#    p-value < 0.05 이면 귀무가설을 기각
#    즉, 전국 평균 미용 요금이 15000원이라는 정부 발표는
#    통계적으로 유의한 차이가 있다고 해석한다