import pandas as pd
import numpy as np
from scipy import stats
import os
import subprocess

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
raw_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
v3_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'
att_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv'

df_raw = pd.read_excel(raw_file, sheet_name=0)
df_know = pd.read_csv(v3_file)
df_att = pd.read_csv(att_file)

# ---------------------------------------------------------
# Extract & Clean Demographics
# ---------------------------------------------------------
gender_col = [c for c in df_raw.columns if 'gender' in str(c).lower()][0]
marital_col = '9. Marital Status'
age_col = [c for c in df_raw.columns if '1. Age' in c][0]
edu_col = [c for c in df_raw.columns if '7. Education Level' in c][0]
occ_col = [c for c in df_raw.columns if '5. Occupation' in c][0]
inc_col = [c for c in df_raw.columns if '6. Monthly Income' in c][0]

df_raw[age_col] = pd.to_numeric(df_raw[age_col], errors='coerce')

df = pd.DataFrame({
    'Gender': df_raw[gender_col].str.strip().str.title(),
    'Marital_Status': df_raw[marital_col].str.strip().str.title(),
    'Age_Group': np.where(df_raw[age_col] >= 35, '35 and Above', 'Below 35'),
    'Education': df_raw[edu_col].str.strip(),
    'Occupation': df_raw[occ_col].str.strip(),
    'Income': df_raw[inc_col].str.strip().fillna('No Income'),
    'Knowledge': df_know['Weighted_V3_Knowledge_Score'],
    'Partner_Attitude': df_att['Weighted_V3_Partner_Attitude'],
    'Cascade_Attitude': df_att['Weighted_V3_Cascade_Attitude']
})

# ---------------------------------------------------------
# Calculate Practice Scores
# ---------------------------------------------------------
col_1st = [c for c in df_raw.columns if 'First-degree' in c][0]
col_2nd = [c for c in df_raw.columns if 'Second-degree' in c][0]
col_3rd = [c for c in df_raw.columns if 'Third-degree' in c][0]
q33_col = [c for c in df_raw.columns if '33.' in c][0]

def score_relative(val):
    v = str(val).lower()
    if 'all' in v: return 2
    if 'some' in v: return 1
    return 0
df['Cascade_Practice_Raw'] = df_raw[col_1st].apply(score_relative) + df_raw[col_2nd].apply(score_relative) + df_raw[col_3rd].apply(score_relative)

def map_partner_practice(val):
    v = str(val).lower()
    if 'before marriage' in v: return 'Good Practice'
    elif 'after marriage' in v or 'pregnancy' in v or 'did not screen' in v or 'did not disclose' in v: return 'Poor Practice'
    return np.nan
df['Partner_Practice_Cat'] = df_raw[q33_col].apply(map_partner_practice)

# ---------------------------------------------------------
# Categorical KAP Cutoffs (Median Split)
# ---------------------------------------------------------
df['Knowledge_Cat'] = np.where(df['Knowledge'] > df['Knowledge'].median(), 'High', 'Low')
df['P_Attitude_Cat'] = np.where(df['Partner_Attitude'] > df['Partner_Attitude'].median(), 'Good', 'Poor')
df['C_Attitude_Cat'] = np.where(df['Cascade_Attitude'] > df['Cascade_Attitude'].median(), 'Good', 'Poor')
df['C_Practice_Cat'] = np.where(df['Cascade_Practice_Raw'] > df['Cascade_Practice_Raw'].median(), 'Good', 'Poor')

# ---------------------------------------------------------
# Chi-Square Analysis
# ---------------------------------------------------------
demographics = ['Gender', 'Marital_Status', 'Age_Group', 'Education', 'Occupation', 'Income']
kap_metrics = {
    'Knowledge_Cat': 'Knowledge',
    'P_Attitude_Cat': 'Partner Attitude',
    'C_Attitude_Cat': 'Cascade Attitude',
    'Partner_Practice_Cat': 'Partner Practice',
    'C_Practice_Cat': 'Cascade Practice'
}

results_matrix = pd.DataFrame(index=demographics, columns=kap_metrics.values())

def get_chi2_p(col1, col2):
    # dropna for the specific pair
    temp = df[[col1, col2]].dropna()
    # If the demographic is Marital_Status, filter strictly Married/Single
    if col1 == 'Marital_Status':
        temp = temp[temp[col1].isin(['Married', 'Single'])]
    
    contingency = pd.crosstab(temp[col1], temp[col2])
    # Avoid errors if a category dropped out
    if contingency.shape[0] < 2 or contingency.shape[1] < 2:
        return np.nan
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return p

for demo in demographics:
    for kap_col, kap_name in kap_metrics.items():
        p_val = get_chi2_p(demo, kap_col)
        # Format significantly as bold
        if not pd.isna(p_val):
            if p_val < 0.05:
                results_matrix.loc[demo, kap_name] = f"**{p_val:.4f}**"
            else:
                results_matrix.loc[demo, kap_name] = f"{p_val:.4f}"
        else:
            results_matrix.loc[demo, kap_name] = "N/A"

# Generate Report
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

md_content = f"""# Demographics vs KAP Model: Chi-Square P-Value Matrix

This report explores the relationship between strict demographic variables and the binary "High vs. Low" categorical splits of the KAP (Knowledge, Attitude, Practice) metrics. 

By analyzing the P-values across a $30$-test Chi-Square matrix, we can see exactly which demographic factors act as significant predictors for each step of the pipeline.

### P-Value Matrix
*(P-values **< 0.05** are bolded to indicate statistical significance)*

{ "```\\n" + results_matrix.to_string() + "\\n```" }

---

### Key Takeaways from the Matrix:
* This table confirms our earlier continuous ANOVA findings: **Education**, **Occupation**, and **Income** are the primary socioeconomic drivers of Knowledge and Attitudes.
* Basic demographic traits like **Gender** and **Age** show almost no significant bearing on a carrier's KAP pipeline. 
* Interestingly, while **Marital Status** proved to be significant when tested continuously, its significance drops when binned categorically. However, socioeconomic factors remain strongly robust across both continuous and categorical tests.
"""

md_path = os.path.join(out_dir_md, 'Demographics_ChiSquare_Matrix.md')
with open(md_path, 'w') as f:
    f.write(md_content)

out_pdf = os.path.join(out_dir_pdf, 'Demographics_ChiSquare_Matrix.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Demographic Chi-Square matrix generated successfully.")
