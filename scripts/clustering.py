import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.utils import resample
from tqdm import tqdm

def load_and_prep_data():
    # load in csv and separate data arrays by survey, scoring, and time spent cols

    data = pd.read_csv('../data/cleaned_data_v2.csv')

    scoring = pd.read_excel('../scoring/scoring.xlsx')
    survey_answer_cols = scoring['id'].tolist()
    time_cols = [(col + '_E') for col in survey_answer_cols]
    score_cols = ['O score', 'C score', 'E score', 'A score', 'N score']

    survey_data = data[survey_answer_cols]
    time_data = data[time_cols]
    score_data = data[score_cols]

    return survey_data, score_data, time_data

def scale_data(data):
    # scale the data
    return StandardScaler().fit_transform(data)

def mb_kmeans(data, n_clusters):
    # compute mini-batch kmeans on data
    kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=1000)
    clusters = kmeans.fit_predict(data)

    return clusters

def compute_pairwise_distances(X):
    n_samples = X.shape[0]
    distance_matrix = np.zeros((n_samples, n_samples))

    for i in tqdm(range(n_samples), desc="Computing pairwise distances"):
        distance_matrix[i] = np.linalg.norm(X - X[i], axis=1)

    return distance_matrix

def manual_silhouette_score(X, labels):
    """
    Compute the silhouette score manually with tqdm progress tracking.

    Parameters:
        X (array-like): Data points (subset of original data).
        labels (array-like): Cluster labels for the subset.

    Returns:
        float: Average silhouette score.
    """
    n_samples = X.shape[0]
    distance_matrix = compute_pairwise_distances(X)  # Precompute all pairwise distances
    unique_labels = np.unique(labels)

    silhouette_scores = []

    for i in tqdm(range(n_samples), desc="Computing silhouette scores"):
        # Get distances for the current sample
        same_cluster = labels == labels[i]
        other_clusters = ~same_cluster

        # a: Mean intra-cluster distance
        a = np.mean(distance_matrix[i, same_cluster]) if np.sum(same_cluster) > 1 else 0

        # b: Mean nearest-cluster distance
        b = np.min([
            np.mean(distance_matrix[i, labels == other]) for other in unique_labels if other != labels[i]
        ])

        # Silhouette score for sample i
        silhouette_scores.append((b - a) / max(a, b))

    return np.mean(silhouette_scores)


survey_data, score_data, time_data = load_and_prep_data()
print('data loaded')
score_data = scale_data(score_data)
print('data scaled')
clusters = mb_kmeans(score_data, 6)
print('clusters generated')
# Sample 10% of the data
subset_size = int(0.1 * len(score_data))  # 10% of data
print('data sampled')
score_data_sample, clusters_6_sample = resample(score_data, clusters, n_samples=subset_size, random_state=42)
print('data reasampled')
# Compute silhouette scores with tqdm
silhouette_6_sample = manual_silhouette_score(score_data_sample, clusters_6_sample)
print('silhouette scores generated')

print(f"Silhouette Score for 6 clusters (10% sample): {silhouette_6_sample}")
