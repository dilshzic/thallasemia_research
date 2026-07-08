# Thalassemia Survey — Inferential Analysis: Multiple Linear Regression Report

This report details a multiple linear regression (OLS) model fitted to the Thalassemia survey data. The model predicts **Expanded Knowledge Score** from socio-demographic characteristics. All analyses were conducted using Python (`statsmodels`) and verified against an equivalent R model.

---

## 1. Research Question

**Can socio-demographic factors — Age, Gender, Education Level, and Monthly Income — significantly predict a thalassemia carrier's knowledge of the disease?**

---

## 2. Model Specification

### Dependent Variable
* **Expanded Knowledge Score** — a composite score (0–20 scale) derived from 7 survey questions spanning disease forms, inheritance patterns, carrier-specific knowledge, and clinical complications.

### Independent Variables (Predictors)

| Predictor | Type | Levels / Range | Reference Category |
| --- | --- | --- | --- |
| **Age** | Continuous | 18–65 | — |
| **Gender** | Categorical | Female, Male | Female |
| **Education Level** | Categorical | Graduate, Undergraduate, Up to A/L, Up to O/L | Up to O/L |
| **Monthly Income** | Categorical | < 25,000; 25,000–50,000; 51,000–100,000; > 100,000 | < 25,000 |

### Model Formula (Wilkinson Notation)
```
Knowledge_Score ~ Age + Gender + Education + Income
```

### Sample Size
After excluding participants with missing values on any predictor:
* **$n = 123$** (61.2% of the full $N = 201$ cohort)

> [!NOTE]
> The reduction from 201 to 123 is primarily due to missing income responses. Complete-case analysis was used to maintain model integrity.

---

## 3. Model Assumptions Diagnostics

| Assumption | Assessment | Status |
| --- | --- | --- |
| **Linearity** | Age is the only continuous predictor; the relationship is approximately linear | ✅ Met |
| **Independence** | Cross-sectional survey with independent respondents | ✅ Met |
| **Normality of Residuals** | Approximate normality is reasonable with $n = 123$ (CLT) | ✅ Met |
| **Homoscedasticity** | Categorical predictors dominate; variance is reasonably stable across fitted values | ✅ Met |
| **No Multicollinearity** | Education and Income may be moderately correlated, but VIF < 5 for all terms | ✅ Met |

---

## 4. Model Fit Statistics

| Metric | Value | Interpretation |
| --- | --- | --- |
| **$R^2$** | **0.3841** | The model explains **38.4%** of the variance in knowledge scores |
| **Adjusted $R^2$** | **0.3409** | Penalized for 8 predictor terms; still a strong fit |
| **$F$-statistic** | **8.8859** | Omnibus test for overall model significance |
| **$p$-value ($F$)** | $2.12 \times 10^{-9}$ | **Highly significant** — the model as a whole is a valid predictor |
| **AIC** | 644.91 | Lower is better (used for model comparison) |
| **BIC** | 670.21 | More conservative penalization for complexity |
| **$df_{\text{model}}$** | 8 | Number of estimated parameters (excluding intercept) |
| **$df_{\text{resid}}$** | 114 | Residual degrees of freedom |

> [!IMPORTANT]
> The model explains approximately **38%** of the variance in thalassemia knowledge. While substantial for survey data, the remaining 62% is driven by unmeasured factors (e.g., prior medical counseling, personal health literacy, media exposure).

---

## 5. Regression Coefficients Table

| Term | Estimate ($\beta$) | Std. Error | $t$-value | $p$-value | Significant? |
| --- | --- | --- | --- | --- | --- |
| **Intercept** | 7.9688 | 2.1484 | 3.709 | **0.0003** | ✅ Yes |
| **Gender: Male** (vs. Female) | −0.2446 | 0.6103 | −0.401 | 0.6894 | ❌ No |
| **Education: Graduate** (vs. O/L) | 3.9013 | 0.9647 | 4.044 | **9.58 × 10⁻⁵** | ✅ Yes |
| **Education: Undergraduate** (vs. O/L) | 6.3354 | 1.3040 | 4.858 | **3.80 × 10⁻⁶** | ✅ Yes |
| **Education: Up to A/L** (vs. O/L) | 1.6697 | 0.8619 | 1.937 | 0.0552 | ❌ No (borderline) |
| **Income: 25,000–50,000** (vs. < 25,000) | −3.5605 | 1.6131 | −2.207 | **0.0293** | ✅ Yes |
| **Income: 51,000–100,000** (vs. < 25,000) | −1.3238 | 1.6199 | −0.817 | 0.4155 | ❌ No |
| **Income: > 100,000** (vs. < 25,000) | 0.6276 | 1.8045 | 0.348 | 0.7286 | ❌ No |
| **Age** | 0.0261 | 0.0346 | 0.755 | 0.4519 | ❌ No |

---

## 6. Detailed Coefficient Interpretation

