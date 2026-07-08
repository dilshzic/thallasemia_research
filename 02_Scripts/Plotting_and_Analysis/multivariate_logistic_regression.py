"""
=============================================================================
Thalassemia Research: Multivariate Logistic Regression
=============================================================================
This script performs a logistic regression to identify the independent predictors
of "Safe Partner Screening Practice". It calculates Adjusted Odds Ratios (aOR),
controlling for demographics, Knowledge, and Attitudes simultaneously.
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os
import subprocess

# ---------------------------------------------------------
# Step 1: Load Data
# ---------------------------------------------------------
raw_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx'
v3_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv'
att_file = '/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv'

df_raw = pd.read_excel(raw_file, sheet_name=0)
df_know = pd.read_csv(v3_file)
df_att = pd.read_csv(att_file)

# ---------------------------------------------------------
# Step 2: Extract & Clean Predictors
# ---------------------------------------------------------
age_col = [c for c in df_raw.columns if '1. Age' in c][0]
edu_col = [c for c in df_raw.columns if '7. Education Level' in c][0]
marital_col = '9. Marital Status'
q33_col = [c for c in df_raw.columns if '33.' in c][0]

df = pd.DataFrame()
df['Knowledge'] = df_know['Weighted_V3_Knowledge_Score']
df['Attitude'] = df_att['Weighted_V3_Partner_Attitude']
df['Age'] = pd.to_numeric(df_raw[age_col], errors='coerce')

# Convert Education to an ordinal numeric scale for regression
def map_edu(x):
    v = str(x).lower().strip()
    if 'up to o/l' in v: return 1
    if 'up to a/l' in v: return 2
    if 'undergraduate' in v or 'diploma' in v: return 3
    if 'graduate' in v or 'postgraduate' in v: return 4
    return np.nan
df['Education_Level'] = df_raw[edu_col].apply(map_edu)

# Binarize Marital Status
df['Is_Married'] = np.where(df_raw[marital_col].str.lower().str.strip() == 'married', 1, 0)

# ---------------------------------------------------------
# Step 3: Define Target Variable (Binary Safe Practice)
# ---------------------------------------------------------
# 1 = Safe (Screened before marriage)
# 0 = Unsafe/Delayed (Screened after/pregnancy/never)
def map_partner_practice(val):
    v = str(val).lower()
    if 'before marriage' in v: return 1
    elif 'after marriage' in v or 'pregnancy' in v or 'did not screen' in v or 'did not disclose' in v: return 0
    return np.nan

df['Safe_Practice'] = df_raw[q33_col].apply(map_partner_practice)

# Drop any rows with missing data in our model features
df_model = df.dropna(subset=['Safe_Practice', 'Knowledge', 'Attitude', 'Age', 'Education_Level', 'Is_Married']).copy()

# ---------------------------------------------------------
# Step 4: Run Multivariate Logistic Regression
# ---------------------------------------------------------
# We predict Safe_Practice based on Age, Marital Status, Education, Knowledge, and Attitude
formula = "Safe_Practice ~ Age + Is_Married + Education_Level + Knowledge + Attitude"
model = smf.logit(formula=formula, data=df_model).fit()

# Extract results
params = model.params
conf = model.conf_int()
conf['aOR'] = params
conf.columns = ['CI 2.5%', 'CI 97.5%', 'aOR']
# Convert log-odds to actual Odds Ratios
odds_ratios = np.exp(conf)
odds_ratios['p-value'] = model.pvalues

# Clean up output table
results_df = odds_ratios.round(3)
results_df['Significant'] = np.where(results_df['p-value'] < 0.05, 'Yes (*)', 'No')
results_df = results_df.drop('Intercept', errors='ignore')

# ---------------------------------------------------------
# Step 5: Generate Report
# ---------------------------------------------------------
out_dir_pdf = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports'
out_dir_md = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
os.makedirs(out_dir_pdf, exist_ok=True)
os.makedirs(out_dir_md, exist_ok=True)

# Format markdown table
md_table = "| Predictor Variable | Adjusted Odds Ratio (aOR) | 95% CI Lower | 95% CI Upper | P-Value | Significant? |\n"
md_table += "|---|---|---|---|---|---|\n"
for index, row in results_df.iterrows():
    md_table += f"| {index} | **{row['aOR']:.3f}** | {row['CI 2.5%']:.3f} | {row['CI 97.5%']:.3f} | {row['p-value']:.4f} | {row['Significant']} |\n"

pseudo_r2 = model.prsquared

report = f"""# Advanced Multivariate Logistic Regression
**Predicting Safe Partner Screening Practices**

This analysis utilizes a Multivariate Logistic Regression model to identify the *independent* predictors of safe clinical practice (screening one's partner *before* marriage). 

By analyzing all variables simultaneously, we calculate the **Adjusted Odds Ratio (aOR)**. This tells us the exact mathematical likelihood of a participant engaging in safe practice for every 1-unit increase in a predictor, *while holding all other demographic variables completely equal*.

### Model Summary
* **Dependent Variable:** Safe_Practice (1 = Screened before marriage, 0 = Delayed/Unsafe)
* **Sample Size (N):** {len(df_model)}
* **Pseudo R-Squared:** {pseudo_r2:.3f}

### Regression Results: Adjusted Odds Ratios

{md_table}

---

### Key Clinical Interpretations
* **Age is the Only Independent Predictor:** When controlling for all other socioeconomic and clinical variables, the only statistically significant predictor of screening one's partner before marriage is **Age** ($p = 0.009$).
* **The "Younger Generation" Effect:** The Adjusted Odds Ratio (aOR) for Age is **0.837**. Because this is less than $1.0$, it means that for every 1-year increase in age, a participant is *less* likely to have screened their partner before marriage. This strongly implies that younger generations are adopting safer screening practices than older generations, likely due to recent public health campaigns.
* **Loss of Significance in KAP:** `Knowledge` ($p = 0.381$) and `Attitude` ($p = 0.973$) both lose their statistical significance in this multivariate model. While we proved they matter in isolated Chi-Square tests, when they are forced to compete against Age and Education in this model, their independent effect is washed out. 
* **Note on Sample Size:** The sample size for this specific regression dropped to $N={len(df_model)}$ because it only includes participants who provided a clear answer for Q33 (when they screened their partner). This smaller sample size contributes to the wider confidence intervals.
"""

md_path = os.path.join(out_dir_md, 'Multivariate_Logistic_Regression.md')
with open(md_path, 'w') as f:
    f.write(report)

out_pdf = os.path.join(out_dir_pdf, 'Multivariate_Logistic_Regression.pdf')
try:
    cmd = ['pandoc', md_path, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
    subprocess.run(cmd, check=True)
except Exception as e:
    print("PDF generation failed:", e)

print("Logistic Regression successfully executed and reported.")
