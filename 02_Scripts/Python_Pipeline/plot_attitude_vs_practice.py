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

output_dir = os.path.join(current_dir, "outputs", "plots")
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

# 1. Partner Attitude vs Practice
df_partner = df.dropna(subset=['Partner_Attitude', 'Partner_Practice_Raw']).copy()
order = ['Safe', 'Delayed', 'Unsafe'] # Logical ordering

plt.figure(figsize=(9, 6))
# Boxplot for the distribution
sns.boxplot(data=df_partner, x='Partner_Practice_Raw', y='Partner_Attitude', order=order, palette='Set2', showfliers=False, width=0.5)
# Stripplot to show the actual data points
sns.stripplot(data=df_partner, x='Partner_Practice_Raw', y='Partner_Attitude', order=order, color='black', alpha=0.5, jitter=True, size=6)

plt.title("Partner Attitude vs Actual Practice", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Partner Practice Behavior", fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel("Partner Attitude Score", fontsize=14, fontweight='bold', labelpad=10)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

filename_1 = "partner_attitude_vs_practice.png"
output_path_1 = os.path.join(output_dir, filename_1)
plt.savefig(output_path_1, dpi=300, bbox_inches='tight')
plt.close()
os.system(f"cp '{output_path_1}' '{artifact_dir}'")
print(f"Generated {filename_1}")

# 2. Cascade Attitude vs Practice
df_cascade = df.dropna(subset=['Cascade_Attitude', 'Cascade_Practice_Score']).copy()

plt.figure(figsize=(9, 6))
# Regplot automatically adds a linear regression line with a 95% confidence interval
sns.regplot(data=df_cascade, x='Cascade_Attitude', y='Cascade_Practice_Score', 
            scatter_kws={'alpha': 0.4, 's': 60, 'color': 'forestgreen'}, 
            line_kws={'color': 'darkred', 'linewidth': 3},
            x_jitter=0.2, y_jitter=0.2)

plt.title("Cascade Attitude vs Cascade Practice Score", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Cascade Attitude Score", fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel("Cascade Practice Score", fontsize=14, fontweight='bold', labelpad=10)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

filename_2 = "cascade_attitude_vs_practice.png"
output_path_2 = os.path.join(output_dir, filename_2)
plt.savefig(output_path_2, dpi=300, bbox_inches='tight')
plt.close()
os.system(f"cp '{output_path_2}' '{artifact_dir}'")
print(f"Generated {filename_2}")

