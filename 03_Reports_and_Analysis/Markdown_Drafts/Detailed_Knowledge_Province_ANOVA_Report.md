# Inferential Statistics: Knowledge Score vs. Residential Province
**One-Way ANOVA & Tukey HSD Post-Hoc Analysis**

This detailed report examines whether clinical knowledge differs significantly based on geographical residence, specifically comparing the Western Province, North Western Province, and all other provinces grouped together.

---

### 1. Descriptive Statistics

| Province Group | N | Mean (Weighted V3) | Std Dev |
|---|---|---|---|
| Western | 120 | 1.872 | 4.524 |
| North Western | 41 | 0.935 | 4.402 |
| Other | 40 | 3.337 | 4.636 |


---

### 2. Hypothesis Testing (One-Way ANOVA)
*The overall test to see if geography matters.*

* **F-Statistic:** 2.929
* **P-Value:** 0.0558
* **Conclusion:** **Borderline/Not Statistically Significant (p > 0.05).**

---

### 3. Post-Hoc Analysis (Tukey HSD)
*Since the ANOVA p-value (0.0558) approaches significance, we run a pairwise Tukey HSD test to identify exactly which provinces differ.*

```
       group1  group2  meandiff  p-adj   lower  upper  reject
North Western   Other    2.4017 0.0466  0.0286 4.7749    True
North Western Western    0.9372 0.4872 -0.9945 2.8689   False
        Other Western   -1.4646 0.1810 -3.4141 0.4850   False
```

**Tukey Interpretation:**
If the `reject` column is True, those two specific provinces have statistically significantly different knowledge scores. If all are False, the variance between any specific pair is not large enough to declare significance independently.

---

### 4. Visualizations
![Violin Plot](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/inferential_tests/Knowledge_Province_Violin.png)
