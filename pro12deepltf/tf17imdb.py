# imdb dataset으로 이진 분류 : 영화 리뷰(긍정, 부정)
# train : 25000, test : 25000

from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os

# 자주 등장하는 단어 1만개만 사용
num_words = 10000

(train_data, train_label), (test_data, test_label) = imdb.load_data(num_words=num_words)

print(type(train_data), train_data.shape)
print(type(test_data), test_data.shape)
print(type(train_data[0]), len(train_data[0]))
print(train_label[0])  # 0: 부정, 1: 긍정

# 단어 인덱스 확인
word_index = imdb.get_word_index()

sorted_word_index = sorted(word_index.items(), key=lambda x: x[1])

for word, index in sorted_word_index[:10]:
    print(word, index)

# 숫자 → 단어로 변환
reversed_word_index = {
    index + 3: word
    for word, index in word_index.items()
}

# 특수 토큰
reversed_word_index[0] = "<PAD>"
reversed_word_index[1] = "<START>"
reversed_word_index[2] = "<UNK>"
reversed_word_index[3] = "<UNUSED>"

# 0번째 리뷰 문장 복원
decoded_review = " ".join(
    reversed_word_index.get(i, "?") for i in train_data[0]
)

print("0번째 리뷰 문장:")
print(decoded_review)

print("0번째 리뷰 정답:", train_label[0])

# 리뷰 길이 확인
review_len = [len(review) for review in train_data]

print("최소 길이:", np.min(review_len))
print("최대 길이:", np.max(review_len))
print("평균 길이:", np.mean(review_len))
print("중앙값:", np.median(review_len))

plt.figure(figsize=(8, 5))
plt.hist(review_len, bins=50)
plt.xlabel("리뷰 길이")
plt.ylabel("건수")
plt.title("IMDB 리뷰 길이 분포")
plt.grid(True)
plt.show()

# padding : 리뷰 문장 문장 길이가 다름. 모델에 넣기 전에 길이를 맞춤
# 각 리뷰를 최대 200 단어 index로 맞춤. 길면 앞부분 자르고, 짧으면 0으로 채움
maxlen = 200

x_train = pad_sequences(train_data, maxlen=maxlen)
x_test = pad_sequences(test_data, maxlen=maxlen)

y_train = np.array(train_label).astype(np.float32)
y_test = np.array(test_label).astype(np.float32)

print('x_train : ', x_train.shape) #  (25000, 200)
print('x_test : ', x_test.shape)    # (25000, 200)
print('y_train : ', y_train.shape)  # (25000,)
print('y_test : ', y_test.shape)    # (25000,)
print('패딩된 1번째 : ', x_train[1])

# 모델 저장용 폴더 준비
MODEL_DIR = "./imdb_model/"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

modelpath = "./imdb_model/imdb_best.keras"

model = Sequential([
    Input(shape=(maxlen, )),
    Embedding(  # 단어 index를 밀집 벡터로 변환
        input_dim=num_words     # 리뷰1개가 단어번호 200개로 들어옴
        ,output_dim=32          # 단어 하나를 32개를 실수로 표현함
        # 밀집 백터화 : 실수 기반의 고정 크기에 실수값으로 채움. 예:[0.2, -0.1, -0.03, 0.5 ...]
    ),
    GlobalAveragePooling1D(),
    # 200개의 단어 벡터를 평균내서 리뷰 전체를 하나의 32차원 벡터화. 이것이 리뷰 전체의 특성
    Dense(units=32, activation='relu'),
    Dropout(0.3),
    Dense(units=16, activation='relu'),
    Dropout(0.3),
    Dense(units=1, activation='sigmoid')
])
print(model.summary())

model.compile(optimizer=Adam(learning_rate=0.001), \
                                loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
chkpoint = ModelCheckpoint(filepath=modelpath, monitor='val_loss', \
                            save_best_only=True, verbose=0)

history = model.fit(x_train, y_train, epochs=50, batch_size=512, \
                    validation_split=0.2, callbacks=[early_stop, chkpoint], verbose=2)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print('테스트 평가 손실 : ', loss)
print('테스트 평가 정확도 : ', acc)

# loss, acc 시각화
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend()
plt.grid(True)
plt.show()

print('\n\n저장된 모델 읽어 분류 예측')
best_model = load_model(modelpath)
best_loss, best_acc = best_model.evaluate(x_test, y_test, verbose=0)
print('best_loss 평가 손실 : ', best_loss)
print('best_acc 평가 정확도 : ', best_acc)

# 기존 데이터를 사용해 예측
new_data = x_test[:5]
new_label = y_test[:5]
pred_prob = best_model.predict(new_data, verbose=0)
pred_class = (pred_prob >= 0.5).astype(int).ravel()
print('예측 확률 : ', pred_prob.ravel())
print('예측 값 : ', pred_class.ravel())
print('예측 실제값 : ', new_label.astype(int).ravel())

for i in range(5):
    result = "긍정" if pred_class[i] == 1 else "부정"
    real = "긍정" if new_label[i] == 1 else "부정"
    print(f"{i + 1}번 리뷰 예측:{result}, 실제:{real}, 긍정확률:{pred_prob[i][0]:.3f}")