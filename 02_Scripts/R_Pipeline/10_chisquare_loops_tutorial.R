# ==============================================================================
# R TUTORIAL SCRIPT 10: For-Loops and Matrices (Advanced Chi-Square)
# Goal: Learn how to automate repeating code (like running 30 Chi-Squares!)
# ==============================================================================

suppressMessages(library(readxl))

# ------------------------------------------------------------------------------
# STEP 1: Load the raw data and previously processed scores
# ------------------------------------------------------------------------------
raw_data_path <- "../../01_Data/Raw_Data/Thalassemia_Research.xlsx"
know_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"
att_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv"

df_raw <- read_excel(raw_data_path, sheet = 1)
df_know <- read.csv(know_path)
df_att <- read.csv(att_path)

edu_col <- grep("education", names(df_raw), ignore.case=TRUE, value=TRUE)[1]
gender_col <- grep("gender", names(df_raw), ignore.case=TRUE, value=TRUE)[1]

df <- data.frame(
  Knowledge = df_know$Weighted_V3_Knowledge_Score,
  Attitude = df_att$Weighted_V3_Partner_Attitude,
  Education = trimws(as.character(df_raw[[edu_col]])),
  Gender = trimws(tolower(as.character(df_raw[[gender_col]])))
)

# Convert scores into categories (Median Split)
df$Knowledge_Cat <- ifelse(df$Knowledge > median(df$Knowledge, na.rm=T), "High", "Low")
df$Attitude_Cat <- ifelse(df$Attitude > median(df$Attitude, na.rm=T), "Good", "Poor")

# ------------------------------------------------------------------------------
# STEP 2: Creating a Matrix (Grid) to store results
# A matrix in R is just an empty 2D grid of rows and columns.
# ------------------------------------------------------------------------------

# Let's say we want to test 2 Demographics against 2 KAP scores.
my_demographics <- c("Gender", "Education")
my_scores <- c("Knowledge_Cat", "Attitude_Cat")

# Create an empty grid with 2 rows and 2 columns
results_grid <- matrix(NA, nrow=length(my_demographics), ncol=length(my_scores))

# Name the rows and columns so we know what they are!
rownames(results_grid) <- my_demographics
colnames(results_grid) <- my_scores

cat("\n--- Here is our empty Matrix Grid ---\n")
print(results_grid)

# ------------------------------------------------------------------------------
# STEP 3: Using FOR LOOPS to fill the grid automatically
# Instead of writing chisq.test() 4 different times, we use a loop!
# 'i' loops through the rows (demographics)
# 'j' loops through the columns (scores)
# ------------------------------------------------------------------------------

cat("\n--- Running Automated Chi-Square Loop ---\n")

for(i in 1:length(my_demographics)) {
  
  for(j in 1:length(my_scores)) {
    
    # 1. Grab the specific Demographic column (e.g., "Gender")
    demo_column <- df[[ my_demographics[i] ]]
    
    # 2. Grab the specific Score column (e.g., "Knowledge_Cat")
    score_column <- df[[ my_scores[j] ]]
    
    # 3. Build the table and run the test!
    my_table <- table(demo_column, score_column)
    
    # suppressWarnings() hides errors if a table has too few people in a category
    test_result <- suppressWarnings( chisq.test(my_table) )
    
    # 4. Save the P-Value directly into our grid at Row [i] and Col [j]!
    # round(value, 4) just rounds the decimal to 4 places.
    results_grid[i, j] <- round(test_result$p.value, 4)
    
  }
}

# ------------------------------------------------------------------------------
# STEP 4: View the Final Results
# ------------------------------------------------------------------------------

cat("\n--- Completed P-Value Matrix ---\n")
print(as.data.frame(results_grid))

cat("\nNotice how Education has tiny numbers (<0.05). Education is significant!\n")
cat("Notice how Gender has large numbers (>0.05). Gender is not significant!\n")
