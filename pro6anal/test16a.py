import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False

# 매출 데이터 읽기
sales_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tsales.csv",
                        dtype={'YMD':'object'})   # int -> object 변환해 읽기
print(sales_data.head(3))
print(sales_data.info())
#         YMD    AMT  CNT
# 0  20190514      0    1
# 1  20190519  18000    1

# 날씨 데이터 읽기
wt_data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tweather.csv")
print(wt_data.head(3)) # 328 * 3 
#    stnId     tm        avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  2018-06-01   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  2018-06-02   23.4   17.6   30.1    0.0    4.5    2.0    0.0
print(wt_data.info())  # 702 * 9  

print()
# sales: YMD 20190514, wt: tm 2018-06-01 병합을 위해 데이터 변환 필요
wt_data.tm = wt_data.tm.map(lambda x:x.replace("-",""))
print(wt_data.head(2)) 
#    stnId        tm  avgTa  minTa  maxTa  sumRn  maxWs  avgWs  ddMes
# 0    108  20180601   23.8   17.5   30.2    0.0    4.3    1.9    0.0
# 1    108  20180602   23.4   17.6   30.1    0.0    4.5    2.0    0.0
print()

# 두 데이터를 병합
frame = sales_data.merge(wt_data, how="left", left_on="YMD", right_on='tm')
print(frame.columns)
# ['YMD', 'AMT', 'CNT', 'stnId', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn',
#   'maxWs', 'avgWs', 'ddMes'],dtype='str'
print(frame.head(), " ", len(frame))   # 328

# 수정: iloc 대신 컬럼명으로 정확히 선택
data = frame[['YMD', 'AMT', 'maxTa', 'sumRn']].copy()
print(data.head())
print("결측치 확인 : ", data.isnull().sum())

# 수정: 결측치 제거
data = data.dropna(subset=['AMT', 'maxTa'])

print(data.maxTa.describe())
# plt.boxplot(data.maxTa)
# plt.show()

# 온도를 세 그룹으로 분리 (연속형 -> 범주형)
print(data.isnull().sum())
data['ta_gubun'] = pd.cut(data['maxTa'], bins=[-5, 8, 24, 37], labels=[0, 1, 2])
print(data.head(3), ' ', data['ta_gubun'].unique())

# 정규성, 등분산성
x1 = np.array(data[data.ta_gubun == 0].AMT)  # 추움
x2 = np.array(data[data.ta_gubun == 1].AMT)  # 보통
x3 = np.array(data[data.ta_gubun == 2].AMT)  # 더움
print(x1[:5])

print()

print(stats.levene(x1, x2, x3).pvalue)
print(stats.bartlett(x1, x2, x3).pvalue)
print()
print(stats.shapiro(x1).pvalue)
print(stats.shapiro(x2).pvalue)
print(stats.shapiro(x3).pvalue)

print()
# 온도별 매출액 평균
np.set_printoptions(suppress=True)
spp = data.loc[:,['AMT', 'ta_gubun']]
print(spp.groupby('ta_gubun').mean())
print(np.mean(x1))  # 1032362.31
print(np.mean(x2))  # 818106.87
print(np.mean(x3))  # 553710.9

group1 = x1
group2 = x2
group3 = x3

# plt.boxplot([group1,group2,group3], showmeans=True)
# plt.show()

print(stats.f_oneway(group1,group2,group3))
# statistic=99.190801, pvalue=2.3607371-34
# 해석 : pvalue=2.3607371-34 < alpha 0.05 이므로 귀무 기각
# 어느 음식점의 매출 데이터는 온도에 따라 매출액 평균에 차이가 있다.

