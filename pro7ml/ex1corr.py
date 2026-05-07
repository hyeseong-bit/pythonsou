# 공분산 / 상관계수
# 변수가 하나인 경우에는 분산은 거리와 관련이 있다.
# 변수가 두 개인 경우에는 분산은 방향을 가진다.

import numpy as np

# 공분산
print(np.cov(np.arange(1, 6),np.arange(2, 7)))  # 우상향
print(np.cov(np.arange(10, 60, 10),np.arange(20, 70, 10)))  # 우상향
print(np.cov(np.arange(100, 600, 100),np.arange(200, 700, 100)))  # 우상향
print(np.cov(np.arange(1, 6),(3,3,3,3,3)))      # 직선(수평선)
print(np.cov(np.arange(1, 6),np.arange(6, 1, -1)))  # 우하향

print()
x = [8,3,6,6,9,4,3,9,3,4]
print('x 평균: ', np.mean(x))
print('x 분산 : ', np.var(x))

y = [6,2,4,6,9,5,1,8,4,5]
print('y 평균: ', np.mean(y))
print('y 분산 : ', np.var(y))

import matplotlib.pyplot as plt
plt.plot(x, y, 'o')
plt.show()
print('x, y의 공분산 : ', np.cov(x, y))
print('x, y의 공분산 : ', np.cov(x, y)[0, 1])  # 5.22222222
x2 = [80,30,60,60,90,40,30,90,30,40]
y2 = [6,2,3,6,9,5,1,8,4,5]
print('x, y의 공분산 : ', np.cov(x2, y2)[0, 1])  # 52.222222
plt.plot(x2, y2, 'o')
plt.show()

print()
# 두 데이터의 단위에 따라 패턴이 일치할지라도 
# 공분산의 크기가 달라지므로 절대적 크기 판단이 어려움
# 공분산을 표준화해서 -1 0 1 범위로 만든 것이 상관계수(r)
print('x, y의 상관계수 : ', np.corrcoef(x, y))           # 피어슨 상관계수
print('x, y의 상관계수 : ', np.corrcoef(x, y)[0, 1])     # 0.8663686
print('x2, y2의 상관계수 : ', np.corrcoef(x2, y2)[0, 1]) # 0.86636

from scipy import stats
print("scipy 모듈 사용 : ", stats.pearsonr(x, y))
# print(stats.spearmanr(x,))

print()
# 비선형 데이터인 경우 공분산, 상관계수 의미없음
m = [-3, -2, -1, 0, 1, 2, 3]
n = [9, 4, 1, 0, 1, 4, 9]
print(np.cov(m, n)[0, 1])      # 0.0
print(np.corrcoef(m, n)[0, 1]) # 0.0
plt.plot(m, n, 'o')
plt.show()