# Thalassemia Survey — Difficulty-Weighted Knowledge Scoring Analysis

This report presents a **sensitivity analysis** using **(1−p) difficulty-weighted scoring** as an alternative to equal-weight raw scoring. Difficult questions (those answered correctly by fewer participants) receive higher weights, rewarding deeper/advanced knowledge rather than surface-level awareness.

---

## 1. Rationale

### The Problem with Equal-Weight Scoring
The 21 binary knowledge items in this survey are **not equally difficult**:
- **10 items** are answered correctly by >60% of participants (EASY)
- **1 item** is answered correctly by 30–60% (MEDIUM)
- **10 items** are answered correctly by <30% (HARD)

With equal weights, a participant who answers 10 easy questions correctly scores the same as one who answers 10 hard questions — yet the latter demonstrates substantially deeper clinical knowledge.

### The (1−p) Weighting Solution
Each item receives a weight equal to **(1 − proportion correct)**:
- An item answered correctly by 90% → weight = **0.10** (nearly everyone knows this)
- An item answered correctly by 5% → weight = **0.95** (rare, advanced knowledge)

This is a standard **difficulty-weighted scoring** method in psychometric assessment.

---

## 2. Item Difficulty and Weights

| Item | Question Content | % Correct | Difficulty | Equal Weight | (1−p) Weight |
| --- | --- | --- | --- | --- | --- |
| Q15 | Is thalassemia a blood-related disease? | 90.0% | EASY | 1.00 | **0.10** |
| Q22 | Hereditary transmission | 89.1% | EASY | 1.00 | **0.11** |
| Q27₁ | Need regular blood transfusions | 84.1% | EASY | 1.00 | **0.16** |
| Q23 | Carrier is usually healthy | 82.6% | EASY | 1.00 | **0.17** |
| Q21 | Can be prevented | 75.1% | EASY | 1.00 | **0.25** |
| Q16₁ | Clinical form: Thalassemia major | 73.1% | EASY | 1.00 | **0.27** |
| Q16₂ | Clinical form: Thalassemia minor | 72.6% | EASY | 1.00 | **0.27** |
| Q17 | Most severe form (Thalassemia major) | 65.2% | EASY | 1.00 | **0.35** |
| Q19 | Requires lifelong treatment | 64.2% | EASY | 1.00 | **0.36** |
| Q24 | 25% chance of affected child | 60.2% | EASY | 1.00 | **0.40** |
| Q27₇ | Infections | 31.8% | MEDIUM | 1.00 | **0.68** |
| Q27₂ | Iron overload | 26.4% | HARD | 1.00 | **0.74** |
| Q16₄ | Clinical form: HbE/β-thalassemia | 23.9% | HARD | 1.00 | **0.76** |
| Q27₃ | Bone deformities | 23.9% | HARD | 1.00 | **0.76** |
| Q27₈ | Shortened lifespan | 20.4% | HARD | 1.00 | **0.80** |
| Q27₅ | Heart problems | 19.4% | HARD | 1.00 | **0.81** |
| Q20 | Cure difficulty (bone marrow transplant) | 14.9% | HARD | 1.00 | **0.85** |
| Q27₆ | Liver damage | 14.4% | HARD | 1.00 | **0.86** |
| Q16₃ | Clinical form: Thalassemia intermedia | 7.5% | HARD | 1.00 | **0.93** |
| Q27₄ | Growth retardation | 7.5% | HARD | 1.00 | **0.93** |
| Q26 | Normal blood count range (40–100) | 5.0% | HARD | 1.00 | **0.95** |

> [!NOTE]
> The maximum possible **equal-weight score** is **21** (all items correct). The maximum possible **difficulty-weighted score** is **11.49** — because easy items contribute very little weight, the scale compresses toward advanced knowledge.

---

## 3. Difficulty-Weighted Score Distribution

| Statistic | Equal-Weight (Raw) | (1−p) Weighted |
| --- | --- | --- |
| **Mean** | 9.51 / 21 (45.3%) | 3.27 / 11.49 (28.5%) |
| **SD** | 3.67 | 2.03 |
| **Median** | 10.0 | 2.50 |
| **Min** | 1.0 | 0.57 |
| **Max** | 20.0 | 10.73 |

The weighted distribution is **right-skewed** (mean > median), confirming that most participants cluster at low weighted scores (they know the easy items) while a smaller group with advanced knowledge pulls the tail rightward.

### Correlation Between Methods
| Measure | Value |
| --- | --- |
| Pearson *r* | **0.8986** |
| Spearman ρ | **0.9345** |

The two methods are highly correlated ($r = 0.90$), but **not identical** — meaning difficulty weighting does meaningfully re-rank some participants. Specifically, **27 participants (13.4%)** were reclassified between High/Low knowledge when using the weighted median split.

---

## 4. Inferential Analysis Results

