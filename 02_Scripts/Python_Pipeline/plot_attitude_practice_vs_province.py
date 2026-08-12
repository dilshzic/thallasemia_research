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

output_dir = os.path.join(current_dir, "outputs", "plots")
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

metrics_to_plot = {
    'Partner_Attitude': 'Partner Attitude Score',
    'Cascade_Attitude': 'Cascade Attitude Score',
    'Cascade_Practice_Score': 'Cascade Practice Score'
}

for col_name, title_name in metrics_to_plot.items():
    df_clean = df.dropna(subset=['Province_Group', col_name]).copy()
    order = df_clean.groupby('Province_Group')[col_name].mean().sort_values().index
    
    plt.figure(figsize=(9, 6))
    ax = sns.barplot(
        data=df_clean, 
        x='Province_Group', 
        y=col_name, 
        order=order,
        palette="flare",
        capsize=.1,
        err_kws={'linewidth': 2},
        edgecolor="black"
    )

    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, -20), 
                    textcoords='offset points',
                    color='white',
                    fontweight='bold',
                    fontsize=14)
                    
    plt.title(f"{title_name} by Residing Province", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Province Group", fontsize=14, fontweight='bold', labelpad=10)
    plt.ylabel(f"Mean {title_name}", fontsize=14, fontweight='bold', labelpad=10)

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    filename = f"{col_name.lower()}_vs_province.png"
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    os.system(f"cp '{output_path}' '{artifact_dir}'")
    print(f"Generated {filename}")

