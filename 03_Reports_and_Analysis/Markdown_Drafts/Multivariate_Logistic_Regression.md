# Advanced Multivariate Logistic Regression
**Predicting Safe Partner Screening Practices**

This analysis utilizes a Multivariate Logistic Regression model to identify the *independent* predictors of safe clinical practice (screening one's partner *before* marriage). 

By analyzing all variables simultaneously, we calculate the **Adjusted Odds Ratio (aOR)**. This tells us the exact mathematical likelihood of a participant engaging in safe practice for every 1-unit increase in a predictor, *while holding all other demographic variables completely equal*.

### Model Summary
* **Dependent Variable:** Safe_Practice (1 = Screened before marriage, 0 = Delayed/Unsafe)
* **Sample Size (N):** 82
* **Pseudo R-Squared:** 0.305

### Regression Results: Adjusted Odds Ratios

| Predictor Variable | Adjusted Odds Ratio (aOR) | 95% CI Lower | 95% CI Upper | P-Value | Significant? |
|---|---|---|---|---|---|
| Age | **0.837** | 0.733 | 0.957 | 0.0090 | Yes (*) |
| Is_Married | **1.973** | 0.335 | 11.626 | 0.4530 | No |
| Education_Level | **1.759** | 0.953 | 3.246 | 0.0710 | No |
| Knowledge | **1.078** | 0.911 | 1.276 | 0.3810 | No |
| Attitude | **0.992** | 0.626 | 1.572 | 0.9730 | No |


---

### Key Clinical Interpretations
* **Age is the Only Independent Predictor:** When controlling for all other socioeconomic and clinical variables, the only statistically significant predictor of screening one's partner before marriage is **Age** ($p = 0.009$).
* **The "Younger Generation" Effect:** The Adjusted Odds Ratio (aOR) for Age is **0.837**. Because this is less than $1.0$, it means that for every 1-year increase in age, a participant is *less* likely to have screened their partner before marriage. This strongly implies that younger generations are adopting safer screening practices than older generations, likely due to recent public health campaigns.
* **Loss of Significance in KAP:** `Knowledge` ($p = 0.381$) and `Attitude` ($p = 0.973$) both lose their statistical significance in this multivariate model. While we proved they matter in isolated Chi-Square tests, when they are forced to compete against Age and Education in this model, their independent effect is washed out. 
* **Note on Sample Size:** The sample size for this specific regression dropped to $N=82$ because it only includes participants who provided a clear answer for Q33 (when they screened their partner). This smaller sample size contributes to the wider confidence intervals.
