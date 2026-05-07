# 다중선형회귀 : tv, radio, newspaper가 sales 얼마나 영향을 주는지 파악

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head(2))
del data['no']
print(data.head(2))

fdata = data[['tv','radio','newspaper']]
ldata = data.iloc[:, [3]]
print(fdata.head(2))
print(ldata[:2])

from sklearn.preprocessing import MinMaxScaler, minmax_scale, StandardScaler

fedata = minmax_scale(fdata, axis=0, copy=True)
print(fedata[:3])

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    fedata, ldata,
    shuffle=True,
    test_size=0.3,
    random_state=123
)

print(x_train[:2], x_train.shape)
print(x_test[:2], x_test.shape)

print()

model = Sequential()
model.add(Input(shape=(3, )))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='linear'))
print(model.summary())

try:
    tf.keras.utils.plot_model(
        model,
        to_file='aaa.png',
        show_shapes=True,
        show_layer_names=True,
        show_dtype=True,
        show_layer_activations=True,
        dpi=96
    )
except ImportError:
    print('Graphviz가 설치되지 않아 모델 구조 이미지 저장은 생략합니다.')

model.compile(optimizer='adam', loss='mse', metrics=['mse'])

history = model.fit(
    x_train, y_train,
    epochs=100,
    batch_size=32,
    verbose=2,
    validation_split=0.2
)

ev_loss = model.evaluate(x_test, y_test, verbose=0)
print('ev_loss : ', ev_loss)

print('history val_loss : ', history.history['val_loss'])
print('history val_mse : ', history.history['val_mse'])
print('history loss : ', history.history['loss'])
print('history mse : ', history.history['mse'])

import matplotlib.pyplot as plt
plt.plot(history.history['val_loss'], label='val_loss')
plt.plot(history.history['loss'], label='loss')
plt.legend()
plt.show()

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(y_test, model.predict(x_test)))

pred = model.predict(x_test[:5])
print('예측값 : ', pred.ravel())
print('실제값 : ', y_test[:5].values.ravel())

print('\n\nFunctional api를 사용한 방법--------')
from tensorflow.keras.models import Model

inputs = Input(shape=(3, ), name='input_layer')
x = Dense(units=16, activation='relu', name='hidden_layer1')(inputs)
x = Dense(units=8, activation='relu', name='hidden_layer2')(x)
outputs = Dense(units=1, activation='linear', name='output_layer')(x)

func_model = Model(inputs=inputs, outputs=outputs)   # 수정
print(func_model.summary())

func_model.compile(optimizer='adam', loss='mse', metrics=['mse'])

func_history = func_model.fit(   # 수정
    x_train, y_train,
    epochs=100,
    batch_size=32,
    verbose=2,
    validation_split=0.2
)

func_ev_loss = func_model.evaluate(x_test, y_test, verbose=0)
print('func_ev_loss : ', func_ev_loss)

print('설명력 :', r2_score(y_test, func_model.predict(x_test)))