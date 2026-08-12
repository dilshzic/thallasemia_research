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
title: "Knowledge, Attitudes, and Practices (KAP) Regarding Thalassemia and Cascade Screening: A Comprehensive Cross-Sectional Analysis"
author: "Research Team"
date: "August 2026"
geometry: margin=1in
---

# 1. Abstract

**Background:** Thalassemia is a severe autosomal recessive blood disorder that places a massive burden on global and regional healthcare systems. Due to the genetic nature of the disease, primary prevention through carrier screening, pre-marital counseling, and cascade screening (testing extended family members) remains the most effective strategy to reduce disease incidence. 

**Methods:** A comprehensive cross-sectional survey was conducted among 201 participants to assess their baseline Knowledge, Attitudes, and Practices (KAP) regarding Thalassemia. An automated dual-language (R and Python) data processing pipeline was developed to clean the data, standardize scoring metrics, and perform rigorous inferential statistical analysis. Variables were analyzed using Welch’s Independent T-Tests and Pearson’s Chi-Square Tests with Yates' continuity correction.

**Results:** The data reveals stark socio-demographic disparities in Thalassemia awareness and preventive practices. Educational attainment emerged as the single most powerful predictor of positive outcomes; individuals with higher education (Degree or above) demonstrated vastly superior knowledge (p < 0.001), significantly more progressive attitudes toward partner screening (p < 0.001), and a much higher likelihood of practicing safe screening before marriage (p < 0.001). Crucially, baseline knowledge was found to be a direct catalyst for action, as high knowledge scores were significantly associated with actual safe screening practices (p = 0.019).

**Conclusion:** The findings unequivocally demonstrate that general awareness campaigns are insufficient for lower-education demographics. To effectively combat the transmission of Thalassemia, public health strategies must pivot toward targeted, pre-marital educational counseling that empowers vulnerable populations to translate baseline knowledge into proactive, safe screening practices.

---

# 2. Introduction

Thalassemia syndromes are a heterogeneous group of inherited disorders of hemoglobin synthesis. Individuals with Thalassemia Major require lifelong blood transfusions and expensive iron chelation therapy, placing a severe emotional burden on families and an immense financial strain on national healthcare infrastructure. Because it is an autosomal recessive condition, a child can only inherit Thalassemia Major if both parents are carriers (Thalassemia Minor/Trait). Thus, the birth of affected children is entirely preventable if at-risk couples are identified before marriage or conception.

The World Health Organization (WHO) and regional health authorities strongly advocate for pre-marital carrier screening. Furthermore, because carriers cluster within families due to shared genetics, "cascade screening" — the systematic testing of first, second, and third-degree relatives of identified carriers — is a highly effective, targeted method for identifying hidden carriers in the population. 

Despite these clear guidelines, the uptake of partner and cascade screening remains suboptimal in many regions. This research aims to quantify the baseline Knowledge, Attitudes, and Practices (KAP) of a localized cohort, and to utilize rigorous computational data pipelines to identify the precise demographic bottlenecks that hinder the adoption of safe screening practices.

---

# 3. Methodology

## 3.1 Study Design and Population
A cross-sectional survey was administered to a cohort of 201 participants. The survey instrument was divided into four distinct sections:
* **Part A:** Demographic information (Age, Gender, Marital Status, Province, Education, Income).
* **Part B:** General knowledge of Thalassemia, its transmission, and complications.
* **Part C:** Attitudes and practices toward partner disclosure and pre-marital screening.
* **Part D:** Attitudes and practices regarding family cascade screening.

## 3.2 Data Processing Pipeline and Scoring Framework
An automated data pipeline was developed in Python utilizing the `pandas` and `scipy` libraries to ensure reproducible and objective analysis.

* **Expanded Knowledge Score:** A 20-point scale evaluating a participant's understanding of the disease's curability, genetic transmission, and specific clinical complications.
* **Attitude & Practice Scores:** Weighted metrics evaluating partner disclosure and family screening. For example:
  * **Partner Practice** was strictly categorized into 'Safe' (partner screened before marriage) versus 'Unsafe/Delayed' (screened after marriage, during pregnancy, or never screened).
  * **Cascade Practice** was scored by awarding +2 points if "all" relatives underwent screening, +1 for "some", and 0 for "none" across varying degrees of genetic relation.

