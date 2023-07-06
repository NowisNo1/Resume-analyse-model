import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN

# dbscan
eps = 40
minPts = 5
# multi dbscan
e = [15, 40]
m = [ 1,  5]


def dbscan(points):
    points_np = np.array(points.loc[:, 'x':'y'].values)
    chunk = DBSCAN(eps=eps, min_samples=minPts).fit_predict(points_np)

    plt.figure(figsize=(6, 8))
    plt.scatter(points_np[:, 0], points_np[:, 1], c=chunk)
    plt.axis('off')
    plt.show()

    return chunk


def dbscan_multi(points):
    points_np = np.array(points)
    chunk = []
    for ee, mm in zip(e, m):
        chunk.append(DBSCAN(eps=ee, min_samples=mm).fit_predict(points_np))
        # plt.figure(figsize=(6, 9))
        # plt.scatter(points_np[:, 0], points_np[:, 1], c=chunk)
        # plt.show()
    return chunk
