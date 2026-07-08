# Weighted V3 Knowledge Scoring Analysis

This report visualizes the participants' Knowledge scores combining the V3 Penalty Schema with the statistical $(1-p)$ inverse-frequency calculation.

### Methodological Context
Formula: `Final Score = Assigned_Weight * (1 - p)`

By scaling the assigned penalties (+2 down to -3) by the proportion of the cohort that gave the answer, we mathematically reward statistically rare knowledge (e.g. knowing the exact transmission genetics) and massively penalize statistically rare, dangerous misconceptions. Common knowledge is scaled down closer to 0, representing the "expected baseline."

### The Distribution
Because most basic knowledge facts were widely known by the cohort, the positive scores were heavily scaled down, causing the bulk of the distribution to center tightly near the low positives. However, the dangerous misconceptions remained incredibly rare, meaning their heavy penalties (-3) stayed intact and pulled the lower tail far into the negatives.

![Distribution of Weighted V3 Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_weighted_v3/Weighted_V3_Knowledge_Dist.png)
![Dot Plot of Weighted V3 Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_weighted_v3/Weighted_V3_Knowledge_DotPlot.png)

---

### K-Means Clustering (k=3)
The K-Means algorithm effectively isolated the highly penalized individuals into the Negative/Low cluster. The Neutral/Medium cluster represents participants who simply possessed the expected baseline knowledge (scoring close to 0 due to the scaling), while the Positive/High cluster represents participants with deep, rare clinical knowledge.

![K-Means Clusters](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_weighted_v3/Weighted_V3_Knowledge_KMeans.png)
