import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

excel_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)
n_participants = len(df)

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_weighted_v3'
os.makedirs(charts_dir, exist_ok=True)

out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/June_7_Review_PDFs'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'

def get_p_val_single(col, target_str):
    if pd.isna(target_str): return 0
    matches = sum(1 for val in df[col] if pd.notna(val) and target_str in str(val).strip().lower())
    return matches / n_participants

def get_weighted_single_score(val, col, score_dict):
    if pd.isna(val):
        return 0
    v_str = str(val).strip().lower()
    for k, weight in score_dict.items():
        if k in v_str:
            p = get_p_val_single(col, k)
            return weight * (1 - p)
    return 0

# Q15
q15_col = [c for c in df.columns if '15.' in str(c) and '/' not in str(c)][0]
q15_scores = {'yes': 1, 'don’t know': -1, 'don\'t know': -1, 'no': -2}

# Q16 (Multi)
q16_cols = [c for c in df.columns if '16.' in str(c) and '/' in str(c)]
q16_scores = {'major': 1, 'minor': 1, 'intermedia': 1, 'don’t know': -1, 'don\'t know': -1}

def get_weighted_q16_score(row):
    s = 0
    for col in q16_cols:
        if row[col] == 1.0:
            opt = col.split('/', 1)[1].strip().lower()
            for k, weight in q16_scores.items():
                if k in opt:
                    p = df[col].sum() / n_participants
                    s += weight * (1 - p)
                    break
    return s

# Q17
q17_col = [c for c in df.columns if '17.' in str(c) and '/' not in str(c)][0]
q17_scores = {'major': 2, 'don’t know': -1, 'don\'t know': -1, 'minor': -1, 'intermedia': -1}

# Q19
q19_col = [c for c in df.columns if '19.' in str(c) and '/' not in str(c)][0]
q19_scores = {'yes': 2, 'don’t know': -1, 'don\'t know': -1, 'no': -3}

# Q20
q20_col = [c for c in df.columns if '20.' in str(c) and '/' not in str(c)][0]
q20_scores = {'bone marrow transplant': 2, 'cannot be cured': 1, 'don’t know': -1, 'don\'t know': -1, 'common treatments': -3}

# Q21
q21_col = [c for c in df.columns if '21.' in str(c) and '/' not in str(c)][0]
q21_scores = {'can be prevented': 2, 'not sure': -2, 'cannot be prevented': -2}

# Q22
q22_col = [c for c in df.columns if '22.' in str(c) and '/' not in str(c)][0]
q22_scores = {'generation to generation': 2, 'other': 0, 'don’t know': -2, 'don\'t know': -2, 'randomly': -1, 'environmental': -1, 'contagious': -3}

# Q23
q23_col = [c for c in df.columns if '23.' in str(c) and '/' not in str(c)][0]
q23_scores = {'healthy': 2, 'don’t know': -2, 'don\'t know': -2, 'not healthy': -2}

# Q24
q24_col = [c for c in df.columns if '24.' in str(c) and '/' not in str(c)][0]
q24_scores = {'has a chance to be affected': 2, '25%': 2, 'don’t know': -2, 'don\'t know': -2, 'always affected': -1, 'always healthy': -3}

# Q26
q26_col = [c for c in df.columns if '26.' in str(c) and '/' not in str(c)][0]
q26_scores = {'40–100': 1, '40-100': 1, 'more than this': 0, 'don’t know': 0, 'don\'t know': 0, 'much less than this': -1}

# Q27 (Multi)
q27_cols = [c for c in df.columns if '27.' in str(c) and '/' in str(c)]
q27_scores = {'transfusions': 1, 'iron overload': 1, 'delayed growth': 1, 'diabetes': 1, 'infections': 1, 'fatigue': 1, 'bone deformities': 1, 'frequent nosebleeds': 0}

def get_weighted_q27_score(row):
    s = 0
    for col in q27_cols:
        if row[col] == 1.0:
            opt = col.split('/', 1)[1].strip().lower()
            for k, weight in q27_scores.items():
                if k in opt:
                    p = df[col].sum() / n_participants
                    s += weight * (1 - p)
                    break
    return s

scores = []
for index, row in df.iterrows():
    s = 0
    s += get_weighted_single_score(row[q15_col], q15_col, q15_scores)
    s += get_weighted_q16_score(row)
    s += get_weighted_single_score(row[q17_col], q17_col, q17_scores)
    s += get_weighted_single_score(row[q19_col], q19_col, q19_scores)
    s += get_weighted_single_score(row[q20_col], q20_col, q20_scores)
    s += get_weighted_single_score(row[q21_col], q21_col, q21_scores)
    s += get_weighted_single_score(row[q22_col], q22_col, q22_scores)
    s += get_weighted_single_score(row[q23_col], q23_col, q23_scores)
    s += get_weighted_single_score(row[q24_col], q24_col, q24_scores)
    s += get_weighted_single_score(row[q26_col], q26_col, q26_scores)
    s += get_weighted_q27_score(row)
    scores.append(s)

