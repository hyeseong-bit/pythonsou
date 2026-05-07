# Roc(Receiver Operatuing Characteristic) Curve는 모든 분류
# 임계값에서 분류 모델의 성능을 보여주는 그래프로 x축이 FPR(1-특이도),
# y축이 TPR(민감도)인 그래프이다.
# 즉 민감도와 특이도의 관계를 표현한 그래프이다.
# ROC Curve는 AUC(Area Under Curve : 그래프 아래의 면적)를 이용해
# 모델의 성능을 평가한다. AUC가 클수록 정확히 분류함을 뜻한다.
# fpr(1-특이도 : 위양성률)이 변할 때 tpr(민감도)이 어떻게 변하는지 알려 주는 곡선이다.

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, random_state=123)
# n_redundant : 독립변수 중 다른 독립변수의 선형조합으로 나타내는 성분수
print(x[:3], x.shape)  # (100, 2)
print(y[:3], y.shape)  # (100,)

# 산포도
# plt.scatter(x[:, 0], x[:, 1])
# plt.show()

model = LogisticRegression().fit(x, y)
y_hat = model.predict(x)
print('y_hat : ', y_hat[:5])  # [0 0 0 1 1]
print('real : ', y[:5])       #  [1 0 0 1 0]
f_value = model.decision_function(x)
print('f_value : ', f_value)
print()
df = pd.DataFrame(np.vstack([f_value, y_hat, y]).T, columns=['f', 'y_hat', 'y'])
print(df.head())

# 모델 성능 파악
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y, y_hat))
acc = (44 + 44) / 100           # TP + TN / 전체 수 정확도
recall = 44 / (44 + 4)          # TP / (TP +FN)     정밀도
precission = 44 / (44 + 8)      # TP / (TP + FP)    재현율
specificity =  44 / ( 8 + 44)   # TN / (FP + TN)    특이도
fallout =  8 / (8 + 44)         # FP / (FP + TN)    위양성율
print('acc : ', acc)
print('recall : ', recall)            # tpr : 1에 근사하면 좋음
print('precission : ', precission)
print('specificity : ', specificity)
print('fallout : ', fallout)          # fpr : 0에 근사하면 좋음
print('fallout : ', 1 - specificity)    
print()
from sklearn import metrics
acc_score = metrics.accuracy_score(y, y_hat)
print('모델 정확도 : ', acc_score)

cl_rep = metrics.classification_report(y, y_hat)
print(cl_rep)

print()
fpr, tpr, thresholds = metrics.roc_curve(y, model.decision_function(x))
print('fpr : ', fpr)
print('tpr : ', tpr)
# thresholds : 분류결정 임계값(결정함수값)

plt.plot(fpr, tpr, 'o-', label='LogisticRegression')
plt.plot([0, 1],[0, 1], 'k--', label='landom classifier lien(AUC:0.5)')
plt.plot([fallout], [recall], 'ro', ms=6)  # 위양성률, 재현율 출력
plt.xlabel('fpr')
plt.ylabel('tpr')
plt.title('ROC Curve')
plt.legend()
plt.show()

print("AUC(Area Under the Curve) : ROC 커브의 면적. 1에 근사할수록 좋은 모델")
print('AUC : ', metrics.auc(fpr, tpr))  # 0.9547275 매우 성능이 우수한 모델!


