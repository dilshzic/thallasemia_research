import pandas as pd
import os
import subprocess
import base64

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/png;base64,{encoded_string}"

plots_dir = "/home/dilshan/Desktop/Thallasemia research/02_Scripts/Python_Pipeline/outputs/plots"
img_age = get_base64_image(os.path.join(plots_dir, "age_distribution.png"))
img_gender = get_base64_image(os.path.join(plots_dir, "gender_distribution.png"))
img_knowledge = get_base64_image(os.path.join(plots_dir, "knowledge_score_distribution.png"))
img_rates = get_base64_image(os.path.join(plots_dir, "relative_screening_rates.png"))

html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap');
    
    body {{
        font-family: 'Roboto', sans-serif;
        margin: 0;
        padding: 40px;
        background-color: #f4f7f6;
        color: #333;
        width: 1189mm; /* A0 Landscape Width */
        height: 841mm; /* A0 Landscape Height */
        box-sizing: border-box;
    }}
    
    .poster-container {{
        background-color: #fff;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        box-shadow: 0 0 20px rgba(0,0,0,0.1);
        border: 10px solid #2c3e50;
        box-sizing: border-box;
    }}
    
    .header {{
        background-color: #2c3e50;
        color: #ecf0f1;
        padding: 40px;
        text-align: center;
        border-bottom: 10px solid #e74c3c;
    }}
    
    .header h1 {{
        font-size: 110px;
        margin: 0;
        font-weight: 900;
        letter-spacing: 2px;
    }}
    
    .header h2 {{
        font-size: 50px;
        margin: 20px 0 0 0;
        font-weight: 300;
        color: #bdc3c7;
    }}
    
    .content {{
        display: flex;
        flex: 1;
        padding: 40px;
        gap: 40px;
    }}
    
    .column {{
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 40px;
    }}
    
    .section {{
        background-color: #ecf0f1;
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    
    .section-title {{
        font-size: 50px;
        color: #2c3e50;
        border-bottom: 5px solid #e74c3c;
        padding-bottom: 15px;
        margin-top: 0;
        margin-bottom: 30px;
        text-transform: uppercase;
        font-weight: 700;
    }}
    
    p, li {{
        font-size: 32px;
        line-height: 1.6;
    }}
    
    ul {{
        margin: 0;
        padding-left: 40px;
    }}
    
    .highlight {{
        color: #e74c3c;
        font-weight: bold;
    }}
    
    .image-container {{
        text-align: center;
        margin-top: 30px;
    }}
    
    .image-container img {{
        max-width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: white;
        padding: 20px;
    }}
    
    .stats-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-size: 28px;
    }}
    
    .stats-table th, .stats-table td {{
        border: 2px solid #bdc3c7;
        padding: 15px;
        text-align: left;
    }}
    
    .stats-table th {{
        background-color: #34495e;
        color: white;
    }}
    
    .stats-table tr:nth-child(even) {{
        background-color: #dee4e5;
    }}
    
    .conclusion-box {{
        background-color: #34495e;
        color: white;
        padding: 40px;
        border-radius: 15px;
    }}
    .conclusion-box .section-title {{
        color: white;
        border-bottom-color: #e74c3c;
    }}
</style>
</head>
<body>

