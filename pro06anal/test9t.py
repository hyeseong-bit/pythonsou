# 독립 표본 t- 검정(independent two sample t-test)
# 서로 다른 두 집단의 평균에 대한 통계 검정에 사용된다
# 비교를 위해 평균과 표준편차 통계량을 사용한다.
# 두 집단의 평균과 표준편차 비율에 대한 재조 검정법이다

# 두 집단의 가설검정 실습 시 분산을 알지 못하는 것으로 한정하겠다
# 남녀의 성적 A 반과 B 반의 키 경기도와 충청도의 소득 따위의 서로 독립인
#  두 집단에서 얻은  표본을 독립표본 (two sample)이라고 한다
# 남녀 두 집단 간 파이썬 시험의 평균 차이 검정

# 실습 : 남녀 두 집단 간 파이썬 시험의 평균 차이 검정
# 남녀의 시험 평균이 우연히 같을 확률은 얼마나 될까?
# 만약 우연히발생했다면 평균은 같은 것이고, 우연이 아니면 평균은 다른 것이다.
# 95% 신뢰 구간에서 우연히 발생할 확률이 5% 이상이면 귀무가설 채택이다.

# 귀무: 남녀 두 집단 간 파이썬 시험의 평균의 차이는 없다.
# 대립: 남녀 두 집단 간 파이썬 시험의 평균의 차이는 있다.

from scipy import stats
import pandas as pd
import numpy as np

male = [78, 85, 100, 72.5, 86.5]
female = [63.2, 76, 52, 100, 70]
print(np.mean(male), ' ', np.mean(female))   # 84.4   72.24

# 두 개의 표본에 대한 독립표본 't-검정' 수행
# two_sample = stats.ttest_ind(male, female)
two_sample = stats.ttest_ind(male, female, equal_var=True)  # 위와 동일, 두 집단의 분산이 같은 경우로 가정

print(two_sample)
tv, pv = two_sample
print('t 검정 통계량 : ', tv)
print('p 값 : ', pv)
# statistic=1.3143634, pvalue=0.22515483, df=8.0
# 해석 : p-value 0.2525 > 0.05 귀무 채택. 통계적으로 유의하지 않다.

# 선행 조건
# 선행조건 1) 두 집단이 정규분포를 따라야 한다.

print('male 의 정규성 : ', stats.shapiro(male))     # p 0.80477 >  0.05 정규성 만족
print('female 의 정규성 : ', stats.shapiro(female)) # p 0.7780431 > 0.05

# 만약 집단의 표본 수가 30개 이상인 경우정규 분포를 따른다고 가정함으로 정규성 검정 안해도 됨.
# 만약 정규성을 만족하지 못하면 비모수 검정인 Mann-whitney test를 한다.
# stats.mannwhitneyu(group1, group2) p > 0.05 인 경우 차이 증거 없음, 아니면 두 집단 평균 차이가 있음

print()
# 선행 조건 2) 두 집단의 분산이 갇다는 가정이 필요. 등분산성(데이터의 퍼짐 정도)
from scipy.stats import levene,bartlett             
# levene: 정규성 상관없이 사용, 이상치에 민감, 어떤 분포도 사용 가능           
# bartlett: 정규성이 있을 때만 사용, 이상치에 덜민감, 정규분포일 때만 사용가능
levene_stat, levene_p = levene(male, female)
print('p value : ', levene_p)  # 0.4384962 >= 0.05 등분산성 만족
two_sample = stats.ttest_ind(male, female, equal_var=True) # 이거 사용
# 만약 등분산 만족 못할 때 Welch's t-test 수행
# two_sample = stats.ttest_ind(male, female, equal_var=False)

