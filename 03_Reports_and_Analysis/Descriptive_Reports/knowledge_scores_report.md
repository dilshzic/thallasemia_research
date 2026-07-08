# Thalassemia Knowledge Scores & Z-Scores Report

This report documents the baseline clinical knowledge scores and standardized Z-scores calculated for all **201 participants** in the Thalassemia Research Questionnaire dataset.

## 1. Methodology: How Knowledge Scores Are Calculated

The composite **Knowledge Score** is engineered by summing the correct binary choices (where `1` indicates checked and `0` indicates unchecked) across two multi-select questions testing clinical pathology:

### A. Q16: Clinical Forms of Thalassemia
Points are awarded for correctly identifying any of the following clinical forms of the disease (excluding "I don't know"):
- Thalassemia major (severe form)
- Thalassemia minor or trait (carrier form)
- Thalassemia intermedia (moderate form)

### B. Q27: Problems & Complications of Thalassemia Major
Points are awarded for correctly identifying any of the secondary complications faced by patients:
- Regular blood transfusions for life
- Iron overload affecting heart and liver
- Delayed growth and puberty
- Risk of diabetes, infertility, and hormonal issues
- Risk of infections from transfusions
- Frequent nosebleeds
- Fatigue
- Bone deformities

The maximum theoretical score is **11** (3 from Q16 + 8 from Q27).

## 2. Methodology: How Z-Scores Are Calculated

A **Z-score** standardizes raw scores to indicate how many standard deviations a participant's score lies above or below the cohort's average score. The formula used is:

$$Z_i = \frac{X_i - \mu}{\sigma}$$

Where:
- $Z_i$ is the Z-score for participant $i$
- $X_i$ is the raw Knowledge Score for participant $i$
- $\mu$ is the cohort mean knowledge score: **`3.8109`**
- $\sigma$ is the cohort sample standard deviation ($N - 1$ degrees of freedom): **`2.5620`**

### Interpretation of Z-Scores
- **$Z = 0$**: The participant has perfectly average knowledge compared to the cohort.
- **$Z > 0$**: The participant's knowledge score is above the average (e.g., $Z = +1.5$ means 1.5 standard deviations above the mean).
- **$Z < 0$**: The participant's knowledge score is below the average.

## 3. Cohort Summary Statistics

| Statistic | Value |
| --- | --- |
| **Total Cohort Size ($N$)** | 201 |
| **Mean Knowledge Score ($\mu$)** | 3.8109 |
| **Standard Deviation ($\sigma$)** | 2.5620 |
| **Minimum Score** | 0 |
| **Maximum Score** | 11 |

## 4. Participant-by-Participant Calculated Scores

