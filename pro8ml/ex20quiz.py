"""
[로지스틱 분류분석 문제2]
게임, TV 시청 데이터로 안경 착용 유무를 분류하시오.
안경 : 값0(착용X), 값1(착용O)
예제 파일 : bodycheck.csv
새로운 데이터(키보드로 입력)로 분류 확인. 스케일링X
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

# 1. 데이터 읽기
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/bodycheck.csv")
print(df.head())
print(df.columns)

# 2. 독립변수, 종속변수 지정
x = df[['게임', 'TV시청']]
y = df['안경유무']

# 3. 학습용 / 평가용 데이터 분리
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.3, random_state=42
)

print('학습용 크기 :', x_train.shape, y_train.shape)
print('평가용 크기 :', x_test.shape, y_test.shape)

# 4. 모델 생성
print('분류 모델 생성 ---------')
model = LogisticRegression(C=0.0099, solver='lbfgs', random_state=0)
print(model)

# 5. 모델 학습
model.fit(x_train, y_train)

# 6. 평가 데이터로 예측
y_pred = model.predict(x_test)

print('예측값 :', y_pred)
print('실제값 :', y_test.values)

print(f'총 갯수:{len(y_test)}, 오류 수:{(y_test != y_pred).sum()}')
print('정확도 :', accuracy_score(y_test, y_pred))

# 7. 새로운 데이터 입력
game = float(input("게임 시간 입력: "))
tv = float(input("TV 시청 시간 입력: "))

# 8. 새 데이터 예측
new_data = [[game, tv]]
pred_new = model.predict(new_data)
proba = model.predict_proba(new_data)

print("예측 결과 :", "안경 착용" if pred_new[0] == 1 else "안경 미착용")
print("확률 :", proba)
