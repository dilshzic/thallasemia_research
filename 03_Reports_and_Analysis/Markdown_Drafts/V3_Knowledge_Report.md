# V3 Knowledge Scoring Analysis

This report visualizes the participants' Knowledge scores after applying the newly proposed V3 schema.

### Methodological Context
Unlike early scoring phases which simply awarded +1 for any positive answer, this updated methodology applies a stretched Likert-style scale ranging from +2 to -3. It heavily penalizes dangerous medical misconceptions (e.g., believing the disease is contagious, or thinking it can be cured with common treatments). Crucially, because this cohort consists entirely of diagnosed carriers, answering "I don't know" to vital clinical facts is actively penalized as a medical danger.

### The Distribution
The heavy penalties effectively isolate participants with dangerous misconceptions, creating a much wider, more continuous numerical spectrum. 

![Distribution of V3 Knowledge Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_v3/V3_Knowledge_Dist.png)
![Dot Plot of V3 Knowledge Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_v3/V3_Knowledge_DotPlot.png)

---

### K-Means Clustering (k=3)
With the mathematical variance increased, K-Means successfully separated the cohort into three distinct clinical knowledge tiers. The zero line flawlessly demarcates the boundary between those who hold generally positive knowledge and those burdened with dangerous misconceptions or lack of basic awareness.

![K-Means Clusters](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/knowledge_v3/V3_Knowledge_KMeans.png)
