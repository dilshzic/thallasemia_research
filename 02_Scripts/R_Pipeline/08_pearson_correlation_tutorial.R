# ==============================================================================
# R TUTORIAL SCRIPT 08: Pearson Correlations
# Goal: Learn how to find the mathematical relationship between two CONTINUOUS numbers.
# ==============================================================================

# ------------------------------------------------------------------------------
# STEP 1: Load Data
# ------------------------------------------------------------------------------
know_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"
att_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv"

# Since both files are simple CSVs, we use the base R read.csv() command.
df_know <- read.csv(know_path)
df_att <- read.csv(att_path)

# ------------------------------------------------------------------------------
# STEP 2: Create a Unified Data Frame
# ------------------------------------------------------------------------------
# Both Knowledge and Attitude are continuous numbers (e.g. 2.45, -1.2, 5.0)
df <- data.frame(
  Knowledge = df_know$Weighted_V3_Knowledge_Score,
  Partner_Attitude = df_att$Weighted_V3_Partner_Attitude
)

# ------------------------------------------------------------------------------
# STEP 3: Running a Pearson Correlation
# When you want to see if one number goes up as another number goes up, you 
# use a Correlation Test!
# 
# The function is: cor.test( Numeric1, Numeric2, method="pearson", use="complete.obs" )
# "complete.obs" tells R to ignore any rows that have missing NA data!
# ------------------------------------------------------------------------------

cat("\n--- Running Pearson Correlation (Knowledge vs Attitude) ---\n")

pearson_test <- cor.test(df$Knowledge, df$Partner_Attitude, 
                         method="pearson", 
                         use="complete.obs")

print(pearson_test)

# ------------------------------------------------------------------------------
# STEP 4: Understanding the Results
# ------------------------------------------------------------------------------
# In a Pearson test, you look at TWO numbers:
# 1. The P-Value: Is the relationship real, or just random chance? (< 0.05 is real).
# 2. The 'r' estimate: How strong is the relationship? 
#    * +1.0 means a perfect positive relationship.
#    * -1.0 means a perfect negative relationship.
#    *  0.0 means no relationship at all.

cat("\nThe P-Value is: ", pearson_test$p.value)
cat("\nThe Pearson 'r' Correlation Coefficient is: ", pearson_test$estimate, "\n")

cat("\nBecause 'r' is +0.382, it means as Knowledge goes up, Attitude ALSO goes up!\n")
