import pandas as pd
import matplotlib.pyplot as plt
import os

# Set output path directly to the conversation's artifact directory so it can be embedded in an artifact
artifact_dir = '/home/dilshan/.gemini/antigravity/brain/2df2cc95-ca41-4d9d-a116-04a1b43127d8/'
output_image = os.path.join(artifact_dir, 'Knowledge_Score_DotPlot.png')

csv_file = '/home/dilshan/Desktop/Thallasemia research/Participant_Weighted_Scores.csv'
df = pd.read_csv(csv_file)

# Sort the scores
sorted_scores = df['Weighted_Knowledge_Score'].sort_values().values

# Create a dot plot
plt.figure(figsize=(12, 7))
plt.plot(range(len(sorted_scores)), sorted_scores, marker='o', linestyle='', color='purple', alpha=0.7, markersize=6)

plt.title('Dot Plot of Sorted Knowledge Scores (Identifying Clusters)', fontsize=16)
plt.xlabel('Participant Rank (Sorted from Lowest to Highest)', fontsize=14)
plt.ylabel('Weighted Knowledge Score', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Annotate potential jumps or clusters visually
plt.tight_layout()

plt.savefig(output_image, dpi=150)
print(f"Chart saved to {output_image}")
