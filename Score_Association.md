---
title: "Score Associations (Regression and Cross-KAP)"
---

# Score Associations

This report evaluates the relationships *between* the Knowledge, Attitude, and Practice scores, as well as the overarching predictive power of demographics on Knowledge using Multiple Linear Regression. Following strict methodological guidelines, **only** Regression, Chi-Square, and T-Tests are presented.

## 1. Multiple Linear Regression: Predicting Expanded Knowledge Score
A multiple linear regression model (OLS) was fitted to predict the continuous **Expanded Knowledge Score** using core demographic factors.

| Term / Predictor | Estimate ($eta$) | Std. Error | t-value | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Intercept | 15.198 | 1.130 | 13.448 | 1.0453e-25 | **Yes** |
| C(B_Gender)[T.Male] | -0.507 | 0.683 | -0.743 | 4.5887e-01 | **No** |
| C(B_Marital)[T.Single] | -0.238 | 0.717 | -0.333 | 7.3999e-01 | **No** |
| C(B_Education)[T.Up to A/L] | -3.960 | 0.707 | -5.603 | 1.3628e-07 | **Yes** |
| C(B_Income)[T.Below/Equal Median] | -2.706 | 1.070 | -2.528 | 1.2755e-02 | **Yes** |

## 2. Cross-KAP T-Tests (Practices vs Continuous Scores)
This analyzes if having a specific practice (e.g., Safe Partner Screening) implies a significantly different continuous Knowledge or Attitude score.

| Practice Category | Continuous Score Evaluated | t-statistic | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
| B_Partner_Practice | Expanded_Knowledge_Score | 2.689 | 9.9938e-03 | **Yes** |
| B_Partner_Practice | Partner_Attitude | 2.298 | 2.6318e-02 | **Yes** |
| Cat_Cascade_Prac | Expanded_Knowledge_Score | -1.938 | 5.4110e-02 | **No** |
| Cat_Cascade_Prac | Cascade_Attitude | -5.164 | 7.3342e-07 | **Yes** |

## 3. Cross-KAP Chi-Square Tests
This evaluates the independence between categorized KAP variables (e.g., High Knowledge vs Good Attitude).

| KAP Categorical Variable 1 | KAP Categorical Variable 2 | Chi-Square | p-value | Significant? |
| :--- | :--- | :--- | :--- | :--- |
| Cat_Knowledge | Cat_Partner_Att | 3.746 | 5.2930e-02 | **No** |
| Cat_Knowledge | B_Partner_Practice | 5.492 | 1.9102e-02 | **Yes** |
| Cat_Knowledge | Cat_Cascade_Prac | 3.129 | 7.6896e-02 | **No** |
| Cat_Partner_Att | B_Partner_Practice | 0.130 | 7.1857e-01 | **No** |
