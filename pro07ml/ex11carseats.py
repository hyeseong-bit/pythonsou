# 회귀분석 문제 3)    
# kaggle.com에서 carseats.csv 파일을 다운 받아 Sales 변수에 영향을 주는 변수들을 선택하여 선형회귀분석을 실시한다.
# 변수 선택은 모델.summary() 함수를 활용하여 타당한 변수만 임의적으로 선택한다.
# 회귀분석모형의 적절성을 위한 조건도 체크하시오. 완성된 모델로 Sales를 예측.

# 선형회귀 분석 모형의 적절성 선행조건
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Carseats.csv")
print(df.head(3), df.shape)
print(df.info())
df = df.drop([df.columns[6],df.columns[9],df.columns[10]],axis=1)
print(df.corr())

lm = smf.ols(formula='Sales ~ Income+Advertising+Price+Age', data=df).fit()
print(lm.summary())

print("\n선형회귀 모델의 적절성 조건 체크 후 모델 사용")
print(df.columns)  # ['Sales','CompPrice','Income','Advertising','Population','Price','Age','Education']
df_lm = df.iloc[:, [0, 2, 3, 5, 6]]
print(df_lm.head(2))
# 잔차향 구하기
fitted = lm.predict(df_lm)
residual = df_lm['Sales'] - fitted
print('residual : ', residual[:3]) 
print('잔차 평균 : ', np.mean(residual))   # -1.41220368e-15

print('잔차의 정규성 : 잔차가 정규성을 따르는지 확인')
from scipy.stats import shapiro
import statsmodels.api as sm

stat, p = shapiro(residual)
print(f"통계량 : {stat}, p-value:{p}")
print("정규성 만족" if p > 0.05 else "정규성 위배")

# Q-Q plot으로 잔차의 정규성 시각화
sm.qqplot(residual, line='s')
plt.title("Q-Q plot으로 정규성 만족 확인")
plt.show()

print("선형성 검정")
from statsmodels.stats.diagnostic import linear_reset  
reset_result = linear_reset(lm, power=2, use_f=True)
print(f'reset_result 결과 : {reset_result.pvalue:.5f}')
print('선형성 만족' if reset_result.pvalue > 0.05 else "선형성 위배")
# 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color':'red'})
plt.plot([fitted.min(), fitted.max()], [0, 0], '--', color='gray')
plt.show()

print("등분산성 검정 : 독립변수의 모든 값에 오차들의 분산은 일정해야 한다")
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residual, sm.add_constant(df_lm['Sales']))
bp_stat, bp_pvalue = bp_test[0], bp_test[1]
print(f"breuschpagan test :  통계량:{bp_stat}, p-value:{bp_pvalue}")
print("등분산성 만족" if bp_pvalue > 0.05 else "등분산성 위배")
# 시각화는 선형성 시각화 참조

print("독립성 검정 : 다중회귀 분석 시 독립변수의 값이 서로 관련되지 않아야 한다.")
# 잔차가 자기상관(인접 관측치의 오차가 상관됨)이 있는지 확인
# Durbin-Watson : 잔차의 자기상관(autocorrelation) 검정 지표.
# 잔차들이 서로 독립적인가? 시간 흐름 데이터에서 중요 (시계열)
# 값의 범위는 0 ~ 4 이고 2이면 정상 (자기상관 없음). < 2이면 양의 자기상관, >2이면 음의 자기상관 
# model.summary()로  확인 가능
import statsmodels.api as sm
print('Durbin-Watson : ', sm.stats.stattools.durbin_watson(residual))
# 1.9314981270829592 이므로 잔차의 자기상관은 없다.

print("다중공선성 검정 : 다중회귀 분석 시 독립변수 간에 강한 상관관계가 있어서는 안된다.")
# VIF(variance_inflation_factor, 분산 인플레 요인, 분산 팽창 지수)
# : 값이 10을 넘으면 다중 공선성이 발생하는 변수라고 할 수 있다
from statsmodels.stats.outliers_influence import variance_inflation_factor
df_ind = df[['Income','Advertising','Population','Price','Age']]   # 독립변수들
vifdf = pd.DataFrame()
vifdf['변수'] = df_ind.columns
vifdf['vif_value'] = [variance_inflation_factor(df_ind.values, i) \
                        for i in range(df_ind.shape[1])]
print(vifdf)     # 10을 초과하지 않았으므로 모두 만족
#    vif_value
# 0   6.019719
# 1   2.164595
# 2   4.232582
# 3  10.831353

# 시각화
sns.barplot(x="변수", y="vif_value", data=vifdf)
plt.title("VIF")
plt.show()

# 유의한 모델이므로 생성된 모델을 파일로 저장하고 이를 재사용
# 방법1
# import pickle
# with open('carseat.pickle', 'wb') as obj:   # 저장
#     pickle.dump(lm, obj)

# with open('carseat.pickle', 'rb') as obj:   # 읽기
#     mymodel = pickle.load(lm, obj)

# 방법2 : pickle은 binary로 i/o 해야 하므로 번거롭다
import joblib
joblib.dump(lm,'carseat.model')
# 이후 부터는 아래처럼 읽어 사용하면 됨
mymodel = joblib.load('carseat.model')

print("새로운 값으로 Sales 예측")
new_df = pd.DataFrame({"Income":[35,62], "Advertising":[6,3], \
                        'Price':[105, 88], 'Age':[32, 55]})
pred = mymodel.predict(new_df)
print("Sales 예측 결과 : ", pred.values)  # [8.71289759 8.49715914]




