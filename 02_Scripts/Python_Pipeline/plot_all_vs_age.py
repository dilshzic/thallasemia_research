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

age_col = '1. Age (What was your age at last birthday?):'
scores = [
    'Expanded_Knowledge_Score',
    'Partner_Attitude',
    'Cascade_Attitude',
    'Cascade_Practice_Score'
]

# Clean and convert age to numeric
df[age_col] = pd.to_numeric(df[age_col], errors='coerce')
df = df.dropna(subset=[age_col] + scores).copy()

# Sort by Age
df = df.sort_values(by=age_col).reset_index(drop=True)

# Min-Max Scaling function
def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

for s in scores:
    df[f"{s}_scaled"] = min_max_scale(df[s])

sns.set_theme(style="whitegrid")
fig, ax1 = plt.subplots(figsize=(14, 8))

x = df.index

# Plot Age on left axis
color_age = 'teal'
ax1.set_xlabel('Participants (Sorted by Age: Youngest to Oldest)', fontsize=12)
ax1.set_ylabel('Age (Years)', color=color_age, fontsize=12, fontweight='bold')
ax1.plot(x, df[age_col], color=color_age, linewidth=3, label="Age (Sorted Base Curve)")
ax1.fill_between(x, df[age_col], color=color_age, alpha=0.1)
ax1.tick_params(axis='y', labelcolor=color_age)

# Instantiate a second axes that shares the same x-axis
ax2 = ax1.twinx()  
ax2.set_ylabel('Normalized Score (0 to 1 Scale)', color='black', fontsize=12, fontweight='bold')

# Plot the 4 rolling trendlines
window = 15
colors = ['crimson', 'dodgerblue', 'forestgreen', 'darkorange']
labels = ['Knowledge Trend', 'Partner Attitude Trend', 'Cascade Attitude Trend', 'Cascade Practice Trend']
scaled_scores = [f"{s}_scaled" for s in scores]

for i, score_col in enumerate(scaled_scores):
    # Optional: Scatter faint raw points if desired, but 4 sets of dots might be messy
    # plt.scatter(x, df[score_col], color=colors[i], alpha=0.1, s=10)
    
    # Plot moving average
    trend = df[score_col].rolling(window=window, min_periods=1, center=True).mean()
    ax2.plot(x, trend, color=colors[i], linewidth=2.5, label=labels[i])

ax2.set_ylim(0, 1)

plt.title("All Scoring Metrics vs. Sorted Age", fontsize=16, fontweight='bold', pad=15)

# Combine Legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', frameon=True, shadow=True)

fig.tight_layout()

output_dir = os.path.join(current_dir, "outputs", "plots")
output_path = os.path.join(output_dir, "all_metrics_vs_sorted_age.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')

# Copy to artifact folder
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.system(f"cp '{output_path}' '{artifact_dir}'")
print("Plot generated successfully!")
