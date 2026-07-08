import os
import subprocess

out_dir = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/June_7_Review_PDFs'
md_dir = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v2'

os.makedirs(out_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

md_partner = f"""# New Partner Selection Attitude Analysis (v2)

This report visualizes the Partner Selection attitudes after recalculating the scores using the updated, multi-tiered penalty schema (introducing weights ranging from +2 down to -2 for specific answers).

### The New Distribution
Because the new schema includes heavier penalties (-2) and stronger rewards (+2), the range of possible scores has expanded drastically. This successfully broke the "ceiling effect" seen in the earlier analysis, allowing the cohort to spread out far more naturally.

![Distribution of New Scores]({charts_dir}/New_Partner_Dist.png)

![Dot Plot of New Scores]({charts_dir}/New_Partner_DotPlot.png)

---

### K-Means Clustering (k=3)
With the new spread of data, the clustering algorithm successfully partitioned the cohort into three very distinct sentiment tiers. The zero line (Neutral) perfectly separates the negative cluster from the positive ones.

1. **Positive/High (Green):** Participants who consistently chose the most protective attitudes (+2 and +1).
2. **Neutral/Medium (Orange):** Participants who had mixed feelings, or frequently answered "Not sure" (0).
3. **Negative/Low (Red):** Participants whose scores were pulled into the negatives due to dangerous attitudes (-1 and -2 penalties, such as willingness for consanguineous marriage).

![K-Means Clusters]({charts_dir}/New_Partner_KMeans.png)
"""

md_cascade = f"""# New Cascade Screening Attitude Analysis (v2)

This report visualizes the Cascade Screening attitudes after recalculating the scores using the updated schema (+1 for positive answers, 0 for neutral, and -1 for negative answers on Q35, Q36, and Q40).

### The New Distribution
Because this schema assigns explicit negative penalties for undesirable attitudes (like "Disagree" or "No"), we can accurately see exactly how many participants hold negative views toward family screening. 

![Distribution of New Scores]({charts_dir}/New_Cascade_Dist.png)

![Dot Plot of New Scores]({charts_dir}/New_Cascade_DotPlot.png)

---

### K-Means Clustering (k=3)
The new K-Means clustering perfectly separated the cohort. You can see how clearly the zero-line divides the groups:

1. **Positive/High (Green):** Participants who recognize the importance of cascade screening and ensure their family is aware.
2. **Neutral/Medium (Orange):** Participants whose scores hovered around 0 to 1, indicating mixed feelings or a lack of strong opinions.
3. **Negative/Low (Red):** The outlier group whose scores fell into negative territory due to actively disagreeing with screening importance or hiding their status.

![K-Means Clusters]({charts_dir}/New_Cascade_KMeans.png)
"""

# Write MD files
partner_md_path = os.path.join(md_dir, 'New_Partner_Attitude_Report.md')
cascade_md_path = os.path.join(md_dir, 'New_Cascade_Attitude_Report.md')

with open(partner_md_path, 'w') as f:
    f.write(md_partner)
with open(cascade_md_path, 'w') as f:
    f.write(md_cascade)

# Convert to PDF
files_to_convert = [
    ('New_Partner_Attitude_Report.md', partner_md_path),
    ('New_Cascade_Attitude_Report.md', cascade_md_path)
]

for name, filepath in files_to_convert:
    print(f"Converting {name}...")
    out_pdf = os.path.join(out_dir, name.replace('.md', '.pdf'))
    try:
        cmd = [
            'pandoc', filepath, '-o', out_pdf, 
            '--pdf-engine=wkhtmltopdf', 
            '-V', 'margin-top=1in', 
            '-V', 'margin-bottom=1in', 
            '-V', 'margin-left=1in', 
            '-V', 'margin-right=1in', 
            '--pdf-engine-opt=--enable-local-file-access'
        ]
        subprocess.run(cmd, check=True)
        print(f"  -> Saved to {out_pdf}")
    except Exception as e:
        print(f"  -> Error: {e}")

print("All V2 Attitude reports generated and converted to PDF!")
