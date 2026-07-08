import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set output path directly to the conversation's artifact directory so it can be embedded in an artifact
artifact_dir = '/home/dilshan/.gemini/antigravity/brain/2df2cc95-ca41-4d9d-a116-04a1b43127d8/'
output_image = os.path.join(artifact_dir, 'Knowledge_Score_Distribution.png')

csv_file = '/home/dilshan/Desktop/Thallasemia research/Participant_Weighted_Scores.csv'
df = pd.read_csv(csv_file)

plt.figure(figsize=(10, 6))
sns.histplot(df['Weighted_Knowledge_Score'], bins=20, kde=True, color='teal', edgecolor='black')

plt.title('Distribution of Weighted Knowledge Scores among Participants', fontsize=16)
plt.xlabel('Weighted Knowledge Score', fontsize=14)
plt.ylabel('Number of Participants', fontsize=14)

# Add median and mean lines
mean_val = df['Weighted_Knowledge_Score'].mean()
median_val = df['Weighted_Knowledge_Score'].median()

plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_val:.2f}')
plt.axvline(median_val, color='orange', linestyle='solid', linewidth=2, label=f'Median: {median_val:.2f}')
plt.legend()
plt.tight_layout()

plt.savefig(output_image)
print(f"Chart saved to {output_image}")
