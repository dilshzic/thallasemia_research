import pandas as pd
import numpy as np

excel_file = '/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

# 1. Define Correct Answers
single_choice = {
    '15. Is thalassemia a blood-related disease?': 'Yes',
    ' 17. What is the most severe form of thalassemia?': 'Thalassemia major (severe form)',
    '19. Does thalassemia major require lifelong treatment?': 'Yes',
    '20. Can thalassemia major be cured?': 'Very difficult (e.g., bone marrow transplant)',
    '21. Can the spread of thalassemia be prevented?': 'Can be prevented',
    '22. How is thalassemia transmitted?': 'From generation to generation (hereditary)',
    '23. Is a thalassemia carrier usually sick or healthy?': 'Healthy',
    '24. A child born from two thalassemia carriers will be:': 'Has a chance to be affected (e.g., 25%)',
    '26. How many thalassemia births occur in Sri Lanka per year?': '40–100'
}

# The multiple choice prefixes
multiple_choice_prefixes = [
    '16. What are the clinical forms of thalassemia? (Tick all that apply)',
    '27. Problems faced by thalassemia major patients (Tick all that apply)',
    '28. What should a thalassemia carrier do after diagnosis? (Tick all that apply)'
]

incorrect_mc_options = [
    'I don’t know', 
    'Frequent nosebleeds', 
    'Ignore it'
]

N = len(df)
item_weights = {}

# Match single choice columns and calculate 1-p
single_choice_cols = {}
for col in df.columns:
    for q, ans in single_choice.items():
        if q in col and '/' not in col:
            single_choice_cols[col] = ans
            break

for col, ans in single_choice_cols.items():
    # Find exact matching key
    match_key = None
    for key in df[col].dropna().unique():
        if str(key).strip().lower() == ans.strip().lower():
            match_key = key
            break
    
    if match_key:
        p = (df[col] == match_key).sum() / N
        item_weights[col] = {
            'type': 'single',
            'correct_ans': match_key,
            'p': p,
            '1-p': 1 - p
        }

# Match multiple choice columns
mc_cols = []
for col in df.columns:
    for prefix in multiple_choice_prefixes:
        if col.startswith(prefix) and '/' in col:
            # Check if it's an incorrect option
            option_str = col.split('/', 1)[1].strip()
            is_incorrect = any(bad.lower() in option_str.lower() for bad in incorrect_mc_options)
            
            if not is_incorrect:
                p = df[col].sum() / N
                item_weights[col] = {
                    'type': 'multi',
                    'p': p,
                    '1-p': 1 - p
                }
            break

# 2. Calculate Score for Each Participant
scores = []
for index, row in df.iterrows():
    score = 0.0
    for col, meta in item_weights.items():
        if meta['type'] == 'single':
            if row[col] == meta['correct_ans']:
                score += meta['1-p']
        elif meta['type'] == 'multi':
            if row[col] == 1.0:
                score += meta['1-p']
    scores.append(score)

df['Weighted_Knowledge_Score'] = scores

# 3. Generate Report
output_csv = '/home/dilshan/Desktop/Thallasemia research/Participant_Weighted_Scores.csv'
report_md = '/home/dilshan/Desktop/Thallasemia research/Participant_Scores_Report.md'

# Only keep ID (if exists, else index) and Score
if '_id' in df.columns:
    out_df = df[['_id', 'Weighted_Knowledge_Score']].copy()
else:
    out_df = pd.DataFrame({'Participant_Index': range(1, N+1), 'Weighted_Knowledge_Score': scores})

out_df.to_csv(output_csv, index=False)

# Stats
mean_score = np.mean(scores)
median_score = np.median(scores)
std_dev = np.std(scores)
min_score = np.min(scores)
max_score = np.max(scores)

max_possible_score = sum(meta['1-p'] for meta in item_weights.values())

md_content = f"""# Participant Weighted Knowledge Scores Report

Based on the calculated `1-p` weights (inverse difficulty), a weighted knowledge score was computed for each of the {N} participants. 
For each participant, they received the `1-p` value for every correct single-choice answer and every correct multiple-choice option they selected. Incorrect or "I don't know" options contributed 0 to the score.

## Summary Statistics
- **Total Possible Score:** {max_possible_score:.4f}
- **Mean Score:** {mean_score:.4f}
- **Median Score:** {median_score:.4f}
- **Standard Deviation:** {std_dev:.4f}
- **Minimum Score:** {min_score:.4f}
- **Maximum Score:** {max_score:.4f}

## Score Distribution

| Metric | Value |
| :--- | :--- |
| **Top 10% Cutoff** | {np.percentile(scores, 90):.4f} |
| **75th Percentile (Q3)** | {np.percentile(scores, 75):.4f} |
| **50th Percentile (Median)** | {median_score:.4f} |
| **25th Percentile (Q1)** | {np.percentile(scores, 25):.4f} |
| **Bottom 10% Cutoff** | {np.percentile(scores, 10):.4f} |

A full list of participant scores has been exported to:
`Participant_Weighted_Scores.csv`

## Item Weights Used
"""

for col, meta in item_weights.items():
    if meta['type'] == 'single':
        md_content += f"- **{col}** (Correct: `{meta['correct_ans']}`) -> Weight: {meta['1-p']:.4f}\\n"
    else:
        option = col.split('/', 1)[1].strip()
        md_content += f"- **{col.split('/',1)[0][:30]}... / {option}** -> Weight: {meta['1-p']:.4f}\\n"

with open(report_md, 'w') as f:
    f.write(md_content)

print(f"Report saved to {report_md}")
print(f"CSV saved to {output_csv}")
