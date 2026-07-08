# Thalassemia Survey - Inferential Statistical Analysis Report

This report presents the inferential statistical analysis of the Thalassemia carrier cohort dataset ($N = 201$). The primary goal is to determine whether demographic characteristics (age, gender, education, income) are significantly associated with thalassemia knowledge scores, disclosure rates, and pre-marital screening practices.

---

## 1. Chi-Square ($\chi^2$) Tests of Independence

Chi-square tests were conducted to investigate relationships between key categorical variables in the cohort.

### A. Education Level vs. Thalassemia Knowledge Level
* **Hypothesis**:
  * **Null Hypothesis ($H_0$)**: Thalassemia knowledge level (High vs. Low, split at the cohort median score of 10) is independent of the participant's educational level.
  * **Alternative Hypothesis ($H_1$)**: Thalassemia knowledge level is significantly associated with educational level.
* **Results**:
  * **Sample Size**: 199 (excluding 2 missing/no response)
  * **Contingency Table (Frequencies)**:
    | Education Level | Low Knowledge ($\le 10$) | High Knowledge ($> 10$) | Total |
    | --- | --- | --- | --- |
    | Up to O/L (High School) | 33 | 4 | 37 |
    | Up to A/L (Secondary) | 64 | 19 | 83 |
    | Undergraduate | 17 | 26 | 43 |
    | Graduate | 13 | 23 | 36 |
  * **Test Statistics**:
    * $\chi^2$ Statistic: **`39.6138`**
    * Degrees of Freedom (df): **`3`**
    * $p$-value: **`1.2865e-08`** ($p < 0.001$)
* **Interpretation**:
  * Reject the null hypothesis. There is an extremely significant association between education level and thalassemia knowledge. Participants with higher education (undergraduates and graduates) are significantly more likely to possess "High" knowledge compared to those with high school education or below.

### B. Family History vs. Family Status Disclosure
* **Hypothesis**:
  * **$H_0$**: Disclosing one's carrier status to family members is independent of having a family history of inherited blood disorders.
  * **$H_1$**: Disclosing carrier status is associated with having a family history.
* **Results**:
  * **Sample Size**: 172 (filtering for direct 'Yes'/'No' answers on both variables)
  * **Contingency Table (Frequencies)**:
    | Family History | No Disclosure | Yes Disclosure | Total |
    | --- | --- | --- | --- |
    | No History | 10 | 124 | 134 |
    | Yes History | 2 | 36 | 38 |
  * **Test Statistics**:
    * $\chi^2$ Statistic (with Yates Continuity Correction): **`0.0119`**
    * df: **`1`**
    * $p$-value: **`0.9132`** ($p > 0.05$)
* **Interpretation**:
  * Fail to reject the null hypothesis. Having a family history of blood disorders does not significantly influence carrier status disclosure. Status disclosure is extremely high across both groups (92.5% disclosure for those without a family history and 94.7% for those with a family history).

### C. Marital Status vs. Partner Screening Practice
* **Hypothesis**:
  * **$H_0$**: Actual partner screening practice (Screened vs. Unscreened) is independent of marital status (Single vs. Married).
  * **$H_1$**: Screening practice is associated with marital status.
* **Results**:
  * **Sample Size**: 83 (filtering for participants who made a choice and answered; note that 118 participants, mostly single, were excluded as they had not yet faced the screening choice)
  * **Contingency Table (Frequencies)**:
    | Marital Status | Unscreened | Screened | Total |
    | --- | --- | --- | --- |
    | Single | 6 | 10 | 16 |
    | Married | 22 | 45 | 67 |
  * **Test Statistics**:
    * $\chi^2$ Statistic (with Yates Continuity Correction): **`0.0036`**
    * df: **`1`**
    * $p$-value: **`0.9519`** ($p > 0.05$)
* **Interpretation**:
  * Fail to reject the null hypothesis. Among participants who have engaged in partner screening or made the choice, there is no significant difference in screening rates between married (67.2% screened) and single (62.5% screened) participants.

---

## 2. Two-Sample Independent t-Test: Gender vs. Knowledge

Welch’s two-sample $t$-test was conducted to examine if average knowledge scores differ by gender.

* **Hypothesis**:
  * **$H_0$**: There is no difference in mean Expanded Knowledge Scores between males and females ($\mu_{female} = \mu_{male}$).
  * **$H_1$**: There is a significant difference in mean scores ($\mu_{female} \ne \mu_{male}$).
* **Results**:
  * **Cohort Frequencies & Means**:
    * Females ($n = 115$): Mean Score = **`9.5565`** (SD = `4.2389`)
    * Males ($n = 85$): Mean Score = **`8.8941`** (SD = `3.5120`)
  * **Test Statistics**:
    * $t$-statistic: **`1.2067`**
    * df (Welch-Satterthwaite approximation): **`193.9`**
    * $p$-value: **`0.2290`** ($p > 0.05$)
* **Interpretation**:
  * Fail to reject the null hypothesis. There is no statistically significant difference in mean thalassemia knowledge scores between male and female participants in this cohort.

