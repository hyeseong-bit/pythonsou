# RandomForest는 분류, 회귀 모두 가능. sklearn 모듈은 대개 그러하다.
# 캘리포니아 주택 가격 데이터로 회귀분석

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# 1. 데이터 불러오기
housing = fetch_california_housing(as_frame=True)

print(housing.DESCR)

pd.set_option('display.max_columns', None)

print(housing.data[:2])
print(housing.target[:2])
print(housing.feature_names[:2])

df = housing.frame
print(df.head(3))

# 2. 독립변수 / 종속변수
x = df.drop('MedHouseVal', axis=1)
y = df['MedHouseVal']

# 3. train / test 분리
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=42
)

# 4. 모델 생성 및 학습
rfmodel = RandomForestRegressor(n_estimators=200, random_state=42)
rfmodel.fit(x_train, y_train)

# 5. 예측 및 평가
y_pred = rfmodel.predict(x_test)

print(f'MSE : {mean_squared_error(y_test, y_pred):.3f}')
print(f'R2(결정계수) : {r2_score(y_test, y_pred):.3f}')

# 6. 변수 중요도 시각화
importances = rfmodel.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(8, 5))
plt.bar(range(x.shape[1]), importances[indices], align='center')
plt.xticks(range(x.shape[1]), x.columns[indices], rotation=45)
plt.xlabel('feature name')
plt.ylabel('feature importances')
plt.tight_layout()
plt.show()

print('중요 변수 순위 정보 저장')
ranking = pd.DataFrame({
    'feature': x.columns[indices],
    'importance': importances[indices]
})
print(ranking)

# 7. 하이퍼파라미터 튜닝
# GridSearchCV와 달리 사용자가 지정한 범위, 분포에서 임의로 일부 조합만 샘플링해 탐색
# 연속적인 값 범위도 가능. 무작위이기 때문에 최적 조합을 놓칠 수 있다.

param_dist = {
    'n_estimators': [200, 400, 800],
    'max_depth': [None, 10, 20, 30],
    'min_samples_leaf': [1, 2, 4],      # 리프노드에 필요한 최소 샘플 수
    'min_samples_split': [2, 4, 6],     # 노드 분할에 필요한 최소 샘플 수
    'max_features': [None, 'sqrt', 'log2', 1.0, 0.8, 0.6]
}

search = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=param_dist,
    n_iter=20,      # 20개의 랜덤한 파라미터 조합 탐색
    scoring='r2',
    cv=3,
    random_state=42,
    verbose=1,
    n_jobs=-1
)

search.fit(x_train, y_train)

print('best_params :', search.best_params_)
best = search.best_estimator_
print('best R2 :', search.best_score_)
print('final R2 :', r2_score(y_test, best.predict(x_test)))