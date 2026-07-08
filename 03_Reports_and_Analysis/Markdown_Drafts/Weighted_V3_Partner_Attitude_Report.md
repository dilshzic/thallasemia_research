# Weighted V3 Partner Selection Attitude Analysis

This report visualizes the Partner Selection attitudes using the cross-question statistical weighting $(1-p)$ combined with the optimized V3 schema.

### Methodology
Formula Used: `Score = Assigned_Weight * (1 - p)`
Where `p` is the proportion of participants who gave that exact answer. 
- **Rare Protective Attitudes:** Heavy reward (e.g., `+2 * High`).
- **Common Protective Attitudes:** Small reward (e.g., `+2 * Low`).
- **Rare Dangerous Attitudes:** Heavy penalty (e.g., `-3 * High`).

### The Distribution
Because the vast majority of participants gave protective answers (high `p`), the rewards shrank dramatically. The distribution squashes closer to zero, but the dangerous outliers (who received heavy penalties because dangerous answers were rare) pull the graph strongly into the negative territory.

![Distribution of Weighted V3 Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_weighted_v3/Weighted_V3_Partner_Dist.png)
![Dot Plot of Weighted V3 Scores](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_weighted_v3/Weighted_V3_Partner_DotPlot.png)

---

### K-Means Clustering (k=3)
The K-Means algorithm effectively isolated the highly penalized individuals into the Negative/Low cluster. 

![K-Means Clusters](/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_weighted_v3/Weighted_V3_Partner_KMeans.png)
