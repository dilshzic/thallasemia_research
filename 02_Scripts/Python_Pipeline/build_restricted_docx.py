import pandas as pd
import os
import subprocess

csv_dir = "/home/dilshan/Desktop/Thallasemia research/02_Scripts/Python_Pipeline/outputs/csv"
out_dir = "/home/dilshan/Desktop/Thallasemia research"

# Load CSVs
df_t = pd.read_csv(os.path.join(csv_dir, "inferential_ttest.csv"))
df_c = pd.read_csv(os.path.join(csv_dir, "inferential_chisq.csv"))
df_z = pd.read_csv(os.path.join(csv_dir, "inferential_ztest.csv"))
df_r = pd.read_csv(os.path.join(csv_dir, "inferential_regression.csv"))

# We will generate Demographic_Associations_New.md and Score_Association_New.md

# ---------------------------------------------------------
# 1. Demographic Associations
# ---------------------------------------------------------
demo_md = """---
title: "Demographic Associations (Restricted Tests)"
---

# Demographic Associations

This report evaluates how demographic factors (Age, Gender, Marital Status, Education, and Income) relate to Thalassemia knowledge, attitudes, and practices. Following strict methodological requirements, **only** T-Tests, Chi-Square Tests, and Z-Tests were used for these bivariate analyses.

## 1. T-Tests (Continuous Scores across Demographics)
This section evaluates whether the mean continuous scores significantly differ across binary demographic groups.

| Independent Variable | Dependent Variable | t-statistic | p-value | Significant (p<0.05)? |
| :--- | :--- | :--- | :--- | :--- |
"""
for _, row in df_t[df_t['Independent_Variable'].str.startswith('B_')].iterrows():
    # Only demographic independent variables (B_Gender, etc.)
    demo_md += f"| {row['Independent_Variable']} | {row['Dependent_Variable']} | {row['t_statistic']:.3f} | {row['p_value']:.4e} | **{row['Significant']}** |\n"

demo_md += """
## 2. Chi-Square Tests (Categorical Scores vs Demographics)
This section evaluates the independence between demographic categories and binarized categorical outcomes (e.g. High vs Low Knowledge).

| Independent Variable | Dependent Categorical Variable | Chi-Square | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
"""
for _, row in df_c[df_c['Variable_1'].str.startswith('B_')].iterrows():
    demo_md += f"| {row['Variable_1']} | {row['Variable_2']} | {row['Statistic']:.3f} | {row['p_value']:.4e} | **{row['Significant']}** |\n"

demo_md += """
## 3. Z-Tests for Proportions (Safe Partner Screening Practices)
This section uses Z-tests for two proportions to determine if the rate of "Safe" partner screening differs between demographic groups.

| Demographic Variable | Outcome | Z-Statistic | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
"""
for _, row in df_z.iterrows():
    demo_md += f"| {row['Independent_Variable']} | {row['Dependent_Variable']} | {row['Statistic']:.3f} | {row['p_value']:.4e} | **{row['Significant']}** |\n"


# ---------------------------------------------------------
# 2. Score Associations
# ---------------------------------------------------------
score_md = """---
title: "Score Associations (Regression and Cross-KAP)"
---

# Score Associations

This report evaluates the relationships *between* the Knowledge, Attitude, and Practice scores, as well as the overarching predictive power of demographics on Knowledge using Multiple Linear Regression. Following strict methodological guidelines, **only** Regression, Chi-Square, and T-Tests are presented.

## 1. Multiple Linear Regression: Predicting Expanded Knowledge Score
A multiple linear regression model (OLS) was fitted to predict the continuous **Expanded Knowledge Score** using core demographic factors.

| Term / Predictor | Estimate ($\beta$) | Std. Error | t-value | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
for _, row in df_r.iterrows():
    score_md += f"| {row['Term']} | {row['Estimate']:.3f} | {row['Std.Error']:.3f} | {row['t_value']:.3f} | {row['p_value']:.4e} | **{row['Significant']}** |\n"

score_md += """
## 2. Cross-KAP T-Tests (Practices vs Continuous Scores)
This analyzes if having a specific practice (e.g., Safe Partner Screening) implies a significantly different continuous Knowledge or Attitude score.

| Practice Category | Continuous Score Evaluated | t-statistic | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
"""
# Filter T-Tests where Independent_Variable is NOT demographic
cross_t = df_t[~df_t['Independent_Variable'].str.startswith('B_G|B_M|B_A|B_E|B_I|B_P')]
# Actually some demographic variables start with B_, but B_Partner_Practice also starts with B_. Let's filter carefully.
demographics = ["B_Gender", "B_Marital", "B_Age", "B_Province", "B_Education", "B_Income"]
for _, row in df_t[~df_t['Independent_Variable'].isin(demographics)].iterrows():
    score_md += f"| {row['Independent_Variable']} | {row['Dependent_Variable']} | {row['t_statistic']:.3f} | {row['p_value']:.4e} | **{row['Significant']}** |\n"

score_md += """
## 3. Cross-KAP Chi-Square Tests
This evaluates the independence between categorized KAP variables (e.g., High Knowledge vs Good Attitude).

| KAP Categorical Variable 1 | KAP Categorical Variable 2 | Chi-Square | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
"""
for _, row in df_c[~df_c['Variable_1'].isin(demographics)].iterrows():
    score_md += f"| {row['Variable_1']} | {row['Variable_2']} | {row['Statistic']:.3f} | {row['p_value']:.4e} | **{row['Significant']}** |\n"

# Write Markdown files
demo_path = os.path.join(out_dir, "Demographic_Associations.md")
score_path = os.path.join(out_dir, "Score_Association.md")

with open(demo_path, "w") as f:
    f.write(demo_md)
with open(score_path, "w") as f:
    f.write(score_md)

# Run Pandoc
try:
    subprocess.run(["pandoc", demo_path, "-o", os.path.join(out_dir, "Demographic_Associations.docx")], check=True)
    subprocess.run(["pandoc", score_path, "-o", os.path.join(out_dir, "Score_Association.docx")], check=True)
    print("Successfully synthesized new Demographics and Score Association documents using only the restricted statistical tests.")
except subprocess.CalledProcessError as e:
    print(f"Error compiling docs: {e}")
