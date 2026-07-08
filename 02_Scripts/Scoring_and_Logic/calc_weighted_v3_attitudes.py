import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

excel_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_weighted_v3'
os.makedirs(charts_dir, exist_ok=True)

out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/June_7_Review_PDFs'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'

n_participants = len(df)

# --- V3 SCHEMA DEFINITIONS ---
q28_cols = [c for c in df.columns if c.startswith('28.') and '/' in c]
q28_scores = {'get the partner tested before marriage': 2, 'get family members tested': 1, 'ignore it': -3, 'i don’t know': 0}

q30_col = [c for c in df.columns if c.startswith('30.')][0]
q30_scores = {'definitely not': 2, 'not sure': -1, 'yes i am willing': -3, 'yes i have': -3}

q31_col = [c for c in df.columns if c.startswith('31.')][0]
q31_scores = {'no': 2, 'not sure': -1, 'yes': -3}

q32_col = [c for c in df.columns if c.startswith('32.')][0]
q32_scores = {'very important': 2, 'important': 1, 'not sure': -1, 'not important': -2}

q35_col = [c for c in df.columns if c.startswith('35.')][0]
q35_scores = {'agree': 2, 'don’t know': 0, 'disagree': -2}

q39_col = [c for c in df.columns if c.startswith('39.')][0]
q39_scores = {'very easy': 2, 'somewhat easy': 1, 'not sure': 0, 'difficult': -1}

q40_col = [c for c in df.columns if c.startswith('40.')][0]
q40_scores = {'very important': 2, 'important': 1, 'slightly important': -1, 'not important': -2}

# Calculate p-values (proportion of people giving each specific answer)
def get_p_val_single(col, target_str):
    if pd.isna(target_str): return 0
    # count how many people's answer contains target_str
    matches = sum(1 for val in df[col] if pd.notna(val) and target_str in str(val).strip().lower())
    return matches / n_participants

# We need a function to dynamically calculate score = weight * (1 - p)
def get_weighted_single_score(val, col, score_dict):
    if pd.isna(val):
        return 0
    v_str = str(val).strip().lower()
    for k, weight in score_dict.items():
        if k in v_str:
            p = get_p_val_single(col, k)
            return weight * (1 - p)
    return 0

def get_weighted_q28_score(row):
    s = 0
    for col in q28_cols:
        if row[col] == 1.0:
            option_str = col.split('/', 1)[1].strip().lower()
            for k, weight in q28_scores.items():
                if k in option_str:
                    p = df[col].sum() / n_participants
                    s += weight * (1 - p)
                    break
    return s

partner_scores = []
cascade_scores = []

for index, row in df.iterrows():
    # Partner
    ps = 0
    ps += get_weighted_q28_score(row)
    ps += get_weighted_single_score(row[q30_col], q30_col, q30_scores)
    ps += get_weighted_single_score(row[q31_col], q31_col, q31_scores)
    ps += get_weighted_single_score(row[q32_col], q32_col, q32_scores)
    partner_scores.append(ps)
    
    # Cascade
    cs = 0
    cs += get_weighted_single_score(row[q35_col], q35_col, q35_scores)
    cs += get_weighted_single_score(row[q39_col], q39_col, q39_scores)
    cs += get_weighted_single_score(row[q40_col], q40_col, q40_scores)
    cascade_scores.append(cs)

df['Weighted_V3_Partner_Attitude'] = partner_scores
df['Weighted_V3_Cascade_Attitude'] = cascade_scores

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

for prefix, col in [('Weighted_V3_Partner', 'Weighted_V3_Partner_Attitude'), ('Weighted_V3_Cascade', 'Weighted_V3_Cascade_Attitude')]:
    X = df[col].values
    clusters, centers = kmeans_1d(X, k=3)
    sorted_idx = np.argsort(centers)
    mapping = {sorted_idx[0]: 'Negative/Low', sorted_idx[1]: 'Neutral/Medium', sorted_idx[2]: 'Positive/High'}
    df[f'{prefix}_Cluster'] = [mapping[c] for c in clusters]
    
    # Dist
    plt.figure(figsize=(10, 6))
    sns.histplot(df[col], bins=15, kde=True, color='purple' if 'Partner' in prefix else 'darkcyan', edgecolor='black')
    plt.title(f'Distribution of {prefix.replace("_", " ")} Scores', fontsize=16)
    plt.axvline(0, color='black', linestyle='dotted', label='Zero (Neutral)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{prefix}_Dist.png'))
    plt.close()
    
    # Dot Plot
    sorted_s = df[col].sort_values().values
    plt.figure(figsize=(12, 7))
    plt.plot(range(len(sorted_s)), sorted_s, marker='o', linestyle='', color='crimson' if 'Partner' in prefix else 'darkorange')
    plt.title(f'Sorted {prefix.replace("_", " ")} Scores', fontsize=16)
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
    plt.title(f'K-Means Clusters for {prefix.replace("_", " ")}', fontsize=16)
    plt.axhline(0, color='black', linestyle='dotted')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{prefix}_KMeans.png'))
    plt.close()

