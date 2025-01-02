# -*- coding: utf-8 -*-
"""PI-Task2-K-Means-Clustering.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1daPSW47DhX9wOsNGORhjHNuYb7nu2YEq

Problem Statement (of the task): to create a K-Means clustering algorithm to group customers of a retail store based on their purchase history (here its the spending score)

#Importing the dataset
"""

import pandas as pd
import numpy as np
df = pd.read_csv("Mall_Customers.csv")

"""#Exploring the data"""

df.head()

df.shape

df.columns

df.info()

df.describe()

df["Gender"].value_counts()

df.isnull().sum()

"""from exploring we have got to know that:
1. the data does not have null or missing values
2. all the features have the correct data types
3. Next we sre performing K-Means clustering

#Preprocessing the Data
"""

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
encoder = LabelEncoder()
df['Gender'] = encoder.fit_transform(df['Gender'])

"""#Model"""

num_clusters=[]
inertia=[]    #Inertia measures how well a dataset was clustered by K-Means

from sklearn.cluster import KMeans
for i in range(1,11):
    model = KMeans(n_clusters=i,init='k-means++',random_state=42)
    model.fit(df)
    num_clusters.append(i)
    inertia.append(model.inertia_)

pd.DataFrame({"num_clusters":num_clusters,"inertia":inertia})

import matplotlib.pyplot as plt
import seaborn as sns

plt.plot(num_clusters, inertia,marker = 'o')
plt.title("Find the best number of Clusters ")
plt.xlabel("Count of Clusters")
plt.ylabel("% of Error")
plt.grid(True)
plt.show()

"""from this graph we can see that the number of optimal clusters are 4 (elbow curve method)"""

model = KMeans(n_clusters=4,init='k-means++',random_state=42)
model.fit(df)

model.inertia_

predict=model.predict(df)

df["clusters"] = predict

df.sample(5)

cluster_1 = df[df.clusters == 0]
cluster_2 = df[df.clusters == 1]
cluster_3 = df[df.clusters == 2]
cluster_4 = df[df.clusters == 3]

plt.scatter(cluster_1['Annual Income (k$)'], cluster_1['Spending Score (1-100)'], label='cluster 1')
plt.scatter(cluster_2['Annual Income (k$)'], cluster_2['Spending Score (1-100)'], label='cluster 2')
plt.scatter(cluster_3['Annual Income (k$)'], cluster_3['Spending Score (1-100)'], label='cluster 3')
plt.scatter(cluster_4['Annual Income (k$)'], cluster_4['Spending Score (1-100)'], label='cluster 4')
plt.title('Final Clusters')
plt.xlabel('Annual Income (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()

"""#Analyzing the data after clustering them"""

sns.countplot(x = df.clusters)                            #number of people in each cluster

df.clusters.value_counts().plot.pie(autopct= '%0.2f%%')                    #number of people in each cluster

sns.boxplot(x=df.clusters,y=df['Annual Income (k$)'])                    #cluster to annual income comparision

sns.boxplot(x=df.clusters,y=df['Spending Score (1-100)'])                 #cluster to spending score comparison

sns.histplot(df.Age)                                                     #age distribution

sns.countplot(x=df["Gender"])                              #gender distribution

import matplotlib.pyplot as plt
import numpy as np

grouped_data = df.groupby(['clusters', 'Gender']).size().unstack(fill_value=0)

male_counts = grouped_data.get(0, [0] * len(grouped_data))
female_counts = grouped_data.get(1, [0] * len(grouped_data))

clusters = grouped_data.index.astype(str)
bar_width = 0.35
x = np.arange(len(clusters))

plt.bar(x - bar_width / 2, male_counts, width=bar_width, label='Male', color='blue')
plt.bar(x + bar_width / 2, female_counts, width=bar_width, label='Female', color='pink')

plt.xlabel('Clusters')
plt.ylabel('Counts')
plt.title('Male vs Female Counts in Each Cluster')
plt.xticks(x, clusters)
plt.legend()

plt.tight_layout()
plt.show()