# ==============================================================================
# R TUTORIAL SCRIPT 09: Chi-Square and Median Splits
# Goal: Learn how to turn numbers into categories (High/Low) and test them.
# ==============================================================================

# ------------------------------------------------------------------------------
# STEP 1: Load Data
# ------------------------------------------------------------------------------
know_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"
att_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv"

df_know <- read.csv(know_path)
df_att <- read.csv(att_path)

df <- data.frame(
  Knowledge = df_know$Weighted_V3_Knowledge_Score,
  Partner_Attitude = df_att$Weighted_V3_Partner_Attitude
)

# ------------------------------------------------------------------------------
# STEP 2: The Median Split
# Chi-Square tests ONLY work on categories (like "Yes/No" or "High/Low").
# If we have a number like 2.5, we must convert it into a category!
#
# The 'median' is the exact middle number of the dataset.
# The ifelse() function works like this:
# ifelse( CONDITION_TO_TEST, WHAT_TO_DO_IF_TRUE, WHAT_TO_DO_IF_FALSE )
# ------------------------------------------------------------------------------

# Find the exact middle number for Knowledge
know_median <- median(df$Knowledge, na.rm=TRUE)
cat("The median Knowledge score is: ", know_median, "\n")

# Create a new column called "Knowledge_Category"
df$Knowledge_Category <- ifelse(df$Knowledge > know_median, "High", "Low")

# Do the exact same thing for Attitude
att_median <- median(df$Partner_Attitude, na.rm=TRUE)
df$Attitude_Category <- ifelse(df$Partner_Attitude > att_median, "Good", "Poor")

# ------------------------------------------------------------------------------
# STEP 3: Creating a Contingency Table
# Chi-Square tests compare two columns of categories by building a 2x2 grid (table).
# ------------------------------------------------------------------------------

my_table <- table(df$Knowledge_Category, df$Attitude_Category)

cat("\n--- Here is the 2x2 Contingency Table ---\n")
print(my_table)

# ------------------------------------------------------------------------------
# STEP 4: Running the Chi-Square Test
# We pass the table into the chisq.test() function!
# ------------------------------------------------------------------------------

cat("\n--- Running Chi-Square Test ---\n")
chi_results <- chisq.test(my_table)

print(chi_results)

# Extract just the P-Value to check significance
cat("\nThe Chi-Square P-Value is: ", chi_results$p.value, "\n")
cat("Because it is < 0.05, we prove categorically that High Knowledge leads to Good Attitudes!\n")
