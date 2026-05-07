#  Advertising.csv 파일을 읽어 tv,radio,newspaper 간의 상관관계를 파악하시오. 
# 또한 sales와 관계를 알기 위해 sales에 상관 관계를 정렬한 후 TV, radio, newspaper에 대한 영향을 해석하시오.
# 그리고 이들의 관계를 heatmap 그래프로 표현하시오. 

import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head())
print(data.describe())

# 상관관계

print()
print(data.corr(method='pearson'))
print(data.drop(columns=['no']).corr()['sales'].sort_values(ascending=False))
#  sales 기준 상관관계
# TV는 매출과 강한 양의 상관관계를 가져 가장 큰 영향을 미친다
# radio는 중간 정도의 양의 상관관계로 일정 수준 영향을 준다
# newspaper는 약한 상관관계로 영향이 미미하다

# 시각화
import seaborn as sns
sns.heatmap(data.corr(), annot=True)
plt.show()