# LogisticRegresion(로지스틱 회귀분석)
# 선형결합을 로그오즈(logit())로 해석하고, 이를 시그모이드 함수를 통해 확률로 변환!
# 이항분류(다항도 가능), 독립변수:연속형, 종속변수:범주형
# LogisticRegresion을 근거로 뉴럴넷의 뉴런에서 사용함

# mtcars dataset 사용
import statsmodels.api as sm

mtcarsdata = sm.datasets.get_rdataset('mtcars')
print(mtcarsdata.keys())
mtcars = sm.datasets.get_rdataset('mtcars').data
print(mtcars.head(2))
print(mtcars.info())

print()
# 연비와 마력수에 따른 변속기 분류(수동, 자동)
mtcar = mtcars.loc[:,['mpg','hp','am']]
print(mtcar.head())
print(mtcar['am'].unique())  # [1(수동) 0(자동)]

# 모델 작성 방법1 : logit()
import numpy as np
import statsmodels.formula.api as smf

formula = 'am ~ hp + mpg'       # '연속형 ~ 범주형 + ...'
result = smf.logit(formula=formula, data=mtcar).fit()
print(result.summary())  #  Logit Regression Results

# print('예측값 : ', result.predict())  # 정확도 판단
pred = result.predict(mtcar[:10])
print('예측값 : ', pred.values)         #  [0.25004729 0.25004729 0.55803435 ...
print('예측값 : ', np.around(pred.values))   # np.around() 0.5 기준으로 0, 1 출력
# 예측값 :  [0. 0. 1. 0. 0. 0. 0. 1. 1. 0.] 
print('실제값 : ', mtcar['am'][:10].values)  
# 실제값 : [1 1 1 0 0 0 0 0 0 0]
print()
print('수치에 대한 집계표(Confusion matrix, 혼돈행렬) 확인 -----')
conf_tab = result.pred_table()
print(conf_tab)
# 현재 모델의 분류 정확도 확인 1 - Confusion matrix 이용
print('분류 정확도 : ',(16 + 10) / len(mtcar))
print('분류 정확도 : ',(conf_tab[0][0]) + conf_tab[1][1] / len(mtcar))   

# 모듈로 확인2 - accuracy_score 이용
from sklearn.metrics import accuracy_score
pred2 = result.predict(mtcar)
print('분류 정확도 : ',accuracy_score(mtcar['am'], np.around(pred2)))

print('*' * 10)
# 모델 작성방법2 : glm() - 일반화된 선형모델
result2 = smf.glm(formula=formula, data=mtcar,family=sm.families.Binomial()).fit()
# Binomial(): 이항분포, Gaucian: 정규분포 - 기본값
print(result2.summary())

glm_pred = result2.predict(mtcar[:10])
print('glm 예측값 : ', np.around(glm_pred.values))
print('glm 실제값 : ', mtcar['am'][:10].values)

glm_pred2 = result2.predict(mtcar)
print('glm 모델 분류 정확도 : ', accuracy_score(mtcar['am'], np.around(glm_pred2)))

# logit()은 변환 함수, glm()은 logit()을 포함한 전체 모델

print('새로운 값으로 분류 ------')
import pandas as pd
newdf = pd.DataFrame()
newdf['mpg'] = [10, 30, 120, 200]
newdf['hp'] = [100, 110, 80, 130]
print(newdf)
new_pred = result2.predict(newdf)
print('예측 결과 : ', np.around(new_pred.values))
print('예측 결과 : ', np.rint(new_pred.values))