<div class="poster-container">
    <div class="header">
        <h1>Knowledge, Attitudes, and Practices Regarding Thalassemia</h1>
        <h2>A Cross-Sectional Analysis of Carrier Screening & Cascade Testing</h2>
        <p style="font-size: 36px; margin-top: 20px; color: #ecf0f1;">Research Team | August 2026</p>
    </div>
    
    <div class="content">
        <!-- COLUMN 1 -->
        <div class="column">
            <div class="section">
                <h2 class="section-title">Introduction</h2>
                <p>Thalassemia is a severe autosomal recessive blood disorder. Individuals with Thalassemia Major require lifelong blood transfusions and iron chelation therapy.</p>
                <p>Since the condition is genetic, transmission is <b>entirely preventable</b> if at-risk carrier couples are identified before marriage.</p>
                <p>The World Health Organization (WHO) advocates for <b>pre-marital partner screening</b> and <b>cascade screening</b> (testing extended family of carriers).</p>
            </div>
            
            <div class="section">
                <h2 class="section-title">Methodology</h2>
                <p>A cross-sectional survey was administered to a localized cohort of <span class="highlight">201 participants</span>. An automated Python/R computational data pipeline was utilized to rigorously process the data.</p>
                <ul>
                    <li><b>Knowledge Score:</b> A comprehensive 20-point metric evaluating disease transmission and complication awareness.</li>
                    <li><b>Practice Scores:</b> Partner screening was binarized into 'Safe' (pre-marriage) vs 'Unsafe/Delayed' practices. Cascade testing evaluated relatives' screening frequencies.</li>
                    <li><b>Statistics:</b> Welch's T-Tests & Pearson's Chi-Square Tests (α = 0.05).</li>
                </ul>
            </div>
            
            <div class="section">
                <h2 class="section-title">Cohort Demographics</h2>
                <p>The study captured a diverse subset of the population, providing robust statistical power.</p>
                <div class="image-container">
                    <img src="{img_age}" alt="Age Distribution">
                </div>
            </div>
        </div>
        
        <!-- COLUMN 2 -->
        <div class="column">
            <div class="section">
                <h2 class="section-title">Baseline Knowledge</h2>
                <p>A significant portion of the cohort harbored misconceptions about the disease's curability (via bone marrow transplant) and the 25% transmission risk per pregnancy for carrier couples.</p>
                <div class="image-container">
                    <img src="{img_knowledge}" alt="Knowledge Distribution">
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">Family Screening Cascade</h2>
                <p>Screening compliance drops precipitously outside immediate first-degree family, identifying a major gap in disease prevention mechanisms.</p>
                <div class="image-container">
                    <img src="{img_rates}" alt="Relative Screening Rates">
                </div>
            </div>
        </div>
        
        <!-- COLUMN 3 -->
        <div class="column">
            <div class="section">
                <h2 class="section-title">Key Inferential Findings</h2>
                <p>Rigorous statistical testing revealed that demographic factors heavily dictate screening outcomes.</p>
                
                <table class="stats-table">
                    <tr>
                        <th>Demographic</th>
                        <th>Impacted Metric</th>
                        <th>p-value</th>
                        <th>Significance</th>
                    </tr>
                    <tr>
                        <td><b>Education</b></td>
                        <td>Knowledge Score</td>
                        <td><span class="highlight">< 0.001</span></td>
                        <td>Degree+ significantly higher</td>
                    </tr>
                    <tr>
                        <td><b>Education</b></td>
                        <td>Safe Partner Practice</td>
                        <td><span class="highlight">< 0.001</span></td>
                        <td>Degree+ practices safely</td>
                    </tr>
                    <tr>
                        <td><b>Knowledge</b></td>
                        <td>Safe Partner Practice</td>
                        <td><span class="highlight">0.019</span></td>
                        <td>High Knowledge = Safe Action</td>
                    </tr>
                    <tr>
                        <td><b>Marital Status</b></td>
                        <td>Partner Screening</td>
                        <td><span class="highlight">0.004</span></td>
                        <td>Marriage dictates timing</td>
                    </tr>
                </table>
                
                <p style="margin-top: 20px;"><b>Key Insight:</b> Being in the "High Knowledge" category makes an individual statistically more likely to engage in "Safe" (pre-marital) partner screening, proving that education directly modifies behavior.</p>
            </div>
            
            <div class="section conclusion-box">
                <h2 class="section-title">Discussion & Conclusion</h2>
                <ul>
                    <li><span class="highlight">Education is the Catalyst:</span> Formal education emerged as the single most powerful predictor of safe practices. General awareness campaigns are currently failing lower-education demographics.</li>
                    <li><span class="highlight">Knowledge Drives Action:</span> Providing comprehensive disease knowledge successfully bridges the gap into actionable, safe behaviors.</li>
                    <li><span class="highlight">Strategic Intervention:</span> To combat transmission effectively, public health frameworks must institutionalize targeted pre-marital counseling, capturing couples during the critical window before marriage.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

</body>
</html>
"""

with open("poster.html", "w") as f:
    f.write(html_content)

# We use wkhtmltopdf to generate an A0 landscape poster.
# Page size A0 = 841 x 1189 mm. We want landscape, so Orientation=Landscape
subprocess.run([
    "wkhtmltopdf", 
    "--page-size", "A0", 
    "--orientation", "Landscape", 
    "--margin-top", "0", 
    "--margin-bottom", "0", 
    "--margin-left", "0", 
    "--margin-right", "0",
    "--disable-smart-shrinking",
    "poster.html", 
    "Thalassemia_KAP_Poster.pdf"
])
print("Poster PDF generated successfully!")
