import os
import subprocess

base_dir = '/home/dilshan/Desktop/Thallasemia research'
out_dir = os.path.join(base_dir, 'June 7 analysis')
os.makedirs(out_dir, exist_ok=True)

md_files = [
    # Root
    ('Knowledge_Weights_Report.md', base_dir),
    ('Participant_Scores_Report.md', base_dir),
    ('Best_Participant_Note.md', base_dir),
    ('1_Distribution_Chart.md', base_dir),
    ('2_Cluster_DotPlot.md', base_dir),
    ('3_KMeans_Clustering.md', base_dir),
    # Raw Analysis
    ('1_Raw_Distribution_Chart.md', os.path.join(base_dir, 'raw_score_analysis')),
    ('2_Raw_Cluster_DotPlot.md', os.path.join(base_dir, 'raw_score_analysis')),
    ('3_Raw_KMeans_Clustering.md', os.path.join(base_dir, 'raw_score_analysis')),
    # Attitude Analysis
    ('Partner_Selection_Attitude_Details.md', os.path.join(base_dir, 'attitude_score_analysis')),
    ('Cascade_Screening_Attitude_Details.md', os.path.join(base_dir, 'attitude_score_analysis'))
]

for filename, folder in md_files:
    in_path = os.path.join(folder, filename)
    out_name = filename.replace('.md', '.pdf')
    out_path = os.path.join(out_dir, out_name)
    
    if os.path.exists(in_path):
        print(f"Converting {filename}...")
        try:
            # enable local file access for wkhtmltopdf to load images
            cmd = ['pandoc', filename, '-o', out_path, '--pdf-engine=wkhtmltopdf', '-V', 'margin-top=1in', '-V', 'margin-bottom=1in', '-V', 'margin-left=1in', '-V', 'margin-right=1in', '--pdf-engine-opt=--enable-local-file-access']
            subprocess.run(cmd, cwd=folder, check=True)
            print(f"  -> Saved to {out_path}")
        except Exception as e:
            print(f"  -> Error: {e}")
    else:
        print(f"File not found: {in_path}")

print("All conversions complete!")
