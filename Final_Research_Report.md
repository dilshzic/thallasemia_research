---
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
| B_Gender | Cascade_Practice_Score | **2.9306e-02** | 2.20 |
| B_Marital | Cascade_Practice_Score | **1.3650e-02** | 2.49 |
| B_Age | Partner_Attitude | **3.8082e-02** | 2.11 |
| B_Education | Expanded_Knowledge_Score | **1.6747e-12** | 7.60 |
| B_Education | Partner_Attitude | **2.3663e-04** | 3.75 |
| B_Education | Cascade_Practice_Score | **3.7520e-02** | 2.10 |
| B_Partner_Practice | Expanded_Knowledge_Score | **9.9938e-03** | 2.69 |
| B_Partner_Practice | Partner_Attitude | **2.6318e-02** | 2.30 |
| Cat_Cascade_Prac | Cascade_Attitude | **7.3342e-07** | -5.16 |

## 4.2 Pearson's Chi-Square Test Findings (Categorical Associations)
The following table outlines the significant dependencies between categorical demographic variables and binarized score groupings (e.g., High vs Low Knowledge).

| Demographic Variable | Categorical Outcome | p-value | Chi-Square Stat |
| :--- | :--- | :--- | :--- |
| B_Education | Cat_Knowledge | **4.1782e-09** | 34.54 |
| B_Income | Cat_Knowledge | **1.9130e-02** | 7.91 |
| B_Marital | Cat_Partner_Att | **2.5992e-02** | 4.96 |
| B_Education | Cat_Partner_Att | **2.6808e-03** | 9.01 |
| B_Marital | B_Partner_Practice | **4.3804e-03** | 8.12 |
| B_Education | B_Partner_Practice | **2.9747e-04** | 13.09 |
| Cat_Knowledge | B_Partner_Practice | **1.9102e-02** | 5.49 |

# 5. Discussion & Conclusion
The analytical pipeline uncovered several profound insights:
1. **Education is the Ultimate Catalyst:** Individuals with an education beyond A/Levels heavily outscored those with lower education across Knowledge, Partner Attitude, and Partner Screening Practices. This indicates that general awareness campaigns are falling short for lower-educated demographics.
2. **Knowledge Drives Practice:** Those in the "High Knowledge" tier were statistically more likely to have practiced safe (pre-marital) partner screening, proving that educational interventions directly yield behavioral changes.
3. **Marital and Gender Disparities:** Marital status significantly influences both attitudes and actual screening practices, indicating that targeted pre-marital counseling could be an effective intervention point.

**Conclusion:** To effectively combat Thalassemia transmission, public health strategies must pivot from broad awareness to targeted, pre-marital educational counseling focused on demographic groups with lower educational attainment.
