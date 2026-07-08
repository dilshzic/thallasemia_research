# Thalassemia Survey Data Analysis Pipeline in R

This is a self-contained R language data analysis pipeline designed to load the thalassemia research dataset, clean the headers and responses, calculate participant knowledge scores/Z-scores, compute descriptive statistics, and generate visualizations.

## Folder Structure

Once executed, the pipeline will structure the project and outputs as follows:

```
R_Pipeline/
├── README.md               # This documentation file
├── run_pipeline.R          # The main orchestration driver script
├── 01_data_loader.R        # Script to load and clean Excel data
├── 02_scoring.R            # Script to calculate Knowledge Scores and Z-scores
├── 03_descriptive_stats.R  # Script to calculate descriptive frequencies
├── 04_visualizations.R     # Script to generate ggplot2 visual plots
└── outputs/                # Folder created automatically for output results
    ├── csv/                # Contains descriptive stats tables (CSV format)
    │   ├── demographics.csv
    │   ├── knowledge.csv
    │   ├── marriage_partner.csv
    │   └── family_screening.csv
    └── plots/              # Contains generated visual plots (PNG format)
        ├── age_distribution.png
        ├── gender_distribution.png
        ├── knowledge_score_distribution.png
        └── relative_screening_rates.png
```

## System Requirements & Prerequisites

To run this pipeline, you need **R (version 4.0 or higher)** installed on your machine. 

### Package Dependencies
The pipeline requires the following R packages, which are part of the standard `tidyverse` ecosystem plus Excel utility packages:
- `readxl` (for reading `.xlsx` files)
- `dplyr` (for data manipulation)
- `tidyr` (for tidying and cleaning)
- `stringr` (for text pattern cleaning)
- `ggplot2` (for plotting and visuals)
- `openpyxl` (Note: R uses standard packages like `openxlsx` or `writexl` if writing back to Excel. The pipeline writes summary statistics to CSV for portability).

**Automatic Dependency Management**: The driver script `run_pipeline.R` will automatically check for these packages and install any that are missing from your system before running.

## How to Run the Pipeline

### Option 1: Using the Terminal (Command Line)
Navigate to the project directory and run the driver script using `Rscript`:

```bash
cd "/home/dilshan/Desktop/Thallasemia research/R_Pipeline"
Rscript run_pipeline.R
```

### Option 2: Using RStudio
1. Open RStudio.
2. Set your working directory to the `R_Pipeline` folder:
   ```R
   setwd("/home/dilshan/Desktop/Thallasemia research/R_Pipeline")
   ```
3. Open `run_pipeline.R` and click **Source** (or run `source("run_pipeline.R")` in the console).

## Output Files Created

1. **`outputs/csv/`**:
   - `demographics.csv`: Summaries of age, gender, education, income, residing province, marital status, and carrier diagnosis year/location.
   - `knowledge.csv`: Accuracy percentages and frequency counts for all 15 knowledge questions.
   - `marriage_partner.csv`: Willingness for consanguineous marriages, carrier-carrier marriage acceptance, and disclosure reasons.
   - `family_screening.csv`: Relatives' screening rates (1st, 2nd, 3rd degree) and family screening barriers.
2. **`outputs/plots/`**:
   - `age_distribution.png`: Histogram showing age spreads with density overlays.
   - `gender_distribution.png`: Sleek bar chart showing gender distribution.
   - `knowledge_score_distribution.png`: Density plot and histogram of raw knowledge scores.
   - `relative_screening_rates.png`: Binned bar charts showing screening coverage across genetic degrees of relation.
