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

edu_col = '7. Education Level:'
knowledge_col = 'Expanded_Knowledge_Score'

# Clean data
df = df.dropna(subset=[edu_col, knowledge_col]).copy()

# Ensure education categories are strings and clean whitespace
df[edu_col] = df[edu_col].astype(str).str.strip()

# Calculate order by mean knowledge score for a clean staircase plot
order = df.groupby(edu_col)[knowledge_col].mean().sort_values().index

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# Create the bar plot with error bars showing a 95% confidence interval
ax = sns.barplot(
    data=df, 
    x=edu_col, 
    y=knowledge_col, 
    order=order,
    palette="viridis",
    capsize=.1,
    err_kws={'linewidth': 2},
    edgecolor="black"
)

# Add the specific mean values on top of the bars
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}", 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, -20), # Push text slightly down into the bar
                textcoords='offset points',
                color='white',
                fontweight='bold',
                fontsize=14)

plt.title("Expanded Knowledge Score by Education Level", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Highest Level of Education", fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel("Mean Expanded Knowledge Score (Max 20)", fontsize=14, fontweight='bold', labelpad=10)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

output_dir = os.path.join(current_dir, "outputs", "plots")
output_path = os.path.join(output_dir, "knowledge_vs_education.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')

# Copy to artifact folder
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.system(f"cp '{output_path}' '{artifact_dir}'")
print("Plot generated successfully!")

