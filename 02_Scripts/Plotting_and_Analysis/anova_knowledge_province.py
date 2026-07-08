"""
=============================================================================
Thalassemia Research: One-Way ANOVA & Post-Hoc Analysis for Residential Province
=============================================================================

This script performs inferential statistical analysis to determine if geographical
residence (Province) significantly impacts a carrier's clinical knowledge.

Steps Performed:
1. Data Ingestion: Loads raw demographics and processed Weighted V3 Knowledge scores.
2. Data Cleaning: Maps the 9 provinces into 3 robust analytical groups:
   - Western
   - North Western
   - Other (All remaining provinces)
3. One-Way ANOVA: Tests if the group means are statistically equal.
4. Tukey HSD Post-Hoc Test: If the ANOVA is significant (or borderline), we run
   a pairwise comparison to see *exactly which* provinces differ from each other.
5. Report Generation: Exports a formatted Markdown and PDF report with Violin Plots.
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import subprocess

# ---------------------------------------------------------
# Step 1: Data Ingestion
# ---------------------------------------------------------
raw_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
df_raw = pd.read_excel(raw_file, sheet_name=0)

v3_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_V3_Knowledge.csv'
v3_weighted_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'

df_v3 = pd.read_csv(v3_file)
df_w_v3 = pd.read_csv(v3_weighted_file)

# Dynamically find the province column
prov_col = [c for c in df_raw.columns if '8. Residing Province' in c][0]

df = pd.DataFrame({
    'Raw_Province': df_raw[prov_col].str.strip(),
    'V3_Score': df_v3['V3_Knowledge_Score'],
    'Weighted_V3_Score': df_w_v3['Weighted_V3_Knowledge_Score']
})

df = df.dropna(subset=['Raw_Province'])

# ---------------------------------------------------------
# Step 2: Grouping Logic
# We group the smaller provinces into "Other" to maintain statistical power (N count).
# ---------------------------------------------------------
def group_province(p):
    if p.lower() == 'western':
        return 'Western'
    elif p.lower() == 'north western':
        return 'North Western'
    else:
        return 'Other'

df['Province_Group'] = df['Raw_Province'].apply(group_province)

# Ensure logical ordinal ordering for plots and tables
prov_order = ['Western', 'North Western', 'Other']
df['Province_Group'] = pd.Categorical(df['Province_Group'], categories=prov_order, ordered=True)

# ---------------------------------------------------------
# Step 3: Hypothesis Testing (One-Way ANOVA)
# ---------------------------------------------------------
# Extract the numeric arrays for each group
groups_wv3 = [df[df['Province_Group'] == level]['Weighted_V3_Score'].values for level in prov_order if len(df[df['Province_Group'] == level]) > 0]

# Run the F-Test
f_stat, p_val = stats.f_oneway(*groups_wv3)

# Calculate Descriptive Statistics
desc_prov = df.groupby('Province_Group').agg(
    N=('Weighted_V3_Score', 'count'),
    Mean_WV3=('Weighted_V3_Score', 'mean'),
    Std_WV3=('Weighted_V3_Score', 'std')
).reset_index()

# ---------------------------------------------------------
# Step 4: Post-Hoc Analysis (Tukey HSD)
# This compares every single pair to find where the exact variance lies.
# ---------------------------------------------------------
tukey = pairwise_tukeyhsd(endog=df['Weighted_V3_Score'], groups=df['Province_Group'], alpha=0.05)
tukey_results = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])

# ---------------------------------------------------------
# Step 5: Visualizations
# ---------------------------------------------------------
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests'
os.makedirs(charts_dir, exist_ok=True)

plt.figure(figsize=(10, 6))
# Using x as hue to silence seaborn deprecation warnings
sns.violinplot(x='Province_Group', y='Weighted_V3_Score', hue='Province_Group', data=df, inner='quartile', palette='Set1', legend=False)
plt.title(f'Weighted V3 Knowledge Score by Province\nOne-Way ANOVA p-value: {p_val:.4f}', fontsize=14)
plt.ylabel('Weighted V3 Knowledge Score')
plt.xlabel('Residing Province')
plt.tight_layout()
plt.savefig(os.path.join(charts_dir, 'Knowledge_Province_Violin.png'))
plt.close()

# ---------------------------------------------------------
# Step 6: Generate Formatted Report
# ---------------------------------------------------------
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'

desc_rows = ""
for _, row in desc_prov.iterrows():
    desc_rows += f"| {row['Province_Group']} | {row['N']} | {row['Mean_WV3']:.3f} | {row['Std_WV3']:.3f} |\n"

tukey_md = "```\n" + tukey_results.to_string(index=False) + "\n```"

report = f"""# Inferential Statistics: Knowledge Score vs. Residential Province
**One-Way ANOVA & Tukey HSD Post-Hoc Analysis**

This detailed report examines whether clinical knowledge differs significantly based on geographical residence, specifically comparing the Western Province, North Western Province, and all other provinces grouped together.

---

### 1. Descriptive Statistics

| Province Group | N | Mean (Weighted V3) | Std Dev |
|---|---|---|---|
{desc_rows}

---

### 2. Hypothesis Testing (One-Way ANOVA)
*The overall test to see if geography matters.*

* **F-Statistic:** {f_stat:.3f}
* **P-Value:** {p_val:.4f}
* **Conclusion:** {'**Statistically Significant (p < 0.05).** Geography does impact knowledge.' if p_val < 0.05 else '**Borderline/Not Statistically Significant (p > 0.05).**'}

---

### 3. Post-Hoc Analysis (Tukey HSD)
*Since the ANOVA p-value ({p_val:.4f}) approaches significance, we run a pairwise Tukey HSD test to identify exactly which provinces differ.*

{tukey_md}

**Tukey Interpretation:**
If the `reject` column is True, those two specific provinces have statistically significantly different knowledge scores. If all are False, the variance between any specific pair is not large enough to declare significance independently.

---

### 4. Visualizations
![Violin Plot]({charts_dir}/Knowledge_Province_Violin.png)
"""

md_path = os.path.join(out_dir_md, 'Detailed_Knowledge_Province_ANOVA_Report.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Detailed_Knowledge_Province_ANOVA_Report.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Detailed ANOVA with Post-Hoc completed. Report generated successfully.")
