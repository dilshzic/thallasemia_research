# Inferential Statistics: Knowledge Score vs. Gender
**Independent Two-Sample T-Test**

This report examines whether there is a statistically significant difference in clinical knowledge between Male and Female thalassemia carriers.

### Descriptive Statistics

| Gender | N | Mean (V3 Score) | Std Dev (V3 Score) | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|---|---|
| Male | 85 | 10.81 | 7.57 | 1.638 | 4.223 |
| Female | 115 | 11.72 | 8.59 | 2.216 | 4.825 |

---

### Hypothesis Testing (Welch's T-Test)
*We use Welch's T-Test (assuming unequal variances) for robust results.*

#### 1. Analysis using the mathematically rigorous **Weighted V3 Knowledge Score**:
* **T-Statistic:** -0.900
* **P-Value:** 0.3694
* **Conclusion:** **Not Statistically Significant (p > 0.05).** There is no significant difference in knowledge between male and female carriers.

#### 2. Analysis using the standard **V3 Knowledge Score**:
* **T-Statistic:** -0.793
* **P-Value:** 0.4287
* **Conclusion:** **Not Statistically Significant (p > 0.05).**

---

### Visualizations

#### Weighted V3 Score Violin Plot
The violin plot demonstrates the distribution density and quartiles for both genders using the rigorously weighted metric.
![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Gender_Violin.png)

#### Standard V3 Score Box Plot
![Box Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Gender_Box.png)
