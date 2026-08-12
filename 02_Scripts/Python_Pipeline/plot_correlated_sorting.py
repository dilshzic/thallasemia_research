import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

# We need these 4 scores
scores = [
    'Expanded_Knowledge_Score',
    'Partner_Attitude',
    'Cascade_Attitude',
    'Cascade_Practice_Score'
]

# Drop NaNs in these columns to be safe
df = df.dropna(subset=scores).copy()

# Sort the dataframe by Expanded_Knowledge_Score
df = df.sort_values(by='Expanded_Knowledge_Score').reset_index(drop=True)

# Min-Max Scaling function
def min_max_scale(series):
    return (series - series.min()) / (series.max() - series.min())

# Normalize the scores
for s in scores:
    df[f"{s}_scaled"] = min_max_scale(df[s])

sns.set_theme(style="whitegrid")
plt.figure(figsize=(14, 8))

x = df.index

# Plot Expanded Knowledge as a solid shaded area
plt.fill_between(x, df['Expanded_Knowledge_Score_scaled'], color="black", alpha=0.1)
plt.plot(x, df['Expanded_Knowledge_Score_scaled'], color="black", linewidth=3, label="Expanded Knowledge (Sorted Base)")

# Plot other variables as smoothed trendlines (Rolling Mean) to show correlation visually
# Window size for smoothing
window = 15

colors = ['crimson', 'dodgerblue', 'forestgreen']
labels = ['Partner Attitude', 'Cascade Attitude', 'Cascade Practice']
other_scores = ['Partner_Attitude_scaled', 'Cascade_Attitude_scaled', 'Cascade_Practice_Score_scaled']

for i, score_col in enumerate(other_scores):
    # Scatter the raw points lightly
    plt.scatter(x, df[score_col], color=colors[i], alpha=0.2, s=15)
    
    # Plot the rolling average to show the trend
    trend = df[score_col].rolling(window=window, min_periods=1, center=True).mean()
    plt.plot(x, trend, color=colors[i], linewidth=2.5, label=f"{labels[i]} (Trend)")

plt.title("Attitude and Practice Scores Scaled and Plotted against Sorted Knowledge Score", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Participants (Sorted by Expanded Knowledge Score from Low to High)", fontsize=12)
plt.ylabel("Normalized Score (0 to 1 Scale)", fontsize=12)
plt.legend(loc='upper left', frameon=True, shadow=True)
plt.margins(x=0.02)
plt.tight_layout()

output_dir = os.path.join(current_dir, "outputs", "plots")
output_path = os.path.join(output_dir, "correlated_knowledge_sort.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight')

# Copy to artifact folder
artifact_dir = "/home/dilshan/.gemini/antigravity-ide/brain/1ca6f901-a148-4b1e-9cc6-9ebee70289e4/"
os.system(f"cp '{output_path}' '{artifact_dir}'")
print("Plot generated successfully!")

