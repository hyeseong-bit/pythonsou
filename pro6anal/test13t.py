# Paored Samples t-test
# 실습 : 복부 수술 전 9 명의 몸무게와 북부 수술 후 몸무게 변화
baseline = [67.2, 67.4, 71.5, 77.6, 86.0, 89.1, 59.5, 81.9, 105.5]
follow_up = [62.4, 64.6, 70.4, 62.6, 80.1, 73.2, 58.2, 71.0, 101.0]

# 귀무: 북부 수술 전 몸무게와 북부 수술 후 몸무게의 변화는 없다.
# 대립: 북부 수술 전 몸무게와 북부 수술 후 몸무게의 변화는 있다.

import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
import pymysql
import pandas as pd

print(np.mean(baseline))
print(np.mean(follow_up))
print('평균의 차이 : ', np.mean(baseline) - np.mean(follow_up)) # 6.91111

# 시각화
plt.bar(np.arange(2), [np.mean(baseline), np.mean(follow_up)])
plt.xlim(0, 1)
plt.xlabel('수술 전후', fontdict={'fontsize':12,'fontweight':'bold'})
plt.show()

result = stats.ttest_rel(baseline, follow_up)
print(result)
# statistic=3.668116, pvalue=0.0063266, df=8
# 해석 : pvalue=0.0063266 < alpha 0.05 이므로 귀각
# 북부 수술 전 몸무게와 북부 수술 후 몸무게의 변화는 있다. 라는 의견을 받아 들임


print('----------')
# two-sample t 검정 : 문제2]  
# 아래와 같은 자료 중에서 남자와 여자를 각각 15명씩 무작위로 비복원 추출하여 혈관 내의 콜레스테롤 양에 차이가 있는지를 검정하시오.

man = [0.9, 2.2, 1.6, 2.8, 4.2, 3.7, 2.6, 2.9, 3.3, 1.2, 3.2, 2.7, 3.8, 4.5, 4, 2.2, 0.8, 0.5, 0.3, 5.3, 5.7, 2.3, 9.8]
women = [1.4, 2.7, 2.1, 1.8, 3.3, 3.2 ,1.6, 1.9 ,2.3 ,2.5 ,2.3 ,1.4 ,2.6 ,3.5 ,2.1 ,6.6 ,7.7 ,8.8 ,6.6 ,6.4]

# 귀무: 남녀 간 콜레스테롤 양에 차이가 없다.
# 대립: 남녀 간 콜레스테롤 양에 차이가 있다.
np.random.seed(0)
man = np.random.choice(man, 15, replace=False)
women = np.random.choice(women, 15, replace=False)

print(np.mean(man))
print(np.mean(women))
print('콜레스테롤 양에 차이 : ', np.mean(man) - np.mean(women))

# 독립표본 t-test
result = stats.ttest_ind(man, women, equal_var=False)
print(result)
# statistic=-0.711472, pvalue=0.48082, df=41.0
# 해석 : pvalue=0.48082 > alpha 0.05 이므로 귀무가설 기각하지 못한다.


print('---------------------------------------')
# [two-sample t 검정 : 문제3]
# DB에 저장된 jikwon 테이블에서 총무부, 영업부 직원의 연봉의 평균에 차이가 존재하는지 검정하시오.
# 연봉이 없는 직원은 해당 부서의 평균연봉으로 채워준다.

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="123",
    database="test",  
    charset="utf8"
)

sql = """
select jikwonpay, busername
from jikwon j join buser b
on j.busernum = b.buserno
where busername in ('총무부', '영업부')
"""

df = pd.read_sql(sql, conn)
conn.close()

df['jikwonpay'] = df.groupby('busername')['jikwonpay'].transform(
    lambda x: x.fillna(x.mean())
)

chongmu = df[df['busername'] == '총무부']['jikwonpay']
yeongup = df[df['busername'] == '영업부']['jikwonpay']

print(np.mean(chongmu))
print(np.mean(yeongup))
print('평균 차이 : ', np.mean(chongmu) - np.mean(yeongup))

# t-test (독립표본)
result = stats.ttest_ind(chongmu, yeongup, equal_var=False)
print(result)
# statistic=0.442001, pvalue=0.666800, df=11.3378362
# 해석: pvalue=0.666800 > alpha 0.05 이므로 귀무가설 기각하지 못한다.

print('-------------------------------')
# [대응표본 t 검정 : 문제4]
# 어느 학급의 교사는 매년 학기 내 치뤄지는 시험성적의 결과가 실력의 차이없이 비슷하게 유지되고 있다고 말하고 있다. 이 때,
#  올해의 해당 학급의 중간고사 성적과 기말고사 성적은 다음과 같다. 점수는 학생 번호 순으로 배열되어 있다.
# 수집된 자료 :  

#    중간 : 80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80
#    기말 : 90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95

# 그렇다면 이 학급의 학업능력이 변화했다고 이야기 할 수 있는가?

mf = [80, 75, 85, 50, 60, 75, 45, 70, 90, 95, 85, 80]
rf = [90, 70, 90, 65, 80, 85, 65, 75, 80, 90, 95, 95]

# 귀무: 매년 학기 내 치뤄지는 시험성적의 결과가 실력의 차이없이 비슷하게 유지되고 있다
# 대립: 매년 학기 내 치뤄지는 시험성적의 결과가 실력의 차이없이 비슷하게 유지되지 않는다.

print(np.mean(mf))
print(np.mean(rf))
print('학업 평균 차이 : ', np.mean(mf) - np.mean(rf))

# 독립표본 t-test
result3 = stats.ttest_rel(mf, rf)
print(result3)
# statistic=-2.628112, pvalue=0.02348, df=11
# 해석:pvalue=0.02348 < 0.05 이므로 귀무가설 기각

