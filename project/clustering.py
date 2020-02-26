import numpy as np
import matplotlib.pyplot as plt
# Though the following import is not directly being used, it is required
# for 3D projection to work
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn.cluster import KMeans, AgglomerativeClustering
from random import choice
from sklearn import datasets


def cluster(nrClusters,nodes, plot= False):

    cust = nodes
    nodeList = []
    for node in nodes:
        nodeList.append(node.getData())

    nodes = np.array(nodeList)

    min_max_scaler = preprocessing.MinMaxScaler()
    #nodes = min_max_scaler.fit_transform(nodes)
    #nodes = preprocessing.scale(nodes)

    estimators = [('k_means', KMeans(n_clusters=nrClusters)),
                  ('Aglo',AgglomerativeClustering(n_clusters=nrClusters))]

    fignum = 1
    titles = [str(nrClusters) +' clusters']
    name, est = choice(estimators)
    fig = plt.figure(fignum, figsize=(4, 3))
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    est.fit(nodes)
    labels = est.labels_

    ax.scatter(nodes[:, 0], nodes[:, 1], nodes[:, 2],
               c=labels.astype(np.float), edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Xco')
    ax.set_ylabel('Yco')
    ax.set_zlabel('Release dates')
    ax.set_title(titles[fignum - 1])
    ax.dist = 12
    fignum = fignum + 1
    if plot:
        plt.show()

    sol = [[] for x in range(nrClusters)]
    for x in range(len(labels)):
        sol[labels[x]].append(cust[x])
    print(sol)
    return sol