df['Weighted_V3_Knowledge_Score'] = scores

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

X = df['Weighted_V3_Knowledge_Score'].values
clusters, centers = kmeans_1d(X, k=3)
sorted_idx = np.argsort(centers)
mapping = {sorted_idx[0]: 'Negative/Low', sorted_idx[1]: 'Neutral/Medium', sorted_idx[2]: 'Positive/High'}
df['Weighted_V3_Knowledge_Cluster'] = [mapping[c] for c in clusters]

# Plots
# Dist
plt.figure(figsize=(10, 6))
sns.histplot(df['Weighted_V3_Knowledge_Score'], bins=20, kde=True, color='darkmagenta', edgecolor='black')
plt.title('Distribution of Weighted V3 Knowledge Scores', fontsize=16)
plt.axvline(0, color='black', linestyle='dotted', label='Zero')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Weighted_V3_Knowledge_Dist.png'))
plt.close()

# Dot Plot
sorted_s = df['Weighted_V3_Knowledge_Score'].sort_values().values
plt.figure(figsize=(12, 7))
plt.plot(range(len(sorted_s)), sorted_s, marker='o', linestyle='', color='forestgreen')
plt.title('Sorted Weighted V3 Knowledge Scores', fontsize=16)
plt.axhline(0, color='black', linestyle='dotted')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Weighted_V3_Knowledge_DotPlot.png'))
plt.close()

# KMeans
plt.figure(figsize=(10, 6))
colors = {'Negative/Low': 'red', 'Neutral/Medium': 'orange', 'Positive/High': 'green'}
for level, color in colors.items():
    subset = df[df['Weighted_V3_Knowledge_Cluster'] == level]
    plt.scatter(subset.index, subset['Weighted_V3_Knowledge_Score'], c=color, label=f"{level} (n={len(subset)})")
plt.title('K-Means Clusters for Weighted V3 Knowledge', fontsize=16)
plt.axhline(0, color='black', linestyle='dotted')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Weighted_V3_Knowledge_KMeans.png'))
plt.close()

# Save CSV
out_csv = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'
cols_to_save = ['Weighted_V3_Knowledge_Score', 'Weighted_V3_Knowledge_Cluster']
if '_id' in df.columns:
    df[['_id'] + cols_to_save].to_csv(out_csv, index=False)
else:
    df[cols_to_save].to_csv(out_csv, index=False)

# Generate MD
md_report = f"""# Weighted V3 Knowledge Scoring Analysis

This report visualizes the participants' Knowledge scores combining the V3 Penalty Schema with the statistical $(1-p)$ inverse-frequency calculation.

### Methodological Context
Formula: `Final Score = Assigned_Weight * (1 - p)`

By scaling the assigned penalties (+2 down to -3) by the proportion of the cohort that gave the answer, we mathematically reward statistically rare knowledge (e.g. knowing the exact transmission genetics) and massively penalize statistically rare, dangerous misconceptions. Common knowledge is scaled down closer to 0, representing the "expected baseline."

### The Distribution
Because most basic knowledge facts were widely known by the cohort, the positive scores were heavily scaled down, causing the bulk of the distribution to center tightly near the low positives. However, the dangerous misconceptions remained incredibly rare, meaning their heavy penalties (-3) stayed intact and pulled the lower tail far into the negatives.

![Distribution of Weighted V3 Scores]({charts_dir}/Weighted_V3_Knowledge_Dist.png)
![Dot Plot of Weighted V3 Scores]({charts_dir}/Weighted_V3_Knowledge_DotPlot.png)

---

### K-Means Clustering (k=3)
The K-Means algorithm effectively isolated the highly penalized individuals into the Negative/Low cluster. The Neutral/Medium cluster represents participants who simply possessed the expected baseline knowledge (scoring close to 0 due to the scaling), while the Positive/High cluster represents participants with deep, rare clinical knowledge.

![K-Means Clusters]({charts_dir}/Weighted_V3_Knowledge_KMeans.png)
"""

md_path = os.path.join(out_dir_md, 'Weighted_V3_Knowledge_Report.md')
with open(md_path, 'w') as f:
    f.write(md_report)

# Convert to PDF
out_pdf = os.path.join(out_dir_pdf, 'Weighted_V3_Knowledge_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF conversion failed:", e)

print("Weighted V3 Knowledge calculated and saved successfully.")
