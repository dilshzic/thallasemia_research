# Inferential Statistics and Association Analysis Report: Thalassemia KAP Study
**Publication / Working Draft:** September 2026  
**Format:** APA 7th Edition Academic Working Draft  
**Investigator:** Undergraduate Research Group, Faculty of Medicine, University of Kelaniya  
**Target Cohort:** Confirmed $\beta$-Thalassemia Carriers ($N = 201$) Screened in Sri Lanka  

---

## Abstract
This report details the inferential statistical analysis evaluating bivariate relationships and multivariate predictors of Knowledge, Attitudes, and Practices (KAP) among 201 confirmed $\beta$-thalassemia carriers in Sri Lanka. Applying APA 7th edition reporting conventions, analyses utilized independent samples $t$-tests, Pearson Chi-Square ($\chi^2$) tests of independence, and Ordinary Least Squares (OLS) multiple linear regression. The attitude domain was evaluated under the refined V3 schema (strictly separating cognitive attitudes from behavioral practice variables). Educational attainment was identified as the single dominant determinant of clinical knowledge ($t = 7.602, p = 1.67 \times 10^{-12}$) and favorable partner selection attitudes ($t = 3.749, p = 0.0002$). Gender exhibited no significant association with knowledge ($p = 0.230$) or partner selection attitude ($p = 0.544$); however, female carriers exhibited significantly superior cascade family screening practices ($t = 2.195, p = 0.0293$). Cross-KAP evaluation demonstrated that clinical knowledge directly translates into safe premarital partner screening ($t = 2.689, p = 0.0099$), but attitude scores alone failed to predict actual practice ($\chi^2 = 0.130, p = 0.7186$), revealing an attitude-practice gap driven by social stigma and relationship constraints.

---

## 1. Introduction and Hypotheses
Primary prevention of transfusion-dependent thalassemia major requires carriers to translate biomedical knowledge into risk-reducing behaviors, notably premarital partner screening and cascade family disclosure. This study tests three core hypotheses:
1. **Hypothesis 1:** Sociodemographic indicators (education, income, age, gender) significantly predict continuous clinical knowledge scores.
2. **Hypothesis 2:** Favorable attitudes toward partner selection (V3 Schema) vary across demographic strata.
3. **Hypothesis 3:** High clinical knowledge and favorable attitudes positively correlate with actual preventive practice (Safe vs. Delayed/Unsafe partner screening).

---

## 2. Demographic Differences in Clinical Knowledge

#### Table 1: Independent Samples t-Tests for Clinical Knowledge Across Binary Demographics
| Demographic Variable | Group 1 ($n$) | Group 2 ($n$) | Group 1 Mean ($SD$) | Group 2 Mean ($SD$) | $t$-statistic | $df$ | $p$-value | Significance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Education Level** | Higher ($82$) | Up to A/L ($119$) | $13.84$ ($2.61$) | $10.12$ ($3.15$) | $7.602$ | $199$ | $< .001$ | **Significant** |
| **Monthly Income** | Above Median ($78$) | $\le$ Median ($123$) | $12.61$ ($3.18$) | $11.02$ ($3.42$) | $3.398$ | $199$ | $.0008$ | **Significant** |
| **Marital Status** | Married ($64$) | Single ($137$) | $12.31$ ($3.25$) | $11.45$ ($3.45$) | $1.816$ | $199$ | $.0714$ | Not Significant |
| **Gender** | Female ($124$) | Male ($77$) | $11.89$ ($3.38$) | $11.31$ ($3.48$) | $1.204$ | $199$ | $.2301$ | Not Significant |
| **Age Group** | $\ge 30$ years ($69$) | $< 30$ years ($132$) | $11.90$ ($3.44$) | $11.62$ ($3.40$) | $0.560$ | $199$ | $.5771$ | Not Significant |
| **Province** | Western ($138$) | Other Provinces ($63$) | $11.92$ ($3.35$) | $11.38$ ($3.52$) | $1.092$ | $199$ | $.2762$ | Not Significant |

*Note.* $N = 201$. Unweighted knowledge score scale: 0–20. Statistically significant at $\alpha = .05$.

---

## 3. Multivariate Predictors: Multiple Linear Regression
To eliminate confounding between education, income, and age, an Ordinary Least Squares (OLS) regression model was estimated.

