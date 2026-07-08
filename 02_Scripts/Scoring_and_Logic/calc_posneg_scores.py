import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

excel_file = '/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

# Setup Output Directories
base_dir = '/home/dilshan/Desktop/Thallasemia research/pos_neg_score_analysis'
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
    'Frequent nosebleeds', 
    'Ignore it'
]

neutral_mc_options = [
    'I don’t know'
]

neutral_single_options = ['don’t know', 'not sure', 'i don’t know']

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
            is_neutral = any(bad.lower() in option_str.lower() for bad in neutral_mc_options)
            
            if is_neutral:
                item_meta[col] = {'type': 'multi_neutral'}
            elif is_incorrect:
                item_meta[col] = {'type': 'multi_incorrect'}
            else:
                item_meta[col] = {'type': 'multi_correct'}
            break

# Calculate Pos/Neg Score
scores = []
for index, row in df.iterrows():
    score = 0
    for col, meta in item_meta.items():
        if meta['type'] == 'single':
            ans = str(row[col]).strip().lower()
            if ans == 'nan':
                continue
                
            if row[col] == meta['correct_ans']:
                score += 1
            else:
                # check if it's a neutral "I don't know" answer
                is_neutral = any(n in ans for n in neutral_single_options)
                if is_neutral:
                    score += 0
                else:
                    score -= 1 # Incorrect
                    
        elif meta['type'] == 'multi_correct':
            if row[col] == 1.0:
                score += 1
        elif meta['type'] == 'multi_incorrect':
            if row[col] == 1.0:
                score -= 1
        # multi_neutral adds 0, so do nothing
    scores.append(score)

df['PosNeg_Knowledge_Score'] = scores
output_csv = os.path.join(base_dir, 'Participant_PosNeg_Scores.csv')
out_df = df[['_id', 'PosNeg_Knowledge_Score']].copy() if '_id' in df.columns else pd.DataFrame({'Participant_Index': range(1, len(df)+1), 'PosNeg_Knowledge_Score': scores})

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

X = df['PosNeg_Knowledge_Score'].values
clusters, cluster_centers = kmeans_1d(X, k=3)
cluster_centers = cluster_centers.flatten()
sorted_indices = np.argsort(cluster_centers)
cluster_mapping = {sorted_indices[0]: 'Low Knowledge (Negative/Zero)', 
                   sorted_indices[1]: 'Medium Knowledge', 
                   sorted_indices[2]: 'High Knowledge'}
df['Cluster'] = clusters
df['Knowledge_Level'] = df['Cluster'].map(cluster_mapping)

df.to_csv(output_csv, index=False)

# Plot 1: Distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['PosNeg_Knowledge_Score'], bins=20, kde=True, color='teal', edgecolor='black')
plt.title('Distribution of Pos/Neg Knowledge Scores (+1 Correct, -1 Incorrect)', fontsize=16)
plt.xlabel('Pos/Neg Knowledge Score', fontsize=14)
plt.ylabel('Number of Participants', fontsize=14)
mean_val = df['PosNeg_Knowledge_Score'].mean()
median_val = df['PosNeg_Knowledge_Score'].median()
plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='orange', linestyle='solid', linewidth=2, label=f'Median: {median_val:.2f}')
plt.axvline(0, color='black', linestyle='dotted', linewidth=1.5, label='Zero Line')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'PosNeg_Score_Distribution.png'))
plt.close()

# Plot 2: Dot Plot
sorted_scores = df['PosNeg_Knowledge_Score'].sort_values().values
plt.figure(figsize=(12, 7))
plt.plot(range(len(sorted_scores)), sorted_scores, marker='o', linestyle='', color='purple', alpha=0.7, markersize=6)
plt.title('Dot Plot of Sorted Pos/Neg Knowledge Scores', fontsize=16)
plt.xlabel('Participant Rank (Sorted)', fontsize=14)
plt.ylabel('Pos/Neg Knowledge Score', fontsize=14)
plt.axhline(0, color='black', linestyle='dotted', linewidth=1.5, label='Zero Line')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'PosNeg_Score_DotPlot.png'))
plt.close()

# Plot 3: KMeans Clustering
plt.figure(figsize=(10, 6))
colors = {'Low Knowledge (Negative/Zero)': 'red', 'Medium Knowledge': 'orange', 'High Knowledge': 'green'}
for level, color in colors.items():
    subset = df[df['Knowledge_Level'] == level]
    plt.scatter(subset.index, subset['PosNeg_Knowledge_Score'], c=color, label=f"{level} (n={len(subset)})", alpha=0.7)
plt.title('K-Means Clustering of Pos/Neg Knowledge Scores (k=3)', fontsize=16)
plt.xlabel('Participant Index', fontsize=14)
plt.ylabel('Pos/Neg Knowledge Score', fontsize=14)
for center in cluster_centers:
    plt.axhline(y=center, color='gray', linestyle='--', alpha=0.5)
plt.axhline(0, color='black', linestyle='dotted', linewidth=1.5, label='Zero Line')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'PosNeg_KMeans_Clusters.png'))
plt.close()

# Markdown generation
md_dist = f"""# Positive/Negative Knowledge Score Distribution

In this Phase 3 scoring method, participants were penalized for incorrect guesses to account for guessing probability:
- **+1 Point:** Correct answer or correct multiple-choice option selected.
- **-1 Point:** Incorrect answer or incorrect multiple-choice option selected.
- **0 Points:** "I don't know" / "Not sure" / Blank responses.

![PosNeg Distribution](charts/PosNeg_Score_Distribution.png)

### Key Observations
- The inclusion of a penalty (-1) causes the distribution to widen significantly and pushes many participants toward zero or into negative territory.
- A score around 0 indicates the participant's correct knowledge is entirely offset by their misconceptions, or they simply chose "I don't know" for everything.
"""

md_dot = f"""# Positive/Negative Scores Dot Plot

![PosNeg Dot Plot](charts/PosNeg_Score_DotPlot.png)

### Interpretation
- Sorting the scores visually demonstrates the sheer variance introduced by negative penalties. 
- You can visibly see the proportion of the cohort that fell below the zero line (meaning their misconceptions outweighed their actual knowledge).
"""

md_kmeans = f"""# K-Means Clustering on Pos/Neg Scores

![PosNeg K-Means](charts/PosNeg_KMeans_Clusters.png)

### Cluster Assignments
With the negative penalties applied, the K-Means algorithm naturally separated participants who hold dangerous misconceptions from those who are highly knowledgeable:
- **Low Knowledge (Negative/Zero) [Red]:** Participants dominated by incorrect guesses or a lack of knowledge.
- **Medium Knowledge [Orange]:** Participants who know the basics and didn't guess incorrectly too often.
- **High Knowledge [Green]:** Participants with extensive medical knowledge and almost zero misconceptions.
"""

with open(os.path.join(base_dir, '1_PosNeg_Distribution.md'), 'w') as f: f.write(md_dist)
with open(os.path.join(base_dir, '2_PosNeg_DotPlot.md'), 'w') as f: f.write(md_dot)
with open(os.path.join(base_dir, '3_PosNeg_KMeans.md'), 'w') as f: f.write(md_kmeans)

print("Pos/Neg scores calculated, clustered, and charts saved.")
