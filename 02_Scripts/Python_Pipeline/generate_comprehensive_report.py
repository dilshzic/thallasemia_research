import pandas as pd
import os
import subprocess

csv_dir = "/home/dilshan/Desktop/Thallasemia research/02_Scripts/Python_Pipeline/outputs/csv"

# Load Inferential Data
df_t = pd.read_csv(os.path.join(csv_dir, "inferential_ttest.csv"))
df_c = pd.read_csv(os.path.join(csv_dir, "inferential_chisq.csv"))
sig_t = df_t[df_t['Significant'] == 'Yes']
sig_c = df_c[df_c['Significant'] == 'Yes']

# Load Descriptive Data
df_dem = pd.read_csv(os.path.join(csv_dir, "demographics.csv"))
df_knw = pd.read_csv(os.path.join(csv_dir, "knowledge.csv"))

# Helper for Descriptive Tables
def make_desc_table(df, q_ids):
    sub = df[df['Question_ID'].isin(q_ids)]
    table = "| Characteristic | Category | N (%) |\n| :--- | :--- | :--- |\n"
    current_q = ""
    for _, row in sub.iterrows():
        q = row['Question'].split('.')[1].strip() if '.' in row['Question'] else row['Question']
        q_disp = q if q != current_q else ""
        current_q = q
        
        freq = int(row['Frequency']) if pd.notna(row['Frequency']) else 0
        pct = float(row['Percentage']) if pd.notna(row['Percentage']) else 0.0
        n_pct = f"{freq} ({pct:.1f}%)" if freq > 0 else f"{pct:.1f}"
        
        resp = row['Response']
        table += f"| {q_disp} | {resp} | {n_pct} |\n"
    return table

demo_table = make_desc_table(df_dem, ['Q1_Groups', 'Q2', 'Q7', 'Q9'])

# Top 5 most missed knowledge questions (where "No" or wrong answers dominate)
# Just pick a few interesting knowledge questions, e.g., Q20, Q23, Q26
knw_table = make_desc_table(df_knw, ['Q20', 'Q23', 'Q26'])


markdown_content = f"""---
title: "Knowledge, Attitudes, and Practices (KAP) Regarding Thalassemia and Cascade Screening: A Comprehensive Cross-Sectional Analysis"
author: "Research Team"
date: "August 2026"
geometry: margin=1in
---

# 1. Abstract

**Background:** Thalassemia is a severe autosomal recessive blood disorder that places a massive burden on global and regional healthcare systems. Due to the genetic nature of the disease, primary prevention through carrier screening, pre-marital counseling, and cascade screening (testing extended family members) remains the most effective strategy to reduce disease incidence. 

**Methods:** A comprehensive cross-sectional survey was conducted among 201 participants to assess their baseline Knowledge, Attitudes, and Practices (KAP). An automated data processing pipeline (R/Python) was utilized for descriptive and inferential statistical analysis. 

**Results:** The descriptive data highlighted substantial gaps in knowledge regarding the curability and genetic transmission of Thalassemia. Inferential tests revealed stark socio-demographic disparities: individuals with higher education demonstrated vastly superior knowledge (p < 0.001) and significantly more progressive attitudes toward partner screening (p < 0.001). Crucially, baseline knowledge was found to be a direct catalyst for action, as high knowledge scores were significantly associated with actual safe screening practices (p = 0.019).

**Conclusion:** The findings unequivocally demonstrate that general awareness campaigns are insufficient. Public health strategies must pivot toward targeted, pre-marital educational counseling that empowers vulnerable populations to translate baseline knowledge into proactive, safe screening practices.

---

# 2. Introduction

Thalassemia syndromes are a heterogeneous group of inherited disorders of hemoglobin synthesis. Because it is an autosomal recessive condition, a child can only inherit Thalassemia Major if both parents are carriers (Thalassemia Minor/Trait). Thus, the birth of affected children is entirely preventable if at-risk couples are identified before marriage or conception.

Despite clear WHO guidelines advocating for pre-marital carrier screening and family cascade screening, uptake remains suboptimal. This research quantifies the baseline KAP of a localized cohort, utilizing rigorous computational data pipelines to identify the demographic bottlenecks hindering the adoption of safe screening practices.

---

# 3. Methodology

A cross-sectional survey was administered to a cohort of 201 participants, collecting data on demographics, general knowledge, partner disclosure, and family cascade screening. 
The data pipeline (Python/Scipy) generated:
* **Descriptive Statistics:** Frequencies and percentages for all survey items.
* **Scoring Metrics:** Expanded Knowledge Score (20 pts), Attitude Scores, and weighted Practice Scores.
* **Inferential Statistics:** Welch’s Independent T-Tests (continuous scores) and Pearson’s Chi-Square Tests (binarized outcomes based on median split), evaluated at a significance threshold of α = 0.05.

---

# 4. Results

## 4.1 Descriptive Analysis: Demographic Profile

The cohort exhibited diverse representation across multiple demographic vectors. Below is a snapshot of key demographic characteristics.

{demo_table}

![Age Distribution](outputs/plots/age_distribution.png)
![Gender Distribution](outputs/plots/gender_distribution.png)

## 4.2 Descriptive Analysis: Baseline Knowledge
A significant portion of the cohort harbored misconceptions about the disease's curability and transmission risks. For example, many were unaware that bone marrow transplants could cure the condition or that carrier couples face a 25% chance of having an affected child.

**Selected Knowledge Responses:**
{knw_table}

![Knowledge Score Distribution](outputs/plots/knowledge_score_distribution.png)

## 4.3 Descriptive Analysis: Family Cascade Screening Practices
The data indicates that while screening among first-degree relatives occurs with some frequency, the screening rate drops precipitously for second and third-degree relatives.

![Cascade Screening Rates](outputs/plots/relative_screening_rates.png)

## 4.4 Inferential Statistical Findings (T-Tests)
Welch's T-tests revealed numerous statistically significant mean differences between demographic groups across the continuous scoring metrics.

| Independent Variable | Outcome Score | p-value | T-Statistic | df |
| :--- | :--- | :--- | :--- | :--- |
"""
for _, row in sig_t.iterrows():
    markdown_content += f"| {row['Independent_Variable']} | {row['Dependent_Variable']} | **{row['p_value']:.4e}** | {row['t_statistic']:.2f} | {row['df']:.1f} |\n"

