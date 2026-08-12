import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import loader_01
import scoring_02

xlsx_path = "/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx"
df = loader_01.load_and_clean_data(xlsx_path)
df = scoring_02.calculate_scores(df)

knowledge_col = 'Expanded_Knowledge_Score'
prov_col = '8. Residing Province:'

def group_province(val):
    val = str(val).lower()
    if 'north' in val and 'western' in val:
        return 'North Western'
    elif 'northwestern' in val:
        return 'North Western'
    elif 'western' in val:
        return 'Western'
    else:
        return 'Other'

df['Province_Group'] = df[prov_col].apply(group_province)

# Clean data
df_clean = df.dropna(subset=['Province_Group', knowledge_col]).copy()

# Calculate order by mean
order = df_clean.groupby('Province_Group')[knowledge_col].mean().sort_values().index

sns.set_theme(style="whitegrid")
plt.figure(figsize=(9, 6))

ax = sns.barplot(
    data=df_clean, 
    x='Province_Group', 
    y=knowledge_col, 
    order=order,
    palette="flare",
    capsize=.1,
    err_kws={'linewidth': 2},
    edgecolor="black"
)

# Add values on top
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}", 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, -20), 
                textcoords='offset points',
                color='white',
                fontweight='bold',
                fontsize=14)
                
plt.title("Expanded Knowledge Score by Residing Province", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Province Group", fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel("Mean Expanded Knowledge Score (Max 20)", fontsize=14, fontweight='bold', labelpad=10)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

output_dir = os.path.join(current_dir, "outputs", "plots")
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "knowledge_vs_province.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

# Copy to artifact folder
os.system(f"cp '{output_path}' '{artifact_dir}'")
print("Plot generated successfully!")
