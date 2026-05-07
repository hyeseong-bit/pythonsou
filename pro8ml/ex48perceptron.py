import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# -------------------------
# 실습1) 논리회로 분류
# -------------------------
feature = np.array([[0,0],[0,1],[1,0],[1,1]])
print(feature)

# label = np.array([0,0,0,1])  # AND
# label = np.array([0,1,1,1])  # OR
label = np.array([0,1,1,0])    # XOR

ml = Perceptron(max_iter=1000, random_state=42)
ml.fit(feature, label)

pred = ml.predict(feature)
print('pred : ', pred)
print('acc : ', accuracy_score(label, pred))

# XOR는 선형 분리가 안 되므로 단층 Perceptron으로는 완벽 분류가 어렵다.


# -------------------------
# 실습2) 일반 자료 분류
# -------------------------
x = np.array([
    [2, 3],
    [3, 3],
    [1, 1],
    [5, 2],
    [6, 1],
])

y = np.array([1, 1, 1, -1, -1])

model = Perceptron(max_iter=1000, eta0=0.1, random_state=42)
model.fit(x, y)

pred = model.predict(x)
print('예측값 : ', pred)
print('실제값 : ', y)
print('정확도 : ', accuracy_score(y, pred))

print('가중치(W) : ', model.coef_)
print('바이어스(B) : ', model.intercept_)

# -------------------------
# 결정 경계 시각화
# w1*x1 + w2*x2 + b = 0
# => x2 = -(w1*x1 + b) / w2
# -------------------------
plt.scatter(x[:, 0], x[:, 1], c=y, cmap='bwr')

w = model.coef_[0]
b = model.intercept_[0]

x_vals = np.linspace(0, 7, 100)
y_vals = -(w[0] * x_vals + b) / w[1]

plt.plot(x_vals, y_vals)
plt.title('sklearn Perceptron Decision Boundary')
plt.xlabel('x1')
plt.ylabel('x2')
plt.show()