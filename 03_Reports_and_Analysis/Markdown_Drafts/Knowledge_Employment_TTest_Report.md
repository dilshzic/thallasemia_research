# Inferential Statistics: Knowledge Score vs. Employment Status
**Independent Two-Sample T-Test**

This report examines whether there is a statistically significant difference in clinical knowledge between Employed and Unemployed thalassemia carriers.

### Descriptive Statistics

| Employment Status | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Employed | 122 | 10.97 | 8.53 | 1.779 | 4.743 |
| Unemployed | 76 | 11.92 | 7.50 | 2.269 | 4.248 |

---

### Hypothesis Testing (Welch's T-Test)
*We use Welch's T-Test (assuming unequal variances) for robust results.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **T-Statistic:** -0.753
* **P-Value:** 0.4522
* **Conclusion:** **Not Statistically Significant (p > 0.05).** There is no significant difference in knowledge based on employment status.

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **T-Statistic:** -0.826
* **P-Value:** 0.4102
* **Conclusion:** **Not Statistically Significant (p > 0.05).**

---

### Visualizations

#### Weighted V3 Score Violin Plot
![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Employment_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Employment_Box.png)
