# ==============================================================================
# Thalassemia Survey Data Analysis Pipeline
# Main Orchestrator Script
# ==============================================================================

cat("======================================================================\n")
cat("Initializing Thalassemia Survey Analysis Pipeline...\n")
cat("======================================================================\n\n")

# --- 1. Package Management & Setup ---
required_packages <- c("readxl", "dplyr", "tidyr", "stringr", "ggplot2")

cat("Checking package dependencies...\n")
missing_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]

if (length(missing_packages) > 0) {
  cat("The following packages are missing and will be installed:\n")
  cat(paste("  -", missing_packages, collapse = "\n"), "\n\n")
  # Use a reliable CRAN mirror
  install.packages(missing_packages, repos = "https://cloud.r-project.org")
} else {
  cat("All required packages are already installed.\n\n")
}

# Load packages
invisible(lapply(required_packages, library, character.only = TRUE))

# --- 2. Environment Configurations ---
# Resolve absolute path to data workbook
xlsx_path <- "/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx"

if (!file.exists(xlsx_path)) {
  # Fallback to looking in the parent folder if scripts are running from a relative folder
  xlsx_path <- "../../01_Data/Raw_Data/Thalassemia_Research.xlsx"
}

if (!file.exists(xlsx_path)) {
  stop("CRITICAL ERROR: Could not find 'Thalassemia_Research.xlsx' in absolute path or parent folder.\n")
}

cat("Dataset located at:", normalizePath(xlsx_path), "\n")

# Create output directories if they do not exist
output_base <- "./outputs"
csv_dir <- file.path(output_base, "csv")
plot_dir <- file.path(output_base, "plots")

if (!dir.exists(output_base)) dir.create(output_base)
if (!dir.exists(csv_dir)) dir.create(csv_dir)
if (!dir.exists(plot_dir)) dir.create(plot_dir)

cat("Output directories initialized under './outputs/'.\n\n")

# --- 3. Run Pipeline Stages ---

# Stage 1: Load and clean data
cat("----------------------------------------------------------------------\n")
cat("Stage 1: Executing Data Loader & Cleaning...\n")
if (file.exists("01_data_loader.R")) {
  source("01_data_loader.R")
} else {
  stop("CRITICAL ERROR: Missing '01_data_loader.R' script.")
}

# Stage 2: Knowledge Scoring & Z-Scores
cat("----------------------------------------------------------------------\n")
cat("Stage 2: Executing Scoring System...\n")
if (file.exists("02_scoring.R")) {
  source("02_scoring.R")
} else {
  stop("CRITICAL ERROR: Missing '02_scoring.R' script.")
}

# Stage 3: Descriptive Statistics Summary
cat("----------------------------------------------------------------------\n")
cat("Stage 3: Running Descriptive Statistics summaries...\n")
if (file.exists("03_descriptive_stats.R")) {
  source("03_descriptive_stats.R")
} else {
  stop("CRITICAL ERROR: Missing '03_descriptive_stats.R' script.")
}

# Stage 4: Visualizations
cat("----------------------------------------------------------------------\n")
cat("Stage 4: Generating plots...\n")
if (file.exists("04_visualizations.R")) {
  source("04_visualizations.R")
} else {
  stop("CRITICAL ERROR: Missing '04_visualizations.R' script.")
}

# Stage 5: Inferential Statistical Analysis
cat("----------------------------------------------------------------------\n")
cat("Stage 5: Executing Inferential Statistical Analysis...\n")
if (file.exists("05_inferential_stats.R")) {
  source("05_inferential_stats.R")
} else {
  stop("CRITICAL ERROR: Missing '05_inferential_stats.R' script.")
}

cat("======================================================================\n")
cat("Pipeline Executed Successfully!\n")

cat("CSV tables are in: ", csv_dir, "\n")
cat("Plots are in:      ", plot_dir, "\n")
cat("======================================================================\n")
