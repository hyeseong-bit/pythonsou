import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# 실습1) 논리회로 분류
feature = np.array([[0,0],[0,1],[1,0],[1,1]])
print(feature)

# label = np.array([0,0,0,1])  # AND
# label = np.array([0,1,1,1])  # OR
label = np.array([0,1,1,0])    # XOR 해결함

# max_iter의 추천 횟수 : 500 ~ 1000
ml = MLPClassifier(max_iter=500, hidden_layer_sizes=10,\
                    solver='adam',  # cost 최소화 방식
                    learning_rate_init=0.01, verbose=1).fit(feature, label)

print(ml)
pred = ml.predict(feature)
print('pred : ', pred)
print('acc : ', accuracy_score(label, pred))

print('-----------------------')
# 실습2) 일반 자료로 분류
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

x, y = make_moons(n_samples=300, noise=0.2, random_state=42)
print(x[:2])    
print(y[:2])    # [1 1]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

model = MLPClassifier(hidden_layer_sizes=(10, 10), solver='adam',\
                    max_iter=1000, random_state=42, activation='relu')
model.fit(x_train, y_train)

pred = model.predict(x_test)
print('acc : ', accuracy_score(y_test, pred)) # 0.96666666

