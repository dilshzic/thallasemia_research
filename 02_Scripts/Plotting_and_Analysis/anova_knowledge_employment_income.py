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

occ_col = [c for c in df_raw.columns if '5. Occupation' in c][0]
inc_col = [c for c in df_raw.columns if '6. Monthly Income' in c][0]

df = pd.DataFrame({
    'Occupation': df_raw[occ_col].str.strip(),
    'Income': df_raw[inc_col].str.strip(),
    'V3_Score': df_v3['V3_Knowledge_Score'],
    'Weighted_V3_Score': df_w_v3['Weighted_V3_Knowledge_Score']
})

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

# ---------------------------------------------------------
# 1. ANOVA: Occupation Category
# ---------------------------------------------------------
df_occ = df.dropna(subset=['Occupation']).copy()
occ_order = ['Not employed', 'Private sector', 'Government sector', 'Self-employed']
df_occ['Occupation'] = pd.Categorical(df_occ['Occupation'], categories=occ_order, ordered=True)

groups_occ_wv3 = [df_occ[df_occ['Occupation'] == level]['Weighted_V3_Score'].values for level in occ_order if len(df_occ[df_occ['Occupation'] == level]) > 0]
f_stat_occ, p_val_occ = stats.f_oneway(*groups_occ_wv3)

desc_occ = df_occ.groupby('Occupation').agg(
    N=('Weighted_V3_Score', 'count'),
    Mean_WV3=('Weighted_V3_Score', 'mean'),
    Std_WV3=('Weighted_V3_Score', 'std')
).reset_index()

plt.figure(figsize=(10, 6))
sns.violinplot(x='Occupation', y='Weighted_V3_Score', data=df_occ, inner='quartile', palette='Set2')
plt.title(f'Weighted V3 Knowledge Score by Occupation\nOne-Way ANOVA p-value: {p_val_occ:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Occupation Category')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Occupation_Violin.png'))
plt.close()

# ---------------------------------------------------------
# 2. ANOVA: Income Level
# ---------------------------------------------------------
df_inc = df.copy()
df_inc['Income'] = df_inc['Income'].fillna('No Income')
inc_order = ['No Income', '< 25,000', '25,000 – 50,000', '51,000 – 100,000', '> 100,000']
df_inc['Income'] = pd.Categorical(df_inc['Income'], categories=inc_order, ordered=True)

groups_inc_wv3 = [df_inc[df_inc['Income'] == level]['Weighted_V3_Score'].values for level in inc_order if len(df_inc[df_inc['Income'] == level]) > 0]
f_stat_inc, p_val_inc = stats.f_oneway(*groups_inc_wv3)

desc_inc = df_inc.groupby('Income').agg(
    N=('Weighted_V3_Score', 'count'),
    Mean_WV3=('Weighted_V3_Score', 'mean'),
    Std_WV3=('Weighted_V3_Score', 'std')
).reset_index()

plt.figure(figsize=(10, 6))
sns.violinplot(x='Income', y='Weighted_V3_Score', data=df_inc, inner='quartile', palette='Set3')
plt.title(f'Weighted V3 Knowledge Score by Monthly Income\nOne-Way ANOVA p-value: {p_val_inc:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Monthly Income (LKR)')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Income_Violin.png'))
plt.close()

# ---------------------------------------------------------
# 3. Generate Combined Report
# ---------------------------------------------------------
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

desc_occ_rows = ""
for _, row in desc_occ.iterrows():
    desc_occ_rows += f"| {row['Occupation']} | {row['N']} | {row['Mean_WV3']:.3f} | {row['Std_WV3']:.3f} |\n"

desc_inc_rows = ""
for _, row in desc_inc.iterrows():
    desc_inc_rows += f"| {row['Income']} | {row['N']} | {row['Mean_WV3']:.3f} | {row['Std_WV3']:.3f} |\n"

report = f"""# Inferential Statistics: Knowledge Score vs. Occupation & Income
**One-Way ANOVA (Analysis of Variance)**

This report examines whether clinical knowledge differs significantly across the 4 specific occupation categories and the 4 monthly income brackets.

---

## 1. Occupation Category ANOVA
*Comparing Not employed, Private sector, Government sector, and Self-employed.*

| Occupation Category | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
{desc_occ_rows}

* **F-Statistic:** {f_stat_occ:.3f}
* **P-Value:** {p_val_occ:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on occupation category.' if p_val_occ < 0.05 else '**Not Statistically Significant (p > 0.05).** The specific sector of employment does not significantly impact knowledge.'}

![Violin Plot]({charts_dir}/Knowledge_Occupation_Violin.png)

---

## 2. Monthly Income ANOVA
*Comparing the four income brackets among those who reported a salary.*

| Monthly Income (LKR) | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
{desc_inc_rows}

* **F-Statistic:** {f_stat_inc:.3f}
* **P-Value:** {p_val_inc:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on income level.' if p_val_inc < 0.05 else '**Not Statistically Significant (p > 0.05).** Income level does not significantly impact knowledge.'}

![Violin Plot]({charts_dir}/Knowledge_Income_Violin.png)
"""

md_path = os.path.join(out_dir_md, 'Knowledge_Occupation_Income_ANOVA_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Knowledge_Occupation_Income_ANOVA_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("ANOVAs completed and combined report generated successfully.")
