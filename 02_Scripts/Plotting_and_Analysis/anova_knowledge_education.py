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

edu_col = [c for c in df_raw.columns if '7. Education Level' in c][0]

df = pd.DataFrame({
    'Education_Level': df_raw[edu_col].str.strip(),
    'V3_Score': df_v3['V3_Knowledge_Score'],
    'Weighted_V3_Score': df_w_v3['Weighted_V3_Knowledge_Score']
})

df = df.dropna(subset=['Education_Level'])

# Define logical order for education levels
edu_order = ['Up to O/L', 'Up to A/L', 'Undergraduate', 'Graduate']
df['Education_Level'] = pd.Categorical(df['Education_Level'], categories=edu_order, ordered=True)

# Group data for ANOVA
groups_v3 = [df[df['Education_Level'] == level]['V3_Score'].values for level in edu_order if len(df[df['Education_Level'] == level]) > 0]
groups_wv3 = [df[df['Education_Level'] == level]['Weighted_V3_Score'].values for level in edu_order if len(df[df['Education_Level'] == level]) > 0]

# Perform One-Way ANOVA
f_stat_v3, p_val_v3 = stats.f_oneway(*groups_v3)
f_stat_wv3, p_val_wv3 = stats.f_oneway(*groups_wv3)

# Descriptive stats
desc_stats = df.groupby('Education_Level').agg(
    N=('Weighted_V3_Score', 'count'),
    Mean_V3=('V3_Score', 'mean'),
    Std_V3=('V3_Score', 'std'),
    Mean_WV3=('Weighted_V3_Score', 'mean'),
    Std_WV3=('Weighted_V3_Score', 'std')
).reset_index()

# Visualize
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

plt.figure(figsize=(10, 6))
sns.violinplot(x='Education_Level', y='Weighted_V3_Score', data=df, inner='quartile', palette='Set2')
plt.title(f'Weighted V3 Knowledge Score by Education Level\nOne-Way ANOVA p-value: {p_val_wv3:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Education Level')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Education_Violin.png'))
plt.close()

plt.figure(figsize=(8, 6))
sns.boxplot(x='Education_Level', y='V3_Score', data=df, palette='Set3')
plt.title(f'V3 Knowledge Score by Education Level\nOne-Way ANOVA p-value: {p_val_v3:.4f}', fontsize=14)
plt.ylabel('V3 Knowledge Score')
plt.xlabel('Education Level')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Education_Box.png'))
plt.close()

# Generate Report
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

desc_table_rows = ""
for _, row in desc_stats.iterrows():
    desc_table_rows += f"| {row['Education_Level']} | {row['N']} | {row['Mean_V3']:.2f} | {row['Std_V3']:.2f} | {row['Mean_WV3']:.3f} | {row['Std_WV3']:.3f} |\n"

report = f"""# Inferential Statistics: Knowledge Score vs. Education Level
**One-Way ANOVA (Analysis of Variance)**

This report examines whether there is a statistically significant difference in clinical knowledge across four different educational attainment levels among thalassemia carriers.

### Descriptive Statistics

| Education Level | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
{desc_table_rows}
---

### Hypothesis Testing (One-Way ANOVA)
*We use an Analysis of Variance (ANOVA) to determine if the means of the four independent groups are significantly different from each other.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **F-Statistic:** {f_stat_wv3:.3f}
* **P-Value:** {p_val_wv3:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on education level.' if p_val_wv3 < 0.05 else '**Not Statistically Significant (p > 0.05).** Education level does not significantly impact knowledge in this cohort.'}

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **F-Statistic:** {f_stat_v3:.3f}
* **P-Value:** {p_val_v3:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).**' if p_val_v3 < 0.05 else '**Not Statistically Significant (p > 0.05).**'}

---

### Visualizations

#### Weighted V3 Score Violin Plot
The violin plot demonstrates the distribution density for each educational group.
![Violin Plot]({charts_dir}/Knowledge_Education_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot]({charts_dir}/Knowledge_Education_Box.png)
"""

md_path = os.path.join(out_dir_md, 'Knowledge_Education_ANOVA_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Knowledge_Education_ANOVA_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("ANOVA completed and report generated successfully.")
