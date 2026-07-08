# New Partner Selection Attitude Analysis (v2)

This report visualizes the Partner Selection attitudes after recalculating the scores using the updated, multi-tiered penalty schema (introducing weights ranging from +2 down to -2 for specific answers).

### The New Distribution
Because the new schema includes heavier penalties (-2) and stronger rewards (+2), the range of possible scores has expanded drastically. This successfully broke the "ceiling effect" seen in the earlier analysis, allowing the cohort to spread out far more naturally.

![Distribution of New Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2/New_Partner_Dist.png)

![Dot Plot of New Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2/New_Partner_DotPlot.png)

---

### K-Means Clustering (k=3)
With the new spread of data, the clustering algorithm successfully partitioned the cohort into three very distinct sentiment tiers. The zero line (Neutral) perfectly separates the negative cluster from the positive ones.

1. **Positive/High (Green):** Participants who consistently chose the most protective attitudes (+2 and +1).
2. **Neutral/Medium (Orange):** Participants who had mixed feelings, or frequently answered "Not sure" (0).
3. **Negative/Low (Red):** Participants whose scores were pulled into the negatives due to dangerous attitudes (-1 and -2 penalties, such as willingness for consanguineous marriage).

![K-Means Clusters](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2/New_Partner_KMeans.png)