### 4.1 Welch's Independent *t*-Test: Gender vs. Knowledge

| Parameter | Equal-Weight | (1−p) Weighted |
| --- | --- | --- |
| **Mean — Female** | 9.56 | **3.48** |
| **Mean — Male** | 8.89 | **3.00** |
| **Mean Difference** | 0.66 | **0.48** |
| **Cohen's *d*** | — | **0.24** (small) |
| **$t$-statistic** | 1.207 | **1.705** |
| **df (Welch)** | 195.38 | **197.14** |
| **$p$-value** | 0.229 | **0.090** |
| **Significant?** | ❌ No | ❌ No |

**Interpretation**: With difficulty weighting, the gender difference becomes *closer* to significance ($p = 0.09$ vs $p = 0.23$) with a small effect size (Cohen's $d = 0.24$), suggesting females may have marginally deeper clinical knowledge. However, the result remains non-significant at $\alpha = 0.05$, and the practical difference is small.

---

### 4.2 One-Way ANOVA: Education Level vs. Knowledge

#### Group Descriptive Statistics (Difficulty-Weighted)

| Education Level | $n$ | Mean | SD | Min | Max |
| --- | --- | --- | --- | --- | --- |
| **Graduate** | 36 | 4.23 | 1.92 | 1.04 | 9.78 |
| **Undergraduate** | 43 | 4.55 | 2.51 | 1.85 | 10.73 |
| **Up to A/L** | 83 | 2.62 | 1.55 | 0.57 | 6.83 |
| **Up to O/L** | 37 | 2.36 | 1.28 | 0.91 | 5.94 |

#### ANOVA Summary Table

| Source | df | SS | MS | $F$ | $p$-value |
| --- | --- | --- | --- | --- | --- |
| **Education Level** | 3 | 169.82 | 56.61 | **16.962** | **$7.88 \times 10^{-10}$** |
| Residuals | 195 | 650.78 | 3.34 | — | — |
| **Total** | 198 | 820.60 | — | — | — |

| Effect Size | Value | Interpretation |
| --- | --- | --- |
| $\eta^2$ | **0.2069** | Large effect (>0.14 threshold) |
| $\omega^2$ | **0.1940** | Population-adjusted; still large |

**Comparison**: The ANOVA remains highly significant. The effect size with difficulty weighting ($\eta^2 = 0.207$) is slightly smaller than with equal weighting ($\eta^2 = 0.238$), meaning education explains **20.7%** of the variance in *advanced* knowledge vs. **23.8%** of the variance in *total* knowledge.

---

### 4.3 Tukey HSD Post-Hoc Comparisons (Difficulty-Weighted)

| Comparison | Mean Diff | $p$-value | Significant? |
| --- | --- | --- | --- |
| **Graduate vs. Undergraduate** | −0.32 | 0.8631 | ❌ No |
| **Graduate vs. Up to A/L** | +1.61 | $9.58 \times 10^{-5}$ | ✅ Yes |
| **Graduate vs. Up to O/L** | +1.87 | $1.15 \times 10^{-4}$ | ✅ Yes |
| **Undergraduate vs. Up to A/L** | +1.93 | $3.64 \times 10^{-7}$ | ✅ Yes |
| **Undergraduate vs. Up to O/L** | +2.19 | $1.43 \times 10^{-6}$ | ✅ Yes |
| **Up to A/L vs. Up to O/L** | +0.26 | 0.8893 | ❌ No |

**Interpretation**: The **same two-tier pattern** persists under difficulty weighting:
- **Tier 1 (Higher)**: Graduate and Undergraduate — not significantly different from each other
- **Tier 2 (Lower)**: Up to A/L and Up to O/L — not significantly different from each other
- All cross-tier comparisons are significant ($p < 0.001$)

---

### 4.4 Chi-Square: Education vs. Knowledge Level (Median Split)

The difficulty-weighted median ($\tilde{x} = 2.50$) was used to classify participants as High vs. Low knowledge.

| Education Level | Low Knowledge | High Knowledge | Total | % High |
| --- | --- | --- | --- | --- |
| **Graduate** | 7 | 29 | 36 | **80.6%** |
| **Undergraduate** | 11 | 32 | 43 | **74.4%** |
| **Up to A/L** | 55 | 28 | 83 | **33.7%** |
| **Up to O/L** | 27 | 10 | 37 | **27.0%** |
| **Total** | **100** | **99** | **199** | 49.7% |

| Parameter | Equal-Weight | (1−p) Weighted |
| --- | --- | --- |
| **$\chi^2$** | 39.61 | **40.29** |
| **df** | 3 | 3 |
| **$p$-value** | $1.29 \times 10^{-8}$ | $9.25 \times 10^{-9}$ |

> [!TIP]
> The Chi-Square is actually **slightly stronger** with difficulty weighting ($\chi^2 = 40.29$ vs $39.61$), suggesting that the difficulty-weighted score produces a cleaner separation between education tiers. Additionally, 27 participants (13.4%) were reclassified, indicating the weighted score does differentiate individual profiles.

---

### 4.5 Multiple Linear Regression

**Model**: $\text{DiffW\_Score} = \beta_0 + \beta_1 \cdot \text{Age} + \beta_2 \cdot \text{Gender} + \beta_3 \cdot \text{Education} + \beta_4 \cdot \text{Income}$

#### Model Fit Comparison

| Metric | Equal-Weight | (1−p) Weighted |
| --- | --- | --- |
| **$R^2$** | 0.384 | **0.374** |
| **Adjusted $R^2$** | 0.341 | **0.330** |
| **$F$-statistic** | 8.886 | **8.516** |
| **$p$-value ($F$)** | $2.12 \times 10^{-9}$ | $4.94 \times 10^{-9}$ |
| **$n$** | 123 | 123 |

#### Coefficient Table (Difficulty-Weighted)

| Term | $\beta$ | SE | $t$ | $p$-value | Sig? |
| --- | --- | --- | --- | --- | --- |
| **Intercept** | 4.117 | 1.077 | 3.824 | **0.0002** | ✅ |
| **Gender: Male** (vs. Female) | −0.420 | 0.306 | −1.373 | 0.173 | ❌ |
| **Education: Graduate** (vs. O/L) | 1.236 | 0.483 | 2.557 | **0.012** | ✅ |
| **Education: Undergraduate** (vs. O/L) | 2.408 | 0.653 | 3.684 | **0.0004** | ✅ |
| **Education: Up to A/L** (vs. O/L) | 0.147 | 0.432 | 0.340 | 0.735 | ❌ |
| **Income: 25–50k** (vs. <25k) | −1.937 | 0.808 | −2.397 | **0.018** | ✅ |
| **Income: 51–100k** (vs. <25k) | −0.872 | 0.812 | −1.074 | 0.285 | ❌ |
| **Income: >100k** (vs. <25k) | 0.619 | 0.904 | 0.685 | 0.495 | ❌ |
| **Age** | −0.005 | 0.017 | −0.286 | 0.776 | ❌ |

**Key Changes from Equal-Weight Model**:
- Education (A/L vs O/L) drops from borderline ($p = 0.055$) to clearly non-significant ($p = 0.735$) — confirming that A/L-educated participants have similar *advanced* knowledge to O/L participants
- Gender effect strengthens slightly ($p = 0.173$ vs $p = 0.689$) but remains non-significant
- All other significance decisions are unchanged

---

## 5. Synthesis: Does Difficulty Weighting Change Conclusions?

| Finding | Equal-Weight | (1−p) Weighted | Changed? |
| --- | --- | --- | --- |
| Gender → Knowledge | Not significant ($p = 0.23$) | Not significant ($p = 0.09$) | ❌ Same |
| Education → Knowledge | Highly significant ($p < 10^{-11}$) | Highly significant ($p < 10^{-10}$) | ❌ Same |
| Tertiary vs Secondary divide | Clear two-tier pattern | Clear two-tier pattern | ❌ Same |
| A/L vs O/L difference | Not significant ($p = 0.36$) | Not significant ($p = 0.89$) | ❌ Same |
| Income (25–50k) anomaly | Significant ($p = 0.029$) | Significant ($p = 0.018$) | ❌ Same |
| Model $R^2$ | 0.384 | 0.374 | ❌ Similar |
| Chi-Square (Edu vs KL) | $\chi^2 = 39.61$ | $\chi^2 = 40.29$ | ❌ Same direction, slightly stronger |

### Conclusion

> [!IMPORTANT]
> **All inferential conclusions are robust to the choice of scoring method.** The (1−p) difficulty-weighted analysis confirms that equal-weight scoring does not mask or distort the key findings. The educational divide remains the primary driver of thalassemia knowledge regardless of whether surface-level or advanced knowledge is emphasized.
>
> The main **nuanced difference** is that difficulty weighting makes the **A/L vs O/L gap disappear more definitively** ($p = 0.89$ vs $p = 0.36$), confirming that both secondary-education groups share similarly limited *advanced* clinical knowledge even if they differ slightly in basic awareness.

### Methodological Note for Publication
*"As a sensitivity analysis, a difficulty-weighted scoring scheme was applied, weighting each item by (1 − p), where p is the proportion of correct responses. This method assigns greater value to items reflecting advanced clinical knowledge. All inferential conclusions — including the significant association between education level and knowledge ($F(3,195) = 16.96$, $p < .001$, $\eta^2 = .207$), and the non-significant gender difference ($t(197) = 1.71$, $p = .090$) — were consistent across both scoring approaches, confirming the robustness of the primary findings."*
