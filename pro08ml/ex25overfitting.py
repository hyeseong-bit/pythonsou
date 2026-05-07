# 과적합(Overfitting) 방지 목적 :
# train-test split : 일반화 성능 향상
# K-Fold: 안정적 평가
# GridSearchCV : 최적의 하이퍼파라미터 검색

# iris dataset 사용

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
print(iris.keys())

train_data = iris.data
train_label = iris.target
print(train_data[:3])
print(train_label[:3])

# 분류모델 작성
df_clf = DecisionTreeClassifier()
df_clf.fit(train_data, train_label)     # 모든 데이터를 학습에 참여
pred = df_clf.predict(train_data)
print('예측값 : ', pred)
print('실제값 : ', train_label)
print('분류 정확도: ', accuracy_score(train_label, pred))   # 1.0 과적합 의심

print('\n과적합 방지 목적의 처리1 - train/test split')
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, \
                                                    test_size=0.3, random_state=121)
df_clf.fit(x_train, y_train)      # train data로 학습
pred2 = df_clf.predict(x_test)    # test data로 예측
print('예측값 : ', pred2)
print('실제값 : ', y_test)
print('분류 정확도: ', accuracy_score(y_test, pred2))   # 분류 정확도:  0.955555 효과: 과적합 여부 확인

print('\n과적합 방지 목적의 처리 2 - 교차검증(cross validation)')
# train data를 분할(k개 만큼)해 학습과 평가를 병행하는 방법 : K-Flod가 가장 일반적
from sklearn.model_selection import KFold
import numpy as np
features = iris.data
label = iris.target
dt_clf2 = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=12)


kfold = KFold(n_splits=5)   # k:5회 접기
cv_acc = []
print('iris shape : ', features.shape)  # 150 by 4
# KFold 학습시 전체 150행이 학습데이터(4/5, 120개), 검증데이터(1/5, 50개)로 분할되어 학습함.

n_iter = 0
# KFold 객체의 split()을 호출하면 Fold 별 학습용, 검증용 테스트의 행 인덱스를 arrary로 변환
for train_index, test_index in  kfold.split(features):
    # print('n_iter : ', n_iter)
    # print('train_index : ', train_index)
    # print('test_index : ', test_index)
    # n_iter = 1
    xtrain , xtest = features[train_index], features[test_index]
    ytrain, ytest = label[train_index], label[test_index]
    # 학습 및 예측
    dt_clf2.fit(xtrain, ytrain)
    pred = dt_clf2.predict(xtest)
    n_iter += 1
    # 반복할 때 마다 정확도 출력
    acc = np.round(accuracy_score(ytest, pred), 5)
    train_size = xtrain.shape[0]
    test_size = xtest.shape[0]
    print(f'반복수:{n_iter}, 교차검증 정확도:{acc} \
            학습데이터 크기:{train_size}, 검증크기:{test_size}')
    print(f'반복수:{n_iter}, 검증데이터:{test_index}')
    cv_acc.append(acc)

print('cv_acc: ',np.array(cv_acc).astype(float))
print('평균 검증 정확도 : ', np.mean(cv_acc))

# 참고 :  StratifiedKFold - 불균형한 분포도를 가진 레이블 데이터 집합을 처리하기 위한 kFold 방식
# 예를 들어 대출 사기 데이터인 경우 대부분은 정상, 사기 레이블은 극히 일부임
# from sklearn.model_selection import StratifiedKFold

print('\n과적합 방지 목적의 처리2-1 - 교차검증 단순화')
# cross_val_score를 이용해 교차검증을 간단히 처리 가능
from sklearn.model_selection import cross_val_score     # 내부적으로 처리함
data = iris.data
label = iris.target

score = cross_val_score(dt_clf2, data, label, scoring='accuracy', cv=5)
print('교차 검증별 정확도:', np.round(score, 5))
print('평균 검증 정확도 : ', np.round(np.mean(score), 3))

print('\n과적합 방지 목적의 처리 3 - GridSearchCV')
# 과적합 방지 간접 방법
# 최적의 파라리터 찾기(내부적으로 KFold 사용해 과적합을 줄이는데 도움을 준다)
from sklearn.model_selection import GridSearchCV
# 연습용으로 일부 파라미터만 사용 : 
# maxdepth : 노드의 최대 깊이
# min_samples_split : 노드 분할을 위한 최소한의 새플수로 과적합 제어

parameters = {'max_depth':[1, 2, 3], 'min_samples_split':[2, 3]}

grid_dtree = GridSearchCV(estimator=dt_clf2, \
                        param_grid=parameters, cv=3, refit=True)

grid_dtree.fit(x_train, y_train)   
# 내부적으로 복수 개의 모형을 생성하고, 이를 실행시켜 최적의 파라미터를 찾아줌
# best_score, best_params_s, best_esmator_, grid_score_ ...

import pandas as pd
pd.set_option('display.max_columns', None)
scores_df = pd.DataFrame(grid_dtree.cv_results_)
print(scores_df)

print('GridSearchCV 최적 파라미터 : ', grid_dtree.best_params_)
print('GridSearchCV 최적 정확도 : ', grid_dtree.best_score_)

# 최적의 모델
bestmodel = grid_dtree.best_estimator_      # 최적의 파라미터로 모델 생성
print(bestmodel)  # DecisionTreeClassifier(max_depth=3, random_state=12)
best_pred = bestmodel.predict(x_test)
print('예측 결과 : ', best_pred)
print('정확도 : ', accuracy_score(y_test, best_pred))

# 과적합 방지 기타 : 불필요한 변수 제거, 정규화(L1, L2), 데이터양 증가, 조기종료...


