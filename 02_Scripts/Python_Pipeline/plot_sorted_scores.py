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
fig, axes = plt.subplots(3, 2, figsize=(15, 18))
axes = axes.flatten()

for i, score in enumerate(scores_to_plot):
    ax = axes[i]
    
    # Sort the score values
    sorted_values = df[score].dropna().sort_values().values
    
    # Plot as a sorted bar chart / fill_between to show the S-curve distribution
    x = range(len(sorted_values))
    ax.fill_between(x, sorted_values, color="skyblue", alpha=0.4)
    ax.plot(x, sorted_values, color="Slateblue", alpha=0.9, linewidth=3)
    
    # Aesthetics
    ax.set_title(f"Sorted Distribution: {score.replace('_', ' ')}", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Participants (Sorted by Score)", fontsize=12)
    ax.set_ylabel("Score Value", fontsize=12)
    ax.margins(x=0)

# Remove the empty 6th subplot
fig.delaxes(axes[5])

plt.tight_layout(pad=4.0)

output_path = os.path.join(current_dir, "outputs", "plots", "sorted_score_distributions.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Plot saved successfully to {output_path}")

# Copy to artifact folder for user viewing
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.system(f"cp '{output_path}' '{artifact_dir}'")

