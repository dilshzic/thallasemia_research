import os
import subprocess

md_dir = "/home/dilshan/Desktop/Thallasemia research/03_Reports_and_Analysis/Markdown_Drafts"
out_dir = "/home/dilshan/Desktop/Thallasemia research"

reports = {
    "Score_Overview": [
        "Participant_Scores_Report.md",
        "Weighted_V3_Score_Breakdown.md"
    ],
    "Score_Association": [
        "Knowledge_Attitude_Correlation_Report.md",
        "Knowledge_Practice_Inferential_Report.md",
        "Attitude_Practice_Inferential_Report.md",
        "Cascade_Practice_Correlation_Report.md"
    ],
    "Demographic_Associations": [
        "KAP_ChiSquare_Report.md",
        "Demographics_ChiSquare_Matrix.md",
        "Knowledge_Age_TTest_Report.md",
        "Knowledge_Education_ANOVA_Report.md",
        "Knowledge_Employment_TTest_Report.md",
        "Knowledge_Gender_TTest_Report.md",
        "Knowledge_Marital_TTest_Report.md",
        "Knowledge_Occupation_Income_ANOVA_Report.md",
        "Knowledge_Province_ANOVA_Report.md",
        "Detailed_Knowledge_Province_ANOVA_Report.md"
    ]
}

for report_name, files in reports.items():
    merged_md_path = os.path.join(out_dir, f"{report_name}.md")
    docx_path = os.path.join(out_dir, f"{report_name}.docx")
    
    with open(merged_md_path, "w") as outfile:
        # Add a title and meta for pandoc if needed, or just append contents
        outfile.write(f"---\ntitle: {report_name.replace('_', ' ')}\n---\n\n")
        
        for f in files:
            file_path = os.path.join(md_dir, f)
            if os.path.exists(file_path):
                with open(file_path, "r") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n\n---\n\n")
            else:
                print(f"Warning: {f} not found.")
                
    # Run pandoc
    try:
        subprocess.run(["pandoc", merged_md_path, "-o", docx_path], check=True)
        print(f"Successfully generated {docx_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating {docx_path}: {e}")
        
    # Optional: clean up the intermediate md file
    if os.path.exists(merged_md_path):
        os.remove(merged_md_path)
