# ==============================================================================
# Thalassemia Survey Data Analysis Pipeline
# Python Main Orchestrator Script
# ==============================================================================

import os
import sys
import subprocess

print("======================================================================")
print("Initializing Thalassemia Survey Python Analysis Pipeline...")
print("======================================================================\n")

# Add current folder to path to enable local module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# --- 1. Package Management & Setup ---
required_packages = {
    "pandas": "pandas",
    "numpy": "numpy",
    "openpyxl": "openpyxl",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "scipy": "scipy",
    "statsmodels": "statsmodels"
}

print("Checking package dependencies...")
missing_packages = []
for pkg_name, pip_name in required_packages.items():
    try:
        __import__(pkg_name)
    except ImportError:
        missing_packages.append(pip_name)

if missing_packages:
    print(f"The following required packages are missing: {', '.join(missing_packages)}")
    print("Attempting to install missing packages via pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user"] + missing_packages + ["--break-system-packages"])
        print("Installation completed successfully!\n")
    except Exception as e:
        print(f"Error installing packages: {e}")
        print("Please manually install the missing packages using: pip install " + " ".join(missing_packages))
        sys.exit(1)
else:
    print("All required packages are already installed.\n")

# --- 2. Environment Configurations ---
xlsx_path = "/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx"

# Relative fallback
if not os.path.exists(xlsx_path):
    xlsx_path = os.path.join(current_dir, "..", "Thalassemia_Research.xlsx")

if not os.path.exists(xlsx_path):
    print(f"CRITICAL ERROR: Could not locate 'Thalassemia_Research.xlsx'. Checked absolute and parent directories.")
    sys.exit(1)

print(f"Dataset located at: {os.path.abspath(xlsx_path)}")

# Output directories setup
output_base = os.path.join(current_dir, "outputs")
csv_dir = os.path.join(output_base, "csv")
plot_dir = os.path.join(output_base, "plots")

os.makedirs(csv_dir, exist_ok=True)
os.makedirs(plot_dir, exist_ok=True)

print("Output directories initialized under './outputs/'.\n")

# --- 3. Run Pipeline Stages ---

# Stage 1: Load and Clean Data
print("----------------------------------------------------------------------")
print("Stage 1: Executing Data Loader & Cleaning...")
try:
    import loader_01
    df = loader_01.load_and_clean_data(xlsx_path)
    print("Stage 1 completed successfully. Cleaned dataframe loaded.\n")
except Exception as e:
    print(f"CRITICAL ERROR during Stage 1: {e}")
    sys.exit(1)

# Stage 2: Knowledge Scoring & Z-Scores
print("----------------------------------------------------------------------")
print("Stage 2: Executing Scoring System...")
try:
    import scoring_02
    df = scoring_02.calculate_scores(df)
    print("Stage 2 completed successfully. Scores integrated into dataframe.\n")
except Exception as e:
    print(f"CRITICAL ERROR during Stage 2: {e}")
    sys.exit(1)

# Stage 3: Descriptive Statistics Summary
print("----------------------------------------------------------------------")
print("Stage 3: Running Descriptive Statistics summaries...")
try:
    import descriptive_03
    descriptive_03.run_descriptive_stats(df, csv_dir)
    print(f"Stage 3 completed successfully. CSV files saved in {csv_dir}.\n")
except Exception as e:
    print(f"CRITICAL ERROR during Stage 3: {e}")
    sys.exit(1)

# Stage 4: Visualizations
print("----------------------------------------------------------------------")
print("Stage 4: Generating plots...")
try:
    import visualizations_04
    visualizations_04.generate_plots(df, plot_dir)
    print(f"Stage 4 completed successfully. Visual plots saved in {plot_dir}.\n")
except Exception as e:
    print(f"CRITICAL ERROR during Stage 4: {e}")
    sys.exit(1)

# Stage 5: Inferential Statistical Analysis
print("----------------------------------------------------------------------")
print("Stage 5: Executing Inferential Statistical Analysis...")
try:
    import inferential_05
    inferential_05.run_inferential_stats(df, csv_dir)
    print(f"Stage 5 completed successfully. Inferential results saved in {csv_dir}.\n")
except Exception as e:
    print(f"CRITICAL ERROR during Stage 5: {e}")
    sys.exit(1)

print("======================================================================")
print("Python Pipeline Executed Successfully!")
print(f"CSV files folder:  {os.path.abspath(csv_dir)}")
print(f"Plot files folder: {os.path.abspath(plot_dir)}")
print("======================================================================\n")