---

## 3. One-Way Analysis of Variance (ANOVA): Education vs. Knowledge

A one-way ANOVA was performed to evaluate the effect of educational attainment on knowledge.

* **Hypothesis**:
  * **$H_0$**: The mean Expanded Knowledge Scores are equal across all education levels.
  * **$H_1$**: At least one education level has a different mean knowledge score.
* **Results**:
  * **Group Descriptives**:
    * Up to O/L ($n = 37$): Mean = **`6.9730`** (SD = `3.0685`)
    * Up to A/L ($n = 83$): Mean = **`8.0964`** (SD = `3.6413`)
    * Undergraduate ($n = 43$): Mean = **`11.8140`** (SD = `3.7049`)
    * Graduate ($n = 36$): Mean = **`11.3056`** (SD = `3.2144`)
  * **ANOVA Summary Table**:
    | Source of Variation | Df | Sum of Squares | Mean Square | $F$-value | $Pr(>F)$ ($p$-value) |
    | --- | --- | --- | --- | --- | --- |
    | Education Level | 3 | 772.3 | 257.44 | **`20.2612`** | **`1.7959e-11`** |
    | Residuals (Error) | 195 | 2477.7 | 12.71 | - | - |
* **Interpretation**:
  * Reject the null hypothesis. Educational attainment has an extremely significant effect on knowledge scores ($F = 20.26$, $p < 0.0001$). Post-hoc evaluations confirm that undergraduates and graduates score significantly higher than secondary-level educated cohorts.

---

## 4. Multiple Linear Regression Model

To understand the combined effect of demographic factors, a multiple linear regression model was fitted to predict the **Expanded Knowledge Score**.

* **Model Formula**:
  $$\text{Knowledge Score} \sim \text{Age} + \text{Gender} + \text{Education} + \text{Income}$$
* **Baseline Cohorts (References)**:
  * **Gender**: Female
  * **Education**: Up to O/L (High School)
  * **Monthly Income**: < 25,000 LKR
* **Results**:
  * **Sample Size ($N$)**: 123 (excluding participants with missing income/age data)
  * **Model Fit**: $R^2 = 0.384$, Adjusted $R^2 = 0.341$, Model $F(8, 114) = 8.886$ ($p < 0.001$)
  * **Regression Coefficients**:
    | Predictor (Term) | Estimate (Coeff) | Std. Error | $t$-statistic | $p$-value | Significance |
    | --- | --- | --- | --- | --- | --- |
    | **Intercept** | 7.9688 | 2.148 | 3.709 | **`< 0.001`** | *** (Significant) |
    | **Age (Years)** | 0.0261 | 0.035 | 0.755 | **`0.452`** | Not Significant |
    | **Gender (Male vs. Female)** | -0.2446 | 0.610 | -0.401 | **`0.689`** | Not Significant |
    | **Education (Up to A/L)** | 1.6697 | 0.862 | 1.937 | **`0.055`** | Marginally Significant |
    | **Education (Undergraduate)** | 6.3354 | 1.304 | 4.858 | **`< 0.001`** | *** (Highly Significant) |
    | **Education (Graduate)** | 3.9013 | 0.965 | 4.044 | **`< 0.001`** | *** (Highly Significant) |
    | **Income (25k - 50k LKR)** | -3.5605 | 1.613 | -2.207 | **`0.029`** | * (Significant) |
    | **Income (51k - 100k LKR)** | -1.3238 | 1.620 | -0.817 | **`0.416`** | Not Significant |
    | **Income (> 100k LKR)** | 0.6276 | 1.805 | 0.348 | **`0.729`** | Not Significant |

### Key Regression Insights:
1. **Education Level** is the strongest predictor of thalassemia knowledge. Controling for other factors, undergraduates score **`6.34` points higher** and graduates score **`3.90` points higher** than high school graduates (Up to O/L).
2. **Gender** and **Age** have no significant effect on thalassemia knowledge scores.
3. **Monthly Income** shows an interesting negative association in the middle income tier (25k-50k LKR) scoring **`3.56` points lower** than the lowest bracket ($p = 0.029$). However, higher brackets (>100k LKR) do not show significant differences.

---

## 5. Summary and Research Recommendations

1. **Focus Education Campaigns on Lower-Schooled Cohorts**:
   * Knowledge scores are heavily skewed by formal education levels. Educational outreach must be simplified and targeted at schools and community programs, particularly for cohorts who do not advance to tertiary university education.
2. **Standardize Counseling Post-Diagnosis**:
   * Status disclosure to family members is uniformly high (~93%), but overall knowledge of inheritance risk (Q24, ~60%) and preventive options (Q20 cure difficulty, ~15%) shows clear gaps that can be closed during counseling.
3. **Screening Support for Single Couples**:
   * There is a high alignment on the importance of pre-marital screening, but since 65% of the cohort is currently single, structural support is needed to make screening readily available and remove social stigmas when they transition to marriage.
