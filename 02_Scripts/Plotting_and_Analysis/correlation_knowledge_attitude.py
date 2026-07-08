import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

# Load Processed Data
att_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv'
know_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'

df_att = pd.read_csv(att_file)
df_know = pd.read_csv(know_file)

# Merge datasets
if '_id' in df_att.columns and '_id' in df_know.columns:
    df = pd.merge(df_know, df_att, on='_id')
else:
    # Fallback to index if _id is missing
    df = pd.concat([df_know, df_att], axis=1)

# Drop any NAs in the score columns just in case
df = df.dropna(subset=['Weighted_V3_Knowledge_Score', 'Weighted_V3_Partner_Attitude', 'Weighted_V3_Cascade_Attitude'])

# Perform Pearson Correlation
r_partner, p_partner = stats.pearsonr(df['Weighted_V3_Knowledge_Score'], df['Weighted_V3_Partner_Attitude'])
r_cascade, p_cascade = stats.pearsonr(df['Weighted_V3_Knowledge_Score'], df['Weighted_V3_Cascade_Attitude'])

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

# Scatter plot: Knowledge vs Partner Attitude
plt.figure(figsize=(9, 6))
sns.regplot(x='Weighted_V3_Knowledge_Score', y='Weighted_V3_Partner_Attitude', data=df, 
            scatter_kws={'alpha':0.6, 'color':'indigo'}, line_kws={'color':'red'})
plt.title(f'Correlation: Knowledge vs Partner Selection Attitude\nPearson r = {r_partner:.3f}, p = {p_partner:.4f}', fontsize=14)
plt.xlabel('Weighted V3 Knowledge Score')
plt.ylabel('Weighted V3 Partner Attitude Score')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Scatter_Knowledge_vs_Partner.png'))
plt.close()

# Scatter plot: Knowledge vs Cascade Attitude
plt.figure(figsize=(9, 6))
sns.regplot(x='Weighted_V3_Knowledge_Score', y='Weighted_V3_Cascade_Attitude', data=df, 
            scatter_kws={'alpha':0.6, 'color':'teal'}, line_kws={'color':'red'})
plt.title(f'Correlation: Knowledge vs Cascade Screening Attitude\nPearson r = {r_cascade:.3f}, p = {p_cascade:.4f}', fontsize=14)
plt.xlabel('Weighted V3 Knowledge Score')
plt.ylabel('Weighted V3 Cascade Attitude Score')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Scatter_Knowledge_vs_Cascade.png'))
plt.close()

# Generate Report
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

report = f"""# Inferential Statistics: Knowledge vs. Attitudes
**Pearson Correlation Analysis**

This report examines whether a participant's level of clinical knowledge directly correlates with their attitudes toward safe partner selection and cascade screening. 

We used the **Weighted V3 Scoring Schema** for all metrics to ensure mathematical rigor and resistance to ceiling effects.

---

### 1. Knowledge vs. Partner Selection Attitude
*Testing if higher clinical knowledge leads to a more responsible attitude regarding choosing a non-carrier partner.*

* **Pearson Correlation Coefficient ($r$):** {r_partner:.3f}
* **P-Value:** {p_partner:.4f}
* **Conclusion:** {'**Statistically Significant Correlation (p < 0.05).** There is a meaningful relationship between knowledge and partner selection attitude.' if p_partner < 0.05 else '**Not Statistically Significant (p > 0.05).** Increased knowledge does not correlate with a better attitude towards partner selection.'}
* **Direction:** {'Positive (Higher knowledge = Better attitude)' if r_partner > 0 else 'Negative'}

![Scatter Plot: Knowledge vs Partner]({charts_dir}/Scatter_Knowledge_vs_Partner.png)

---

### 2. Knowledge vs. Cascade Screening Attitude
*Testing if higher clinical knowledge leads to a more responsible attitude regarding disclosing status to family members.*

* **Pearson Correlation Coefficient ($r$):** {r_cascade:.3f}
* **P-Value:** {p_cascade:.4f}
* **Conclusion:** {'**Statistically Significant Correlation (p < 0.05).** There is a meaningful relationship between knowledge and cascade screening attitude.' if p_cascade < 0.05 else '**Not Statistically Significant (p > 0.05).** Increased knowledge does not correlate with a better attitude towards cascade screening.'}
* **Direction:** {'Positive (Higher knowledge = Better attitude)' if r_cascade > 0 else 'Negative'}

![Scatter Plot: Knowledge vs Cascade]({charts_dir}/Scatter_Knowledge_vs_Cascade.png)
"""

md_path = os.path.join(out_dir_md, 'Knowledge_Attitude_Correlation_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Knowledge_Attitude_Correlation_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Correlation analysis completed and report generated successfully.")
