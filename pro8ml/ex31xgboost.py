import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# pip install xgboost lightgbm
import xgboost as xgb
from lightgbm import LGBMClassifier

data = load_breast_cancer()
x = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

print(x[:3], x.shape)   # (569, 30)
print(y[:3], y.shape)
print('레이블 분포 : ', {name: (y == i).sum() for i, name in enumerate(data.target_names)})
# malignant(악성): 212, benign(양성): 357

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=12, stratify=y
)
print(x_train.shape, x_test.shape)   # (455, 30) (114, 30)

# XGBoost 모델
xgb_clf = xgb.XGBClassifier(
    booster='gbtree',        # tree 기반
    max_depth=6,             # 개별 트리 최대 깊이
    n_estimators=200,        # 약한 분류기 개수
    eval_metric='logloss',
    random_state=42
)
xgb_clf.fit(x_train, y_train)

# LightGBM 모델
lgb_clf = LGBMClassifier(
    n_estimators=200,
    random_state=42
)
lgb_clf.fit(x_train, y_train)

# 예측 / 평가
pred_xgb = xgb_clf.predict(x_test)
pred_lgb = lgb_clf.predict(x_test)

print(f'XGBClassifier acc : {accuracy_score(y_test, pred_xgb):.5f}')
print(f'LGBMClassifier acc : {accuracy_score(y_test, pred_lgb):.5f}')

print('\n[XGBoost classification_report]')
print(classification_report(y_test, pred_xgb))

print('\n[LightGBM classification_report]')
print(classification_report(y_test, pred_lgb))

# 피처 중요도 : gain 기준으로 통일
booster = xgb_clf.get_booster()
xgb_gain = pd.Series(booster.get_score(importance_type='gain'))

lgb_gain = pd.Series(
    lgb_clf.booster_.feature_importance(importance_type='gain'),
    index=x_train.columns
)

# gain 비율(%) 계산
xgb_gain_pct = 100 * xgb_gain / (xgb_gain.sum() if xgb_gain.sum() != 0 else 1)
lgb_gain_pct = 100 * lgb_gain / (lgb_gain.sum() if lgb_gain.sum() != 0 else 1)

# 사용되지 않은 피처는 0으로 채움
xgb_gain_pct = xgb_gain_pct.reindex(x_train.columns).fillna(0)
lgb_gain_pct = lgb_gain_pct.reindex(x_train.columns).fillna(0)

comp_df = pd.DataFrame({
    'XGBoost (gain%)': xgb_gain_pct,
    'LightGBM (gain%)': lgb_gain_pct
}).sort_values('XGBoost (gain%)', ascending=False)

print('\n중요 피처(변수) top-10')
print(comp_df.head(10))

# 시각화
topk = 5
top = comp_df.head(topk)[::-1]

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
xmax = float(top.max().max())  # 두 모델의 최대값

for ax, col in zip(axes, ['XGBoost (gain%)', 'LightGBM (gain%)']):
    ax.barh(top.index, top[col])
    ax.set_title(f'{col.split()[0]} Feature Importance')
    ax.set_xlabel('Importance (%)')
    ax.set_xlim(0, xmax)

plt.tight_layout()
plt.show()