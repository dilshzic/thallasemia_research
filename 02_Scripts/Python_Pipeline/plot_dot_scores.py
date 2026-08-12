import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

# Make sure we can import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import loader_01
import scoring_02

# Load and score data
xlsx_path = "/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx"
df = loader_01.load_and_clean_data(xlsx_path)
df = scoring_02.calculate_scores(df)

# The 5 numeric scores to plot
scores_to_plot = [
    'Knowledge_Score',
    'Expanded_Knowledge_Score',
    'Partner_Attitude',
    'Cascade_Attitude',
    'Cascade_Practice_Score'
]

sns.set_theme(style="whitegrid")
output_dir = os.path.join(current_dir, "outputs", "plots")
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"

for score in scores_to_plot:
    plt.figure(figsize=(10, 6))
    
    # Sort the values to make the dot plot look clean (like the S-curve but with dots)
    sorted_values = df[score].dropna().sort_values().values
    x = range(len(sorted_values))
    
    # Scatter plot with dots
    plt.scatter(x, sorted_values, color="crimson", alpha=0.7, s=40, edgecolors='k')
    
    # Aesthetics
    plt.title(f"Sorted Dot Plot: {score.replace('_', ' ')}", fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Participants (Sorted by Score)", fontsize=12)
    plt.ylabel("Score Value", fontsize=12)
    plt.margins(x=0.02)
    plt.tight_layout()
    
    filename = f"dotplot_{score}.png"
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Copy to artifact folder
    os.system(f"cp '{output_path}' '{artifact_dir}'")
    print(f"Generated {filename}")

