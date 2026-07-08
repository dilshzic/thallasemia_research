# Thalassemia Survey - Inferential Analysis: Chi-Square Tests Report

This report presents the detailed results of Chi-Square ($\chi^2$) tests of independence conducted on the Thalassemia survey dataset. These tests evaluate the relationships between key categorical variables (Education, Family History, Marital Status, Disclosure, and Partner Screening).

---

## 1. Test 1: Education Level vs. Thalassemia Knowledge Level

### Objective
To determine if a participant's level of formal education is significantly associated with their thalassemia knowledge. 

### Variables
* **Independent Variable**: Education Level (Graduate, Undergraduate, Up to A/L, Up to O/L)
* **Dependent Variable**: Knowledge Level (Split at the cohort median score of 10: "High" ($>10$) vs. "Low" ($\le 10$))

### Hypotheses
* **Null Hypothesis ($H_0$)**: Thalassemia knowledge level is independent of educational level.
* **Alternative Hypothesis ($H_1$)**: Thalassemia knowledge level is significantly associated with educational level.

### Contingency Table & Cell Proportions
The table shows the raw counts and column percentages (low vs. high within each education tier):

| Education Level | Low Knowledge ($\le 10$) | High Knowledge ($> 10$) | Total Group Size | % High Knowledge |
| --- | --- | --- | --- | --- |
| **Graduate** | 13 | 23 | 36 | 63.89% |
| **Undergraduate** | 17 | 26 | 43 | 60.47% |
| **Up to A/L** | 64 | 19 | 83 | 22.89% |
| **Up to O/L** | 33 | 4 | 37 | 10.81% |
| **Total** | **127** | **72** | **199** | **36.18%** |

*Note: 2 participants were excluded due to missing education responses.*

### Chi-Square Test Results
* **$\chi^2$ Statistic**: **`39.6138`**
* **Degrees of Freedom (df)**: **`3`**
* **$p$-value**: **`1.2865e-08`** ($p < 0.001$)

### Interpretation & Discussion
* **Statistical Decision**: Reject $H_0$ at the $\alpha = 0.05$ level.
* **Findings**: There is an extremely significant relationship between educational level and thalassemia knowledge. 
  * Over 60% of graduates and undergraduates scored in the High Knowledge category.
  * In contrast, only 22.9% of those with secondary education (A/L) and 10.8% with high school (O/L) achieved High Knowledge.
  * This confirms that general formal education heavily correlates with clinical disease awareness.

---

## 2. Test 2: Family History vs. Family Status Disclosure

### Objective
To evaluate whether knowing a relative with an inherited blood disorder influences a carrier's likelihood of disclosing their carrier status to family members.

### Variables
* **Independent Variable**: Family History of Inherited Blood Disorder (Yes vs. No)
* **Dependent Variable**: Status Disclosure to Family Members (Yes vs. No)

### Hypotheses
* **$H_0$**: Status disclosure to family members is independent of having a family history of inherited blood disorders.
* **$H_1$**: Status disclosure is significantly associated with having a family history.

### Contingency Table & Cell Proportions
| Family History | No Disclosure | Yes Disclosure | Total | % Disclosed |
| --- | --- | --- | --- | --- |
| **No History** | 10 | 124 | 134 | 92.54% |
| **Yes History** | 2 | 36 | 38 | 94.74% |
| **Total** | **12** | **160** | **172** | **93.02%** |

*Note: Excludes participants who responded "I don't know" for family history or had missing values.*

### Chi-Square Test Results
* **$\chi^2$ Statistic (with Yates Continuity Correction)**: **`0.0119`**
* **df**: **`1`**
* **$p$-value**: **`0.9132`** ($p > 0.05$)

### Interpretation & Discussion
* **Statistical Decision**: Fail to reject $H_0$.
* **Findings**: Disclosure rates are extremely high (~93%) and do not significantly differ between those with a family history (94.7%) and those without (92.5%). Thalassemia carriers are highly willing to share their diagnosis with family members regardless of background history, suggesting a lack of familial stigma in status sharing.

---

## 3. Test 3: Marital Status vs. Partner Screening Practice

### Objective
To determine if married carriers are more likely to have screened their partners compared to single carriers who made a screening decision.

### Variables
* **Independent Variable**: Marital Status (Single vs. Married)
* **Dependent Variable**: Partner Screening Practice (Recoded: "Screened" vs. "Unscreened")
  * *Screened*: Partner tested before/after marriage or during pregnancy.
  * *Unscreened*: Did not screen, or did not disclose status to partner.

### Hypotheses
* **$H_0$**: Partner screening practice is independent of marital status.
* **$H_1$**: Partner screening practice is significantly associated with marital status.

### Contingency Table & Cell Proportions
| Marital Status | Unscreened | Screened | Total | % Screened |
| --- | --- | --- | --- | --- |
| **Single** | 6 | 10 | 16 | 62.50% |
| **Married** | 22 | 45 | 67 | 67.16% |
| **Total** | **28** | **55** | **83** | **66.27%** |

*Note: Excludes 118 participants (mostly single) who responded "Other" (e.g. "Still not married") or did not answer.*

### Chi-Square Test Results
* **$\chi^2$ Statistic (with Yates Continuity Correction)**: **`0.0036`**
* **df**: **`1`**
* **$p$-value**: **`0.9519`** ($p > 0.05$)

### Interpretation & Discussion
* **Statistical Decision**: Fail to reject $H_0$.
* **Findings**: For participants who have faced a partner screening decision, marital status does not significantly impact their choice. Screening rates are high (~66%) in both groups. 
* **Key Context**: The majority of single participants (115 out of 131) were excluded because they specified they are not married yet and have not screened a partner. This highlights that once single carriers enter relationships, they screen at a rate comparable to those already married.
