# Weighted V3 Attitude Scoring: Mathematical Breakdown

This document provides the exact mathematical calculations used to determine the final score for every single participant response in the "Weighted V3" attitude analysis. 

The algorithm uses an inverse-frequency probability calculation to scale the rewards and penalties.

### Mathematical Formula:
`Final Weighted Score = Assigned Weight * (1 - p)`
*(Where **p** is the proportion of the 201 participants who gave that exact answer).*

---

### Q28. What should a thalassemia carrier do after diagnosis? (Tick all that apply)
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| Get The Partner Tested Before Marriage | 2 | 0.791 | 0.209 | **0.418** |
| Get Family Members Tested | 1 | 0.786 | 0.214 | **0.214** |
| I Don't Know | 0 | 0.075 | 0.925 | **0.000** |
| Ignore It | -3 | 0.000 | 1.000 | **-3.000** |

### Q30. Are you willing to / Do you have a consanguineous marriage?
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| Definitely Not | 2 | 0.796 | 0.204 | **0.408** |
| Not Sure | -1 | 0.174 | 0.826 | **-0.826** |
| Yes I Am Willing | -3 | 0.015 | 0.985 | **-2.955** |
| Yes I Have | -3 | 0.010 | 0.990 | **-2.970** |

### Q31. Do you accept marriage between two thalassemia carriers?
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| No | 2 | 0.935 | 0.065 | **0.129** |
| Not Sure | -1 | 0.164 | 0.836 | **-0.836** |
| Yes | -3 | 0.050 | 0.950 | **-2.851** |

### Q32. How important is thalassemia screening before marriage?
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| Very Important | 2 | 0.672 | 0.328 | **0.657** |
| Important | 1 | 0.925 | 0.075 | **0.075** |
| Not Sure | -1 | 0.065 | 0.935 | **-0.935** |
| Not Important | -2 | 0.020 | 0.980 | **-1.960** |

### Q35. Do you think is it important for your family members to undergo screening?
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| Agree | 2 | 0.970 | 0.030 | **0.060** |
| Don't Know | 0 | 0.025 | 0.975 | **0.000** |
| Disagree | -2 | 0.020 | 0.980 | **-1.960** |

### Q39. How easy is it to convince relatives to undergo screening?
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| Very Easy | 2 | 0.144 | 0.856 | **1.711** |
| Somewhat Easy | 1 | 0.463 | 0.537 | **0.537** |
| Not Sure | 0 | 0.164 | 0.836 | **0.000** |
| Difficult | -1 | 0.189 | 0.811 | **-0.811** |

### Q40. How important is cascade screening in thalassemia prevention?
| Answer Option | Assigned Weight (V3) | Proportion (p) | Multiplier (1-p) | **Final Weighted Score** |
|---|---|---|---|---|
| Very Important | 2 | 0.587 | 0.413 | **0.826** |
| Important | 1 | 0.985 | 0.015 | **0.015** |
| Slightly Important | -1 | 0.040 | 0.960 | **-0.960** |
| Not Important | -2 | 0.010 | 0.990 | **-1.980** |
