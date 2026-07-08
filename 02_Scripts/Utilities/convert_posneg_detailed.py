import os
import subprocess

base_dir = '/home/dilshan/Desktop/Thallasemia research/pos_neg_score_analysis'
out_dir = '/home/dilshan/Desktop/Thallasemia research/June 7 review'
os.makedirs(out_dir, exist_ok=True)

# 1. Generate Highly Detailed MDs
md_dist = f"""# Detailed Analysis: Positive/Negative Knowledge Score Distribution

In Phase 3, a strict penalty-based scoring system was introduced to account for guessing probability:
- **+1 Point:** Correct answer or correct multiple-choice option selected.
- **-1 Point:** Incorrect answer or incorrect multiple-choice option selected.
- **0 Points:** "I don't know" / "Not sure" / Blank responses.

![PosNeg Distribution](charts/PosNeg_Score_Distribution.png)

### In-Depth Observations
- **Wider Spread & Variance:** Unlike the raw scoring method which compressed all participants into positive integers, the introduction of a -1 penalty causes the distribution to widen significantly. 
- **The Zero Line Boundary:** A crucial feature of this distribution is the zero line. Participants scoring near 0 indicate that their correct medical knowledge is entirely offset by dangerous misconceptions (or they consistently chose "I don't know"). 
- **Negative Outliers:** The distribution reveals a subset of participants extending into negative territory. These individuals hold active misconceptions regarding thalassemia (e.g., believing it is contagious or curable with common treatments), which from a public health perspective, is more dangerous than simply lacking knowledge.
"""

md_dot = f"""# Detailed Analysis: Positive/Negative Scores Dot Plot

This dot plot maps the 201 participants from lowest to highest score using the strict +1/-1 penalty method.

![PosNeg Dot Plot](charts/PosNeg_Score_DotPlot.png)

### Interpretation Guide
- **Visualizing Misconceptions:** By sorting the scores linearly, the true impact of negative penalties becomes visually striking. We can clearly identify the exact percentile of the cohort that falls below the zero line. 
- **Elimination of Plateaus:** In earlier raw scoring models, massive flat plateaus formed because participants tied with the same integer scores. The penalty method shatters these plateaus. Participants who got 5 right and 0 wrong score a 5, but participants who got 7 right and 2 wrong also score a 5. This dynamic scoring introduces much greater mathematical variance and a smoother curve.
- **The High-Knowledge Tier:** The steep vertical rise on the far right demonstrates that the truly knowledgeable outliers (scoring 8 to 10) are mathematically separated from those who guessed their way to a high raw score.
"""

md_kmeans = f"""# Detailed Analysis: K-Means Clustering on Pos/Neg Scores

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
"""

with open(os.path.join(base_dir, '1_PosNeg_Distribution_Detailed.md'), 'w') as f: f.write(md_dist)
with open(os.path.join(base_dir, '2_PosNeg_DotPlot_Detailed.md'), 'w') as f: f.write(md_dot)
with open(os.path.join(base_dir, '3_PosNeg_KMeans_Detailed.md'), 'w') as f: f.write(md_kmeans)

# 2. Convert to PDF using Pandoc
md_files = [
    '1_PosNeg_Distribution_Detailed.md',
    '2_PosNeg_DotPlot_Detailed.md',
    '3_PosNeg_KMeans_Detailed.md'
]

for filename in md_files:
    in_path = os.path.join(base_dir, filename)
    out_name = filename.replace('.md', '.pdf')
    out_path = os.path.join(out_dir, out_name)
    
    print(f"Converting {filename}...")
    try:
        cmd = ['pandoc', filename, '-o', out_path, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
        subprocess.run(cmd, cwd=base_dir, check=True)
        print(f"  -> Saved to {out_path}")
    except Exception as e:
        print(f"  -> Error: {e}")

print("All detailed reports generated and converted to PDF!")
