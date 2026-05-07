#  scipy.stats.linregress() <= 꼭 하기 : 심심하면 해보기 => statsmodels ols(), LinearRegression 사용

# 나이에 따라서 지상파와 종편 프로를 좋아하는 사람들의 하루 평균 시청 시간과 운동량에 대한 데이터는 아래와 같다.
#  - 지상파 시청 시간을 입력하면 어느 정도의 운동 시간을 갖게 되는지 회귀분석 모델을 작성한 후에 예측하시오.
#  - 지상파 시청 시간을 입력하면 어느 정도의 종편 시청 시간을 갖게 되는지 회귀분석 모델을 작성한 후에 예측하시오.
#     참고로 결측치는 해당 칼럼의 평균 값을 사용하기로 한다. 이상치가 있는 행은 제거. 운동 10시간 초과는 이상치로 한다.  
# 구분,지상파,종편,운동

# 1,0.9,0.7,4.2
# 2,1.2,1.0,3.8
# 3,1.2,1.3,3.5
# 4,1.9,2.0,4.0
# 5,3.3,3.9,2.5
# 6,4.1,3.9,2.0
# 7,5.8,4.1,1.3
# 8,2.8,2.1,2.4
# 9,3.8,3.1,1.3
# 10,4.8,3.1,35.0
# 11,NaN,3.5,4.0
# 12,0.9,0.7,4.2
# 13,3.0,2.0,1.8
# 14,2.2,1.5,3.5
# 15,2.0,2.0,3.5


import numpy as np
import pandas as pd
from scipy.stats import linregress
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

# 데이터프레임 생성
df = pd.DataFrame({
    '지상파': [0.9,1.2,1.2,1.9,3.3,4.1,5.8,2.8,3.8,4.8,np.nan,0.9,3.0,2.2,2.0],
    '종편':   [0.7,1.0,1.3,2.0,3.9,3.9,4.1,2.1,3.1,3.1,3.5,0.7,2.0,1.5,2.0],
    '운동':   [4.2,3.8,3.5,4.0,2.5,2.0,1.3,2.4,1.3,35.0,4.0,4.2,1.8,3.5,3.5]
})

# 결측치 평균으로 대체
df = df.fillna(df.mean())

# 운동 10초과 이상치 제거
df = df[df['운동'] <= 10]

# 1. linregress
r1 = linregress(df['지상파'], df['운동'])
r2 = linregress(df['지상파'], df['종편'])

print('=== linregress ===')
print('운동 = {:.6f} * 지상파 + {:.6f}'.format(r1.slope, r1.intercept))
print('종편 = {:.6f} * 지상파 + {:.6f}'.format(r2.slope, r2.intercept))

# 2. statsmodels OLS
x_sm = sm.add_constant(df['지상파'])
m1 = sm.OLS(df['운동'], x_sm).fit()
m2 = sm.OLS(df['종편'], x_sm).fit()

print('\n=== OLS ===')
print('운동 = {:.6f} * 지상파 + {:.6f}'.format(m1.params['지상파'], m1.params['const']))
print('종편 = {:.6f} * 지상파 + {:.6f}'.format(m2.params['지상파'], m2.params['const']))

# 3. LinearRegression
x_lr = df[['지상파']]
lr1 = LinearRegression()
lr2 = LinearRegression()

lr1.fit(x_lr, df['운동'])
lr2.fit(x_lr, df['종편'])

print('\n=== LinearRegression ===')
print('운동 = {:.6f} * 지상파 + {:.6f}'.format(lr1.coef_[0], lr1.intercept_))
print('종편 = {:.6f} * 지상파 + {:.6f}'.format(lr2.coef_[0], lr2.intercept_))

# 예측
x = float(input('\n지상파 시청 시간 입력: '))

print('\n예상 운동 시간 : {:.6f}'.format(r1.slope * x + r1.intercept))
print('예상 종편 시청 시간 : {:.6f}'.format(r2.slope * x + r2.intercept))