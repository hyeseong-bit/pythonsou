# 이원분산분석 : 요인 복수 - 각 요인의 레벨(그룹)도 복수
# 두 개의 요인에 대해 집단(독립변수) 각각이 종속변수에(평균)에 영향을 주는지 검정
# 주효과(개별효과) : 독립변수들이 각각 독립적으로 종속변수에 미치는 영향을 검정하는 것
# 상호작용효과(교호작용) : 독립변수들이 서로 연관되어 종속변수에 미치는 영향을 검정하는 것

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# 실습1 : 태아 수와 관측자 수가 태아의 머리둘레 평균에 영향을 주는가?
# 주효과 가설

# 귀무: 태아 수와 태아의 머리둘레 평균은 차이가 없다.
# 대립: 태아 수와 태아의 머리둘레 평균은 차이가 있다.
# 귀무: 관측자 수와 태아의 머리둘레 평균은 차이가 없다.
# 대립: 관측자 수와 태아의 머리둘레 평균은 차이가 있다.

# 교호작용 가설
# 귀무 : 교호작용이 없다 (태아수와 관측자 수는 관련이 없다)
# 대립 : 교호작용이 있다 (태아수와 관측자 수는 관련이 있다)

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3_2.txt")
print(data.head(3), data.shape)   # (36, 3)
print(data['태아수'].unique())     # [1 2 3]
print(data['관측자수'].unique())   # [1 2 3 4]

# 시각화
# data.boxplot(column='머리둘레', by='태아수')
# plt.show()
# data.boxplot(column='머리둘레', by='관측자수')
# plt.show()
# linreg = ols("머리둘레 ~ C(태아수) + C(관측자수)", data=data).fit()  # 교호작용X
# linreg = ols("머리둘레 ~ C(태아수) + C(관측자수) + C(태아수):C(관측자수)", data=data).fit()  # 교호작용O
linreg = ols("머리둘레 ~ C(태아수) * C(관측자수)", data=data).fit()  # 교호작용O

pd.set_option('display.max_columns', None)
result = anova_lm(linreg, typ=2)
print(result)
#                     sum_sq    df            F        PR(>F)
# C(태아수)          324.008889   2.0  2113.101449  1.051039e-27  
# C(관측자수)           1.198611   3.0     5.211353  6.497055e-03
# C(태아수):C(관측자수)    0.562222   6.0     1.222222  3.295509e-01

#  C(태아수) PR(>F) 1.051039e-27 < 0.05  : 귀무기각. 태아 수와 태아의 머리둘레 평균은 차이가 있다(유의사항)
#  C(관측자수) PR(>F) 6.497055e-03  < 0.05: 귀무기각. 관측자 수와 태아의 머리둘레 평균은 차이가 있다(유의사항)
#  상호작용 PR(>F) 3.295509e-01 > 0.05 : 귀무채택. 대아수와 관측자 수는 관련이 없다
# 해석 :
# 태아수와 관측자 수는 각각 종속변수에 유의한 영향을 미친다.
# 그러나 태아수와 관측자 수 간의 상호작용 효과는 유의하지 않다.
# 주효과는 있음, 상호작용은 없음

print('-------------------------------')
# 실습2 : poison과 treat가 독퍼짐 시간의 평균에 영향을 주는가?
# 주효과 가설

# 귀무: poison 종류와 독퍼짐 시간의 평균은 차이가 없다.
# 대립: poison 종류와 독퍼짐 시간의 평균은 차이가 있다.
# 귀무 : treat(응급처지) 방법과 독 퍼짐 시간의 평균은 차이가 없다.
# 대립 : treat(응급처지) 방법과 독 퍼짐 시간의 평균은 차이가 있다.

# 교호작용 가설
# 귀무 : 교호작용이 없다 (poison 종류와 응급처지 방법은 관련이 없다)
# 대립 : 교호작용이 있다 (poison 종류와 응급처지 방법은 관련이 있다)

data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv", index_col=0)
print(data2.head(3), data2.shape)   
print(data2.groupby('poison').agg(len))
print(data2.groupby('treat').agg(len))
print(data2.groupby(['poison','treat']).agg(len)) # 요인별 레벨의 표본수는 4로 동일 (모든 집단 별 표본수 동일하므로 균형설계가 잘됨)

result2 = ols('time ~ C(poison) * C(treat)', data=data2).fit()
print(anova_lm(result2))
#                       df    sum_sq   mean_sq          F        PR(>F)
# C(poison)            2.0  1.033013  0.516506  23.221737  3.331440e-07
# C(treat)             3.0  0.921206  0.307069  13.805582  3.777331e-06
# C(poison):C(treat)   6.0  0.250138  0.041690   1.874333  1.122506e-01

# C(poison) PR(>F) 3.331440e-07 < 0.05  : 귀무기각. poison 종류와 독퍼짐 시간의 평균은 차이가 있다.(유의사항)
# C(treat) PR(>F) 3.777331e-06  < 0.05: 귀무기각. treat(응급처지) 방법과 독 퍼짐 시간의 평균은 차이가 있다(유의사항)
# 주효과는 있음, 상호 작용없음

# 사후 분석
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tkResult1 = pairwise_tukeyhsd(endog=data2.time, groups=data2.poison)
print(tkResult1)
tkResult1.plot_simultaneous(xlabel='mean of time',ylabel='poison')
plt.show()
plt.close()
tkResult2 = pairwise_tukeyhsd(endog=data2.time, groups=data2.treat)
print(tkResult2)
tkResult2.plot_simultaneous(xlabel='mean of time',ylabel='treat')
plt.show()
plt.close()