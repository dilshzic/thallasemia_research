# Inferential Statistics: Knowledge Score vs. Occupation & Income
**One-Way ANOVA (Analysis of Variance)**

This report examines whether clinical knowledge differs significantly across the 4 specific occupation categories and the 4 monthly income brackets.

---

## 1. Occupation Category ANOVA
*Comparing Not employed, Private sector, Government sector, and Self-employed.*

| Occupation Category | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
| Not employed | 76 | 2.269 | 4.248 |
| Private sector | 66 | 0.686 | 4.657 |
| Government sector | 48 | 3.188 | 4.472 |
| Self-employed | 8 | 2.353 | 5.284 |


* **F-Statistic:** 3.119
* **P-Value:** 0.0272
* **Conclusion:** **Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on occupation category.

![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Occupation_Violin.png)

---

## 2. Monthly Income ANOVA
*Comparing the four income brackets among those who reported a salary.*

| Monthly Income (LKR) | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
| No Income | 74 | 1.826 | 4.029 |
| < 25,000 | 5 | 5.859 | 4.426 |
| 25,000 – 50,000 | 42 | 0.343 | 5.565 |
| 51,000 – 100,000 | 66 | 2.205 | 3.889 |
| > 100,000 | 14 | 5.149 | 4.951 |


* **F-Statistic:** 4.260
* **P-Value:** 0.0025
* **Conclusion:** **Statistically Significant (p < 0.05).** There is a meaningful difference in knowledge based on income level.

![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Income_Violin.png)
