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
counsel_col = '25. After diagnosis, was counseling/information sufficient?'

# Ensure strings and clean whitespace
df[counsel_col] = df[counsel_col].astype(str).str.strip()

# Create Output Directory
output_dir = os.path.join(current_dir, "outputs", "plots")
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

df_clean = df.dropna(subset=[counsel_col, knowledge_col]).copy()
# Filter out empty or pure 'nan'
df_clean = df_clean[df_clean[counsel_col].str.lower() != 'nan']
df_clean = df_clean[df_clean[counsel_col] != '']

# Calculate order by mean
order = df_clean.groupby(counsel_col)[knowledge_col].mean().sort_values().index

plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=df_clean, 
    x=counsel_col, 
    y=knowledge_col, 
    order=order,
    palette="mako",
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
                
plt.title("Expanded Knowledge Score by Counseling Satisfaction", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Was counseling/information sufficient?", fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel("Mean Expanded Knowledge Score (Max 20)", fontsize=14, fontweight='bold', labelpad=10)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

output_path = os.path.join(output_dir, "knowledge_vs_counseling.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

# Copy to artifact folder
os.system(f"cp '{output_path}' '{artifact_dir}'")
print("Plot generated successfully!")
