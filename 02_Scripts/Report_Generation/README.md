# Thalassemia Research: Report & PDF Generation Pipeline

This directory contains automated report generation code developed for the Thalassemia Carrier KAP Study ($N = 201$) at the Faculty of Medicine, University of Kelaniya.

## Overview
* **`generate_apa_reports.py`**: Standalone Python script that builds two publication-ready APA 7th edition reports:
  1. `Knowledge_Assessment_Report_APA.pdf` (Unweighted linear scoring, dual cut-off comparison: Empirical Mean vs. Modified Bloom's criteria, and clinical misconception analysis).
  2. `Association_and_Inferential_Report_APA.pdf` (Bivariate $t$-tests, OLS Multiple Linear Regression, V3 Attitude associations, and Cross-KAP concordance analysis).

## Prerequisites
* Python 3.8+
* `reportlab` library:
  ```bash
  pip install reportlab
  ```

## Usage
Run the generator directly:
```bash
python generate_apa_reports.py
```
Generated PDF files and Markdown source drafts will be saved to `output_reports/`.
