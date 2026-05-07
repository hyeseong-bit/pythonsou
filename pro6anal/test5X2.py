# 이원카이제곱 - 교차분할표 이용
# : 두 개 이상의 변인 집단 또는 범주를 대상으로 검정을 수행한다
# 분석대상의 집단 수에 의해서 독립성 검정과 동질성 검정으로 나뉜다
# 독립성 : 동일 집단의 두 번인 학력수준과 대학진학 여부를 대상으로 관련성이 있는가
# 독립성 검정은 두 변수 사이의 연관성을 검정한다

# 실습
# 교육수준(독립변수, x)과 흡연용(종속변수, y) 간의 관련성 분석, smoke csv

# 귀무 : 교육수준과 흡연율 간에 관계가 없다.(독립이다, 연관성이 없다)
# 대립 : 교육수준과 흡연율 간에 관계가 있다.(독립 아니다, 연관성이 있다)

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/smoke.csv")
print(data.head(3))
print()
print(data['education'].unique()) # [1:대학원졸 2: 대졸 3:고졸]
print(data['smoking'].unique()) # [1:과흡연 2:보통 3:노담]

# 학력 수준별 흡연 빈도수 : 교차표 사용
ctab = pd.crosstab(index=data['education'], columns=data['smoking'])  # 빈도수
# ctab = pd.crosstab(index=data['education'], columns=data['smoking'], normalize=True)
ctab.index = ['대학원졸','대졸', '고졸']
ctab.columns = ['과흡연', '보통' ,'노담']
print(ctab)

# 이원카이제곱 검정
chi_result = [ctab.loc['대학원졸'],ctab.loc['대졸'],ctab.loc['고졸']]
# chi2, p, dof, expected = stats.chi2_contingency(chi_result)
chi2, p, dof, expected = stats.chi2_contingency(ctab)

print(f"chi2:{chi2}, p:{p}, dof:{dof}")
# chi2:18.910915, p:0.000818257, dof:4
print("expected : \n", expected)    # 예측된 기대도수

# 판정1 : 유의수준:0.05 > p:0.000818257 이므로 귀무가설이 기각
# 교육수준과 흡연율 간에 관계가 있다.smoke.csv(수집자료)는 우연히 발생된 자료가 아니다.

# 판정2 : chi2:18.910915, dof:4, critical value:
# chi2 값이 임계치 우측에 있으므로 귀무가설이 기각되고 대립가설이 채택

# 이후 다영한 자료, 의견등으로 보고서 작성

print('---독립성 검정 : 실습 2--------------')
# 남성과 여성의 스포츠 음료 선호도 검정

# 귀무(H0) : 성별과 음료 선호는 서로 관련 없다.
# 대립(H1) : 성별과 음료 선호는 서로 관련 있다.

data = pd.DataFrame({
    '게토레이':[30, 20],
    '포카리':[20, 30],
    '비토500':[10, 30]
}, index=['남성','여성'])

print(data)
chi2, p, dof, expected = stats.chi2_contingency(data)

print('p-value : ', p)          # 0.0033880
print('chi2 value : ', chi2)    # 11.375
print('dof : ', dof)
print('기대도수 : \n', expected)

# 남성    30   20     10
# 여성    20   30     30
# p-value :  0.003388052521834713
# chi2 value :  11.375
# dof :  2
# 기대도수 :
# 21.42857143 21.42857143 17.14285714
#  28.57142857 28.57142857 22.85714286

# 판정 : 예상된 기대도수와 관측값은 서로 관련이 있는가?
# 유의수준 0.05 > p value 0.0033880 이므로 귀무기설 기각
# 성별과 음료 선호는 관련 있다.

# 하트맵 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
sns.heatmap(data=data, annot=True, fmt='d',cmap="Blues")
plt.title('성별에 따른 음료선호')
plt.xlabel('음료')
plt.ylabel('성별')
plt.show()

