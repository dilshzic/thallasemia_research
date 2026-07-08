# Thalassemia Research: Updated Attitude Scoring Schemas

This document outlines the advanced scoring logic implemented during the attitude calculation refinements. It details the multi-tiered integer assignments and the inverse-frequency probability weighting applied to Partner Selection and Cascade Screening.

---

## 1. The V2 / V3 Penalty Schema
Unlike early scoring phases which simply awarded +1 for any positive attitude, this updated methodology applies a stretched Likert-style scale. It heavily penalizes dangerous medical attitudes (e.g., -3) while rewarding highly protective attitudes (e.g., +2). This shatters statistical "ceiling effects" and creates continuous data distributions.

### A. Partner Selection Attitudes
*(Note: Q34 was removed in V3 as it represented a barrier/practice rather than a pure attitude).*

* **Q28: What should a carrier do after diagnosis?**
  * `Get the partner tested before marriage` **(+2)**
  * `Get family members tested` **(+1)**
  * `I don't know` **(0)**
  * `Ignore it` **(-3)**
* **Q30: Are you willing to / Do you have a consanguineous marriage?**
  * `Definitely not` **(+2)**
  * `Not sure` **(-1)**
  * `Yes I am willing` or `Yes I have` **(-3)**
* **Q31: Do you accept marriage between two thalassemia carriers?**
  * `No` **(+2)**
  * `Not sure` **(-1)**
  * `Yes` **(-3)**
* **Q32: How important is thalassemia screening before marriage?**
  * `Very important` **(+2)**
  * `Important` **(+1)**
  * `Not sure` **(-1)**
  * `Not important` **(-2)**

### B. Cascade Screening Attitudes
*(Note: Q36 was removed in V3 as it is a practice metric, not an attitude).*

* **Q35: Is it important for your family members to undergo screening?**
  * `Agree` **(+2)**
  * `Don't know` **(0)**
  * `Disagree` **(-2)**
* **Q39: How easy is it to convince relatives to undergo screening?**
  * `Very easy` **(+2)**
  * `Somewhat easy` **(+1)**
  * `Not sure` **(0)**
  * `Difficult` **(-1)**
* **Q40: How important is cascade screening in thalassemia prevention?**
  * `Very important` **(+2)**
  * `Important` **(+1)**
  * `Slightly important` **(-1)**
  * `Not important` **(-2)**

---

## 2. The "Weighted V3" Schema (Cross-Question Inverse Frequency)
To make the data mathematically robust against extremely common baseline responses, the **Weighted V3** schema applies probability calculus on top of the assigned integer weights.

### Mathematical Formula:
$$ \text{Final Score} = \text{Assigned Weight} \times (1 - p) $$
*(Where $p$ is the proportion of the total 201 participants who selected that exact answer).*

### Psychological Implication:
1. **Common Protective Attitude:** If a participant selects "Definitely not" for consanguineous marriage (+2 weight) and 85% of the cohort also selected it ($p=0.85$), their reward is scaled down: `+2 * 0.15 = +0.30`. They are rewarded, but only slightly, because this attitude is medically expected.
2. **Rare Dangerous Misconception:** If a participant selects "Yes" to consanguineous marriage (-3 penalty weight) and only 5% of the cohort selected it ($p=0.05$), their penalty remains massive: `-3 * 0.95 = -2.85`.

By applying this calculus, the algorithm creates a highly sensitive, truly continuous spectrum that perfectly isolates dangerous medical outliers for targeted educational intervention.
