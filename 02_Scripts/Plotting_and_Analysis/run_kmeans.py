import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

artifact_dir = '/home/dilshan/.gemini/antigravity/brain/2df2cc95-ca41-4d9d-a116-04a1b43127d8/'
output_image = os.path.join(artifact_dir, 'KMeans_Clusters.png')

csv_file = '/home/dilshan/Desktop/Thallasemia research/Participant_Weighted_Scores.csv'
df = pd.read_csv(csv_file)

# Custom 1D KMeans
def kmeans_1d(X, k=3, max_iters=100):
    # Initialize centroids randomly from the data
    np.random.seed(42)
    centroids = np.random.choice(X, size=k, replace=False)
    for _ in range(max_iters):
        # Assign clusters
        distances = np.abs(X[:, np.newaxis] - centroids)
        clusters = np.argmin(distances, axis=1)
        
        # Update centroids
        new_centroids = np.array([X[clusters == i].mean() if len(X[clusters == i]) > 0 else centroids[i] for i in range(k)])
        
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    return clusters, centroids

X = df['Weighted_Knowledge_Score'].values
clusters, cluster_centers = kmeans_1d(X, k=3)
df['Cluster'] = clusters

# Order clusters so 0 is Low, 1 is Medium, 2 is High
cluster_centers = cluster_centers.flatten()
sorted_indices = np.argsort(cluster_centers)
cluster_mapping = {sorted_indices[0]: 'Low Knowledge', 
                   sorted_indices[1]: 'Medium Knowledge', 
                   sorted_indices[2]: 'High Knowledge'}

df['Knowledge_Level'] = df['Cluster'].map(cluster_mapping)

# Save the updated CSV
output_csv = '/home/dilshan/Desktop/Thallasemia research/Participant_Clustered_Scores.csv'
df.to_csv(output_csv, index=False)

# Plotting the clusters
plt.figure(figsize=(10, 6))

colors = {'Low Knowledge': 'red', 'Medium Knowledge': 'orange', 'High Knowledge': 'green'}
for level, color in colors.items():
    subset = df[df['Knowledge_Level'] == level]
    # We plot against a jittered y-axis or just a 1D strip plot, but let's use the sorted rank approach again
    # We sort the subset by score just to stack them nicely, or we can just do a scatter plot with index
    plt.scatter(subset.index, subset['Weighted_Knowledge_Score'], c=color, label=f"{level} (n={len(subset)})", alpha=0.7)

plt.title('K-Means Clustering of Knowledge Scores (k=3)', fontsize=16)
plt.xlabel('Participant Index (Unsorted)', fontsize=14)
plt.ylabel('Weighted Knowledge Score', fontsize=14)
plt.axhline(y=cluster_centers[sorted_indices[0]], color='red', linestyle='--', alpha=0.5)
plt.axhline(y=cluster_centers[sorted_indices[1]], color='orange', linestyle='--', alpha=0.5)
plt.axhline(y=cluster_centers[sorted_indices[2]], color='green', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

plt.savefig(output_image, dpi=150)
print(f"Cluster boundaries based on centers: {cluster_centers[sorted_indices]}")
print(f"Chart saved to {output_image}")
