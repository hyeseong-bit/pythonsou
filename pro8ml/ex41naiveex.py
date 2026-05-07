import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. 데이터 읽기
df = pd.read_csv("mushrooms.csv")

print(df.head(2))
print(df.info())

# 2. 종속변수(class) 숫자 변환
# edible = e, poisonous = p
# 식용: 0, 독버섯: 1 로 변환
df['class'] = df['class'].map({'e': 0, 'p': 1})

# 3. 독립변수 / 종속변수 분리
x = df.drop('class', axis=1)
y = df['class']

# 4. 범주형 데이터 원핫인코딩
x = pd.get_dummies(x)

# 5. XGBoost로 중요변수 추출
from xgboost import XGBClassifier, plot_importance

xgb_model = XGBClassifier(
    eval_metric='logloss',
    random_state=42
)

xgb_model.fit(x, y)

# 중요도 시각화
plt.figure(figsize=(10, 8))
plot_importance(xgb_model, max_num_features=10)
plt.title('XGBoost Feature Importance')
plt.show()

# 중요변수 데이터프레임으로 정리
feat_impo = pd.DataFrame({
    'feature': x.columns,
    'importance': xgb_model.feature_importances_
}).sort_values(by='importance', ascending=False)

print(feat_impo.head(10))

# 6. 중요변수 선택 (상위 10개)
top_features = feat_impo.head(10)['feature']
x_selected = x[top_features]


# 7. 학습용 / 테스트용 분리
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(
    x_selected, y, test_size=0.2, random_state=42, stratify=y
)

# 8. Naive Bayes 모델 학습
from sklearn.naive_bayes import GaussianNB

nb_model = GaussianNB()
nb_model.fit(x_train, y_train)

# 9. 예측
pred = nb_model.predict(x_test)

# 10. 평가
from sklearn.metrics import accuracy_score, confusion_matrix

print('\n분류 정확도 :', accuracy_score(y_test, pred)) # 0.9870769230769231
print('\nconfusion_matrix :\n', confusion_matrix(y_test, pred))

# 11. 교차검증
from sklearn.model_selection import cross_val_score

scores = cross_val_score(nb_model, x_selected, y, cv=5)
print('각 fold 정확도 :', scores)   # [0.88676923 0.98830769 0.97969231 0.48430769 0.67241379]
print('평균 정확도 :', scores.mean()) #  0.8022981