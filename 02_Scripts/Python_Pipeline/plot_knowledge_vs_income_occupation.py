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
income_col = '6. Monthly Income (LKR):'
occ_col = '5. Occupation:'

# Ensure strings and clean whitespace
df[income_col] = df[income_col].astype(str).str.strip()
df[occ_col] = df[occ_col].astype(str).str.strip()

# Create Output Directory
output_dir = os.path.join(current_dir, "outputs", "plots")
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

def create_bar_plot(df, group_col, title, x_label, output_filename):
    df_clean = df.dropna(subset=[group_col, knowledge_col]).copy()
    
    # Calculate order by mean
    order = df_clean.groupby(group_col)[knowledge_col].mean().sort_values().index
    
    plt.figure(figsize=(12, 7))
    ax = sns.barplot(
        data=df_clean, 
        x=group_col, 
        y=knowledge_col, 
        order=order,
        palette="rocket",
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
                    
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel(x_label, fontsize=14, fontweight='bold', labelpad=10)
    plt.ylabel("Mean Expanded Knowledge Score (Max 20)", fontsize=14, fontweight='bold', labelpad=10)
    
    # Rotate x labels if they are long
    plt.xticks(rotation=15, fontsize=11, ha='right')
    plt.yticks(fontsize=12)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Copy to artifact folder
    os.system(f"cp '{output_path}' '{artifact_dir}'")
    print(f"Generated {output_filename}")

create_bar_plot(df, income_col, "Expanded Knowledge Score by Monthly Income", "Monthly Income (LKR)", "knowledge_vs_income.png")
create_bar_plot(df, occ_col, "Expanded Knowledge Score by Occupation", "Occupation", "knowledge_vs_occupation.png")

