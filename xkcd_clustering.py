''' Creates clusters, txtfiles and wordclouds from xkcd tweeter/user descrptions '''

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans

import pandas as pd
import numpy as np
import sys
import wordcloud
import os

data = pd.read_csv('xkcd_tweets.csv')
data = data[data['language'] == 'English'].drop_duplicates(cols='user_id')
dataset = data['descriptions'].dropna().values

# Vectorize
true_k = 17 # use NaturalLanguage.py to determine optimal K 
vectorizer = TfidfVectorizer(max_df=1.0, max_features=None,
                            stop_words='english', norm='l2', use_idf=True)
X = vectorizer.fit_transform(dataset)

# Reduce Dimensions with SVD
lsa = TruncatedSVD(25) # use NaturalLanguage.py to determine optimal rank
X = lsa.fit_transform(X)
X = Normalizer(copy=False).fit_transform(X)

# Cluster
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, verbose=False)
km.fit(X)


# Create cluster outputs
output_dict = {'cluster': km.labels_, 'values': dataset}
output_df = pd.DataFrame(output_dict)

# Create text files 
for i in range(true_k):
    print len(output_df[output_df.cluster == i]), round(100*len(output_df[output_df.cluster == i]) / float(len(output_df)), 2)

    cluster_text = output_df['values'][output_df.cluster == i].values
    temp = "cluster " + str(i) + ".txt"
    
    with open(temp, "w") as outfile:
       for j in cluster_text:
           outfile.write("%s\n" % j)

# Create wordclouds
for i in range(true_k):
    text = open('cluster ' + str(i) + '.txt').read()
    # Separate into a list of (word, frequency).
    words = wordcloud.process_text(text)
    # Compute the position of the words.
    elements = wordcloud.fit_words(words, font_path='/Library/Fonts/Arial Black.ttf', width=600, height=300)
    # Draw the positioned words to a PNG file.
    wordcloud.draw(elements, 'cluster ' + str(i) + '.png', font_path="/Library/Fonts/Arial Black.ttf", width=600, height=300)
