# New Cascade Screening Attitude Analysis (v2)

This report visualizes the Cascade Screening attitudes after recalculating the scores using the updated schema (+1 for positive answers, 0 for neutral, and -1 for negative answers on Q35, Q36, and Q40).

### The New Distribution
Because this schema assigns explicit negative penalties for undesirable attitudes (like "Disagree" or "No"), we can accurately see exactly how many participants hold negative views toward family screening. 

![Distribution of New Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2/New_Cascade_Dist.png)

![Dot Plot of New Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2/New_Cascade_DotPlot.png)

---

### K-Means Clustering (k=3)
The new K-Means clustering perfectly separated the cohort. You can see how clearly the zero-line divides the groups:

1. **Positive/High (Green):** Participants who recognize the importance of cascade screening and ensure their family is aware.
2. **Neutral/Medium (Orange):** Participants whose scores hovered around 0 to 1, indicating mixed feelings or a lack of strong opinions.
3. **Negative/Low (Red):** The outlier group whose scores fell into negative territory due to actively disagreeing with screening importance or hiding their status.

![K-Means Clusters](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2/New_Cascade_KMeans.png)