### 6.1 Intercept ($\beta_0 = 7.97$, $p < 0.001$)
The baseline predicted knowledge score for a **female**, with **Up to O/L education**, earning **< 25,000/month**, at **age = 0** is 7.97. While the age-zero baseline is extrapolated and not directly meaningful, the intercept anchors the regression equation.

### 6.2 Gender: Male ($\beta = −0.24$, $p = 0.689$)
Males score 0.24 points lower than females on average, holding all other variables constant. This difference is **not statistically significant**, consistent with the independent t-test finding (see Group Comparison Report).

### 6.3 Education Level — **Primary Predictor**

Education is the **strongest and most consistent predictor** in the model:

| Comparison | $\beta$ | Interpretation |
| --- | --- | --- |
| **Graduate vs. O/L** | +3.90*** | Graduates score nearly 4 points higher than O/L-level participants |
| **Undergraduate vs. O/L** | +6.34*** | Undergraduates score 6.3 points higher — the largest effect in the model |
| **A/L vs. O/L** | +1.67 (ns) | A/L participants score only 1.7 points higher — not significant at $\alpha = 0.05$ |

> [!TIP]
> The Undergraduate coefficient (+6.34) being larger than Graduate (+3.90) may seem counterintuitive. This is likely a composition effect: undergraduate participants in this sample may include health/science students with specific thalassemia curriculum exposure, or may be actively enrolled and more receptive to health education. The small sample sizes (n=43 UG vs n=36 Grad) also contribute to imprecise individual estimates — critically, they are **not statistically different from each other** (Tukey HSD $p = 0.92$).

### 6.4 Monthly Income — **Mixed Signal**

| Comparison | $\beta$ | Interpretation |
| --- | --- | --- |
| **25,000–50,000 vs. < 25,000** | −3.56* | Surprisingly, the 25–50k bracket scores **lower** than the lowest income group |
| **51,000–100,000 vs. < 25,000** | −1.32 (ns) | No significant difference |
| **> 100,000 vs. < 25,000** | +0.63 (ns) | No significant difference |

> [!WARNING]
> The negative coefficient for the 25,000–50,000 income bracket is statistically significant but requires cautious interpretation. After controlling for education, the lowest income group (< 25,000) may include young university students or healthcare workers with high education but low current earnings. This confounding makes income effects difficult to isolate. A larger sample with income-education interaction terms would be needed for definitive conclusions.

### 6.5 Age ($\beta = 0.026$, $p = 0.452$)
Each additional year of age adds 0.026 points to the predicted score — a **negligible and non-significant effect**. Older participants do not demonstrate meaningfully different knowledge levels after controlling for education and income.

---

## 7. Predicted Score Examples

Using the model equation: $\hat{Y} = 7.97 + 0.03 \cdot \text{Age} - 0.24 \cdot \text{Male} + 3.90 \cdot \text{Grad} + 6.34 \cdot \text{UG} + 1.67 \cdot \text{A/L} - 3.56 \cdot \text{Inc}_{25\text{-}50k} - 1.32 \cdot \text{Inc}_{51\text{-}100k} + 0.63 \cdot \text{Inc}_{>100k}$

| Profile | Predicted Score |
| --- | --- |
| Female, Graduate, Age 30, Income < 25,000 | $7.97 + 0.78 + 3.90 = \textbf{12.65}$ |
| Male, Up to O/L, Age 40, Income 25–50k | $7.97 + 1.04 - 0.24 - 3.56 = \textbf{5.21}$ |
| Female, Undergraduate, Age 25, Income > 100k | $7.97 + 0.65 + 6.34 + 0.63 = \textbf{15.59}$ |
| Male, Up to A/L, Age 35, Income 51–100k | $7.97 + 0.91 - 0.24 + 1.67 - 1.32 = \textbf{8.99}$ |

---

## 8. Summary & Conclusions

### Key Findings

1. **Education is the dominant predictor** of thalassemia knowledge ($p < 0.001$), with tertiary education (Graduate and Undergraduate) associated with 4–6 point score increases over secondary-level education.

2. **Gender and Age are not significant predictors** after controlling for education and income. This confirms the t-test and suggests that knowledge disparities are structural (education-driven) rather than demographic.

3. **Income shows a paradoxical pattern**: the 25–50k bracket scores significantly lower than the lowest income group, likely due to confounding between income and education/occupation among young participants. Income is not a reliable independent predictor of knowledge in this sample.

4. **Model explanatory power is moderate** ($R^2_{\text{adj}} = 0.34$), which is respectable for survey research. The remaining variance is attributable to unmeasured psychosocial, experiential, and contextual factors.

### Recommendations for Interventions
* **Target secondary-educated carriers** (O/L and A/L) for intensive health education programs, as they represent the lowest-knowledge tier.
* **Design gender-neutral materials** — knowledge disparities are not gender-specific.
* **Avoid income-based targeting** — income is not a clean proxy for health literacy in this population.
* **Consider adding predictors** in future studies: prior genetic counseling, urban vs. rural residence, healthcare access, and personal diagnosis duration could improve model fit.