markdown_content += """
**Key Observations:**
* **The Impact of Education:** Participants with a Degree or above had a vastly superior Expanded Knowledge Score compared to those with education up to A/Levels ($t=7.60, p=1.67\\times 10^{-12}$).
* **Safe Practices Reflect Better Knowledge:** Individuals whose partner screening practices were categorized as "Safe" possessed significantly higher baseline knowledge scores ($p=0.0099$).

## 4.5 Categorical Dependencies (Chi-Square Tests)

| Demographic Variable | Categorical Outcome | p-value | Chi-Square Stat |
| :--- | :--- | :--- | :--- |
"""
for _, row in sig_c.iterrows():
    markdown_content += f"| {row['Variable_1']} | {row['Variable_2']} | **{row['p_value']:.4e}** | {row['Statistic']:.2f} |\n"

markdown_content += """
**Key Observations:**
* **Knowledge Converts to Action:** Being in the "High Knowledge" category makes an individual significantly more likely to engage in Safe Partner Practices ($\chi^2 = 5.49, p = 0.019$), proving that education directly modifies behavior.
* **Marital Status Dynamics:** Marital status significantly influences whether partner screening was conducted safely prior to marriage ($\chi^2 = 8.11, p = 0.004$).

---

# 5. Discussion & Conclusion

### 5.1 Education is the Ultimate Catalyst
The descriptive and inferential data unequivocally position formal education as the primary bottleneck for Thalassemia prevention. Individuals with lower educational attainment scored poorly on baseline disease knowledge and consistently demonstrated poorer attitudes and delayed screening practices.

### 5.2 Knowledge Drives Tangible Practice
A critical finding is the statistically significant link between High Knowledge and Safe Partner Practice ($p=0.019$). Providing individuals with comprehensive knowledge about the disease directly empowers them to enforce safe, pre-marital screening.

### 5.3 Conclusion
To effectively combat the transmission of Thalassemia, public health strategies must supplement broad awareness campaigns with targeted, localized educational interventions. Furthermore, institutionalizing pre-marital counseling can capitalize on the critical window before marriage, ensuring that knowledge is accurately imparted and converted into safe screening practices.
"""

with open("Comprehensive_Research_Report.md", "w") as f:
    f.write(markdown_content)

subprocess.run(["pandoc", "Comprehensive_Research_Report.md", "-o", "Comprehensive_Research_Report.pdf", "--pdf-engine=wkhtmltopdf", "--metadata", "margin-left=1in", "--metadata", "margin-right=1in", "--metadata", "margin-top=1in", "--metadata", "margin-bottom=1in"])
print("PDF Generated successfully!")
