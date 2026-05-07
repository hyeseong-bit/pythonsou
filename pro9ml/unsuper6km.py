# 쇼핑몰 고객 세분화 연습

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib as mpl

# 한글 폰트 설정
mpl.rc('font', family='Malgun Gothic')
mpl.rcParams['axes.unicode_minus'] = False
# 가상의 고객 데이터 생성
np.random.seed(0)
n_customers = 200   # 고객은 200명
annul_spending = np.random.normal(50000, 15000, n_customers)    # 연간 지출액
monthly_visits = np.random.normal(5, 2, n_customers)  # 월 방문 횟수

# 구간 나누기(음수 제거 - clip을 사용해 0으로 대체)
# a = np.array([-3.2, -0.5, 1.7]) -> np.clip(a, 0, 1) -> [0, 0, 1]
annul_spending = np.clip(annul_spending, 0, None)
monthly_visits = np.clip(monthly_visits, 0, None)

data = pd.DataFrame({
    'annul spending':annul_spending,
    'monthly visits': monthly_visits
})
print(data.head(), data.size)

# 산포도
plt.scatter(data['annul spending'], data['monthly visits'])
plt.xlabel('연간 지출액')
plt.ylabel('한달 방문수')
plt.title('소비자 분포')
plt.show()

# KMeans 군집화
kMeans = KMeans(n_clusters=3, random_state=0)
clusters = kMeans.fit_predict(data) 

# 군집 결과 시각화
data['cluster'] = clusters
# print(data.head(3))
# 군집 결과 시각화
for cluster_id in np.unique(clusters):
    cluster_data = data[data['cluster'] == cluster_id]
    print(data[data['cluster'] == cluster_id])
    plt.scatter(cluster_data['annul spending'], cluster_data['monthly visits'], label =f'군집{cluster_id}')

# 중심점
plt.scatter(kMeans.cluster_centers_[:,0], kMeans.cluster_centers_[:,1],
            c='black', marker='X', s=200, label='중심점')
plt.xlabel('연간 지출액')
plt.ylabel('한달 방문수')
plt.title('수비자 군집 현황')
plt.legend()
plt.show()
