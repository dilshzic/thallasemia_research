import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

excel_file = '/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

# Setup Output Directories
base_dir = '/home/dilshan/Desktop/Thallasemia research/raw_score_analysis'
charts_dir = os.path.join(base_dir, 'charts')
os.makedirs(charts_dir, exist_ok=True)

# 1. Define Correct Answers
single_choice = {
    '15. Is thalassemia a blood-related disease?': 'Yes',
    ' 17. What is the most severe form of thalassemia?': 'Thalassemia major (severe form)',
    '19. Does thalassemia major require lifelong treatment?': 'Yes',
    '20. Can thalassemia major be cured?': 'Very difficult (e.g., bone marrow transplant)',
    '21. Can the spread of thalassemia be prevented?': 'Can be prevented',
    '22. How is thalassemia transmitted?': 'From generation to generation (hereditary)',
    '23. Is a thalassemia carrier usually sick or healthy?': 'Healthy',
    '24. A child born from two thalassemia carriers will be:': 'Has a chance to be affected (e.g., 25%)',
    '26. How many thalassemia births occur in Sri Lanka per year?': '40–100'
}

multiple_choice_prefixes = [
    '16. What are the clinical forms of thalassemia? (Tick all that apply)',
    '27. Problems faced by thalassemia major patients (Tick all that apply)',
    '28. What should a thalassemia carrier do after diagnosis? (Tick all that apply)'
]

incorrect_mc_options = [
    'I don’t know', 
    'Frequent nosebleeds', 
    'Ignore it'
]

# Match columns
single_choice_cols = {}
for col in df.columns:
    for q, ans in single_choice.items():
        if q in col and '/' not in col:
            single_choice_cols[col] = ans
            break

item_meta = {}
for col, ans in single_choice_cols.items():
    match_key = None
    for key in df[col].dropna().unique():
        if str(key).strip().lower() == ans.strip().lower():
            match_key = key
            break
    if match_key:
        item_meta[col] = {'type': 'single', 'correct_ans': match_key}

for col in df.columns:
    for prefix in multiple_choice_prefixes:
        if col.startswith(prefix) and '/' in col:
            option_str = col.split('/', 1)[1].strip()
            is_incorrect = any(bad.lower() in option_str.lower() for bad in incorrect_mc_options)
            if not is_incorrect:
                item_meta[col] = {'type': 'multi'}
            break

# Calculate Raw Score (1 point per correct answer)
scores = []
for index, row in df.iterrows():
    score = 0
    for col, meta in item_meta.items():
        if meta['type'] == 'single':
            if row[col] == meta['correct_ans']:
                score += 1
        elif meta['type'] == 'multi':
            if row[col] == 1.0:
                score += 1
    scores.append(score)

df['Raw_Knowledge_Score'] = scores
output_csv = os.path.join(base_dir, 'Participant_Raw_Scores.csv')
if '_id' in df.columns:
    out_df = df[['_id', 'Raw_Knowledge_Score']].copy()
else:
    out_df = pd.DataFrame({'Participant_Index': range(1, len(df)+1), 'Raw_Knowledge_Score': scores})
out_df.to_csv(output_csv, index=False)

# Custom 1D KMeans
def kmeans_1d(X, k=3, max_iters=100):
    np.random.seed(42)
    centroids = np.random.choice(X, size=k, replace=False)
    for _ in range(max_iters):
        distances = np.abs(X[:, np.newaxis] - centroids)
        clusters = np.argmin(distances, axis=1)
        new_centroids = np.array([X[clusters == i].mean() if len(X[clusters == i]) > 0 else centroids[i] for i in range(k)])
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    return clusters, centroids

X = df['Raw_Knowledge_Score'].values
clusters, cluster_centers = kmeans_1d(X, k=3)
cluster_centers = cluster_centers.flatten()
sorted_indices = np.argsort(cluster_centers)
cluster_mapping = {sorted_indices[0]: 'Low Knowledge', 
                   sorted_indices[1]: 'Medium Knowledge', 
                   sorted_indices[2]: 'High Knowledge'}
df['Cluster'] = clusters
df['Knowledge_Level'] = df['Cluster'].map(cluster_mapping)

df.to_csv(os.path.join(base_dir, 'Participant_Raw_Clustered_Scores.csv'), index=False)

# Plot 1: Distribution
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.histplot(df['Raw_Knowledge_Score'], bins=20, kde=True, color='dodgerblue', edgecolor='black')
plt.title('Distribution of Raw Knowledge Scores (1 Pt/Answer)', fontsize=16)
plt.xlabel('Raw Knowledge Score', fontsize=14)
plt.ylabel('Number of Participants', fontsize=14)
mean_val = df['Raw_Knowledge_Score'].mean()
median_val = df['Raw_Knowledge_Score'].median()
plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='orange', linestyle='solid', linewidth=2, label=f'Median: {median_val:.2f}')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Raw_Score_Distribution.png'))
plt.close()

# Plot 2: Dot Plot
sorted_scores = df['Raw_Knowledge_Score'].sort_values().values
plt.figure(figsize=(12, 7))
plt.plot(range(len(sorted_scores)), sorted_scores, marker='o', linestyle='', color='crimson', alpha=0.7, markersize=6)
plt.title('Dot Plot of Sorted Raw Knowledge Scores', fontsize=16)
plt.xlabel('Participant Rank (Sorted)', fontsize=14)
plt.ylabel('Raw Knowledge Score', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Raw_Score_DotPlot.png'))
plt.close()

# Plot 3: KMeans Clustering
plt.figure(figsize=(10, 6))
colors = {'Low Knowledge': 'red', 'Medium Knowledge': 'orange', 'High Knowledge': 'green'}
for level, color in colors.items():
    subset = df[df['Knowledge_Level'] == level]
    plt.scatter(subset.index, subset['Raw_Knowledge_Score'], c=color, label=f"{level} (n={len(subset)})", alpha=0.7)
plt.title('K-Means Clustering of Raw Knowledge Scores (k=3)', fontsize=16)
plt.xlabel('Participant Index', fontsize=14)
plt.ylabel('Raw Knowledge Score', fontsize=14)
for center in cluster_centers:
    plt.axhline(y=center, color='gray', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Raw_KMeans_Clusters.png'))
plt.close()

print("Raw scores calculated and all plots saved in raw_score_analysis/charts/")
