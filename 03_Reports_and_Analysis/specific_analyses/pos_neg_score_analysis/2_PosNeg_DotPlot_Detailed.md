# Detailed Analysis: Positive/Negative Scores Dot Plot

This dot plot maps the 201 participants from lowest to highest score using the strict +1/-1 penalty method.

![PosNeg Dot Plot](charts/PosNeg_Score_DotPlot.png)

### Interpretation Guide
- **Visualizing Misconceptions:** By sorting the scores linearly, the true impact of negative penalties becomes visually striking. We can clearly identify the exact percentile of the cohort that falls below the zero line. 
- **Elimination of Plateaus:** In earlier raw scoring models, massive flat plateaus formed because participants tied with the same integer scores. The penalty method shatters these plateaus. Participants who got 5 right and 0 wrong score a 5, but participants who got 7 right and 2 wrong also score a 5. This dynamic scoring introduces much greater mathematical variance and a smoother curve.
- **The High-Knowledge Tier:** The steep vertical rise on the far right demonstrates that the truly knowledgeable outliers (scoring 8 to 10) are mathematically separated from those who guessed their way to a high raw score.
