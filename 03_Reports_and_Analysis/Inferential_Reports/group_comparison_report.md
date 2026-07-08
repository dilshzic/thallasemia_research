# Thalassemia Survey — Inferential Analysis: Group Comparison Report

This report presents the results of parametric group-comparison tests applied to the Thalassemia survey dataset (N = 201). All tests use the **Expanded Knowledge Score** (0–20 scale) as the continuous dependent variable.

---

## 1. Welch's Independent-Samples _t_-Test: Gender vs. Knowledge Score

### Objective
To determine whether male and female thalassemia carriers differ significantly in their overall knowledge of the disease.

### Variables
* **Independent Variable**: Gender (Female vs. Male)
* **Dependent Variable**: Expanded Knowledge Score (0–20)

### Hypotheses
* **Null Hypothesis ($H_0$)**: The mean Expanded Knowledge Score is equal for females and males ($\mu_F = \mu_M$).
* **Alternative Hypothesis ($H_1$)**: The mean Expanded Knowledge Score differs significantly between females and males ($\mu_F \ne \mu_M$).

### Assumptions Check
* **Independence**: Participants were sampled independently.
* **Normality**: With $n > 30$ in both groups, the Central Limit Theorem supports approximate normality of sampling means.
* **Homogeneity of Variance**: Welch's correction is applied (does **not** assume equal variances), making this a robust choice.

### Group Descriptive Statistics

| Group | $n$ | Mean | SD | Median |
| --- | --- | --- | --- | --- |
| **Female** | 115 | 9.5565 | 4.2389 | 10.0 |
| **Male** | 85 | 8.8941 | 3.5120 | 9.0 |
| **Overall** | 200 | 9.2753 | 3.9408 | 9.5 |

*Note: 1 participant excluded due to missing gender response.*

### Test Results
| Parameter | Value |
| --- | --- |
| **$t$-statistic** | **1.2067** |
| **Degrees of Freedom (Welch-Satterthwaite)** | **195.38** |
| **$p$-value** | **0.2290** |
| **Mean Difference** ($\bar{x}_F - \bar{x}_M$) | **0.6624** |

### Interpretation & Discussion

* **Statistical Decision**: Fail to reject $H_0$ at $\alpha = 0.05$.
* **Findings**: Female carriers scored slightly higher on average (9.56 vs. 8.89), but this difference is **not statistically significant** ($p = 0.229$). Gender does not appear to be a meaningful predictor of thalassemia knowledge in this cohort.
* **Clinical Implication**: Health literacy interventions need not be gender-specific; both groups exhibit comparable baseline knowledge with similarly broad variability.

---

## 2. One-Way ANOVA: Education Level vs. Knowledge Score

### Objective
To determine whether the mean Expanded Knowledge Score differs significantly across levels of formal education.

### Variables
* **Independent Variable**: Education Level (4 groups: Graduate, Undergraduate, Up to A/L, Up to O/L)
* **Dependent Variable**: Expanded Knowledge Score (0–20)

### Hypotheses
* **$H_0$**: $\mu_{\text{Grad}} = \mu_{\text{UG}} = \mu_{\text{A/L}} = \mu_{\text{O/L}}$  (all education groups have the same mean knowledge score)
* **$H_1$**: At least one group mean differs from the others.

### Group Descriptive Statistics

| Education Level | $n$ | Mean | SD | Min | Max |
| --- | --- | --- | --- | --- | --- |
| **Graduate** | 36 | 11.3056 | 3.2144 | 2 | 19 |
| **Undergraduate** | 43 | 11.8140 | 3.7049 | 5 | 20 |
| **Up to A/L** | 83 | 8.0964 | 3.6413 | 0 | 15 |
| **Up to O/L** | 37 | 6.9730 | 3.0685 | 2 | 14 |
| **Overall** | 199 | 9.2864 | 3.9436 | 0 | 20 |

*Note: 2 participants excluded due to missing education responses.*

### ANOVA Summary Table

| Source | df | Sum of Squares (SS) | Mean Square (MS) | $F$-statistic | $p$-value |
| --- | --- | --- | --- | --- | --- |
| **Education Level** | 3 | 736.9943 | 245.6648 | **20.2612** | **$1.80 \times 10^{-11}$** |
| Residuals | 195 | 2364.3524 | 12.1249 | — | — |
| **Total** | 198 | 3101.3467 | — | — | — |

### Test Results Interpretation
* **Statistical Decision**: Reject $H_0$ at $\alpha = 0.05$ ($p < 0.001$).
* **Effect Size**: $\eta^2 = \frac{SS_{\text{between}}}{SS_{\text{total}}} = \frac{736.99}{3101.35} = 0.2377$ — a **large effect** (> 0.14 threshold). Education level accounts for approximately **23.8%** of the total variance in knowledge scores.
* **Key Finding**: Education level is a highly significant predictor of thalassemia knowledge, with tertiary-educated participants scoring nearly 5 points higher on average than those with only secondary-level education.

---

## 3. Tukey HSD Post-Hoc Pairwise Comparisons

Since the ANOVA was significant, Tukey's Honestly Significant Difference (HSD) test was conducted to identify **which specific pairs** of education groups differ.

### Pairwise Results

| Comparison | Test Statistic | $p$-value | Significant? |
| --- | --- | --- | --- |
| **Graduate vs. Undergraduate** | −0.5084 | 0.9167 | ❌ No |
| **Graduate vs. Up to A/L** | 3.2092 | $4.14 \times 10^{-5}$ | ✅ Yes |
| **Graduate vs. Up to O/L** | 4.3326 | $1.73 \times 10^{-6}$ | ✅ Yes |
| **Undergraduate vs. Up to A/L** | 3.7176 | $2.86 \times 10^{-7}$ | ✅ Yes |
| **Undergraduate vs. Up to O/L** | 4.8410 | $1.98 \times 10^{-8}$ | ✅ Yes |
| **Up to A/L vs. Up to O/L** | 1.1234 | 0.3630 | ❌ No |

### Post-Hoc Interpretation

The Tukey HSD results reveal a **clear two-tier pattern** in thalassemia knowledge:

1. **Higher-Knowledge Tier** — **Graduate** ($\bar{x}=11.31$) and **Undergraduate** ($\bar{x}=11.81$) participants show statistically equivalent knowledge ($p = 0.92$). Both groups score significantly higher than the secondary-education groups.

2. **Lower-Knowledge Tier** — **Up to A/L** ($\bar{x}=8.10$) and **Up to O/L** ($\bar{x}=6.97$) participants also show statistically equivalent knowledge ($p = 0.36$). Both groups score significantly lower than the tertiary-education groups.

3. **Key Implication**: The critical threshold for thalassemia literacy appears to be the transition from secondary (A/L or O/L) to tertiary (Undergraduate/Graduate) education. This identifies **secondary-educated carriers** as the priority target population for tailored health education interventions.

---

## Summary

| Test | $F$ / $t$ Statistic | $p$-value | Significant? | Practical Implication |
| --- | --- | --- | --- | --- |
| Welch's _t_-test (Gender) | $t = 1.207$ | 0.229 | ❌ No | Gender-neutral education is appropriate |
| One-Way ANOVA (Education) | $F = 20.261$ | $1.80 \times 10^{-11}$ | ✅ Yes | Education level explains 23.8% of knowledge variance |
| Tukey HSD Post-hoc | — | See above | Mixed | Tertiary vs. secondary is the critical divide |
