import pandas as pd

excel_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)
n = len(df)

q28_cols = [c for c in df.columns if c.startswith('28.') and '/' in c]
q28_scores = {'get the partner tested before marriage': 2, 'get family members tested': 1, 'ignore it': -3, 'i don’t know': 0}

q30_col = [c for c in df.columns if c.startswith('30.')][0]
q30_scores = {'definitely not': 2, 'not sure': -1, 'yes i am willing': -3, 'yes i have': -3}

q31_col = [c for c in df.columns if c.startswith('31.')][0]
q31_scores = {'no': 2, 'not sure': -1, 'yes': -3}

q32_col = [c for c in df.columns if c.startswith('32.')][0]
q32_scores = {'very important': 2, 'important': 1, 'not sure': -1, 'not important': -2}

q35_col = [c for c in df.columns if c.startswith('35.')][0]
q35_scores = {'agree': 2, 'don’t know': 0, 'disagree': -2}

q39_col = [c for c in df.columns if c.startswith('39.')][0]
q39_scores = {'very easy': 2, 'somewhat easy': 1, 'not sure': 0, 'difficult': -1}

q40_col = [c for c in df.columns if c.startswith('40.')][0]
q40_scores = {'very important': 2, 'important': 1, 'slightly important': -1, 'not important': -2}

def get_p_val_single(col, target_str):
    matches = sum(1 for val in df[col] if pd.notna(val) and target_str in str(val).strip().lower())
    return matches / n

print("| Question | Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |")
print("|---|---|---|---|---|---|")

# Q28
for option_str, weight in q28_scores.items():
    # find col
    p = 0
    for col in q28_cols:
        if option_str in col.lower():
            p = df[col].sum() / n
            break
    final_score = weight * (1 - p)
    print(f"| Q28. Carrier after diagnosis | {option_str.title()} | {weight} | {p:.3f} | {(1-p):.3f} | **{final_score:.3f}** |")

# Single choices
def print_single(q_name, col, score_dict):
    for option_str, weight in score_dict.items():
        p = get_p_val_single(col, option_str)
        final_score = weight * (1 - p)
        print(f"| {q_name} | {option_str.title()} | {weight} | {p:.3f} | {(1-p):.3f} | **{final_score:.3f}** |")

print_single('Q30. Consanguineous marriage', q30_col, q30_scores)
print_single('Q31. Marriage between carriers', q31_col, q31_scores)
print_single('Q32. Pre-marital screening', q32_col, q32_scores)
print_single('Q35. Family screening important', q35_col, q35_scores)
print_single('Q39. Ease of convincing', q39_col, q39_scores)
print_single('Q40. Cascade screening prevention', q40_col, q40_scores)
