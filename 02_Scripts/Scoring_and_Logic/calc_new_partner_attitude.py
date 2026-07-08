import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

excel_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

base_dir = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/specific_analyses/attitude_score_v2_analysis'
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2'
os.makedirs(base_dir, exist_ok=True)
os.makedirs(charts_dir, exist_ok=True)

# 1. Map columns for Q28 (multiple choice)
q28_cols = [c for c in df.columns if c.startswith('28.') and '/' in c]
q28_scores = {
    'Get the partner tested before marriage': 1,
    'Get family members tested': 0,
    'Ignore it': -1,
    'I don’t know': 0
}

def get_q28_score(row):
    s = 0
    for col in q28_cols:
        if row[col] == 1.0:
            option_str = col.split('/', 1)[1].strip()
            # Match option
            for key, val in q28_scores.items():
                if key.lower() in option_str.lower():
                    s += val
                    break
    return s

# 2. Map columns for single choice questions
q30_col = [c for c in df.columns if c.startswith('30.')][0]
q30_scores = {
    'yes i am willing': -2,
    'yes i have': -2,
    'not sure': -1,
    'definitely not': 1
}

q31_col = [c for c in df.columns if c.startswith('31.')][0]
q31_scores = {
    'yes': -1,
    'no': 1,
    'not sure': 0
}

q32_col = [c for c in df.columns if c.startswith('32.')][0]
q32_scores = {
    'very important': 2,
    'important': 1,
    'not sure': 0,
    'not important': -1
}

q34_col = [c for c in df.columns if c.startswith('34.')][0]
q34_scores = {
    'fear of rejection': 0,
    'lack of understanding about its importance': -1,
    'cultural or family pressure': 0,
    'did not think it was necessary': -1,
    'concern about causing worry or stress': -1,
    'other': 0
}

def get_single_score(val, score_dict):
    if pd.isna(val):
        return 0
    v_str = str(val).strip().lower()
    for k, s in score_dict.items():
        if k in v_str:
            return s
    return 0

# Calculate new scores
scores = []
for index, row in df.iterrows():
    s = 0
    s += get_q28_score(row)
    s += get_single_score(row[q30_col], q30_scores)
    s += get_single_score(row[q31_col], q31_scores)
    s += get_single_score(row[q32_col], q32_scores)
    s += get_single_score(row[q34_col], q34_scores)
    scores.append(s)

df['New_Partner_Attitude_Score'] = scores

# Save CSV
out_csv = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_New_Partner_Attitude.csv'
if '_id' in df.columns:
    df[['_id', 'New_Partner_Attitude_Score']].to_csv(out_csv, index=False)
else:
    pd.DataFrame({'New_Partner_Attitude_Score': scores}).to_csv(out_csv, index=False)

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

X = df['New_Partner_Attitude_Score'].values
clusters, centers = kmeans_1d(X, k=3)
sorted_idx = np.argsort(centers)
mapping = {sorted_idx[0]: 'Negative/Low', sorted_idx[1]: 'Neutral/Medium', sorted_idx[2]: 'Positive/High'}
df['Cluster'] = [mapping[c] for c in clusters]

# Plots
# 1. Dist
plt.figure(figsize=(10, 6))
sns.histplot(df['New_Partner_Attitude_Score'], bins=10, kde=True, color='purple', edgecolor='black')
plt.title('Distribution of New Partner Selection Attitude Scores', fontsize=16)
plt.axvline(0, color='black', linestyle='dotted', label='Zero (Neutral)')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'New_Partner_Dist.png'))
plt.close()

# 2. Dot Plot
sorted_s = df['New_Partner_Attitude_Score'].sort_values().values
plt.figure(figsize=(12, 7))
plt.plot(range(len(sorted_s)), sorted_s, marker='o', linestyle='', color='crimson')
plt.title('Sorted New Partner Selection Attitude Scores', fontsize=16)
plt.axhline(0, color='black', linestyle='dotted')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'New_Partner_DotPlot.png'))
plt.close()

# 3. KMeans Plot
plt.figure(figsize=(10, 6))
colors = {'Negative/Low': 'red', 'Neutral/Medium': 'orange', 'Positive/High': 'green'}
for level, color in colors.items():
    subset = df[df['Cluster'] == level]
    plt.scatter(subset.index, subset['New_Partner_Attitude_Score'], c=color, label=f"{level} (n={len(subset)})")
plt.title('K-Means Clusters for New Partner Selection Attitude', fontsize=16)
plt.axhline(0, color='black', linestyle='dotted')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'New_Partner_KMeans.png'))
plt.close()

print("New attitude scores calculated and saved successfully.")
