# KAP Model Chi-Square Tests
**Categorical Cutoff Analysis (Knowledge, Attitude, Practice)**

We mapped the continuous scoring data into binary categorical brackets (e.g. "High" vs "Low") to perform strict $2 \times 2$ Chi-Square tests of independence. 

### Cutoff Definitions (Median Split Approach)
* **Knowledge Cutoff:** 2.682
* **Partner Attitude Cutoff:** 1.408
* **Cascade Attitude Cutoff:** 0.886
* **Partner Practice:** "Good" = Screened before marriage. "Poor" = Screened after/pregnancy or did not screen.
* **Cascade Practice Cutoff:** Score > 1.0 = "Good Practice", <= 1.0 = "Poor Practice".

---

### Knowledge vs Partner Attitude
```
P_Attitude_Cat  Good Attitude  Poor Attitude
Knowledge_Cat                               
High Knowledge             60             40
Low Knowledge              35             66
```

* **Chi-Square Statistic:** 11.955
* **P-Value:** 0.0005
* **Conclusion:** **Statistically Significant Correlation (p < 0.05).**
---

### Knowledge vs Cascade Attitude
```
C_Attitude_Cat  Good Attitude  Poor Attitude
Knowledge_Cat                               
High Knowledge             54             46
Low Knowledge              42             59
```

* **Chi-Square Statistic:** 2.627
* **P-Value:** 0.1051
* **Conclusion:** **Not Statistically Significant (p > 0.05).**
---

### Knowledge vs Partner Practice
```
P_Practice_Cat  Good Practice  Poor Practice
Knowledge_Cat                               
High Knowledge             14             26
Low Knowledge               7             36
```

* **Chi-Square Statistic:** 2.916
* **P-Value:** 0.0877
* **Conclusion:** **Not Statistically Significant (p > 0.05).**
---

### Knowledge vs Cascade Practice
```
C_Practice_Cat  Good Practice  Poor Practice
Knowledge_Cat                               
High Knowledge             46             54
Low Knowledge              44             57
```

* **Chi-Square Statistic:** 0.042
* **P-Value:** 0.8373
* **Conclusion:** **Not Statistically Significant (p > 0.05).**
---

### Partner Attitude vs Partner Practice
```
P_Practice_Cat  Good Practice  Poor Practice
P_Attitude_Cat                              
Good Attitude              14             22
Poor Attitude               7             40
```

* **Chi-Square Statistic:** 5.006
* **P-Value:** 0.0253
* **Conclusion:** **Statistically Significant Correlation (p < 0.05).**
---

### Cascade Attitude vs Cascade Practice
```
C_Practice_Cat  Good Practice  Poor Practice
C_Attitude_Cat                              
Good Attitude              54             42
Poor Attitude              36             69
```

* **Chi-Square Statistic:** 8.916
* **P-Value:** 0.0028
* **Conclusion:** **Statistically Significant Correlation (p < 0.05).**
---
