# Inferential Statistics: Knowledge Score vs. Age Group
**Independent Two-Sample T-Test**

This report examines whether there is a statistically significant difference in clinical knowledge between carriers who are younger than 35 and those who are 35 or older.

### Descriptive Statistics

| Age Group | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Below 35 | 149 | 11.74 | 7.94 | 2.164 | 4.431 |
| 35 and Above | 50 | 9.56 | 8.27 | 1.013 | 4.566 |

---

### Hypothesis Testing (Welch's T-Test)
*We use Welch's T-Test (assuming unequal variances) for robust results.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **T-Statistic:** -1.554
* **P-Value:** 0.1240
* **Conclusion:** **Not Statistically Significant (p > 0.05).** There is no significant difference in knowledge based on this age split.

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **T-Statistic:** -1.627
* **P-Value:** 0.1076
* **Conclusion:** **Not Statistically Significant (p > 0.05).**

---

### Visualizations

#### Weighted V3 Score Violin Plot
![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Age_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Age_Box.png)
