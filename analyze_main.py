import pandas as pd
from matplotlib import pyplot as plt
import csv

import umap
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN

umap = umap.UMAP()

data = pd.read_csv('data.csv')
# pca = PCA(n_components=1024)
# data_pca = pca.fit_transform(data.loc[:, data.columns != 'com_id'])
# print(sum(pca.explained_variance_ratio_))
#
# kmeans = KMeans(n_clusters=3)
# data_clusters = kmeans.fit_predict(data_pca)

data_features = data.loc[:, data.columns[:-2]]
# data_proj = umap.fit_transform(data_features)

# kmeans = KMeans(n_clusters=6)
# data_clusters = kmeans.fit_predict(data_proj)

dbscan = DBSCAN(eps=0.65, metric='cosine')
data_clusters = dbscan.fit_predict(data_features)

print(max(data_clusters))

result = pd.concat((data[['com_id']], pd.DataFrame(data_clusters, columns=['clstr'])), axis=1)
result.to_csv('comments_clustered.csv')

# plt.scatter(data_proj[:, 0], data_proj[:, 1], c=[('r', 'g', 'b', 'y', 'c', 'm')[i] for i in data_clusters])
# plt.show()
