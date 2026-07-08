# Inferential Statistics: Knowledge Score vs. Marital Status
**Independent Two-Sample T-Test**

This report examines whether there is a statistically significant difference in clinical knowledge between Married and Single thalassemia carriers.

### Descriptive Statistics

| Marital Status | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Married | 70 | 9.77 | 7.99 | 1.067 | 4.381 |
| Single | 131 | 12.17 | 8.14 | 2.456 | 4.604 |

---

### Hypothesis Testing (Welch's T-Test)
*We use Welch's T-Test (assuming unequal variances) for robust results.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **T-Statistic:** -2.104
* **P-Value:** 0.0371
* **Conclusion:** **Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge between married and single carriers.

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **T-Statistic:** -2.014
* **P-Value:** 0.0459
* **Conclusion:** **Statistically Significant (p < 0.05).**

---

### Visualizations

#### Weighted V3 Score Violin Plot
The violin plot demonstrates the distribution density and quartiles for both groups using the rigorously weighted metric.
![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Marital_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Marital_Box.png)
