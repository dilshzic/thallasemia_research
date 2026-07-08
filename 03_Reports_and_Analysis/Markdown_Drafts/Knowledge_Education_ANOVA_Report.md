# Inferential Statistics: Knowledge Score vs. Education Level
**One-Way ANOVA (Analysis of Variance)**

This report examines whether there is a statistically significant difference in clinical knowledge across four different educational attainment levels among thalassemia carriers.

### Descriptive Statistics

| Education Level | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Up to O/L | 37 | 6.62 | 7.04 | -0.649 | 3.727 |
| Up to A/L | 83 | 9.24 | 8.57 | 0.715 | 4.574 |
| Undergraduate | 43 | 16.51 | 5.29 | 5.032 | 3.484 |
| Graduate | 36 | 14.72 | 6.56 | 3.885 | 3.840 |

---

### Hypothesis Testing (One-Way ANOVA)
*We use an Analysis of Variance (ANOVA) to determine if the means of the four independent groups are significantly different from each other.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **F-Statistic:** 18.439
* **P-Value:** 0.0000
* **Conclusion:** **Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on education level.

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **F-Statistic:** 17.041
* **P-Value:** 0.0000
* **Conclusion:** **Statistically Significant (p < 0.05).**

---

### Visualizations

#### Weighted V3 Score Violin Plot
The violin plot demonstrates the distribution density for each educational group.
![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Education_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Education_Box.png)
