from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Heart.csv')
print(df.head(2), df.shape)

x = df[['Age', 'Sex', 'RestBP', 'Chol', 'Fbs', 'RestECG',
        'MaxHR', 'ExAng', 'Oldpeak', 'Slope', 'Ca']]
y = df['AHD']

# 결측치 확인
print(x.isnull().sum())

# 결측치 처리 : 평균값으로 대체
imputer = SimpleImputer(strategy='mean')
x = imputer.fit_transform(x)

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=1
)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

model = svm.SVC(C=1.0, kernel='rbf', probability=True)
print(model)

model.fit(x_train, y_train)

# 분류 예측
y_pred = model.predict(x_test)
print('예측값 : ', y_pred)
print('실제값 : ', y_test.values)

print(f'총 갯수:{len(y_test)}, 오류 수:{(y_test != y_pred).sum()}')
print('정확도 : ', metrics.accuracy_score(y_test, y_pred))

# 확률 확인
proba = model.predict_proba(x_test[:5])
print('예측 확률 : ')
print(proba)

# 임의의 값으로 예측
new_data = [[63, 1, 145, 233, 1, 2, 150, 0, 2.3, 3, 0]]
new_pred = model.predict(new_data)
new_proba = model.predict_proba(new_data)

print('새 데이터 분류 결과 : ', new_pred)
print('새 데이터 분류 확률 : ', new_proba)