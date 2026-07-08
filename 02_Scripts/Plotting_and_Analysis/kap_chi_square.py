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

# Extract relative columns for cascade practice
col_1st = [c for c in df_raw.columns if 'First-degree' in c][0]
col_2nd = [c for c in df_raw.columns if 'Second-degree' in c][0]
col_3rd = [c for c in df_raw.columns if 'Third-degree' in c][0]

def score_relative(val):
    v = str(val).lower()
    if 'all' in v: return 2
    if 'some' in v: return 1
    return 0

cascade_practice_score = df_raw[col_1st].apply(score_relative) + df_raw[col_2nd].apply(score_relative) + df_raw[col_3rd].apply(score_relative)

# Partner practice column
q33_col = [c for c in df_raw.columns if '33.' in c][0]

def map_partner_practice(val):
    v = str(val).lower()
    if 'before marriage' in v:
        return 'Good Practice'
    elif 'after marriage' in v or 'pregnancy' in v or 'did not screen' in v or 'did not disclose' in v:
        return 'Poor Practice'
    return np.nan

partner_practice_binary = df_raw[q33_col].apply(map_partner_practice)

# Build unified DataFrame
df = pd.DataFrame({
    'Knowledge': df_know['Weighted_V3_Knowledge_Score'],
    'Partner_Attitude': df_att['Weighted_V3_Partner_Attitude'],
    'Cascade_Attitude': df_att['Weighted_V3_Cascade_Attitude'],
    'Partner_Practice_Raw': partner_practice_binary,
    'Cascade_Practice_Raw': cascade_practice_score
})

# ---------------------------------------------------------
# Define Cutoffs (Median Split)
# ---------------------------------------------------------
know_med = df['Knowledge'].median()
p_att_med = df['Partner_Attitude'].median()
c_att_med = df['Cascade_Attitude'].median()
c_prac_med = df['Cascade_Practice_Raw'].median()

# Ensure we drop NaNs before making binary to avoid skew
df_k_pa = df.dropna(subset=['Knowledge', 'Partner_Attitude']).copy()
df_k_pa['Knowledge_Cat'] = np.where(df_k_pa['Knowledge'] > know_med, 'High Knowledge', 'Low Knowledge')
df_k_pa['P_Attitude_Cat'] = np.where(df_k_pa['Partner_Attitude'] > p_att_med, 'Good Attitude', 'Poor Attitude')

df_k_ca = df.dropna(subset=['Knowledge', 'Cascade_Attitude']).copy()
df_k_ca['Knowledge_Cat'] = np.where(df_k_ca['Knowledge'] > know_med, 'High Knowledge', 'Low Knowledge')
df_k_ca['C_Attitude_Cat'] = np.where(df_k_ca['Cascade_Attitude'] > c_att_med, 'Good Attitude', 'Poor Attitude')

df_k_pp = df.dropna(subset=['Knowledge', 'Partner_Practice_Raw']).copy()
df_k_pp['Knowledge_Cat'] = np.where(df_k_pp['Knowledge'] > know_med, 'High Knowledge', 'Low Knowledge')
df_k_pp['P_Practice_Cat'] = df_k_pp['Partner_Practice_Raw']

df_k_cp = df.dropna(subset=['Knowledge', 'Cascade_Practice_Raw']).copy()
df_k_cp['Knowledge_Cat'] = np.where(df_k_cp['Knowledge'] > know_med, 'High Knowledge', 'Low Knowledge')
df_k_cp['C_Practice_Cat'] = np.where(df_k_cp['Cascade_Practice_Raw'] > c_prac_med, 'Good Practice', 'Poor Practice')

df_a_pp = df.dropna(subset=['Partner_Attitude', 'Partner_Practice_Raw']).copy()
df_a_pp['P_Attitude_Cat'] = np.where(df_a_pp['Partner_Attitude'] > p_att_med, 'Good Attitude', 'Poor Attitude')
df_a_pp['P_Practice_Cat'] = df_a_pp['Partner_Practice_Raw']

