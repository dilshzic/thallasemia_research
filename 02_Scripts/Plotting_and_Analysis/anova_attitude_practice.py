import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

raw_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df_raw = pd.read_excel(raw_file, sheet_name=0)

att_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv'
df_att = pd.read_csv(att_file)

q33_col = [c for c in df_raw.columns if '33.' in c][0]
q36_col = [c for c in df_raw.columns if '36.' in c][0]

df = pd.DataFrame({
    'Partner_Practice_Raw': df_raw[q33_col].astype(str).str.strip(),
    'Family_Practice_Raw': df_raw[q36_col].astype(str).str.strip(),
    'Partner_Attitude': df_att['Weighted_V3_Partner_Attitude'],
    'Cascade_Attitude': df_att['Weighted_V3_Cascade_Attitude']
})

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. Partner Screening Practice vs Partner Attitude (ANOVA)
# ---------------------------------------------------------
def map_partner_practice(val):
    v = str(val).lower()
    if 'before marriage' in v:
        return 'Safe Practice (Before Marriage)'
    elif 'after marriage' in v or 'pregnancy' in v:
        return 'Delayed Practice (After Marriage / Pregnancy)'
    elif 'did not screen' in v or 'did not disclose' in v:
        return 'Unsafe Practice (No Screening / No Disclosure)'
    else:
        return np.nan

df['Partner_Practice'] = df['Partner_Practice_Raw'].apply(map_partner_practice)
df_partner = df.dropna(subset=['Partner_Practice', 'Partner_Attitude']).copy()

partner_order = ['Unsafe Practice (No Screening / No Disclosure)', 'Delayed Practice (After Marriage / Pregnancy)', 'Safe Practice (Before Marriage)']
df_partner['Partner_Practice'] = pd.Categorical(df_partner['Partner_Practice'], categories=partner_order, ordered=True)

groups_att_partner = [df_partner[df_partner['Partner_Practice'] == level]['Partner_Attitude'].values for level in partner_order if len(df_partner[df_partner['Partner_Practice'] == level]) > 0]
f_stat_partner, p_val_partner = stats.f_oneway(*groups_att_partner)

desc_partner = df_partner.groupby('Partner_Practice').agg(
    N=('Partner_Attitude', 'count'),
    Mean_Attitude=('Partner_Attitude', 'mean'),
    Std_Attitude=('Partner_Attitude', 'std')
).reset_index()

plt.figure(figsize=(10, 6))
sns.violinplot(y='Partner_Practice', x='Partner_Attitude', data=df_partner, inner='quartile', palette='magma')
plt.title(f'Weighted V3 Partner Attitude by Actual Partner Screening Practice\nOne-Way ANOVA p-value: {p_val_partner:.4f}', fontsize=14)
plt.xlabel('Weighted V3 Partner Selection Attitude Score')
plt.ylabel('Practice')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Attitude_PartnerPractice_Violin.png'))
plt.close()

# ---------------------------------------------------------
# 2. Family Disclosure Practice vs Cascade Attitude (T-Test)
# ---------------------------------------------------------
df_family = df[df['Family_Practice_Raw'].isin(['Yes', 'No'])].dropna(subset=['Cascade_Attitude']).copy()

family_yes = df_family[df_family['Family_Practice_Raw'] == 'Yes']
family_no = df_family[df_family['Family_Practice_Raw'] == 'No']

t_stat_family, p_val_family = stats.ttest_ind(family_yes['Cascade_Attitude'], family_no['Cascade_Attitude'], equal_var=False)

desc_family = df_family.groupby('Family_Practice_Raw').agg(
    N=('Cascade_Attitude', 'count'),
    Mean_Attitude=('Cascade_Attitude', 'mean'),
    Std_Attitude=('Cascade_Attitude', 'std')
).reset_index()

plt.figure(figsize=(10, 6))
sns.violinplot(x='Family_Practice_Raw', y='Cascade_Attitude', data=df_family, inner='quartile', palette='cividis')
plt.title(f'Weighted V3 Cascade Attitude by Actual Family Disclosure\nT-Test p-value: {p_val_family:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Cascade Screening Attitude Score')
plt.xlabel('Did you disclose to family?')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Attitude_FamilyPractice_Violin.png'))
plt.close()

# ---------------------------------------------------------
# 3. Generate Combined Report
# ---------------------------------------------------------
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'

desc_partner_rows = ""
for _, row in desc_partner.iterrows():
    desc_partner_rows += f"| {row['Partner_Practice']} | {row['N']} | {row['Mean_Attitude']:.3f} | {row['Std_Attitude']:.3f} |\n"

desc_family_rows = ""
for _, row in desc_family.iterrows():
    desc_family_rows += f"| {row['Family_Practice_Raw']} | {row['N']} | {row['Mean_Attitude']:.3f} | {row['Std_Attitude']:.3f} |\n"

report = f"""# Inferential Statistics: Attitude Score vs. Actual Practices

This report examines whether a participant's stated attitudes correlate with the actual actions they took regarding partner screening and family disclosure.

---

## 1. Partner Selection Attitude vs. Actual Partner Screening (ANOVA)
*Testing if a positive attitude towards choosing a non-carrier partner resulted in safer screening practices in reality.*

| Behavioral Tier | N | Mean (Partner Attitude) | Std Dev |
|---|---|---|---|
{desc_partner_rows}

* **F-Statistic:** {f_stat_partner:.3f}
* **P-Value:** {p_val_partner:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** Attitudes translate directly to actual practice.' if p_val_partner < 0.05 else '**Not Statistically Significant (p > 0.05).** There is a disconnect between stated attitudes and actual behavior.'}

![Violin Plot]({charts_dir}/Attitude_PartnerPractice_Violin.png)

---

## 2. Cascade Screening Attitude vs. Actual Family Disclosure (T-Test)
*Testing if a positive attitude regarding the necessity of family testing resulted in actually telling their family.*

| Disclosed to Family? | N | Mean (Cascade Attitude) | Std Dev |
|---|---|---|---|
{desc_family_rows}

* **T-Statistic:** {t_stat_family:.3f}
* **P-Value:** {p_val_family:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** Positive attitudes lead to actual disclosure.' if p_val_family < 0.05 else '**Not Statistically Significant (p > 0.05).** Attitudes do not dictate disclosure behavior.'}

![Violin Plot]({charts_dir}/Attitude_FamilyPractice_Violin.png)
"""

md_path = os.path.join(out_dir_md, 'Attitude_Practice_Inferential_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Attitude_Practice_Inferential_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Attitude vs Practice tests completed. Report generated successfully.")
