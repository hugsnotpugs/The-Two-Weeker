''' Code to help with NLP analysis: 
    NLPOperations Methods
    1. Find the optimal rank of your data matrix (LSA / SVD / PCA)
    2. Find the optimal k in k-means clustering (spherical) 
    Note: NLPOperations takes vectorized data as an input (i.e. TF-IDF) '''

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist, pdist

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

### Class takes vectorized data as inputs
class NLPOperations():
    
    def __init__(self, vectorized_data):
        self.X = vectorized_data
        
    def find_rank(self, rank, vertline=None):
        
        svd = TruncatedSVD(rank)
        svd.fit(self.X)
        scree = svd.explained_variance_ratio_
        
        fig, ax = plt.subplots()
        plt.scatter(np.arange(0, len(scree[1:])), scree[1:], s=25, alpha=0.5)
        ax.set_ylim(0, scree[1:].max()*1.05)
        
        if vertline != None:
            plt.axvline(vertline, c='red', alpha=0.75)

        plt.show()
        
    def find_k(self, rank=None, max_clusters=1, vertline=None):
        
        if rank != None:
            svd = TruncatedSVD(rank)
            self.X = svd.fit_transform(self.X)
            self.X = Normalizer(copy=False).fit_transform(self.X)
        
        k_range = range(1, max_clusters)
        clusters = [KMeans(n_clusters=k).fit(self.X) for k in k_range]
        centroids = [cluster.cluster_centers_ for cluster in clusters]
        k_cosine = [cdist(self.X, cent, metric='cosine') for cent in centroids]
        dist = [np.min(k_cos, axis=1) for k_cos in k_cosine]
        
        wcss = [sum(d[np.isnan(d) == False]**2) for d in dist] # Within cluster sum of squares
        tss = sum(pdist(self.X)**2)/self.X.shape[0] # Total sum of squares
        bss = tss - wcss # Explained variance
                
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(10, 3)
        plt.tight_layout()
        
        ax1.set_title('BSS')
        ax1.plot(np.arange(1, len(bss)+1), bss)
        ax1.scatter(np.arange(1, len(bss)+1), bss)        
        ax2.set_title('WCSS')
        ax2.plot(np.arange(1, len(wcss)+1), wcss)
        ax2.scatter(np.arange(1, len(wcss)+1), wcss)
        plt.axvline(vertline, c='red', alpha=0.75) if vertline != None else None
            
        plt.show()

        


