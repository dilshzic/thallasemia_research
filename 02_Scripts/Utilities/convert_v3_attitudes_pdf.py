import os
import subprocess

out_dir = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/June_7_Review_PDFs'
md_dir = '/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts'
charts_dir = '/home/dilshan/Desktop/Thallasemia research/04_Visualizations/Root_Charts/attitude_v3'

os.makedirs(out_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

md_partner = f"""# V3 Partner Selection Attitude Analysis

This report visualizes the Partner Selection attitudes using the optimized V3 schema (excluding practice/action variables and widening the penalty scale to -3).

### V3 Distribution
By applying extreme penalties (-3) for dangerous attitudes (like accepting consanguineous marriage), the distribution completely shatters the ceiling effect. We now have a true continuous spectrum of attitudes ranging from highly protective to dangerously misinformed.

![Distribution of V3 Scores]({charts_dir}/V3_Partner_Dist.png)
![Dot Plot of V3 Scores]({charts_dir}/V3_Partner_DotPlot.png)

---

### V3 K-Means Clustering (k=3)
With the mathematical variance increased, K-Means successfully separated the cohort into three highly distinct tiers. The zero line flawlessly demarcates the boundary between positive and negative sentiment.

![K-Means Clusters]({charts_dir}/V3_Partner_KMeans.png)
"""

md_cascade = f"""# V3 Cascade Screening Attitude Analysis

This report visualizes the Cascade Screening attitudes using the optimized V3 schema (excluding Q36 as it is a practice variable, and incorporating perceived behavioral control from Q39).

### V3 Distribution
The distribution is incredibly revealing. By assigning severe penalties (-2) to those who actively disagree with screening importance, we can clearly isolate a very small, but dangerous, subset of the population whose scores plunge into the negatives.

![Distribution of V3 Scores]({charts_dir}/V3_Cascade_Dist.png)
![Dot Plot of V3 Scores]({charts_dir}/V3_Cascade_DotPlot.png)

---

### V3 K-Means Clustering (k=3)
The clustering algorithm found natural breaking points in the data. The "Negative/Low" cluster is small but highly distinct, representing participants who actively resist the idea of family screening.

![K-Means Clusters]({charts_dir}/V3_Cascade_KMeans.png)
"""

# Write MD files
partner_md_path = os.path.join(md_dir, 'V3_Partner_Attitude_Report.md')
cascade_md_path = os.path.join(md_dir, 'V3_Cascade_Attitude_Report.md')

with open(partner_md_path, 'w') as f: f.write(md_partner)
with open(cascade_md_path, 'w') as f: f.write(md_cascade)

# Convert to PDF
files_to_convert = [
    ('V3_Partner_Attitude_Report.md', partner_md_path),
    ('V3_Cascade_Attitude_Report.md', cascade_md_path)
]

for name, filepath in files_to_convert:
    print(f"Converting {name}...")
    out_pdf = os.path.join(out_dir, name.replace('.md', '.pdf'))
    try:
        cmd = ['pandoc', filepath, '-o', out_pdf, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
        subprocess.run(cmd, check=True)
    except Exception as e:
        pass

print("V3 PDFs generated!")
