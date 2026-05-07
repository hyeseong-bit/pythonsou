# 스펨 메일 분류기

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
# Multinomial Naive Bayes (다항 나이브 베이즈).
# 텍스트에서 가장 많이 쓰는 NB 모델
# 단어의 "빈도(count)"를 기반으로 분류함
# 형태 : "단어가 많이 나왔으면 그 단어 빈도에 비례해 확률이 커짐"

# 학습용 데이터
texts = [
    "무료 쿠폰 잠금 무료 클릭",
    "한번만 클릭하면 무료",
    "오늘 회의는 2시야",
    "지금 할인 행사 진행 중",
    "회의 자료는 메일로 보내주세요",
    "지금 바로 쿠폰 확인"
]
labels = ["spam","spam","ham","spam","ham","spam"]

# 단어 등장 횟수 기반 벡터
vect = CountVectorizer() # 문서들로부터 단어의 순서 정보는 버리고, 단어 빈도수 정보를 추출
x = vect.fit_transform(texts)
print(vect.get_feature_names_out()) # ['2시야' '메일로' '무료' '바로' ...
print(x.toarray()) # [0 0 2 0 0 0 0 1 0 0 1 1 0 0 0 0 0 0 0]
print(vect.vocabulary_)  # {'무료': 2, '쿠폰': 10, '잠금': 7, '클릭': 11,
print(x)    # (0, 2) 2 <= (문서번호, 단어 번호)

# 모델
from sklearn.metrics import accuracy_score
model = MultinomialNB()
model.fit(x, labels)
pred = model.predict(x)
print('정확도 : ', accuracy_score(labels, pred))

print()
# 새로운 문장 테스트
test_text = ["무료 쿠폰 지금 발급", "간부 회의는 언제 하나요?"]
x_test = vect.transform(test_text)
print(x_test)

# 예측 + 확률 출력
preds = model.predict(x_test)
probs = model.predict_proba(x_test)
class_names = model.classes_

for text, pred, prob in zip(test_text, preds, probs):
    prob_str = ", ".join([f"{cls}:{p:.4f}" for cls, p in zip(class_names, prob)])
    print(f"'{text}' -> 예측:{pred} / 확률:[{prob_str}]")