# Thalassemia Survey Data Analysis Pipeline in Python

This is a self-contained, modular Python data analysis pipeline that mirrors the R pipeline's structure and execution flow. It loads the thalassemia research dataset, cleans column headers and participant responses, calculates knowledge scores/Z-scores, compiles descriptive statistics, and runs inferential tests (Chi-Square, t-test, ANOVA, multiple regression), saving all outputs (tables and plots) to a dedicated `outputs/` directory.

## Folder Structure

```
Python_Pipeline/
├── README.md               # This documentation file
├── run_pipeline.py         # Main driver script (orchestrator)
├── loader_01.py            # Stage 1: Load and clean Excel data
├── scoring_02.py           # Stage 2: Calculate Knowledge Scores and Z-scores
├── descriptive_03.py       # Stage 3: Calculate descriptive statistics (frequencies)
├── visualizations_04.py    # Stage 4: Generate visual plots (matplotlib/seaborn)
├── inferential_05.py       # Stage 5: Run Chi-Square, t-test, ANOVA, and regression
└── outputs/                # Folder created automatically for output results
    ├── csv/                # Summary tables in CSV format
    │   ├── demographics.csv
    │   ├── knowledge.csv
    │   ├── marriage_partner.csv
    │   ├── family_screening.csv
    │   ├── inferential_chisq.csv
    │   ├── inferential_ttest.csv
    │   ├── inferential_anova.csv
    │   └── inferential_regression.csv
    └── plots/              # Visual plots in PNG format
        ├── age_distribution.png
        ├── gender_distribution.png
        ├── knowledge_score_distribution.png
        └── relative_screening_rates.png
```

## System Requirements & Prerequisites

To run this pipeline, you need **Python (version 3.8 or higher)** installed on your machine.

### Package Dependencies
The pipeline requires the following Python libraries:
- `pandas` (data manipulation)
- `numpy` (numerical helper functions)
- `openpyxl` (engine to read `.xlsx` files)
- `matplotlib` (plotting library)
- `seaborn` (statistical visualization)
- `scipy` (statistical tests: Chi-Square, t-test, ANOVA)
- `statsmodels` (ordinary least squares regression model)

**Automatic Dependency Management**: The orchestrator script `run_pipeline.py` will automatically check for these packages and attempt to notify you or install them before running.

## How to Run the Pipeline

Open your terminal, navigate to the `Python_Pipeline` directory, and run `run_pipeline.py`:

```bash
cd "/home/dilshan/Desktop/Thallasemia research/Python_Pipeline"
python3 run_pipeline.py
```

All CSV tables will be created in `outputs/csv/` and all plots in `outputs/plots/`.
