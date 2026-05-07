import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
from sklearn.decomposition import PCA

import os
os.environ['OMP_NUM_THREADS'] = '1'

# 한글 폰트
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드
iris = load_iris()
x = iris.data
y = iris.target
feature_names = iris.feature_names

df = pd.DataFrame(x, columns=feature_names)
print('iris data shape : ', x.shape)
print(df.head(3))

# 스케일링
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# KMeans
k = 3
kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, random_state=42)
clusters = kmeans.fit_predict(x_scaled)
df['cluster'] = clusters

print('클러스터 중심값:\n', kmeans.cluster_centers_)

# PCA
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
print('PCA 설명 분산 비율:', pca.explained_variance_ratio_)

# KMeans 시각화
plt.figure(figsize=(6, 5))
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=clusters, palette='Set2')
plt.title('KMeans Clustering')
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# 교차표
ct = pd.crosstab(y, clusters)
print('\n교차표:\n', ct)

print('\n클래스별 대표 군집')
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f'실제 클래스 {i} -> 군집 {max_cluster}')

# 정량 평가
print('\n정량 평가')
ari = adjusted_rand_score(y, clusters)
nmi = normalized_mutual_info_score(y, clusters)
sil_score = silhouette_score(x_scaled, clusters)

print(f'ARI : {ari:.4f}')
print(f'NMI : {nmi:.4f}')
print(f'Silhouette Score : {sil_score:.4f}')

# Elbow Method
inertia = []
k_range = range(1, 10)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(x_scaled)
    inertia.append(km.inertia_)

plt.figure(figsize=(6, 4))
plt.plot(k_range, inertia, marker='o')
plt.title('Elbow Method')
plt.xlabel('k')
plt.ylabel('Inertia')
plt.show()

# 실제 vs 군집 비교
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=y, palette='Set1')
plt.title('실제 라벨')

plt.subplot(1, 2, 2)
sns.scatterplot(x=x_pca[:, 0], y=x_pca[:, 1], hue=clusters, palette='Set2')
plt.title('KMeans 군집 결과')

plt.show()

# 클러스터 평균
pd.set_option('display.max_columns', None)
clusters_mean = df.groupby('cluster').mean()
print('\n클러스터별 평균:\n', clusters_mean)

# =========================
# ANOVA
# =========================
# 귀무가설(H0): 군집 간 평균 차이가 없다
# 대립가설(H1): 군집 간 평균 차이가 있다

from scipy.stats import f_oneway

print('\nANOVA 결과')
for col in feature_names:
    g0 = df[df['cluster'] == 0][col]
    g1 = df[df['cluster'] == 1][col]
    g2 = df[df['cluster'] == 2][col]

    f_stat, p_val = f_oneway(g0, g1, g2)
    print(f'{col} : F={f_stat:.4f}, p={p_val:.4f}')

    if p_val < 0.05:
        print('→ 군집 간 평균 차이 있음 (유의함)')
    else:
        print('→ 군집 간 평균 차이 없음')

# =========================
# Tukey
# =========================
from statsmodels.stats.multicomp import pairwise_tukeyhsd

feature = 'petal length (cm)'
tukey = pairwise_tukeyhsd(
    endog=df[feature], groups=df['cluster'], alpha=0.05
)

print('\nTukey 결과')
print(tukey)

tukey.plot_simultaneous(figsize=(6, 4))
plt.title(f'Tukey HSD - {feature}')
plt.xlabel('평균 차이')
plt.show()

# =========================
# Boxplot
# =========================
for col in feature_names:
    plt.figure(figsize=(5, 3))
    sns.boxplot(x='cluster', y=col, data=df)
    plt.title(f'{col} by cluster')
    plt.show()

# =========================
# 라벨 추가
# =========================
clusters_mean["label"] = ['Type A', 'Type B', 'Type C']
print('\n라벨 추가된 클러스터 평균:\n', clusters_mean)