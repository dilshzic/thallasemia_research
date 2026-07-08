# ==============================================================================
# R TUTORIAL SCRIPT 06: Independent T-Tests
# Goal: Learn how to compare the means of TWO distinct groups (e.g., Male vs Female).
# ==============================================================================

# ------------------------------------------------------------------------------
# STEP 1: Load Libraries
# Libraries are like toolboxes. 'readxl' helps us read Excel files.
# 'dplyr' gives us powerful tools to clean and filter data.
# ------------------------------------------------------------------------------
suppressMessages(library(readxl))
suppressMessages(library(dplyr))

# ------------------------------------------------------------------------------
# STEP 2: Define Paths and Load Data
# R needs to know exactly where the files are on your computer.
# We use <- to assign a value to a variable (it's exactly like = in Python).
# ------------------------------------------------------------------------------
raw_data_path <- "../../01_Data/Raw_Data/Thalassemia_Research.xlsx"
know_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"

# read_excel reads the first sheet of the excel file
df_raw <- read_excel(raw_data_path, sheet = 1)
# read.csv reads standard CSV files
df_know <- read.csv(know_path)

# ------------------------------------------------------------------------------
# STEP 3: Data Cleaning & Merging
# Finding the exact column names using grep() which searches for text.
# ignore.case=TRUE ensures it finds "Gender" even if we type "gender".
# ------------------------------------------------------------------------------
gender_col <- grep("gender", names(df_raw), ignore.case=TRUE, value=TRUE)[1]
marital_col <- "9. Marital Status"

# Create a clean data frame (like a pandas DataFrame or Excel table)
# We only pull the specific columns we want to test.
df <- data.frame(
  Knowledge = df_know$Weighted_V3_Knowledge_Score,
  # We use trimws() to remove accidental spaces, and tolower() to make it lowercase
  Gender = trimws(tolower(as.character(df_raw[[gender_col]]))),
  Marital_Status = trimws(tolower(as.character(df_raw[[marital_col]])))
)

# ------------------------------------------------------------------------------
# STEP 4: Running Welch's T-Test
# A t-test compares the averages of TWO groups. 
# In R, the formula is: t.test( NumericVariable ~ CategoricalVariable, data=YourData )
# The ~ symbol means "explained by" or "vs".
# ------------------------------------------------------------------------------
cat("\n--- Running T-Test for Gender (Male vs Female) ---\n")
# We just pass the formula. R handles the math automatically!
gender_test <- t.test(Knowledge ~ Gender, data = df)

# We can print the full result:
print(gender_test)

# Or we can specifically pull out just the p-value using the $ symbol:
cat("\nThe precise P-Value for Gender is: ", gender_test$p.value, "\n")


cat("\n--- Running T-Test for Marital Status (Married vs Single) ---\n")
# Before testing Marital Status, we must filter out people who answered "Other" or NA.
# We use dplyr's filter() command to only keep Married and Single people.
df_filtered <- df %>% filter(Marital_Status %in% c("married", "single"))

marital_test <- t.test(Knowledge ~ Marital_Status, data = df_filtered)
print(marital_test)
cat("\nThe precise P-Value for Marital Status is: ", marital_test$p.value, "\n")

cat("\nNotice how the Marital Status p-value is < 0.05. This means it is Statistically Significant!\n")
