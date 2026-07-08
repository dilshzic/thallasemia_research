# K-Means Knowledge Score Clustering

A 1D K-Means clustering algorithm ($k=3$) was applied to the `Weighted_Knowledge_Score` of all 201 participants. This algorithm objectively divided the participants into three distinct knowledge tiers based on proximity to the cluster centers.

![K-Means Clusters](charts/KMeans_Clusters.png)

### Cluster Assignments
1. **Low Knowledge (Red):** 
   - **Cluster Center:** ~1.41
   - **Description:** These participants only answered the easiest questions correctly and missed almost all of the multiple-choice medical specifics.
2. **Medium Knowledge (Orange):**
   - **Cluster Center:** ~3.40
   - **Description:** This cluster represents the average participant. They knew the basics (like inheritance and prevention) but missed the rare facts and deeper clinical complications.
3. **High Knowledge (Green):**
   - **Cluster Center:** ~6.74
   - **Description:** This elite cluster contains the highly knowledgeable outliers (including the top participant scoring 10.3) who correctly identified rare statistics and complex medical treatments.
