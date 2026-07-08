import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

excel_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v3'
os.makedirs(charts_dir, exist_ok=True)

# Helper function
def get_single_score(val, score_dict):
    if pd.isna(val):
        return 0
    v_str = str(val).strip().lower()
    for k, s in score_dict.items():
        if k in v_str:
            return s
    return 0

# --- PARTNER SELECTION V3 ---
q28_cols = [c for c in df.columns if c.startswith('28.') and '/' in c]
q28_scores = {
    'get the partner tested before marriage': 2,
    'get family members tested': 1,
    'ignore it': -3,
    'i don’t know': 0
}

def get_q28_score(row):
    s = 0
    for col in q28_cols:
        if row[col] == 1.0:
            option_str = col.split('/', 1)[1].strip()
            for key, val in q28_scores.items():
                if key.lower() in option_str.lower():
                    s += val
                    break
    return s

q30_col = [c for c in df.columns if c.startswith('30.')][0]
q30_scores = {'definitely not': 2, 'not sure': -1, 'yes i am willing': -3, 'yes i have': -3}

q31_col = [c for c in df.columns if c.startswith('31.')][0]
q31_scores = {'no': 2, 'not sure': -1, 'yes': -3}

q32_col = [c for c in df.columns if c.startswith('32.')][0]
q32_scores = {'very important': 2, 'important': 1, 'not sure': -1, 'not important': -2}

# --- CASCADE SCREENING V3 ---
q35_col = [c for c in df.columns if c.startswith('35.')][0]
q35_scores = {'agree': 2, 'don’t know': 0, 'disagree': -2}

q39_col = [c for c in df.columns if c.startswith('39.')][0]
q39_scores = {'very easy': 2, 'somewhat easy': 1, 'not sure': 0, 'difficult': -1}

q40_col = [c for c in df.columns if c.startswith('40.')][0]
q40_scores = {'very important': 2, 'important': 1, 'slightly important': -1, 'not important': -2}

partner_scores = []
cascade_scores = []

for index, row in df.iterrows():
    # Partner
    ps = 0
    ps += get_q28_score(row)
    ps += get_single_score(row[q30_col], q30_scores)
    ps += get_single_score(row[q31_col], q31_scores)
    ps += get_single_score(row[q32_col], q32_scores)
    partner_scores.append(ps)
    
    # Cascade
    cs = 0
    cs += get_single_score(row[q35_col], q35_scores)
    cs += get_single_score(row[q39_col], q39_scores)
    cs += get_single_score(row[q40_col], q40_scores)
    cascade_scores.append(cs)

df['V3_Partner_Attitude'] = partner_scores
df['V3_Cascade_Attitude'] = cascade_scores

# KMeans
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

for prefix, col in [('V3_Partner', 'V3_Partner_Attitude'), ('V3_Cascade', 'V3_Cascade_Attitude')]:
    X = df[col].values
    clusters, centers = kmeans_1d(X, k=3)
    sorted_idx = np.argsort(centers)
    mapping = {sorted_idx[0]: 'Negative/Low', sorted_idx[1]: 'Neutral/Medium', sorted_idx[2]: 'Positive/High'}
    df[f'{prefix}_Cluster'] = [mapping[c] for c in clusters]
    
    # Dist
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col], bins=15, kde=True, color='indigo' if 'Partner' in prefix else 'teal', edgecolor='black')
    plt.title(f'Distribution of {prefix} Attitude Scores', fontsize=16)
    plt.axvline(0, color='black', linestyle='dotted', label='Zero (Neutral)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{prefix}_Dist.png'))
    plt.close()
    
    # Dot Plot
    sorted_s = df[col].sort_values().values
    plt.figure(figsize=(12, 7))
    plt.plot(range(len(sorted_s)), sorted_s, marker='o', linestyle='', color='crimson' if 'Partner' in prefix else 'darkorange')
    plt.title(f'Sorted {prefix} Attitude Scores', fontsize=16)
    plt.axhline(0, color='black', linestyle='dotted')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{prefix}_DotPlot.png'))
    plt.close()
    
    # KMeans
    plt.figure(figsize=(10, 6))
    colors = {'Negative/Low': 'red', 'Neutral/Medium': 'orange', 'Positive/High': 'green'}
    for level, color in colors.items():
        subset = df[df[f'{prefix}_Cluster'] == level]
        plt.scatter(subset.index, subset[col], c=color, label=f"{level} (n={len(subset)})")
    plt.title(f'K-Means Clusters for {prefix} Attitude', fontsize=16)
    plt.axhline(0, color='black', linestyle='dotted')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{prefix}_KMeans.png'))
    plt.close()

# Save CSV
out_csv = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_V3_Attitudes.csv'
cols_to_save = ['V3_Partner_Attitude', 'V3_Partner_Cluster', 'V3_Cascade_Attitude', 'V3_Cascade_Cluster']
if '_id' in df.columns:
    df[['_id'] + cols_to_save].to_csv(out_csv, index=False)
else:
    df[cols_to_save].to_csv(out_csv, index=False)

print("V3 scores calculated and saved.")
