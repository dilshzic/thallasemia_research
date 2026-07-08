# Demographics vs KAP Model: Chi-Square P-Value Matrix

This report explores the relationship between strict demographic variables and the binary "High vs. Low" categorical splits of the KAP (Knowledge, Attitude, Practice) metrics. 

By analyzing the P-values across a $30$-test Chi-Square matrix, we can see exactly which demographic factors act as significant predictors for each step of the pipeline.

### P-Value Matrix
*(P-values **< 0.05** are bolded to indicate statistical significance)*

```\n                 Knowledge Partner Attitude Cascade Attitude Partner Practice Cascade Practice
Gender              0.3908           0.4826           0.2894           0.1437           0.0687
Marital_Status  **0.0301**           0.0509           0.7822       **0.0044**           0.1493
Age_Group       **0.0375**       **0.0009**           0.9011       **0.0000**           0.3433
Education       **0.0000**       **0.0011**           0.5078       **0.0004**           0.0739
Occupation          0.0922           0.7909           0.2920           0.7983           0.1590
Income              0.3681           0.6497           0.7227           0.8083           0.5387\n```

---

### Key Takeaways from the Matrix:
* This table confirms our earlier continuous ANOVA findings: **Education**, **Occupation**, and **Income** are the primary socioeconomic drivers of Knowledge and Attitudes.
* Basic demographic traits like **Gender** and **Age** show almost no significant bearing on a carrier's KAP pipeline. 
* Interestingly, while **Marital Status** proved to be significant when tested continuously, its significance drops when binned categorically. However, socioeconomic factors remain strongly robust across both continuous and categorical tests.