# f_oneway(): 정규성이 깨지면 stats.kruskal()사용, 등분산성이 깨지면 welch ANOBA
#stats.kruskal()
print(stats.kruskal(group1,group2,group3)) # 귀무 기각
# statistic=132.70225, pvalue=1.52781425e-29
# welch's ANOVA
# pip install pingouin
from pingouin import welch_anova
print(welch_anova(dv="AMT", between='ta_gubun', data=data))  # 귀무 기각
#      Source  ddof1     ddof2           F         p_unc       np2
# 0  ta_gubun      2  189.6514  122.221242  7.907874e-35  0.379038

# 사후 검증
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog= data['AMT'], groups=data['ta_gubun'], alpha=0.05)
print(tukResult)

# 시각화
tukResult.plot_simultaneous(xlabel='mena', ylabel='group')
plt.show()

print('-----------------------------------------')
# 빵을 기름에 튀길 때 네 가지 기름의 종류에 따라 빵에 흡수된 기름의 양을 측정하였다.
# 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 존재하는지를 분산분석을 통해 알아보자.
# 조건 : NaN이 들어 있는 행은 해당 칼럼의 평균값으로 대체하여 사용한다.
# 수집된 자료 :  
# kind quantity
# 1 64
# 2 72
# 3 68
# 4 77
# 2 56
# 1 NaN
# 3 95
# 4 78
# 2 55
# 1 91
# 2 63
# 3 49
# 4 70
# 1 80
# 2 90
# 1 33
# 1 44
# 3 55
# 4 66
# 2 77

oil = pd.DataFrame({
    'kind':[1,2,3,4,2,1,3,4,2,1,2,3,4,1,2,1,1,3,4,2],
    'quantity':[64,72,68,77,56,np.nan,95,78,55,91,63,49,70,80,90,33,44,55,66,77]
})

oil['quantity'] = oil['quantity'].fillna(oil['quantity'].mean())

g1 = oil[oil['kind'] == 1]['quantity']
g2 = oil[oil['kind'] == 2]['quantity']
g3 = oil[oil['kind'] == 3]['quantity']
g4 = oil[oil['kind'] == 4]['quantity']

print(stats.shapiro(g1).pvalue)
print(stats.shapiro(g2).pvalue)
print(stats.shapiro(g3).pvalue)
print(stats.shapiro(g4).pvalue)

print(stats.levene(g1, g2, g3, g4).pvalue)
print(stats.bartlett(g1, g2, g3, g4).pvalue)

print(stats.f_oneway(g1, g2, g3, g4))
# statistic=0.266935, pvalue=0.84824
# 해석:  pvalue=0.84824 > alpha 0.05 이므로 귀무가설 채택


print('---------------------------------------')
# DB에 저장된 buser와 jikwon 테이블을 이용하여 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 있는지 검정하시오.
#  만약에 연봉이 없는 직원이 있다면 작업에서 제외한다

import MySQLdb
import pandas as pd
import scipy.stats as stats

conn = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='123',
    db='test',
    charset='utf8'
)

sql = """
select 
    b.busername as busername,
    j.jikwonpay as jikwonpay
from jikwon j
join buser b
    on j.busernum = b.buserno
where j.jikwonpay is not null
and b.busername in ('총무부', '영업부', '전산부', '관리부')
"""

df = pd.read_sql(sql, conn)
conn.close()

g1 = df[df['busername'] == '총무부']['jikwonpay']
g2 = df[df['busername'] == '영업부']['jikwonpay']
g3 = df[df['busername'] == '전산부']['jikwonpay']
g4 = df[df['busername'] == '관리부']['jikwonpay']

print(stats.shapiro(g1).pvalue)
print(stats.shapiro(g2).pvalue)
print(stats.shapiro(g3).pvalue)
print(stats.shapiro(g4).pvalue)

print(stats.levene(g1, g2, g3, g4).pvalue)
print(stats.bartlett(g1, g2, g3, g4).pvalue)

print(stats.f_oneway(g1, g2, g3, g4))
# statistic=0.4124407, pvalue=0.74544
# 해석: pvalue=0.74544 > alpha 0.05 이므로 귀무가설 채택