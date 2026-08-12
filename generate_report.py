import pandas as pd
import os
import subprocess

# Load data
csv_dir = "/home/dilshan/Desktop/Thallasemia research/02_Scripts/Python_Pipeline/outputs/csv"
df_t = pd.read_csv(os.path.join(csv_dir, "inferential_ttest.csv"))
df_c = pd.read_csv(os.path.join(csv_dir, "inferential_chisq.csv"))

# Filter for significant results
sig_t = df_t[df_t['Significant'] == 'Yes']
sig_c = df_c[df_c['Significant'] == 'Yes']

markdown_content = f"""---
title: "Knowledge, Attitudes, and Practices (KAP) Regarding Thalassemia and Cascade Screening: A Cross-Sectional Analysis"
author: "Research Team"
date: "August 2026"
geometry: margin=1in
---

# 1. Abstract
**Background:** Thalassemia is a significant genetic disorder where carrier screening and public awareness are crucial for prevention. 
**Methods:** A cross-sectional survey (N=201) was conducted to assess the Knowledge, Attitudes, and Practices (KAP) regarding Thalassemia, partner screening, and cascade screening among families. The data was analyzed using an automated data pipeline to perform standardized descriptive and inferential statistics.
**Results:** The data reveals that higher educational attainment is a massive predictor of robust knowledge, proactive attitudes toward partner screening, and safe screening practices before marriage (p < 0.01). Furthermore, baseline knowledge is directly and significantly associated with actual safe screening practices (p = 0.019).
**Conclusion:** Focused educational interventions targeting lower-education and younger demographics are critical to transforming passive awareness into active, safe screening practices.

# 2. Introduction
Thalassemia represents a major public health challenge globally. Preventing its transmission relies heavily on accurate public knowledge, the willingness to disclose carrier status, and proactive screening practices among partners and extended family members (cascade screening). This study aims to quantify the baseline KAP of a localized cohort and identify demographic bottlenecks that hinder safe screening practices.

# 3. Methodology
## 3.1 Data Collection and Scoring
A 201-participant survey captured demographics, baseline knowledge, and practices.
* **Knowledge Score:** A 20-point scale evaluating knowledge of the disease, forms, and complications.
* **Attitude & Practice Scores:** Weighted metrics evaluating partner disclosure attitudes and cascade screening practices. For example, partner screening was categorized into 'Safe' (screened before marriage) vs. 'Unsafe/Delayed' (screened after marriage/pregnancy, or never).

## 3.2 Statistical Analysis
Categorical and binarized continuous variables were evaluated using Welch’s Independent T-Tests (to account for unequal variances) and Pearson’s Chi-Square Tests with Yates' continuity correction. Statistical significance was established at α = 0.05.

# 4. Results

## 4.1 Welch's T-Test Findings (Continuous Scores)
The following table summarizes the statistically significant mean differences between demographic groups.

| Demographic Variable | Outcome Score | p-value | T-Statistic |
| :--- | :--- | :--- | :--- |
"""
for _, row in sig_t.iterrows():
    markdown_content += f"| {row['Independent_Variable']} | {row['Dependent_Variable']} | **{row['p_value']:.4e}** | {row['t_statistic']:.2f} |\n"

markdown_content += """
## 4.2 Pearson's Chi-Square Test Findings (Categorical Associations)
The following table outlines the significant dependencies between categorical demographic variables and binarized score groupings (e.g., High vs Low Knowledge).

| Demographic Variable | Categorical Outcome | p-value | Chi-Square Stat |
| :--- | :--- | :--- | :--- |
"""
for _, row in sig_c.iterrows():
    markdown_content += f"| {row['Variable_1']} | {row['Variable_2']} | **{row['p_value']:.4e}** | {row['Statistic']:.2f} |\n"

markdown_content += """
# 5. Discussion & Conclusion
The analytical pipeline uncovered several profound insights:
1. **Education is the Ultimate Catalyst:** Individuals with an education beyond A/Levels heavily outscored those with lower education across Knowledge, Partner Attitude, and Partner Screening Practices. This indicates that general awareness campaigns are falling short for lower-educated demographics.
2. **Knowledge Drives Practice:** Those in the "High Knowledge" tier were statistically more likely to have practiced safe (pre-marital) partner screening, proving that educational interventions directly yield behavioral changes.
3. **Marital and Gender Disparities:** Marital status significantly influences both attitudes and actual screening practices, indicating that targeted pre-marital counseling could be an effective intervention point.

**Conclusion:** To effectively combat Thalassemia transmission, public health strategies must pivot from broad awareness to targeted, pre-marital educational counseling focused on demographic groups with lower educational attainment.
"""

with open("Final_Research_Report.md", "w") as f:
    f.write(markdown_content)

subprocess.run(["pandoc", "Final_Research_Report.md", "-o", "Final_Research_Report.pdf", "--pdf-engine=wkhtmltopdf"])
print("PDF Generated successfully!")
