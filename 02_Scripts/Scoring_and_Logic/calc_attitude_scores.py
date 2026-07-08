import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

excel_file = '/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

base_dir = '/home/dilshan/Desktop/Thallasemia research/attitude_score_analysis'
charts_dir = os.path.join(base_dir, 'charts')
os.makedirs(charts_dir, exist_ok=True)

# Define positive attitude criteria
partner_selection_criteria = {
    '30. Are you willing to / Do you have a consanguineous marriage? ': ['Definitely not'],
    '31. Do you accept marriage between two thalassemia carriers? ': ['No '],
    '32. How important is thalassemia screening before marriage? ': ['Very important ', 'Important ']
}

cascade_screening_criteria = {
    '35. Do you think is it important for your family members to undergo screening?': ['Agree '],
    '39. How easy is it to convince relatives to undergo screening?': ['Very easy ', 'Somewhat easy '],
    '40. How important is cascade screening in thalassemia prevention?': [' Very important', 'Important ']
}

# Find exact column names in df
partner_cols = {}
cascade_cols = {}

for col in df.columns:
    for q, pos_answers in partner_selection_criteria.items():
        if q in col:
            partner_cols[col] = pos_answers
    for q, pos_answers in cascade_screening_criteria.items():
        if q in col:
            cascade_cols[col] = pos_answers

# Calculate p-values (proportion of positive responses)
partner_weights = {}
for col, pos_ans in partner_cols.items():
    p = df[col].isin(pos_ans).sum() / len(df)
    partner_weights[col] = 1 - p

cascade_weights = {}
for col, pos_ans in cascade_cols.items():
    p = df[col].isin(pos_ans).sum() / len(df)
    cascade_weights[col] = 1 - p

# Calculate Scores
raw_partner = []
weighted_partner = []
raw_cascade = []
weighted_cascade = []

for index, row in df.iterrows():
    # Partner
    rp = 0
    wp = 0
    for col, pos_ans in partner_cols.items():
        if row[col] in pos_ans:
            rp += 1
            wp += partner_weights[col]
    raw_partner.append(rp)
    weighted_partner.append(wp)
    
    # Cascade
    rc = 0
    wc = 0
    for col, pos_ans in cascade_cols.items():
        if row[col] in pos_ans:
            rc += 1
            wc += cascade_weights[col]
    raw_cascade.append(rc)
    weighted_cascade.append(wc)

df['Raw_Partner_Attitude'] = raw_partner
df['Weighted_Partner_Attitude'] = weighted_partner
df['Raw_Cascade_Attitude'] = raw_cascade
df['Weighted_Cascade_Attitude'] = weighted_cascade

# Save data
output_csv = os.path.join(base_dir, 'Participant_Attitude_Scores.csv')
if '_id' in df.columns:
    out_df = df[['_id', 'Raw_Partner_Attitude', 'Weighted_Partner_Attitude', 'Raw_Cascade_Attitude', 'Weighted_Cascade_Attitude']]
else:
    out_df = pd.DataFrame({
        'Raw_Partner_Attitude': raw_partner,
        'Weighted_Partner_Attitude': weighted_partner,
        'Raw_Cascade_Attitude': raw_cascade,
        'Weighted_Cascade_Attitude': weighted_cascade
    })
out_df.to_csv(output_csv, index=False)

# Ploting function
def plot_dist_and_dot(series, title_prefix, filename_prefix):
    # Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(series, bins=15, kde=True, color='mediumpurple', edgecolor='black')
    plt.title(f'Distribution of {title_prefix}', fontsize=16)
    plt.xlabel('Score', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.axvline(series.mean(), color='red', linestyle='dashed', label=f'Mean: {series.mean():.2f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{filename_prefix}_Dist.png'))
    plt.close()
    
    # Dot Plot (sorted)
    sorted_s = series.sort_values().values
    plt.figure(figsize=(12, 7))
    plt.plot(range(len(sorted_s)), sorted_s, marker='o', linestyle='', color='darkorange', alpha=0.7)
    plt.title(f'Dot Plot of Sorted {title_prefix}', fontsize=16)
    plt.xlabel('Participant Rank', fontsize=14)
    plt.ylabel('Score', fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, f'{filename_prefix}_DotPlot.png'))
    plt.close()

plot_dist_and_dot(df['Raw_Partner_Attitude'], 'Raw Partner Selection Attitude', 'Raw_Partner')
plot_dist_and_dot(df['Weighted_Partner_Attitude'], 'Weighted Partner Selection Attitude', 'Weighted_Partner')
plot_dist_and_dot(df['Raw_Cascade_Attitude'], 'Raw Cascade Screening Attitude', 'Raw_Cascade')
plot_dist_and_dot(df['Weighted_Cascade_Attitude'], 'Weighted Cascade Screening Attitude', 'Weighted_Cascade')

print("Attitude scores calculated and charts saved.")