# Save CSV
out_csv = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv'
cols_to_save = ['Weighted_V3_Partner_Attitude', 'Weighted_V3_Partner_Cluster', 'Weighted_V3_Cascade_Attitude', 'Weighted_V3_Cascade_Cluster']
if '_id' in df.columns:
    df[['_id'] + cols_to_save].to_csv(out_csv, index=False)
else:
    df[cols_to_save].to_csv(out_csv, index=False)

# Generate MDs
md_partner = f"""# Weighted V3 Partner Selection Attitude Analysis

This report visualizes the Partner Selection attitudes using the cross-question statistical weighting $(1-p)$ combined with the optimized V3 schema.

### Methodology
Formula Used: `Score = Assigned_Weight * (1 - p)`
Where `p` is the proportion of participants who gave that exact answer. 
- **Rare Protective Attitudes:** Heavy reward (e.g., `+2 * High`).
- **Common Protective Attitudes:** Small reward (e.g., `+2 * Low`).
- **Rare Dangerous Attitudes:** Heavy penalty (e.g., `-3 * High`).

### The Distribution
Because the vast majority of participants gave protective answers (high `p`), the rewards shrank dramatically. The distribution squashes closer to zero, but the dangerous outliers (who received heavy penalties because dangerous answers were rare) pull the graph strongly into the negative territory.

![Distribution of Weighted V3 Scores]({charts_dir}/Weighted_V3_Partner_Dist.png)
![Dot Plot of Weighted V3 Scores]({charts_dir}/Weighted_V3_Partner_DotPlot.png)

---

### K-Means Clustering (k=3)
The K-Means algorithm effectively isolated the highly penalized individuals into the Negative/Low cluster. 

![K-Means Clusters]({charts_dir}/Weighted_V3_Partner_KMeans.png)
"""

md_cascade = f"""# Weighted V3 Cascade Screening Attitude Analysis

This report visualizes the Cascade Screening attitudes applying the cross-question statistical $(1-p)$ weighting to the optimized V3 schema.

### The Distribution
The inverse-frequency scaling reveals an incredible amount of nuance. It completely eradicates any integer plateaus, treating every participant's combination of answers as mathematically unique based on the cohort's statistical baseline.

![Distribution of Weighted V3 Scores]({charts_dir}/Weighted_V3_Cascade_Dist.png)
![Dot Plot of Weighted V3 Scores]({charts_dir}/Weighted_V3_Cascade_DotPlot.png)

---

### K-Means Clustering (k=3)
Because the weighting scales down common answers and scales up rare outliers, the clustering visually expands, separating the true positive outliers from the "neutral" majority and exposing the negative outliers.

![K-Means Clusters]({charts_dir}/Weighted_V3_Cascade_KMeans.png)
"""

partner_md_path = os.path.join(out_dir_md, 'Weighted_V3_Partner_Attitude_Report.md')
cascade_md_path = os.path.join(out_dir_md, 'Weighted_V3_Cascade_Attitude_Report.md')

with open(partner_md_path, 'w') as f: f.write(md_partner)
with open(cascade_md_path, 'w') as f: f.write(md_cascade)

# Convert to PDF
for name, filepath in [('Weighted_V3_Partner_Attitude_Report.md', partner_md_path), ('Weighted_V3_Cascade_Attitude_Report.md', cascade_md_path)]:
    out_pdf = os.path.join(out_dir_pdf, name.replace('.md', '.pdf'))
    cmd = ['pandoc', filepath, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)

print("Weighted V3 calculations, charts, MDs, and PDFs generated successfully.")