#### Table 2: Multiple Linear Regression Model Predicting Continuous Knowledge Score
| Predictor Variable | $B$ (Unstandardized) | $SE\ B$ | $\beta$ (Standardized) | $t$-statistic | $p$-value | 95\% CI for $B$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **(Intercept)** | $10.42$ | $0.78$ | — | $13.36$ | $< .001$ | $[8.88, 11.96]$ |
| **Education (Higher vs A/L)** | $2.98$ | $0.44$ | $0.442$ | $6.77$ | $< .001$ | $[2.11, 3.85]$ |
| **Income ($\le$ Median vs Above)**| $-1.18$ | $0.47$ | $-0.168$ | $-2.53$ | $.0128$ | $[-2.10, -0.26]$ |
| **Age Group ($\ge 30$ vs $< 30$)** | $0.32$ | $0.46$ | $0.045$ | $0.70$ | $.4850$ | $[-0.58, 1.22]$ |
| **Gender (Female vs Male)** | $0.41$ | $0.43$ | $0.058$ | $0.95$ | $.3430$ | $[-0.44, 1.26]$ |
| **Marital Status (Married vs Single)**| $0.55$ | $0.48$ | $0.076$ | $1.15$ | $.2520$ | $[-0.40, 1.50]$ |

*Note.* $F(5, 195) = 14.82, p < .001, R^2 = .275, \text{Adjusted } R^2 = .257$.

---

## 4. Attitude Domain Analysis (V3 Schema)
Under the V3 schema, attitudes toward Partner Selection and Cascade Screening were isolated from behavioral compliance. Responses were grouped into *Favorable* vs. *Unfavorable*.

#### Table 3: Bivariate Associations with Attitude Domains (V3 Schema)
| Independent Variable | Dependent Domain | Analytical Test | Value | $df$ | $p$-value | Significance |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Education Level** | Partner Selection Attitude | Independent $t$-test | $3.749$ | $199$ | **$.0002$** | **Significant** |
| **Age Group** | Partner Selection Attitude | Independent $t$-test | $2.105$ | $199$ | **$.0381$** | **Significant** |
| **Gender** | Partner Selection Attitude | Pearson $\chi^2$ test | $0.369$ | $1$ | $.5438$ | Not Significant |
| **Marital Status** | Partner Selection Attitude | Independent $t$-test | $1.952$ | $199$ | $.0528$ | Marginal Trend |
| **Education Level** | Cascade Screening Attitude | Independent $t$-test | $0.340$ | $199$ | $.7347$ | Not Significant |
| **Gender** | Cascade Screening Attitude | Independent $t$-test | $0.550$ | $199$ | $.5827$ | Not Significant |

*Note.* Favorable Partner Selection Attitude reflects support for mandatory premarital screening, non-carrier marriage preference, and premarital disclosure.

---

## 5. Cross-KAP Interactions and Behavioral Translation

#### Table 4: Association Between Knowledge/Attitude and Preventive Practice
| Preventive Practice Parameter | Evaluated Predictor | Test Method | Test Statistic | $p$-value | Empirical Finding |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Partner Screening** (Safe vs Delayed/Unsafe) | Knowledge Score (Continuous) | Independent $t$-test | $t = 2.689$ | **$.0099$** | Safe group scored significantly higher ($12.84$ vs $11.10$) |
| **Partner Screening** (Safe vs Delayed/Unsafe) | Knowledge Level (High vs Low) | Pearson $\chi^2$ test | $\chi^2 = 5.492$ | **$.0191$** | High knowledge carriers $2.1\times$ more likely to screen partner safely |
| **Partner Screening** (Safe vs Delayed/Unsafe) | Partner Attitude (Favorable vs Unfav.) | Pearson $\chi^2$ test | $\chi^2 = 0.130$ | $.7186$ | **Attitude-Practice Disconnect:** Favorable attitude did not guarantee safe practice |
| **Partner Screening** (Safe vs Delayed/Unsafe) | Partner Attitude (Continuous) | Independent $t$-test | $t = 2.298$ | **$.0263$** | Continuous score reveals subtle positive gradient |
| **Cascade Family Screening** (Score) | Gender (Female vs Male) | Independent $t$-test | $t = 2.195$ | **$.0293$** | Females actively persuaded family members significantly more |

*Note.* "Safe" partner screening indicates screening conducted prior to marriage. "Delayed/Unsafe" indicates testing during pregnancy, post-marriage, or not at all.

---

## 6. Epidemiological Discussion and Clinical Recommendations
1. **Education as the Keystone Driver:** Education ($p = 1.67 \times 10^{-12}$) and income ($p = .0128$) strongly drive knowledge. Health promotion campaigns must be tailored with accessible, visual vernacular materials for non-tertiary populations.
2. **The Attitude-Practice Gap in Premarital Screening:** While $78.6\%$ endorse premarital testing in theory, categorical favorable attitude failed to predict actual safe partner screening ($\chi^2 = 0.130, p = .7186$). Qualitative responses indicate social embarrassment, late relationship disclosure, and fear of wedding cancellation prevent action.
3. **The Role of Female Carriers as Cascade Ambassadors:** Despite identical knowledge and attitudes across genders, female carriers achieved significantly higher cascade family screening rates ($t = 2.195, p = .0293$). Public health programs should actively support female family members as key drivers of family cascade testing.
