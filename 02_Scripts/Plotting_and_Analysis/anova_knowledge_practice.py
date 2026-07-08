import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

raw_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df_raw = pd.read_excel(raw_file, sheet_name=0)

v3_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_V3_Knowledge.csv'
v3_weighted_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'

df_v3 = pd.read_csv(v3_file)
df_w_v3 = pd.read_csv(v3_weighted_file)

q33_col = [c for c in df_raw.columns if '33.' in c][0]
q36_col = [c for c in df_raw.columns if '36.' in c][0]

df = pd.DataFrame({
    'Partner_Practice_Raw': df_raw[q33_col].astype(str).str.strip(),
    'Family_Practice_Raw': df_raw[q36_col].astype(str).str.strip(),
    'V3_Score': df_v3['V3_Knowledge_Score'],
    'Weighted_V3_Score': df_w_v3['Weighted_V3_Knowledge_Score']
})

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. Partner Screening Practice (ANOVA)
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
        return np.nan # Exclude 'Other' or 'nan'

df['Partner_Practice'] = df['Partner_Practice_Raw'].apply(map_partner_practice)
df_partner = df.dropna(subset=['Partner_Practice']).copy()

partner_order = ['Unsafe Practice (No Screening / No Disclosure)', 'Delayed Practice (After Marriage / Pregnancy)', 'Safe Practice (Before Marriage)']
df_partner['Partner_Practice'] = pd.Categorical(df_partner['Partner_Practice'], categories=partner_order, ordered=True)

groups_wv3_partner = [df_partner[df_partner['Partner_Practice'] == level]['Weighted_V3_Score'].values for level in partner_order if len(df_partner[df_partner['Partner_Practice'] == level]) > 0]
f_stat_partner, p_val_partner = stats.f_oneway(*groups_wv3_partner)

desc_partner = df_partner.groupby('Partner_Practice').agg(
    N=('Weighted_V3_Score', 'count'),
    Mean_WV3=('Weighted_V3_Score', 'mean'),
    Std_WV3=('Weighted_V3_Score', 'std')
).reset_index()

plt.figure(figsize=(10, 6))
sns.violinplot(y='Partner_Practice', x='Weighted_V3_Score', data=df_partner, inner='quartile', palette='coolwarm')
plt.title(f'Weighted V3 Knowledge Score by Partner Screening Practice\nOne-Way ANOVA p-value: {p_val_partner:.4f}', fontsize=14)
plt.xlabel('Weighted V3 Knowledge Score')
plt.ylabel('Practice')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_PartnerPractice_Violin.png'))
plt.close()

# ---------------------------------------------------------
# 2. Family Disclosure Practice (T-Test)
# ---------------------------------------------------------
df_family = df[df['Family_Practice_Raw'].isin(['Yes', 'No'])].copy()

family_yes = df_family[df_family['Family_Practice_Raw'] == 'Yes']
family_no = df_family[df_family['Family_Practice_Raw'] == 'No']

t_stat_family, p_val_family = stats.ttest_ind(family_yes['Weighted_V3_Score'], family_no['Weighted_V3_Score'], equal_var=False)

desc_family = df_family.groupby('Family_Practice_Raw').agg(
    N=('Weighted_V3_Score', 'count'),
    Mean_WV3=('Weighted_V3_Score', 'mean'),
    Std_WV3=('Weighted_V3_Score', 'std')
).reset_index()

plt.figure(figsize=(10, 6))
sns.violinplot(x='Family_Practice_Raw', y='Weighted_V3_Score', data=df_family, inner='quartile', palette='viridis')
plt.title(f'Weighted V3 Knowledge Score by Family Disclosure\nT-Test p-value: {p_val_family:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Did you disclose to family?')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_FamilyPractice_Violin.png'))
plt.close()

# ---------------------------------------------------------
# 3. Generate Combined Report
# ---------------------------------------------------------
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

desc_partner_rows = ""
for _, row in desc_partner.iterrows():
    desc_partner_rows += f"| {row['Partner_Practice']} | {row['N']} | {row['Mean_WV3']:.3f} | {row['Std_WV3']:.3f} |\n"

desc_family_rows = ""
for _, row in desc_family.iterrows():
    desc_family_rows += f"| {row['Family_Practice_Raw']} | {row['N']} | {row['Mean_WV3']:.3f} | {row['Std_WV3']:.3f} |\n"

report = f"""# Inferential Statistics: Knowledge Score vs. Actual Practices

This report examines whether clinical knowledge dictates the actual actions a carrier takes regarding family planning (Partner Screening) and cascade screening (Family Disclosure).

---

## 1. Partner Screening Practice (One-Way ANOVA)
*We grouped the participants into three behavioral tiers: Safe (Screened before marriage), Delayed (Screened after marriage/pregnancy), and Unsafe (Did not screen/disclose).*
*Note: Participants marked 'Other' (usually single/unmarried) were excluded.*

| Behavioral Tier | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
{desc_partner_rows}

* **F-Statistic:** {f_stat_partner:.3f}
* **P-Value:** {p_val_partner:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** Clinical knowledge determines partner screening behavior.' if p_val_partner < 0.05 else '**Not Statistically Significant (p > 0.05).** Clinical knowledge does not significantly alter actual partner screening practices.'}

![Violin Plot]({charts_dir}/Knowledge_PartnerPractice_Violin.png)

---

## 2. Family Disclosure Practice (Welch's T-Test)
*Comparing carriers who disclosed their status to their family versus those who kept it a secret.*

| Disclosed to Family? | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
{desc_family_rows}

* **T-Statistic:** {t_stat_family:.3f}
* **P-Value:** {p_val_family:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** Clinical knowledge influences family disclosure.' if p_val_family < 0.05 else '**Not Statistically Significant (p > 0.05).** Clinical knowledge does not significantly influence whether a carrier tells their family.'}

![Violin Plot]({charts_dir}/Knowledge_FamilyPractice_Violin.png)
"""

md_path = os.path.join(out_dir_md, 'Knowledge_Practice_Inferential_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Knowledge_Practice_Inferential_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Practice ANOVA and T-Tests completed. Report generated successfully.")
