import os
import subprocess

out_dir = "/home/dilshan/Desktop/Thallasemia research"

md_content = """---
title: "Scoring Methodology: Knowledge, Attitudes, and Practices (KAP)"
---

# Scoring Methodology

This document outlines the detailed mathematical and logical schema used to calculate the Knowledge, Attitude, and Practice scores for the Thalassemia study cohort.

## 1. Expanded Knowledge Score (Continuous, Max 20 Points)

The **Expanded Knowledge Score** is constructed as a composite metric of correct answers across all 11 knowledge questions in the survey. Participants receive points for correctly identifying facts and selecting valid multiple-choice options.

| Question | Concept Tested | Correct Answer Criteria | Points |
| :--- | :--- | :--- | :--- |
| **Q15** | Disease Nature | Selects `Yes` (Blood-related) | 1 |
| **Q16** | Clinical Forms | Sum of checked correct forms (Major, Minor, Intermedia) | 0 to 3 |
| **Q17** | Severity | Selects `Thalassemia major (severe form)` | 1 |
| **Q19** | Lifelong Treatment | Selects `Yes` | 1 |
| **Q20** | Curability | Selects `Very difficult (e.g., bone marrow transplant)` or `Cannot be cured` | 1 |
| **Q21** | Preventability | Selects `Can be prevented` | 1 |
| **Q22** | Transmission | Selects `From generation to generation (hereditary)` | 1 |
| **Q23** | Carrier Health | Selects `Healthy` | 1 |
| **Q24** | Genetic Probability | Selects `Has a chance to be affected (e.g., 25%)` | 1 |
| **Q26** | Epidemiology | Selects `40–100` births per year | 1 |
| **Q27** | Complications | Sum of checked correct complications (8 possible options) | 0 to 8 |
| **Total** | | | **Max 20** |

---

## 2. Attitude Scores (Categorical / Continuous)

Attitude scores use a weighted penalty system. Proactive and responsible attitudes receive positive points, while dangerous misconceptions or harmful attitudes receive negative penalties.

### 2.1 Partner Screening Attitude
This score aggregates attitudes toward screening a prospective partner.

* **Q28: Action after diagnosis**
  * `Get the partner tested` -> **+1**
  * `Get family members tested` -> **+1**
  * `Ignore it` -> **-2**
* **Q30: Willingness for consanguineous marriage**
  * `Definitely Not` -> **+1**
  * `Not Sure` -> **-1**
  * `Yes I am willing` / `Yes I have` -> **-2**
* **Q31: Accept marriage between two carriers**
  * `No` -> **+1**
  * `Yes` -> **-1**
* **Q32: Importance of pre-marital screening**
  * `Very Important` -> **+2**
  * `Important` -> **+1**
  * `Not Important` -> **-1**
* **Q34: Harmful reasons for non-disclosure**
  * `Lack of understanding`, `Not necessary`, or `Causing worry` -> **-1**

### 2.2 Cascade Screening Attitude
This score aggregates attitudes toward disclosing status to family members.

* **Q35: Importance of family screening**
  * `Agree` -> **+1**
  * `Disagree` -> **-1**
* **Q36: Comfort with family status disclosure**
  * `Yes` -> **+1**
  * `No` -> **-1**
* **Q40: Importance of cascade screening**
  * `Very Important` -> **+2**
  * `Important` -> **+1**
  * `Not Important` -> **-1**

---

## 3. Practice Scores (Categorical / Continuous)

Practice scores measure the actual behavioral actions taken by the participants.

### 3.1 Partner Screening Practice (Categorical)
This categorizes the timing and safety of partner screening behaviors:
* **Safe**: Screened *before* marriage.
* **Delayed**: Screened *after* marriage or during pregnancy.
* **Unsafe**: Did *not* screen, or did *not* disclose status to the partner.

### 3.2 Cascade Practice Score (Continuous, Max 6 Points)
This measures the extent to which a participant convinced their extended family to undergo screening.
* **First-degree relatives**: `All` (+2), `Some` (+1), `None` (0)
* **Second-degree relatives**: `All` (+2), `Some` (+1), `None` (0)
* **Third-degree relatives**: `All` (+2), `Some` (+1), `None` (0)
* **Total Possible Score**: **Max 6**
"""

md_path = os.path.join(out_dir, "Scoring_Methodology.md")
docx_path = os.path.join(out_dir, "Scoring_Methodology.docx")

with open(md_path, "w") as f:
    f.write(md_content)

try:
    subprocess.run(["pandoc", md_path, "-o", docx_path], check=True)
    print(f"Successfully generated {docx_path}")
    if os.path.exists(md_path):
        os.remove(md_path)
except subprocess.CalledProcessError as e:
    print(f"Error generating document: {e}")