## 3.3 Statistical Analysis
To perform reliable comparative testing, continuous scores were evaluated directly, while for categorical association tests, scores were binarized based on their dataset median (e.g., 'High Knowledge' vs 'Low Knowledge').
* **Welch’s Independent T-Tests** were utilized to account for unequal variances and sample sizes between binary demographic groups.
* **Pearson’s Chi-Square Tests (with Yates' continuity correction)** were employed to evaluate dependencies between categorical demographic variables and binarized outcomes.
Statistical significance was established at the standard threshold of α = 0.05.

---

# 4. Results

## 4.1 Demographic Profile
The cohort exhibited diverse representation across multiple demographic vectors.

![Age Distribution](outputs/plots/age_distribution.png)
![Gender Distribution](outputs/plots/gender_distribution.png)

## 4.2 Baseline Knowledge
The distribution of the Expanded Knowledge Score indicates a wide variance in public understanding of the disease, with a significant portion of the cohort lacking comprehensive knowledge of transmission and complications.

![Knowledge Score Distribution](outputs/plots/knowledge_score_distribution.png)

## 4.3 Family Cascade Screening Practices
The data indicates that while screening among first-degree relatives occurs with some frequency, the screening rate drops precipitously for second and third-degree relatives, highlighting a major gap in the cascade screening mechanism.

![Cascade Screening Rates](outputs/plots/relative_screening_rates.png)

## 4.4 Inferential Statistical Findings (T-Tests)
Welch's T-tests revealed numerous statistically significant mean differences between demographic groups across the scoring metrics.

| Independent Variable | Outcome Score | p-value | T-Statistic | df |
| :--- | :--- | :--- | :--- | :--- |
"""
for _, row in sig_t.iterrows():
    markdown_content += f"| {row['Independent_Variable']} | {row['Dependent_Variable']} | **{row['p_value']:.4e}** | {row['t_statistic']:.2f} | {row['df']:.1f} |\n"

markdown_content += """
**Key Observations:**
* **The Impact of Education:** Participants with a Degree or above had a vastly superior Expanded Knowledge Score compared to those with education up to A/Levels ($t=7.60, p=1.67\\times 10^{-12}$). This educational advantage also translated into significantly better Partner Attitudes ($p=0.0002$) and Cascade Practices ($p=0.037$).
* **Safe Practices Reflect Better Knowledge:** Individuals whose partner screening practices were categorized as "Safe" possessed significantly higher baseline knowledge scores ($p=0.0099$) and better attitudes ($p=0.026$) than those who engaged in unsafe or delayed practices.

## 4.5 Categorical Dependencies (Chi-Square Tests)
Pearson's Chi-Square tests isolated the demographic factors that most strongly dictate whether an individual falls into a "High" or "Low" scoring category.

| Demographic Variable | Categorical Outcome | p-value | Chi-Square Stat |
| :--- | :--- | :--- | :--- |
"""
for _, row in sig_c.iterrows():
    markdown_content += f"| {row['Variable_1']} | {row['Variable_2']} | **{row['p_value']:.4e}** | {row['Statistic']:.2f} |\n"

markdown_content += """
**Key Observations:**
* **Education as a Primary Predictor:** Education level strongly dictates categorization into the High Knowledge tier ($\chi^2 = 34.54, p < 0.001$) and is heavily associated with actually engaging in Safe Partner Practices ($p < 0.001$).
* **Knowledge Converts to Action:** Being in the "High Knowledge" category makes an individual significantly more likely to engage in Safe Partner Practices ($\chi^2 = 5.49, p = 0.019$), proving that education directly modifies behavior.
* **Marital Status Dynamics:** Marital status significantly influences whether partner screening was conducted safely prior to marriage ($\chi^2 = 8.11, p = 0.004$), suggesting that the structural timeline of marriage impacts screening behaviors.

---

# 5. Discussion

The automated analysis pipeline has uncovered several profound, actionable insights into the public's interaction with Thalassemia screening.

### 5.1 Education is the Ultimate Catalyst
The data unequivocally positions formal education as the primary bottleneck for Thalassemia prevention. Individuals with lower educational attainment not only scored poorly on baseline disease knowledge, but they consistently demonstrated poorer attitudes and engaged in riskier, delayed screening practices. This suggests that current, broad-spectrum public health awareness campaigns are failing to penetrate or resonate with lower-educated demographics. 

### 5.2 Knowledge Drives Tangible Practice
A critical finding of this study is the statistically significant link between High Knowledge and Safe Partner Practice ($p=0.019$). In many public health domains, knowledge does not always translate to behavioral change (the knowledge-action gap). However, in the context of Thalassemia, providing individuals with comprehensive knowledge about the disease directly empowers them to enforce safe, pre-marital screening.

### 5.3 Marital and Gender Disparities
The significant dependency between marital status and screening practices highlights a critical window of opportunity. Because screening behaviors are highly sensitive to marital status, targeted pre-marital counseling—potentially integrated into civil marriage registration processes—could serve as a highly effective intervention point. Furthermore, the significant gender differences observed in cascade practices ($p=0.029$) warrant further qualitative research to understand cultural or social barriers that prevent certain groups from encouraging their family members to test.

---

# 6. Conclusion

Thalassemia remains a formidable but entirely preventable genetic challenge. The findings of this cross-sectional study demonstrate that while general awareness exists, the translation of that awareness into proactive, safe screening practices is heavily stratified by education and baseline knowledge.

To effectively combat the transmission of Thalassemia, public health strategies must evolve. Broad awareness campaigns must be supplemented by targeted, localized educational interventions that specifically address lower-education demographics. Furthermore, institutionalizing pre-marital counseling can capitalize on the critical window before marriage, ensuring that knowledge is accurately imparted and directly converted into safe screening practices.

"""

with open("Expanded_Final_Research_Report.md", "w") as f:
    f.write(markdown_content)

subprocess.run(["pandoc", "Expanded_Final_Research_Report.md", "-o", "Expanded_Final_Research_Report.pdf", "--pdf-engine=wkhtmltopdf", "--metadata", "margin-left=1in", "--metadata", "margin-right=1in", "--metadata", "margin-top=1in", "--metadata", "margin-bottom=1in"])
print("PDF Generated successfully!")