| Participant ID | Raw Knowledge Score | Z-Score |
| --- | --- | --- |
| 1 | 10 | 2.415669 |
| 2 | 1 | -1.097149 |
| 3 | 3 | -0.316523 |
| 4 | 11 | 2.805982 |
| 5 | 6 | 0.854417 |
| 6 | 2 | -0.706836 |
| 7 | 7 | 1.244730 |
| 8 | 5 | 0.464104 |
| 9 | 5 | 0.464104 |
| 10 | 0 | -1.487462 |
| 11 | 4 | 0.073791 |
| 12 | 0 | -1.487462 |
| 13 | 3 | -0.316523 |
| 14 | 1 | -1.097149 |
| 15 | 1 | -1.097149 |
| 16 | 5 | 0.464104 |
| 17 | 7 | 1.244730 |
| 18 | 3 | -0.316523 |
| 19 | 6 | 0.854417 |
| 20 | 2 | -0.706836 |
| 21 | 3 | -0.316523 |
| 22 | 6 | 0.854417 |
| 23 | 3 | -0.316523 |
| 24 | 1 | -1.097149 |
| 25 | 1 | -1.097149 |
| 26 | 4 | 0.073791 |
| 27 | 3 | -0.316523 |
| 28 | 2 | -0.706836 |
| 29 | 7 | 1.244730 |
| 30 | 3 | -0.316523 |
| 31 | 4 | 0.073791 |
| 32 | 3 | -0.316523 |
| 33 | 3 | -0.316523 |
| 34 | 1 | -1.097149 |
| 35 | 9 | 2.025356 |
| 36 | 3 | -0.316523 |
| 37 | 5 | 0.464104 |
| 38 | 7 | 1.244730 |
| 39 | 3 | -0.316523 |
| 40 | 4 | 0.073791 |
| 41 | 8 | 1.635043 |
| 42 | 8 | 1.635043 |
| 43 | 6 | 0.854417 |
| 44 | 5 | 0.464104 |
| 45 | 3 | -0.316523 |
| 46 | 5 | 0.464104 |
| 47 | 7 | 1.244730 |
| 48 | 2 | -0.706836 |
| 49 | 1 | -1.097149 |
| 50 | 3 | -0.316523 |
| 51 | 3 | -0.316523 |
| 52 | 2 | -0.706836 |
| 53 | 1 | -1.097149 |
| 54 | 3 | -0.316523 |
| 55 | 1 | -1.097149 |
| 56 | 8 | 1.635043 |
| 57 | 1 | -1.097149 |
| 58 | 1 | -1.097149 |
| 59 | 3 | -0.316523 |
| 60 | 8 | 1.635043 |
| 61 | 3 | -0.316523 |
| 62 | 5 | 0.464104 |
| 63 | 4 | 0.073791 |
| 64 | 3 | -0.316523 |
| 65 | 5 | 0.464104 |
| 66 | 1 | -1.097149 |
| 67 | 1 | -1.097149 |
| 68 | 3 | -0.316523 |
| 69 | 5 | 0.464104 |
| 70 | 2 | -0.706836 |
| 71 | 7 | 1.244730 |
| 72 | 5 | 0.464104 |
| 73 | 4 | 0.073791 |
| 74 | 3 | -0.316523 |
| 75 | 8 | 1.635043 |
| 76 | 8 | 1.635043 |
| 77 | 0 | -1.487462 |
| 78 | 3 | -0.316523 |
| 79 | 1 | -1.097149 |
| 80 | 8 | 1.635043 |
| 81 | 7 | 1.244730 |
| 82 | 2 | -0.706836 |
| 83 | 6 | 0.854417 |
| 84 | 4 | 0.073791 |
| 85 | 3 | -0.316523 |
| 86 | 0 | -1.487462 |
| 87 | 1 | -1.097149 |
| 88 | 5 | 0.464104 |
| 89 | 8 | 1.635043 |
| 90 | 1 | -1.097149 |
| 91 | 3 | -0.316523 |
| 92 | 3 | -0.316523 |
| 93 | 3 | -0.316523 |
| 94 | 3 | -0.316523 |
| 95 | 3 | -0.316523 |
| 96 | 3 | -0.316523 |
| 97 | 6 | 0.854417 |
| 98 | 3 | -0.316523 |
| 99 | 3 | -0.316523 |
| 100 | 3 | -0.316523 |
| 101 | 3 | -0.316523 |
| 102 | 3 | -0.316523 |
| 103 | 3 | -0.316523 |
| 104 | 3 | -0.316523 |
| 105 | 3 | -0.316523 |
| 106 | 9 | 2.025356 |
| 107 | 5 | 0.464104 |
| 108 | 0 | -1.487462 |
| 109 | 5 | 0.464104 |
| 110 | 5 | 0.464104 |
| 111 | 5 | 0.464104 |
| 112 | 5 | 0.464104 |
| 113 | 0 | -1.487462 |
| 114 | 5 | 0.464104 |
| 115 | 5 | 0.464104 |
| 116 | 3 | -0.316523 |
| 117 | 1 | -1.097149 |
| 118 | 3 | -0.316523 |
| 119 | 3 | -0.316523 |
| 120 | 11 | 2.805982 |
| 121 | 3 | -0.316523 |
| 122 | 5 | 0.464104 |
| 123 | 3 | -0.316523 |
| 124 | 11 | 2.805982 |
| 125 | 4 | 0.073791 |
| 126 | 11 | 2.805982 |
| 127 | 6 | 0.854417 |
| 128 | 3 | -0.316523 |
| 129 | 1 | -1.097149 |
| 130 | 7 | 1.244730 |
| 131 | 9 | 2.025356 |
| 132 | 3 | -0.316523 |
| 133 | 2 | -0.706836 |
| 134 | 7 | 1.244730 |
| 135 | 5 | 0.464104 |
| 136 | 10 | 2.415669 |
| 137 | 5 | 0.464104 |
| 138 | 1 | -1.097149 |
| 139 | 3 | -0.316523 |
| 140 | 3 | -0.316523 |
| 141 | 3 | -0.316523 |
| 142 | 3 | -0.316523 |
| 143 | 3 | -0.316523 |
| 144 | 1 | -1.097149 |
| 145 | 0 | -1.487462 |
| 146 | 1 | -1.097149 |
| 147 | 1 | -1.097149 |
| 148 | 0 | -1.487462 |
| 149 | 0 | -1.487462 |
| 150 | 1 | -1.097149 |
| 151 | 3 | -0.316523 |
| 152 | 3 | -0.316523 |
| 153 | 1 | -1.097149 |
| 154 | 1 | -1.097149 |
| 155 | 1 | -1.097149 |
| 156 | 4 | 0.073791 |
| 157 | 5 | 0.464104 |
| 158 | 1 | -1.097149 |
| 159 | 3 | -0.316523 |
| 160 | 2 | -0.706836 |
| 161 | 0 | -1.487462 |
| 162 | 5 | 0.464104 |
| 163 | 4 | 0.073791 |
| 164 | 6 | 0.854417 |
| 165 | 3 | -0.316523 |
| 166 | 0 | -1.487462 |
| 167 | 0 | -1.487462 |
| 168 | 4 | 0.073791 |
| 169 | 5 | 0.464104 |
| 170 | 0 | -1.487462 |
| 171 | 7 | 1.244730 |
| 172 | 2 | -0.706836 |
| 173 | 4 | 0.073791 |
| 174 | 3 | -0.316523 |
| 175 | 4 | 0.073791 |
| 176 | 0 | -1.487462 |
| 177 | 5 | 0.464104 |
| 178 | 3 | -0.316523 |
| 179 | 3 | -0.316523 |
| 180 | 2 | -0.706836 |
| 181 | 3 | -0.316523 |
| 182 | 7 | 1.244730 |
| 183 | 2 | -0.706836 |
| 184 | 3 | -0.316523 |
| 185 | 4 | 0.073791 |
| 186 | 9 | 2.025356 |
| 187 | 5 | 0.464104 |
| 188 | 7 | 1.244730 |
| 189 | 0 | -1.487462 |
| 190 | 6 | 0.854417 |
| 191 | 4 | 0.073791 |
| 192 | 5 | 0.464104 |
| 193 | 6 | 0.854417 |
| 194 | 5 | 0.464104 |
| 195 | 6 | 0.854417 |
| 196 | 0 | -1.487462 |
| 197 | 6 | 0.854417 |
| 198 | 9 | 2.025356 |
| 199 | 5 | 0.464104 |
| 200 | 7 | 1.244730 |
| 201 | 3 | -0.316523 |
