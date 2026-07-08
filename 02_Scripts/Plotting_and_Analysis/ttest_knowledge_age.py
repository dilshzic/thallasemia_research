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

age_col = [c for c in df_raw.columns if '1. Age' in c][0]

# Convert age to numeric, handling any potential non-numeric entries
df_raw[age_col] = pd.to_numeric(df_raw[age_col], errors='coerce')

df = pd.DataFrame({
    'Age': df_raw[age_col],
    'V3_Score': df_v3['V3_Knowledge_Score'],
    'Weighted_V3_Score': df_w_v3['Weighted_V3_Knowledge_Score']
})

df = df.dropna(subset=['Age'])

# Create Binary Group
df['Age_Group'] = np.where(df['Age'] >= 35, '35 and Above', 'Below 35')

above_35 = df[df['Age_Group'] == '35 and Above']
below_35 = df[df['Age_Group'] == 'Below 35']

# T-Test for V3 Score
t_stat_v3, p_val_v3 = stats.ttest_ind(above_35['V3_Score'], below_35['V3_Score'], equal_var=False)

# T-Test for Weighted V3 Score
t_stat_wv3, p_val_wv3 = stats.ttest_ind(above_35['Weighted_V3_Score'], below_35['Weighted_V3_Score'], equal_var=False)

# Visualize
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

plt.figure(figsize=(10, 6))
sns.violinplot(x='Age_Group', y='Weighted_V3_Score', data=df, inner='quartile', color='gold', order=['Below 35', '35 and Above'])
plt.title(f'Weighted V3 Knowledge Score by Age Group\nT-Test p-value: {p_val_wv3:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Age Group')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Age_Violin.png'))
plt.close()

plt.figure(figsize=(8, 6))
sns.boxplot(x='Age_Group', y='V3_Score', data=df, color='skyblue', order=['Below 35', '35 and Above'])
plt.title(f'V3 Knowledge Score by Age Group\nT-Test p-value: {p_val_v3:.4f}', fontsize=14)
plt.ylabel('V3 Knowledge Score')
plt.xlabel('Age Group')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Age_Box.png'))
plt.close()

# Generate Report
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

report = f"""# Inferential Statistics: Knowledge Score vs. Age Group
**Independent Two-Sample T-Test**

This report examines whether there is a statistically significant difference in clinical knowledge between carriers who are younger than 35 and those who are 35 or older.

### Descriptive Statistics

| Age Group | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Below 35 | {len(below_35)} | {below_35['V3_Score'].mean():.2f} | {below_35['V3_Score'].std():.2f} | {below_35['Weighted_V3_Score'].mean():.3f} | {below_35['Weighted_V3_Score'].std():.3f} |
| 35 and Above | {len(above_35)} | {above_35['V3_Score'].mean():.2f} | {above_35['V3_Score'].std():.2f} | {above_35['Weighted_V3_Score'].mean():.3f} | {above_35['Weighted_V3_Score'].std():.3f} |

---

### Hypothesis Testing (Welch's T-Test)
*We use Welch's T-Test (assuming unequal variances) for robust results.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **T-Statistic:** {t_stat_wv3:.3f}
* **P-Value:** {p_val_wv3:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on age.' if p_val_wv3 < 0.05 else '**Not Statistically Significant (p > 0.05).** There is no significant difference in knowledge based on this age split.'}

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **T-Statistic:** {t_stat_v3:.3f}
* **P-Value:** {p_val_v3:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).**' if p_val_v3 < 0.05 else '**Not Statistically Significant (p > 0.05).**'}

---

### Visualizations

#### Weighted V3 Score Violin Plot
![Violin Plot]({charts_dir}/Knowledge_Age_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot]({charts_dir}/Knowledge_Age_Box.png)
"""

md_path = os.path.join(out_dir_md, 'Knowledge_Age_TTest_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Knowledge_Age_TTest_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("T-Tests completed and report generated successfully.")
