import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

raw_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df_raw = pd.read_excel(raw_file, sheet_name=0)

v3_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'
att_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv'

df_know = pd.read_csv(v3_file)
df_att = pd.read_csv(att_file)

# Extract relative columns
col_1st = [c for c in df_raw.columns if 'First-degree' in c][0]
col_2nd = [c for c in df_raw.columns if 'Second-degree' in c][0]
col_3rd = [c for c in df_raw.columns if 'Third-degree' in c][0]

def score_relative(val):
    v = str(val).lower()
    if 'all' in v: return 2
    if 'some' in v: return 1
    return 0 # "don't know" or NaN

# Build DataFrame
df = pd.DataFrame({
    'Knowledge': df_know['Weighted_V3_Knowledge_Score'],
    'Cascade_Attitude': df_att['Weighted_V3_Cascade_Attitude']
})

df['Score_1st'] = df_raw[col_1st].apply(score_relative)
df['Score_2nd'] = df_raw[col_2nd].apply(score_relative)
df['Score_3rd'] = df_raw[col_3rd].apply(score_relative)

df['Cascade_Practice_Score'] = df['Score_1st'] + df['Score_2nd'] + df['Score_3rd']

df = df.dropna(subset=['Knowledge', 'Cascade_Attitude', 'Cascade_Practice_Score'])

# ---------------------------------------------------------
# Correlations
# ---------------------------------------------------------
r_know, p_know = stats.pearsonr(df['Knowledge'], df['Cascade_Practice_Score'])
r_att, p_att = stats.pearsonr(df['Cascade_Attitude'], df['Cascade_Practice_Score'])

charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

# Scatter: Knowledge vs Practice
plt.figure(figsize=(9, 6))
sns.regplot(x='Knowledge', y='Cascade_Practice_Score', data=df, 
            scatter_kws={'alpha':0.6, 'color':'indigo', 's': df.groupby(['Knowledge', 'Cascade_Practice_Score']).Cascade_Practice_Score.transform('size') * 10}, 
            line_kws={'color':'red'}, x_jitter=0.2, y_jitter=0.2)
plt.title(f'Correlation: Knowledge vs Cascade Screening Practice (Relatives)\nPearson r = {r_know:.3f}, p = {p_know:.4f}', fontsize=14)
plt.xlabel('Weighted V3 Knowledge Score')
plt.ylabel('Cascade Practice Score (0-6 scale)')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Scatter_Knowledge_vs_CascadePractice.png'))
plt.close()

# Scatter: Attitude vs Practice
plt.figure(figsize=(9, 6))
sns.regplot(x='Cascade_Attitude', y='Cascade_Practice_Score', data=df, 
            scatter_kws={'alpha':0.6, 'color':'teal', 's': df.groupby(['Cascade_Attitude', 'Cascade_Practice_Score']).Cascade_Practice_Score.transform('size') * 10}, 
            line_kws={'color':'red'}, x_jitter=0.2, y_jitter=0.2)
plt.title(f'Correlation: Cascade Attitude vs Cascade Screening Practice (Relatives)\nPearson r = {r_att:.3f}, p = {p_att:.4f}', fontsize=14)
plt.xlabel('Weighted V3 Cascade Attitude Score')
plt.ylabel('Cascade Practice Score (0-6 scale)')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Scatter_Attitude_vs_CascadePractice.png'))
plt.close()

# ---------------------------------------------------------
# Generate Report
# ---------------------------------------------------------
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'

report = f"""# Inferential Statistics: Cascade Screening Practice (Relatives)
**Pearson Correlation Analysis**

This report quantifies "Cascade Practice" by examining exactly *how far* the participant went in getting their relatives screened. 

**The Cascade Practice Score (Scale 0-6):**
* First-degree relatives (parents, siblings, children): All (+2), Some (+1), Don't know (+0)
* Second-degree relatives (grandparents, uncles, aunts): All (+2), Some (+1), Don't know (+0)
* Third-degree relatives (cousins): All (+2), Some (+1), Don't know (+0)

We then tested this 0-6 behavioral score against both the participant's Knowledge and their Cascade Attitude.

---

### 1. Knowledge vs. Cascade Practice (Relatives)
*Does a higher clinical understanding of thalassemia translate into more extensive family screening?*

* **Pearson Correlation Coefficient ($r$):** {r_know:.3f}
* **P-Value:** {p_know:.4f}
* **Conclusion:** {'**Statistically Significant Correlation (p < 0.05).** Higher knowledge leads to more extensive screening.' if p_know < 0.05 else '**Not Statistically Significant (p > 0.05).** Knowledge does not directly translate into screening execution.'}

![Scatter Plot: Knowledge vs Practice]({charts_dir}/Scatter_Knowledge_vs_CascadePractice.png)

---

### 2. Cascade Attitude vs. Cascade Practice (Relatives)
*Does a strong belief that family members should be screened translate into actual screening execution?*

* **Pearson Correlation Coefficient ($r$):** {r_att:.3f}
* **P-Value:** {p_att:.4f}
* **Conclusion:** {'**Statistically Significant Correlation (p < 0.05).** Positive attitudes translate directly into action.' if p_att < 0.05 else '**Not Statistically Significant (p > 0.05).** There is a disconnect between wanting relatives to get screened and them actually doing it.'}

![Scatter Plot: Attitude vs Practice]({charts_dir}/Scatter_Attitude_vs_CascadePractice.png)
"""

md_path = os.path.join(out_dir_md, 'Cascade_Practice_Correlation_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Cascade_Practice_Correlation_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Cascade Practice Correlation completed and report generated successfully.")
