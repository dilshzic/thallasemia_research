---
title: "Demographic Associations (Restricted Tests)"
---

# Demographic Associations

This report evaluates how demographic factors (Age, Gender, Marital Status, Education, and Income) relate to Thalassemia knowledge, attitudes, and practices. Following strict methodological requirements, **only** T-Tests, Chi-Square Tests, and Z-Tests were used for these bivariate analyses.

## 1. T-Tests (Continuous Scores across Demographics)
This section evaluates whether the mean continuous scores significantly differ across binary demographic groups.

| Independent Variable | Dependent Variable | t-statistic | p-value | Significant (p<0.05)? |
| :--- | :--- | :--- | :--- | :--- |
| B_Gender | Expanded_Knowledge_Score | 1.204 | 2.3014e-01 | **No** |
| B_Gender | Partner_Attitude | 1.197 | 2.3281e-01 | **No** |
| B_Gender | Cascade_Attitude | 0.550 | 5.8266e-01 | **No** |
| B_Gender | Cascade_Practice_Score | 2.195 | 2.9306e-02 | **Yes** |
| B_Marital | Expanded_Knowledge_Score | 1.816 | 7.1443e-02 | **No** |
| B_Marital | Partner_Attitude | 1.952 | 5.2842e-02 | **No** |
| B_Marital | Cascade_Attitude | 1.425 | 1.5643e-01 | **No** |
| B_Marital | Cascade_Practice_Score | 2.492 | 1.3650e-02 | **Yes** |
| B_Age | Expanded_Knowledge_Score | 0.560 | 5.7707e-01 | **No** |
| B_Age | Partner_Attitude | 2.105 | 3.8082e-02 | **Yes** |
| B_Age | Cascade_Attitude | 1.481 | 1.4272e-01 | **No** |
| B_Age | Cascade_Practice_Score | 1.320 | 1.8978e-01 | **No** |
| B_Province | Expanded_Knowledge_Score | 1.293 | 2.0033e-01 | **No** |
| B_Province | Partner_Attitude | 1.565 | 1.2165e-01 | **No** |
| B_Province | Cascade_Attitude | 0.040 | 9.6841e-01 | **No** |
| B_Province | Cascade_Practice_Score | -0.275 | 7.8422e-01 | **No** |
| B_Education | Expanded_Knowledge_Score | 7.602 | 1.6747e-12 | **Yes** |
| B_Education | Partner_Attitude | 3.749 | 2.3663e-04 | **Yes** |
| B_Education | Cascade_Attitude | 0.340 | 7.3469e-01 | **No** |
| B_Education | Cascade_Practice_Score | 2.101 | 3.7520e-02 | **Yes** |
| B_Partner_Practice | Expanded_Knowledge_Score | 2.689 | 9.9938e-03 | **Yes** |
| B_Partner_Practice | Partner_Attitude | 2.298 | 2.6318e-02 | **Yes** |

## 2. Chi-Square Tests (Categorical Scores vs Demographics)
This section evaluates the independence between demographic categories and binarized categorical outcomes (e.g. High vs Low Knowledge).

| Independent Variable | Dependent Categorical Variable | Chi-Square | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
| B_Gender | Cat_Knowledge | 1.865 | 1.7203e-01 | **No** |
| B_Marital | Cat_Knowledge | 2.079 | 1.4930e-01 | **No** |
| B_Age | Cat_Knowledge | 0.334 | 5.6346e-01 | **No** |
| B_Province | Cat_Knowledge | 1.954 | 1.6216e-01 | **No** |
| B_Education | Cat_Knowledge | 34.539 | 4.1782e-09 | **Yes** |
| B_Income | Cat_Knowledge | 7.913 | 1.9130e-02 | **Yes** |
| B_Gender | Cat_Partner_Att | 0.369 | 5.4375e-01 | **No** |
| B_Marital | Cat_Partner_Att | 4.957 | 2.5992e-02 | **Yes** |
| B_Education | Cat_Partner_Att | 9.013 | 2.6808e-03 | **Yes** |
| B_Gender | B_Partner_Practice | 2.138 | 1.4365e-01 | **No** |
| B_Marital | B_Partner_Practice | 8.119 | 4.3804e-03 | **Yes** |
| B_Education | B_Partner_Practice | 13.086 | 2.9747e-04 | **Yes** |
| B_Income | B_Partner_Practice | 0.363 | 8.3406e-01 | **No** |
| B_Gender | Cat_Cascade_Prac | 3.314 | 6.8683e-02 | **No** |
| B_Education | Cat_Cascade_Prac | 2.636 | 1.0447e-01 | **No** |

## 3. Z-Tests for Proportions (Safe Partner Screening Practices)
This section uses Z-tests for two proportions to determine if the rate of "Safe" partner screening differs between demographic groups.

| Demographic Variable | Outcome | Z-Statistic | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
| B_Gender | B_Partner_Practice | 1.716 | 8.6217e-02 | **No** |
| B_Marital | B_Partner_Practice | -3.169 | 1.5275e-03 | **Yes** |
| B_Education | B_Partner_Practice | 3.889 | 1.0081e-04 | **Yes** |
