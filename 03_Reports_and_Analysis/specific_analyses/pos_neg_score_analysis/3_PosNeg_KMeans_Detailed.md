# Detailed Analysis: K-Means Clustering on Pos/Neg Scores

A K-Means algorithm ($k=3$) was deployed on the penalized Positive/Negative scores to objectively categorize the participants into three knowledge tiers.

![PosNeg K-Means](charts/PosNeg_KMeans_Clusters.png)

### Cluster Psychology & Medical Implications
With negative penalties applied, the K-Means algorithm naturally separated the cohort based on the severity of their misconceptions:

1. **Low Knowledge (Red / Negative Tier):** 
   - **Characteristics:** This cluster is dominated by participants who guessed incorrectly frequently or lacked basic knowledge entirely. 
   - **Implication:** This group requires urgent, targeted medical education to unlearn dangerous myths (such as transmission vectors or false cures).
   
2. **Medium Knowledge (Orange / Moderate Tier):**
   - **Characteristics:** Participants who understand the foundational basics of thalassemia (e.g., inherited, requires screening) and avoided guessing incorrectly on the complex medical questions.
   
3. **High Knowledge (Green / Expert Tier):**
   - **Characteristics:** This elite cluster successfully identified complex medical complications (iron overload, endocrine issues) and possessed almost zero misconceptions. They achieved high positive scores without accumulating negative penalties.
