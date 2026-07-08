import pandas as pd
import numpy as np

excel_file = '/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)

# Total responses
total_responses = len(df)

report_lines = []
report_lines.append("# Thalassemia Research: Knowledge Questions Weight Report")
report_lines.append(f"**Total Responses:** {total_responses}\\n")
report_lines.append("This report calculates the weight (percentage of respondents) for the correct answers in the single-choice knowledge questions, and the weight for each option in the multiple-choice knowledge questions. Demographic and practice-related questions have been excluded.\\n")

# Define single choice questions and their assumed correct answers
single_choice = {
    '15. Is thalassemia a blood-related disease?': 'Yes',
    ' 17. What is the most severe form of thalassemia?': 'Thalassemia major (severe form)  ',
    '19. Does thalassemia major require lifelong treatment?': 'Yes',
    '20. Can thalassemia major be cured?': 'Yes', # BMT is a cure, but we will also show the distribution if needed. We'll just match "Yes". If "Yes" is not exact, we will use strip().
    '21. Can the spread of thalassemia be prevented?': 'Yes',
    '22. How is thalassemia transmitted?': 'From parents to children (Inherited) ',
    '23. Is a thalassemia carrier usually sick or healthy?': 'Healthy ',
    '24. A child born from two thalassemia carriers will be:': '25% major, 50% carrier, 25% healthy',
    '26. How many thalassemia births occur in Sri Lanka per year?': '40–100  '
}

report_lines.append("## Single-Choice Questions (Weight of Correct Answer)\\n")
for col in df.columns:
    for q, correct_ans in single_choice.items():
        if q in col and '/' not in col: # ensure it's the exact column, not an indicator
            # find exact match or strip match
            val_counts = df[col].value_counts()
            
            # Try to find the exact correct answer key
            match = None
            for key in val_counts.keys():
                if str(key).strip().lower() == correct_ans.strip().lower():
                    match = key
                    break
            
            if match:
                correct_count = val_counts[match]
                weight = (correct_count / total_responses) * 100
                report_lines.append(f"**{col}**")
                report_lines.append(f"- Correct Answer: `{correct_ans.strip()}`")
                report_lines.append(f"- Weight: **{weight:.2f}%** ({correct_count}/{total_responses})\\n")
            else:
                # If "Yes" wasn't found for some reason, just show highest
                report_lines.append(f"**{col}**")
                report_lines.append(f"- Correct Answer: `{correct_ans.strip()}` (Not found in responses)")
                report_lines.append(f"- Top response: `{list(val_counts.keys())[0]}` with {(val_counts.iloc[0]/total_responses)*100:.2f}%\\n")

report_lines.append("## Multiple-Choice Questions (Weight of Each Option)\\n")
# Multiple choice are identified by the column having a '/'
multiple_choice_prefixes = [
    '16. What are the clinical forms of thalassemia? (Tick all that apply)',
    '27. Problems faced by thalassemia major patients (Tick all that apply)',
    '28. What should a thalassemia carrier do after diagnosis? (Tick all that apply)'
]

for prefix in multiple_choice_prefixes:
    # Find all columns that start with this prefix and have a '/'
    option_cols = [c for c in df.columns if c.startswith(prefix) and '/' in c]
    if option_cols:
        report_lines.append(f"**{prefix}**")
        for col in option_cols:
            option_name = col.split('/', 1)[1].strip()
            # The column values are usually 1.0 (selected) or 0.0 (not selected)
            # Sometimes NaNs are present, which mean 0
            selected_count = df[col].sum()
            weight = (selected_count / total_responses) * 100
            report_lines.append(f"- Option: `{option_name}` -> Weight: **{weight:.2f}%** ({int(selected_count)}/{total_responses})")
        report_lines.append("\\n")

with open('Knowledge_Weights_Report.md', 'w') as f:
    f.write('\\n'.join(report_lines))

print("Report generated successfully.")
