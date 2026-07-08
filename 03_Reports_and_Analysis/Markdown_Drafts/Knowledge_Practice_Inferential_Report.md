# Inferential Statistics: Knowledge Score vs. Actual Practices

This report examines whether clinical knowledge dictates the actual actions a carrier takes regarding family planning (Partner Screening) and cascade screening (Family Disclosure).

---

## 1. Partner Screening Practice (One-Way ANOVA)
*We grouped the participants into three behavioral tiers: Safe (Screened before marriage), Delayed (Screened after marriage/pregnancy), and Unsafe (Did not screen/disclose).*
*Note: Participants marked 'Other' (usually single/unmarried) were excluded.*

| Behavioral Tier | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
| Unsafe Practice (No Screening / No Disclosure) | 28 | 1.583 | 5.299 |
| Delayed Practice (After Marriage / Pregnancy) | 34 | 1.342 | 4.097 |
| Safe Practice (Before Marriage) | 21 | 4.105 | 3.822 |


* **F-Statistic:** 2.779
* **P-Value:** 0.0681
* **Conclusion:** **Not Statistically Significant (p > 0.05).** Clinical knowledge does not significantly alter actual partner screening practices.

![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_PartnerPractice_Violin.png)

---

## 2. Family Disclosure Practice (Welch's T-Test)
*Comparing carriers who disclosed their status to their family versus those who kept it a secret.*

| Disclosed to Family? | N | Mean (Weighted V3) | Std Dev (Weighted) |
|---|---|---|---|
| No | 15 | 0.375 | 6.606 |
| Yes | 182 | 2.139 | 4.378 |


* **T-Statistic:** 1.016
* **P-Value:** 0.3258
* **Conclusion:** **Not Statistically Significant (p > 0.05).** Clinical knowledge does not significantly influence whether a carrier tells their family.

![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_FamilyPractice_Violin.png)
