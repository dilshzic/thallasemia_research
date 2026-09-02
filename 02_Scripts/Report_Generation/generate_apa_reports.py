#!/usr/bin/env python3
"""
Thalassemia Research: APA 7th Edition Report & PDF Generator
Faculty of Medicine, University of Kelaniya
Community Medicine Research Project (N = 201)

This script automates the generation of:
1. Knowledge Assessment and Scoring Report (Markdown & APA PDF)
2. Inferential Statistics & Association Analysis Report (Markdown & APA PDF)
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Configure output directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ----------------------------------------------------------------------
# APA 7th Edition Running Head and Page Numbering Canvas
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self.running_head = "THALASSEMIA RESEARCH DRAFT REPORT"

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#333333"))
        
        # Header (Running head on left, page number on right)
        self.drawString(54, 11 * inch - 36, self.running_head.upper())
        self.drawRightString(8.5 * inch - 54, 11 * inch - 36, f"{self._pageNumber}")
        
        # Header rule
        self.setStrokeColor(colors.HexColor("#B0B0B0"))
        self.setLineWidth(0.5)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer rule and text
        self.setFont("Times-Italic", 8)
        self.drawString(54, 32, "Faculty of Medicine, University of Kelaniya | Community Medicine Research Project")
        self.drawRightString(8.5 * inch - 54, 32, f"Page {self._pageNumber} of {total_pages}")
        self.line(54, 42, 8.5 * inch - 54, 42)
        
        self.restoreState()


class KnowledgeCanvas(NumberedCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running_head = "KNOWLEDGE ASSESSMENT AND SCORING REPORT"


class AssociationCanvas(NumberedCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running_head = "INFERENTIAL STATISTICS & ASSOCIATION REPORT"


# ----------------------------------------------------------------------
# APA 7th Edition Typography and Style Hierarchy
# ----------------------------------------------------------------------
def get_apa_styles():
    styles = getSampleStyleSheet()
    
    apa_title = ParagraphStyle(
        'APATitle',
        fontName='Times-Bold',
        fontSize=15,
        leading=19,
        alignment=1, # Centered
        spaceAfter=8,
        textColor=colors.HexColor("#111111")
    )
    
    apa_meta = ParagraphStyle(
        'APAMeta',
        fontName='Times-Italic',
        fontSize=9.5,
        leading=13,
        alignment=1, # Centered
        spaceAfter=14,
        textColor=colors.HexColor("#444444")
    )
    
    apa_h1 = ParagraphStyle(
        'APAH1',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=0,
        spaceBefore=12,
        spaceAfter=5,
        textColor=colors.HexColor("#1A2B4C"),
        keepWithNext=True
    )
    
    apa_h2 = ParagraphStyle(
        'APAH2',
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        alignment=0,
        spaceBefore=8,
        spaceAfter=3,
        textColor=colors.HexColor("#222222"),
        keepWithNext=True
    )
    
    apa_body = ParagraphStyle(
        'APABody',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        alignment=4, # Justified
        spaceAfter=6,
        textColor=colors.HexColor("#1A1A1A")
    )
    
    apa_abstract = ParagraphStyle(
        'APAAbstract',
        fontName='Times-Roman',
        fontSize=9,
        leading=12.5,
        alignment=4,
        textColor=colors.HexColor("#2A2A2A")
    )
    
    tbl_header = ParagraphStyle(
        'APATblHeader',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.black
    )
    
    tbl_cell = ParagraphStyle(
        'APATblCell',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=0,
        textColor=colors.HexColor("#111111")
    )
    
    tbl_cell_center = ParagraphStyle(
        'APATblCellCenter',
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        alignment=1,
        textColor=colors.HexColor("#111111")
    )
    
    tbl_note = ParagraphStyle(
        'APATblNote',
        fontName='Times-Italic',
        fontSize=7.5,
        leading=10,
        alignment=0,
        spaceBefore=2,
        textColor=colors.HexColor("#555555")
    )

    table_num = ParagraphStyle(
        'APATableNum',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=12,
        spaceBefore=8,
        spaceAfter=1,
        textColor=colors.black,
        keepWithNext=True
    )

    table_title = ParagraphStyle(
        'APATableTitle',
        fontName='Times-Italic',
        fontSize=9.5,
        leading=12,
        spaceAfter=4,
        textColor=colors.black,
        keepWithNext=True
    )

    bullet_style = ParagraphStyle(
        'APABullet',
        fontName='Times-Roman',
        fontSize=9,
        leading=12.5,
        leftIndent=14,
        spaceAfter=3,
        textColor=colors.HexColor("#1A1A1A")
    )

    return {
        'title': apa_title, 'meta': apa_meta, 'h1': apa_h1, 'h2': apa_h2,
        'body': apa_body, 'abstract': apa_abstract, 'th': tbl_header, 'td': tbl_cell,
        'td_c': tbl_cell_center, 'note': tbl_note, 't_num': table_num, 't_title': table_title,
        'bullet': bullet_style
    }


def make_apa_table(data, col_widths, num_str, title_str, note_str="", styles=None):
    if styles is None:
        styles = get_apa_styles()
    elements = []
    elements.append(Paragraph(num_str, styles['t_num']))
    elements.append(Paragraph(title_str, styles['t_title']))
    
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.2, colors.black),      # Top rule
        ('LINEBELOW', (0, 0), (-1, 0), 0.75, colors.black),     # Header underline
        ('LINEBELOW', (0, -1), (-1, -1), 1.2, colors.black),   # Bottom rule
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(t)
    if note_str:
        elements.append(Paragraph(note_str, styles['note']))
    elements.append(Spacer(1, 8))
    return KeepTogether(elements)


# ----------------------------------------------------------------------
# PDF Generation Routines
# ----------------------------------------------------------------------
def build_knowledge_pdf(output_path=None):
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "Knowledge_Assessment_Report_APA.pdf")
    
    styles = get_apa_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    story = []
    story.append(Paragraph("Knowledge Assessment and Scoring Report: Thalassemia Carrier Status and Genetics", styles['title']))
    story.append(Paragraph("Faculty of Medicine, University of Kelaniya | Community Medicine Research Project<br/>Target Cohort: Confirmed β-Thalassemia Carriers (N = 201) | September 2026", styles['meta']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#B0B0B0"), spaceAfter=10))
    
    story.append(Paragraph("<b>Abstract</b>", styles['h2']))
    story.append(Paragraph(
        "This report evaluates clinical and genetic knowledge among 201 confirmed β-thalassemia carriers identified across community, workplace, and educational screening programs in Sri Lanka. Applying an unweighted linear scoring methodology (scale 0–20), arbitrary difficulty weights were eliminated in favor of transparent scoring. Knowledge was categorized under two frameworks: (a) an empirical cohort mean split (M = 11.72, SD = 3.41) and (b) modified Bloom’s criteria (Good ≥ 80%, Moderate 60–79%, Poor &lt; 60%). While baseline recognition of thalassemia as an inherited disorder was high (86.6%–94.5%), profound deficits emerged in quantitative inheritance risks: only 41.3% recognized the 25% recurrence risk for two carrier parents, and 44.3% erroneously believed that thalassemia major can be cured with routine medical therapies. These results demonstrate that routine carrier screening fails to confer genetic literacy without structured, comprehensive post-test genetic counseling.",
        styles['abstract']
    ))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. Introduction and Study Context", styles['h1']))
    story.append(Paragraph(
        "β-Thalassemia remains the most common monogenic disorder in Sri Lanka, placing an immense clinical and economic burden on the national healthcare system. Primary prevention hinges on premarital carrier screening and cascade family testing. However, the efficacy of these preventive modalities is fundamentally mediated by carriers' depth of comprehension regarding their own genetic status, offspring recurrence risks, and disease severity. This report establishes a standardized, unweighted scoring rubric to evaluate the clinical literacy of diagnosed carriers.",
        styles['body']
    ))
    
    story.append(Paragraph("2. Methodological Design and Scoring Scheme", styles['h1']))
    story.append(Paragraph(
        "The survey instrument captured five core biomedical domains across validated multiple-choice and multi-select items: (a) General etiology and pathophysiology; (b) Clinical forms (Major, Intermedia, Trait); (c) Mendelian inheritance and offspring probabilities; (d) Complications and curative boundaries; and (e) Prevention awareness (premarital screening and cascade testing).",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Scoring Protocol:</b> Each correct response received 1.0 point, with partial credit assigned proportionally to multi-item questions, yielding a continuous unweighted scale from 0 to 20. Cohort-dependent inverse-frequency weights (1-p) were discarded to ensure external validity and curriculum alignment.",
        styles['body']
    ))
    story.append(Paragraph(
        "<b>Categorization Framework:</b> Because predefined thresholds were not established a priori, the dataset is stratified under both an empirical cohort mean cut-off (M = 11.72) and academic modified Bloom’s taxonomy thresholds (Good ≥ 16, Moderate 12–15, Poor ≤ 11).",
        styles['body']
    ))
    story.append(Spacer(1, 6))
    
    t1_data = [
        [Paragraph("Categorization Framework", styles['th']), Paragraph("Level Definition", styles['th']), Paragraph("Score Range", styles['th']), Paragraph("Frequency (n)", styles['th']), Paragraph("Percentage (%)", styles['th']), Paragraph("Cumulative %", styles['th'])],
        [Paragraph("<b>Empirical Mean Split</b>", styles['td']), Paragraph("High Knowledge", styles['td']), Paragraph("≥ 11.72", styles['td_c']), Paragraph("108", styles['td_c']), Paragraph("53.7%", styles['td_c']), Paragraph("53.7%", styles['td_c'])],
        [Paragraph("", styles['td']), Paragraph("Low Knowledge", styles['td']), Paragraph("&lt; 11.72", styles['td_c']), Paragraph("93", styles['td_c']), Paragraph("46.3%", styles['td_c']), Paragraph("100.0%", styles['td_c'])],
        [Paragraph("<b>Modified Bloom’s Criteria</b>", styles['td']), Paragraph("Good Knowledge", styles['td']), Paragraph("≥ 16.00 (≥80%)", styles['td_c']), Paragraph("33", styles['td_c']), Paragraph("16.4%", styles['td_c']), Paragraph("16.4%", styles['td_c'])],
        [Paragraph("", styles['td']), Paragraph("Moderate Knowledge", styles['td']), Paragraph("12.00–15.99 (60–79%)", styles['td_c']), Paragraph("88", styles['td_c']), Paragraph("43.8%", styles['td_c']), Paragraph("60.2%", styles['td_c'])],
        [Paragraph("", styles['td']), Paragraph("Poor Knowledge", styles['td']), Paragraph("&lt; 12.00 (&lt;60%)", styles['td_c']), Paragraph("80", styles['td_c']), Paragraph("39.8%", styles['td_c']), Paragraph("100.0%", styles['td_c'])],
    ]
    t1_widths = [1.5 * inch, 1.4 * inch, 1.2 * inch, 0.9 * inch, 1.0 * inch, 1.0 * inch]
    story.append(make_apa_table(t1_data, t1_widths, "Table 1", "<i>Participant Knowledge Categorization Under Alternative Assessment Frameworks</i>", "<i>Note.</i> N = 201. Unweighted linear score scale (0–20 points). Mean = 11.72, SD = 3.41, Median = 12.00.", styles))
    
    story.append(Paragraph("3. Item-Level Clinical Analysis and Misconception Profile", styles['h1']))
    story.append(Paragraph(
        "Item-level accuracy revealed stark discrepancies between broad awareness and operational genetic knowledge. Table 2 details participant accuracy across all assessed clinical competencies.",
        styles['body']
    ))
    
    t2_data = [
        [Paragraph("Item & Clinical Concept", styles['th']), Paragraph("Core Concept Evaluated", styles['th']), Paragraph("Correct (n)", styles['th']), Paragraph("Accuracy (%)", styles['th']), Paragraph("Dominant Misconception / Error", styles['th']), Paragraph("Error (%)", styles['th'])],
        [Paragraph("<b>Q14: Disease Nature</b>", styles['td']), Paragraph("Inherited hemoglobin disorder", styles['td']), Paragraph("190", styles['td_c']), Paragraph("94.5%", styles['td_c']), Paragraph("Nutritional / infectious condition", styles['td']), Paragraph("5.5%", styles['td_c'])],
        [Paragraph("<b>Q15: Carrier Health</b>", styles['td']), Paragraph("Carrier is clinically asymptomatic", styles['td']), Paragraph("137", styles['td_c']), Paragraph("68.2%", styles['td_c']), Paragraph("Believed carrier has active illness", styles['td']), Paragraph("31.8%", styles['td_c'])],
        [Paragraph("<b>Q16: Clinical Forms</b>", styles['td']), Paragraph("Identified Major, Intermedia, Trait", styles['td']), Paragraph("114", styles['td_c']), Paragraph("56.7%", styles['td_c']), Paragraph("Only recognized severe Major form", styles['td']), Paragraph("43.3%", styles['td_c'])],
        [Paragraph("<b>Q18: Transfusion Care</b>", styles['td']), Paragraph("Lifelong monthly transfusions", styles['td']), Paragraph("167", styles['td_c']), Paragraph("83.1%", styles['td_c']), Paragraph("Believed transfusions are temporary", styles['td']), Paragraph("16.9%", styles['td_c'])],
        [Paragraph("<b>Q19: Hereditary Origin</b>", styles['td']), Paragraph("Autosomal genetic transmission", styles['td']), Paragraph("174", styles['td_c']), Paragraph("86.6%", styles['td_c']), Paragraph("Contagious / environmental origin", styles['td']), Paragraph("13.4%", styles['td_c'])],
        [Paragraph("<b>Q20: Curative Limits</b>", styles['td']), Paragraph("Curable only via bone marrow BMT", styles['td']), Paragraph("76", styles['td_c']), Paragraph("37.8%", styles['td_c']), Paragraph("Believed curable via standard drugs", styles['td']), Paragraph("44.3%", styles['td_c'])],
        [Paragraph("<b>Q23: Offspring Risk</b>", styles['td']), Paragraph("25% risk per pregnancy (2 carriers)", styles['td']), Paragraph("83", styles['td_c']), Paragraph("41.3%", styles['td_c']), Paragraph("Believed 100% risk or did not know", styles['td']), Paragraph("58.7%", styles['td_c'])],
        [Paragraph("<b>Q25: Post-test Advice</b>", styles['td']), Paragraph("Received adequate genetic counseling", styles['td']), Paragraph("118", styles['td_c']), Paragraph("58.7%", styles['td_c']), Paragraph("Received no formal counseling", styles['td']), Paragraph("41.3%", styles['td_c'])],
        [Paragraph("<b>Q26: Iron Overload</b>", styles['td']), Paragraph("Hemosiderosis in liver & heart", styles['td']), Paragraph("125", styles['td_c']), Paragraph("62.2%", styles['td_c']), Paragraph("Unaware of iron chelation therapy", styles['td']), Paragraph("37.8%", styles['td_c'])],
        [Paragraph("<b>Q27: Partner Screening</b>", styles['td']), Paragraph("Premarital screening of spouse", styles['td']), Paragraph("158", styles['td_c']), Paragraph("78.6%", styles['td_c']), Paragraph("Screening during pregnancy only", styles['td']), Paragraph("21.4%", styles['td_c'])],
    ]
    t2_widths = [1.4 * inch, 1.6 * inch, 0.8 * inch, 0.9 * inch, 1.6 * inch, 0.7 * inch]
    story.append(make_apa_table(t2_data, t2_widths, "Table 2", "<i>Item-Level Response Accuracy and Documented Clinical Misconceptions</i>", "<i>Note.</i> N = 201. Data collected from validated self-administered questionnaire administered in sinhala/tamil.", styles))
    
    story.append(Paragraph("4. Key Clinical and Educational Insights", styles['h1']))
    story.append(Paragraph("<b>1. The Quantitative Probability Deficit:</b> Although 86.6% understood that thalassemia is hereditary, only 41.3% correctly identified the 25% risk. In total, 58.7% either believed that carrier couples will inevitably have an affected child (100%) or stated they had no idea. This 'all-or-nothing' misunderstanding induces excessive fatalism and social stigma surrounding marriage.", styles['bullet']))
    story.append(Paragraph("<b>2. Misconceptions of Curability:</b> Nearly 45% believed that thalassemia major can be cured with routine medical interventions, drastically underestimating the severity of the disease and reducing adherence to premarital testing.", styles['bullet']))
    story.append(Paragraph("<b>3. Carrier Self-Perception:</b> Over 31% viewed their carrier state as a disease requiring treatment. Proper counseling must reassure carriers that their trait is clinically benign while reinforcing their genetic responsibility during marriage partner selection.", styles['bullet']))
    story.append(Paragraph("<b>4. Counseling Gaps:</b> Over 41% reported receiving inadequate information at diagnosis, confirming an urgent need for standardized patient counseling brochures.", styles['bullet']))
    
    doc.build(story, canvasmaker=KnowledgeCanvas)
    print(f"Knowledge PDF built at: {output_path}")


def build_association_pdf(output_path=None):
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "Association_and_Inferential_Report_APA.pdf")
    
    styles = get_apa_styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    story = []
    story.append(Paragraph("Inferential Statistics and Association Analysis Report: Thalassemia KAP Study", styles['title']))
    story.append(Paragraph("Faculty of Medicine, University of Kelaniya | Community Medicine Research Project<br/>Target Cohort: Confirmed β-Thalassemia Carriers (N = 201) | September 2026", styles['meta']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#B0B0B0"), spaceAfter=10))
    
    story.append(Paragraph("<b>Abstract</b>", styles['h2']))
    story.append(Paragraph(
        "This report documents the inferential statistical analyses examining bivariate associations and multivariate predictors of Knowledge, Attitudes, and Practices (KAP) among 201 confirmed β-thalassemia carriers in Sri Lanka. Strict APA 7th edition reporting standards are followed. Attitude was operationalized using the refined V3 schema (Favorable vs. Unfavorable), isolating cognitive perspectives from behavioral actions. Bivariate analyses confirmed that educational level is the single dominant determinant of clinical knowledge (t = 7.602, p = 1.67 × 10⁻¹²) and favorable partner selection attitude (t = 3.749, p = 0.0002). Gender showed no association with knowledge (p = 0.230) or partner attitude (p = 0.544). However, female carriers demonstrated significantly superior cascade family screening practices (t = 2.195, p = 0.0293). Cross-KAP evaluation demonstrated that clinical knowledge directly predicts safe premarital partner screening (t = 2.689, p = 0.0099), while favorable attitudes alone do not guarantee compliance (χ² = 0.130, p = 0.7186), evidencing a notable attitude-practice gap.",
        styles['abstract']
    ))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. Sociodemographic Predictors of Clinical Knowledge", styles['h1']))
    story.append(Paragraph(
        "Independent samples t-tests were conducted to evaluate continuous unweighted knowledge scores across binary demographic classifications. Table 1 outlines the bivariate comparative statistics.",
        styles['body']
    ))
    
    t1_data = [
        [Paragraph("Demographic Factor", styles['th']), Paragraph("Comparison Groups", styles['th']), Paragraph("Sample (n)", styles['th']), Paragraph("Group Mean (SD)", styles['th']), Paragraph("t-statistic", styles['th']), Paragraph("df", styles['th']), Paragraph("p-value", styles['th']), Paragraph("Significance", styles['th'])],
        [Paragraph("<b>Education Level</b>", styles['td']), Paragraph("Higher (Tertiary/Diploma)<br/>Up to A/L", styles['td']), Paragraph("82<br/>119", styles['td_c']), Paragraph("13.84 (2.61)<br/>10.12 (3.15)", styles['td_c']), Paragraph("7.602", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph("&lt; .001", styles['td_c']), Paragraph("<b>Significant</b>", styles['td_c'])],
        [Paragraph("<b>Monthly Income</b>", styles['td']), Paragraph("&gt; LKR 50,000<br/>≤ LKR 50,000", styles['td']), Paragraph("78<br/>123", styles['td_c']), Paragraph("12.61 (3.18)<br/>11.02 (3.42)", styles['td_c']), Paragraph("3.398", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".0008", styles['td_c']), Paragraph("<b>Significant</b>", styles['td_c'])],
        [Paragraph("<b>Marital Status</b>", styles['td']), Paragraph("Married<br/>Single", styles['td']), Paragraph("64<br/>137", styles['td_c']), Paragraph("12.31 (3.25)<br/>11.45 (3.45)", styles['td_c']), Paragraph("1.816", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".0714", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
        [Paragraph("<b>Gender</b>", styles['td']), Paragraph("Female<br/>Male", styles['td']), Paragraph("124<br/>77", styles['td_c']), Paragraph("11.89 (3.38)<br/>11.31 (3.48)", styles['td_c']), Paragraph("1.204", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".2301", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
        [Paragraph("<b>Age Group</b>", styles['td']), Paragraph("≥ 30 years<br/>&lt; 30 years", styles['td']), Paragraph("69<br/>132", styles['td_c']), Paragraph("11.90 (3.44)<br/>11.62 (3.40)", styles['td_c']), Paragraph("0.560", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".5771", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
        [Paragraph("<b>Province</b>", styles['td']), Paragraph("Western<br/>Other Provinces", styles['td']), Paragraph("138<br/>63", styles['td_c']), Paragraph("11.92 (3.35)<br/>11.38 (3.52)", styles['td_c']), Paragraph("1.092", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".2762", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
    ]
    t1_widths = [1.2 * inch, 1.5 * inch, 0.7 * inch, 1.4 * inch, 0.7 * inch, 0.4 * inch, 0.6 * inch, 0.8 * inch]
    story.append(make_apa_table(t1_data, t1_widths, "Table 1", "<i>Independent Samples t-Tests for Clinical Knowledge Across Demographics</i>", "<i>Note.</i> N = 201. Unweighted knowledge score scale: 0–20. Two-tailed significance at α = .05.", styles))
    
    story.append(Paragraph("2. Multivariate Linear Regression Model", styles['h1']))
    story.append(Paragraph(
        "To establish whether educational level independently predicts knowledge after controlling for confounding socioeconomic factors, an Ordinary Least Squares (OLS) regression was specified. Table 2 provides the model coefficients.",
        styles['body']
    ))
    
    t2_data = [
        [Paragraph("Model Predictor", styles['th']), Paragraph("B (Unstandardized)", styles['th']), Paragraph("SE B", styles['th']), Paragraph("β (Standardized)", styles['th']), Paragraph("t-statistic", styles['th']), Paragraph("p-value", styles['th']), Paragraph("95% CI for B", styles['th'])],
        [Paragraph("<b>(Intercept)</b>", styles['td']), Paragraph("10.42", styles['td_c']), Paragraph("0.78", styles['td_c']), Paragraph("—", styles['td_c']), Paragraph("13.36", styles['td_c']), Paragraph("&lt; .001", styles['td_c']), Paragraph("[8.88, 11.96]", styles['td_c'])],
        [Paragraph("<b>Education (Higher vs A/L)</b>", styles['td']), Paragraph("2.98", styles['td_c']), Paragraph("0.44", styles['td_c']), Paragraph("0.442", styles['td_c']), Paragraph("6.77", styles['td_c']), Paragraph("&lt; .001", styles['td_c']), Paragraph("[2.11, 3.85]", styles['td_c'])],
        [Paragraph("<b>Income (≤ Median vs Above)</b>", styles['td']), Paragraph("-1.18", styles['td_c']), Paragraph("0.47", styles['td_c']), Paragraph("-0.168", styles['td_c']), Paragraph("-2.53", styles['td_c']), Paragraph(".0128", styles['td_c']), Paragraph("[-2.10, -0.26]", styles['td_c'])],
        [Paragraph("<b>Age (≥ 30 vs &lt; 30)</b>", styles['td']), Paragraph("0.32", styles['td_c']), Paragraph("0.46", styles['td_c']), Paragraph("0.045", styles['td_c']), Paragraph("0.70", styles['td_c']), Paragraph(".4850", styles['td_c']), Paragraph("[-0.58, 1.22]", styles['td_c'])],
        [Paragraph("<b>Gender (Female vs Male)</b>", styles['td']), Paragraph("0.41", styles['td_c']), Paragraph("0.43", styles['td_c']), Paragraph("0.058", styles['td_c']), Paragraph("0.95", styles['td_c']), Paragraph(".3430", styles['td_c']), Paragraph("[-0.44, 1.26]", styles['td_c'])],
        [Paragraph("<b>Marital Status (Married vs Single)</b>", styles['td']), Paragraph("0.55", styles['td_c']), Paragraph("0.48", styles['td_c']), Paragraph("0.076", styles['td_c']), Paragraph("1.15", styles['td_c']), Paragraph(".2520", styles['td_c']), Paragraph("[-0.40, 1.50]", styles['td_c'])],
    ]
    t2_widths = [1.8 * inch, 1.1 * inch, 0.7 * inch, 1.0 * inch, 0.8 * inch, 0.7 * inch, 1.2 * inch]
    story.append(make_apa_table(t2_data, t2_widths, "Table 2", "<i>OLS Multiple Linear Regression Model Predicting Clinical Knowledge Score</i>", "<i>Note.</i> Model R² = .275, Adjusted R² = .257, F(5, 195) = 14.82, p &lt; .001. Dependent variable: Continuous Knowledge Score.", styles))
    
    story.append(Paragraph("3. Attitude Domain Analysis (V3 Schema)", styles['h1']))
    story.append(Paragraph(
        "Attitude scoring under the V3 schema isolates internal cognitive beliefs regarding partner screening and cascade family testing, excluding behavioral items (e.g., Q36). Table 3 illustrates associations between demographic factors and attitude scores.",
        styles['body']
    ))
    
    t3_data = [
        [Paragraph("Independent Variable", styles['th']), Paragraph("Attitude Domain Evaluated", styles['th']), Paragraph("Statistical Test", styles['th']), Paragraph("Value", styles['th']), Paragraph("df", styles['th']), Paragraph("p-value", styles['th']), Paragraph("Significance", styles['th'])],
        [Paragraph("<b>Education Level</b>", styles['td']), Paragraph("Partner Selection Attitude", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("3.749", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".0002", styles['td_c']), Paragraph("<b>Significant</b>", styles['td_c'])],
        [Paragraph("<b>Age Group</b>", styles['td']), Paragraph("Partner Selection Attitude", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("2.105", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".0381", styles['td_c']), Paragraph("<b>Significant</b>", styles['td_c'])],
        [Paragraph("<b>Gender</b>", styles['td']), Paragraph("Partner Selection (Fav vs Unfav)", styles['td']), Paragraph("Pearson χ² test", styles['td']), Paragraph("0.369", styles['td_c']), Paragraph("1", styles['td_c']), Paragraph(".5438", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
        [Paragraph("<b>Marital Status</b>", styles['td']), Paragraph("Partner Selection Attitude", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("1.952", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".0528", styles['td_c']), Paragraph("Marginal Trend", styles['td_c'])],
        [Paragraph("<b>Education Level</b>", styles['td']), Paragraph("Cascade Screening Attitude", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("0.340", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".7347", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
        [Paragraph("<b>Gender</b>", styles['td']), Paragraph("Cascade Screening Attitude", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("0.550", styles['td_c']), Paragraph("199", styles['td_c']), Paragraph(".5827", styles['td_c']), Paragraph("Not Sig.", styles['td_c'])],
    ]
    t3_widths = [1.3 * inch, 1.7 * inch, 1.2 * inch, 0.7 * inch, 0.4 * inch, 0.7 * inch, 1.0 * inch]
    story.append(make_apa_table(t3_data, t3_widths, "Table 3", "<i>Bivariate Associations with Attitude Domains Under V3 Schema</i>", "<i>Note.</i> V3 Schema evaluates Partner Selection and Cascade Screening on zero-centered favorable/unfavorable scales.", styles))
    
    story.append(Paragraph("4. Cross-KAP Interactions and Behavioral Concordance", styles['h1']))
    story.append(Paragraph(
        "A central question of the research is whether elevated knowledge and favorable attitudes translate into safe premarital practice. Table 4 presents the cross-KAP test results.",
        styles['body']
    ))
    
    t4_data = [
        [Paragraph("Preventive Practice Measure", styles['th']), Paragraph("Evaluated Predictor", styles['th']), Paragraph("Test Method", styles['th']), Paragraph("Test Stat.", styles['th']), Paragraph("p-value", styles['th']), Paragraph("Empirical Conclusion", styles['th'])],
        [Paragraph("<b>Partner Screening Practice</b><br/>(Safe vs Delayed/Unsafe)", styles['td']), Paragraph("Knowledge Score (Continuous)", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("t = 2.689", styles['td_c']), Paragraph("<b>.0099</b>", styles['td_c']), Paragraph("Safe group scored significantly higher (12.84 vs 11.10)", styles['td'])],
        [Paragraph("<b>Partner Screening Practice</b><br/>(Safe vs Delayed/Unsafe)", styles['td']), Paragraph("Knowledge Level (High vs Low)", styles['td']), Paragraph("Pearson χ² test", styles['td']), Paragraph("χ² = 5.492", styles['td_c']), Paragraph("<b>.0191</b>", styles['td_c']), Paragraph("High knowledge carriers 2.1× more likely to screen partner safely", styles['td'])],
        [Paragraph("<b>Partner Screening Practice</b><br/>(Safe vs Delayed/Unsafe)", styles['td']), Paragraph("Partner Attitude (Fav vs Unfav)", styles['td']), Paragraph("Pearson χ² test", styles['td']), Paragraph("χ² = 0.130", styles['td_c']), Paragraph(".7186", styles['td_c']), Paragraph("<b>Attitude-Practice Disconnect:</b> Favorable attitude failed to predict practice", styles['td'])],
        [Paragraph("<b>Cascade Family Screening</b><br/>(Continuous Practice Score)", styles['td']), Paragraph("Gender (Female vs Male)", styles['td']), Paragraph("Independent t-test", styles['td']), Paragraph("t = 2.195", styles['td_c']), Paragraph("<b>.0293</b>", styles['td_c']), Paragraph("Females achieved significantly higher active family screening compliance", styles['td'])],
    ]
    t4_widths = [1.6 * inch, 1.5 * inch, 1.1 * inch, 0.8 * inch, 0.6 * inch, 1.7 * inch]
    story.append(make_apa_table(t4_data, t4_widths, "Table 4", "<i>Cross-KAP Concordance and Behavioral Predictors of Preventive Screening</i>", "<i>Note.</i> Safe partner practice defined as partner screening conducted strictly prior to marriage.", styles))
    
    story.append(Paragraph("5. Epidemiological Synthesis and Recommendations", styles['h1']))
    story.append(Paragraph("<b>1. Educational Inequity in Risk Protection:</b> Educational level is the primary determinant of knowledge (p &lt; 0.001) and attitude (p = 0.0002). National campaigns must develop plain-language, visual counseling materials tailored for non-tertiary communities.", styles['bullet']))
    story.append(Paragraph("<b>2. Addressing the Attitude-Practice Disconnect:</b> While theoretical attitudes toward premarital screening are high, they do not reliably translate into safe practice (p = 0.7186). Qualitative disclosures identify relational pressure, fear of broken engagements, and late disclosure as key barriers. Genetic counseling must focus on negotiation and disclosure strategies.", styles['bullet']))
    story.append(Paragraph("<b>3. Leveraging Female Leadership in Cascade Screening:</b> Female carriers were significantly more effective in convincing relatives to undergo cascade screening (t = 2.195, p = 0.0293). Interventions should equip female carriers with structured family screening invitation tools.", styles['bullet']))
    
    doc.build(story, canvasmaker=AssociationCanvas)
    print(f"Association PDF built at: {output_path}")


if __name__ == "__main__":
    print("Building Knowledge and Association PDFs...")
    build_knowledge_pdf()
    build_association_pdf()
    print("PDF generation complete.")
