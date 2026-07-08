# ==============================================================================
# R TUTORIAL SCRIPT 07: One-Way ANOVA
# Goal: Learn how to compare the means of MORE THAN TWO groups (e.g., Education Levels).
# ==============================================================================

suppressMessages(library(readxl))

# ------------------------------------------------------------------------------
# STEP 1: Load Data
# ------------------------------------------------------------------------------
raw_data_path <- "../../01_Data/Raw_Data/Thalassemia_Research.xlsx"
know_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"

df_raw <- read_excel(raw_data_path, sheet = 1)
df_know <- read.csv(know_path)

# ------------------------------------------------------------------------------
# STEP 2: Extract Education Level
# ------------------------------------------------------------------------------
# We use grep() to find the column that has "education" in the title.
edu_col <- grep("education", names(df_raw), ignore.case=TRUE, value=TRUE)[1]

df <- data.frame(
  Knowledge = df_know$Weighted_V3_Knowledge_Score,
  # We use trimws() to strip any accidental spaces at the start/end of the text
  Education = trimws(as.character(df_raw[[edu_col]]))
)

# ------------------------------------------------------------------------------
# STEP 3: Running the ANOVA (Analysis of Variance)
# A T-Test only works for 2 groups. When you have 3 or more groups (like Education),
# you must use ANOVA to avoid mathematically inflating your error rate!
#
# In R, the function is aov(Numeric ~ Categorical, data=...)
# ------------------------------------------------------------------------------

cat("\n--- Running One-Way ANOVA for Education Level ---\n")

# Run the aov model and save it to a variable called 'anova_model'
anova_model <- aov(Knowledge ~ Education, data = df)

# By itself, 'anova_model' doesn't show much. We must wrap it in summary() 
# to calculate the actual F-Statistic and P-Value!
summary_data <- summary(anova_model)

print(summary_data)

# ------------------------------------------------------------------------------
# STEP 4: Extracting just the P-Value from the Summary
# The summary object is a complex list. To grab exactly the p-value programmatically:
# [[1]] gets the first table.
# [["Pr(>F)"]] gets the Probability column (the p-value).
# [1] gets the very first number in that column.
# ------------------------------------------------------------------------------

p_val <- summary_data[[1]][["Pr(>F)"]][1]
cat("\nThe extracted exact P-Value is: ", p_val, "\n")

if(p_val < 0.05) {
  cat("Because the p-value is tiny, Education Level is a highly significant predictor of Knowledge!\n")
} else {
  cat("Education Level is not significant.\n")
}
