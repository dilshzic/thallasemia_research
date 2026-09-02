import os
import subprocess

inferential_dir = "/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Inferential_Reports"
descriptive_dir = "/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Descriptive_Reports"
out_dir = "/home/dilshan/Desktop/Thallasemia research"

reports = {
    "Score_Overview_Raw": [
        os.path.join(descriptive_dir, "expanded_knowledge_scores_report.md")
    ],
    "Score_Association_Raw": [
        os.path.join(inferential_dir, "practices_attitudes_stats_summary.md"),
        os.path.join(inferential_dir, "regression_analysis_report.md")
    ],
    "Demographic_Associations_Raw": [
        os.path.join(inferential_dir, "chi_square_report.md"),
        os.path.join(inferential_dir, "group_comparison_report.md")
    ]
}

for report_name, files in reports.items():
    merged_md_path = os.path.join(out_dir, f"{report_name}.md")
    docx_path = os.path.join(out_dir, f"{report_name}.docx")
    
    with open(merged_md_path, "w") as outfile:
        # Add a title and meta for pandoc if needed, or just append contents
        title_friendly = report_name.replace('_', ' ').replace('Raw', '(Raw Scores)')
        outfile.write(f"---\ntitle: {title_friendly}\n---\n\n")
        
        for file_path in files:
            if os.path.exists(file_path):
                with open(file_path, "r") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n---\n\n")
            else:
                print(f"Warning: {file_path} not found.")
                
    # Run pandoc
    try:
        subprocess.run(["pandoc", merged_md_path, "-o", docx_path], check=True)
        print(f"Successfully generated {docx_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating {docx_path}: {e}")
        
    # Optional: clean up the intermediate md file
    if os.path.exists(merged_md_path):
        os.remove(merged_md_path)