df_a_cp = df.dropna(subset=['Cascade_Attitude', 'Cascade_Practice_Raw']).copy()
df_a_cp['C_Attitude_Cat'] = np.where(df_a_cp['Cascade_Attitude'] > c_att_med, 'Good Attitude', 'Poor Attitude')
df_a_cp['C_Practice_Cat'] = np.where(df_a_cp['Cascade_Practice_Raw'] > c_prac_med, 'Good Practice', 'Poor Practice')

# ---------------------------------------------------------
# Chi-Square Testing Function
# ---------------------------------------------------------
def do_chi2(data, col1, col2):
    contingency = pd.crosstab(data[col1], data[col2])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    return contingency, chi2, p

res = []

# 1. Knowledge vs Partner Attitude
cont, chi, p = do_chi2(df_k_pa, 'Knowledge_Cat', 'P_Attitude_Cat')
res.append(('Knowledge vs Partner Attitude', cont, chi, p))

# 2. Knowledge vs Cascade Attitude
cont, chi, p = do_chi2(df_k_ca, 'Knowledge_Cat', 'C_Attitude_Cat')
res.append(('Knowledge vs Cascade Attitude', cont, chi, p))

# 3. Knowledge vs Partner Practice
cont, chi, p = do_chi2(df_k_pp, 'Knowledge_Cat', 'P_Practice_Cat')
res.append(('Knowledge vs Partner Practice', cont, chi, p))

# 4. Knowledge vs Cascade Practice
cont, chi, p = do_chi2(df_k_cp, 'Knowledge_Cat', 'C_Practice_Cat')
res.append(('Knowledge vs Cascade Practice', cont, chi, p))

# 5. Partner Attitude vs Partner Practice
cont, chi, p = do_chi2(df_a_pp, 'P_Attitude_Cat', 'P_Practice_Cat')
res.append(('Partner Attitude vs Partner Practice', cont, chi, p))

# 6. Cascade Attitude vs Cascade Practice
cont, chi, p = do_chi2(df_a_cp, 'C_Attitude_Cat', 'C_Practice_Cat')
res.append(('Cascade Attitude vs Cascade Practice', cont, chi, p))


# Generate Markdown
md_content = f"""# KAP Model Chi-Square Tests
**Categorical Cutoff Analysis (Knowledge, Attitude, Practice)**

We mapped the continuous scoring data into binary categorical brackets (e.g. "High" vs "Low") to perform strict $2 \\times 2$ Chi-Square tests of independence. 

### Cutoff Definitions (Median Split Approach)
* **Knowledge Cutoff:** {know_med:.3f}
* **Partner Attitude Cutoff:** {p_att_med:.3f}
* **Cascade Attitude Cutoff:** {c_att_med:.3f}
* **Partner Practice:** "Good" = Screened before marriage. "Poor" = Screened after/pregnancy or did not screen.
* **Cascade Practice Cutoff:** Score > {c_prac_med:.1f} = "Good Practice", <= {c_prac_med:.1f} = "Poor Practice".

---
"""

for title, cont, chi, p in res:
    # Convert contingency table to markdown string
    table_str = "```\n" + cont.to_string() + "\n```"
    
    md_content += f"""
### {title}
{table_str}

* **Chi-Square Statistic:** {chi:.3f}
* **P-Value:** {p:.4f}
* **Conclusion:** {'**Statistically Significant Correlation (p < 0.05).**' if p < 0.05 else '**Not Statistically Significant (p > 0.05).**'}
---
"""

out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

md_path = os.path.join(out_dir_md, 'KAP_ChiSquare_Report.md')
with open(md_path, 'w') as f:
    f.write(md_content)

out_pdf = os.path.join(out_dir_pdf, 'KAP_ChiSquare_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Chi-Square testing complete and report generated successfully.")
