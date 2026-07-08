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

# The datasets should align by index assuming no rows were dropped
gender_col = [c for c in df_raw.columns if 'gender' in str(c).lower()][0]

df = pd.DataFrame({
    'Gender': df_raw[gender_col].str.strip().str.title(),
    'V3_Score': df_v3['V3_Knowledge_Score'],
    'Weighted_V3_Score': df_w_v3['Weighted_V3_Knowledge_Score']
})

# Filter out any missing gender
df = df.dropna(subset=['Gender'])

males = df[df['Gender'] == 'Male']
females = df[df['Gender'] == 'Female']

# T-Test for V3 Score
t_stat_v3, p_val_v3 = stats.ttest_ind(males['V3_Score'], females['V3_Score'], equal_var=False)

# T-Test for Weighted V3 Score
t_stat_wv3, p_val_wv3 = stats.ttest_ind(males['Weighted_V3_Score'], females['Weighted_V3_Score'], equal_var=False)

# Visualize
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

plt.figure(figsize=(10, 6))
sns.violinplot(x='Gender', y='Weighted_V3_Score', data=df, palette='muted', inner='quartile')
plt.title(f'Weighted V3 Knowledge Score by Gender\nT-Test p-value: {p_val_wv3:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Gender')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Gender_Violin.png'))
plt.close()

plt.figure(figsize=(8, 6))
sns.boxplot(x='Gender', y='V3_Score', data=df, palette='pastel')
plt.title(f'V3 Knowledge Score by Gender\nT-Test p-value: {p_val_v3:.4f}', fontsize=14)
plt.ylabel('V3 Knowledge Score')
plt.xlabel('Gender')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Gender_Box.png'))
plt.close()

# Generate Report
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

report = f"""# Inferential Statistics: Knowledge Score vs. Gender
**Independent Two-Sample T-Test**

This report examines whether there is a statistically significant difference in clinical knowledge between Male and Female thalassemia carriers.

### Descriptive Statistics

| Gender | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Male | {len(males)} | {males['V3_Score'].mean():.2f} | {males['V3_Score'].std():.2f} | {males['Weighted_V3_Score'].mean():.3f} | {males['Weighted_V3_Score'].std():.3f} |
| Female | {len(females)} | {females['V3_Score'].mean():.2f} | {females['V3_Score'].std():.2f} | {females['Weighted_V3_Score'].mean():.3f} | {females['Weighted_V3_Score'].std():.3f} |

---

### Hypothesis Testing (Welch's T-Test)
*We use Welch's T-Test (assuming unequal variances) for robust results.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **T-Statistic:** {t_stat_wv3:.3f}
* **P-Value:** {p_val_wv3:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge between genders.' if p_val_wv3 < 0.05 else '**Not Statistically Significant (p > 0.05).** There is no significant difference in knowledge between male and female carriers.'}

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **T-Statistic:** {t_stat_v3:.3f}
* **P-Value:** {p_val_v3:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).**' if p_val_v3 < 0.05 else '**Not Statistically Significant (p > 0.05).**'}

---

### Visualizations

#### Weighted V3 Score Violin Plot
The violin plot demonstrates the distribution density and quartiles for both genders using the rigorously weighted metric.
![Violin Plot]({charts_dir}/Knowledge_Gender_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot]({charts_dir}/Knowledge_Gender_Box.png)
"""

md_path = os.path.join(out_dir_md, 'Knowledge_Gender_TTest_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Knowledge_Gender_TTest_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("T-Tests completed and report generated successfully.")
