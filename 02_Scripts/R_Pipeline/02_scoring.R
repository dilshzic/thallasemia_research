# ==============================================================================
# Pipeline Stage 2: Knowledge Scores & Z-Scores Calculation
# ==============================================================================

# 1. Checking for Data
# Make sure the 'df' data we cleaned in Stage 1 actually exists before we try scoring it.
if (!exists("df")) {
  stop("CRITICAL ERROR: Dataframe 'df' is not available in environment. Run Stage 1 first.")
}

cat("Calculating scoring metrics...\n")

# 2. Finding the Questions (Q16 & Q27)
# grep() searches for column names that match the text of Questions 16 and 27.
q16_cols <- grep("^16\\. What are the clinical forms of thalassemia\\? \\(Tick all that apply\\)/", colnames(df), value = TRUE)

# Remove the "I don't know" option from Q16 so it doesn't count as a correct answer.
q16_cols <- q16_cols[!grepl("I don’t know", q16_cols)]

q27_cols <- grep("^27\\. Problems faced by thalassemia major patients \\(Tick all that apply\\):/", colnames(df), value = TRUE)

cat("Found", length(q16_cols), "columns for Q16 (forms) and", length(q27_cols), "columns for Q27 (complications).\n")

# 3. Converting Answers to Numbers
# Checkboxes are text, but we need numbers to calculate a score.
# This changes text to numbers, and replaces missing data (NA) with a 0.
df_numeric_scores <- df %>%
  dplyr::mutate(across(c(all_of(q16_cols), all_of(q27_cols)), ~ {
    val <- as.numeric(.x)
    ifelse(is.na(val), 0, val)
  }))

# 4. Calculating the Total Score
# rowSums() adds up all the points from Q16 and Q27 for each person.
df$Knowledge_Score <- rowSums(df_numeric_scores[, c(q16_cols, q27_cols)])

# 5. Standardizing the Score (Z-Score)
# A Z-score tells us how far a person's score is from the group average.
# It uses the mean (average) and standard deviation (spread of the scores).
mean_basic <- mean(df$Knowledge_Score)
sd_basic <- sd(df$Knowledge_Score)
df$Knowledge_Score_Z_Score <- (df$Knowledge_Score - mean_basic) / sd_basic

cat("Basic Knowledge Scores summary:\n")
cat("  Mean Score: ", round(mean_basic, 4), "\n")
cat("  SD Score:   ", round(sd_basic, 4), "\n\n")


# --- Compute Expanded Knowledge Score (All 11 knowledge questions, max 20 points) ---
# Correct answers definitions:
q15_correct <- "Yes"
q17_correct <- "Thalassemia major (severe form)"
q19_correct <- "Yes"
q20_correct <- c("Very difficult (e.g., bone marrow transplant)", "Cannot be cured")
q21_correct <- "Can be prevented"
q22_correct <- "From generation to generation (hereditary)"
q23_correct <- "Healthy"
q24_correct <- "Has a chance to be affected (e.g., 25%)"
q26_correct <- "40–100"

cat("Computing Expanded Knowledge Scores (max 20 points)...\n")

# Initialize expanded score vector
expanded_scores <- numeric(nrow(df))

# Add Q15 score (1 point)
q15_col <- "15. Is thalassemia a blood-related disease?"
expanded_scores <- expanded_scores + as.numeric(df[[q15_col]] == q15_correct & !is.na(df[[q15_col]]))

# Add Q16 score (sum of form checkboxes: up to 3 points)
expanded_scores <- expanded_scores + rowSums(df_numeric_scores[, q16_cols])

# Add Q17 score (1 point)
q17_col <- "17. What is the most severe form of thalassemia?"
# Use grepl or exact match since it has double spaces in raw data but normalized inStage 1 loader
expanded_scores <- expanded_scores + as.numeric(df[[q17_col]] == q17_correct & !is.na(df[[q17_col]]))

# Add Q19 score (1 point)
q19_col <- "19. Does thalassemia major require lifelong treatment?"
expanded_scores <- expanded_scores + as.numeric(df[[q19_col]] == q19_correct & !is.na(df[[q19_col]]))

# Add Q20 score (1 point)
q20_col <- "20. Can thalassemia major be cured?"
expanded_scores <- expanded_scores + as.numeric(df[[q20_col]] %in% q20_correct & !is.na(df[[q20_col]]))

# Add Q21 score (1 point)
q21_col <- "21. Can the spread of thalassemia be prevented?"
expanded_scores <- expanded_scores + as.numeric(df[[q21_col]] == q21_correct & !is.na(df[[q21_col]]))

# Add Q22 score (1 point)
q22_col <- "22. How is thalassemia transmitted?"
expanded_scores <- expanded_scores + as.numeric(df[[q22_col]] == q22_correct & !is.na(df[[q22_col]]))

# Add Q23 score (1 point)
q23_col <- "23. Is a thalassemia carrier usually sick or healthy?"
expanded_scores <- expanded_scores + as.numeric(df[[q23_col]] == q23_correct & !is.na(df[[q23_col]]))

# Add Q24 score (1 point)
q24_col <- "24. A child born from two thalassemia carriers will be:"
expanded_scores <- expanded_scores + as.numeric(df[[q24_col]] == q24_correct & !is.na(df[[q24_col]]))

# Add Q26 score (1 point)
q26_col <- "26. How many thalassemia births occur in Sri Lanka per year?"
expanded_scores <- expanded_scores + as.numeric(df[[q26_col]] == q26_correct & !is.na(df[[q26_col]]))

# Add Q27 score (sum of complications: up to 8 points)
expanded_scores <- expanded_scores + rowSums(df_numeric_scores[, q27_cols])

# Store Expanded scores in dataframe
df$Expanded_Knowledge_Score <- expanded_scores

# Calculate Expanded Z-score
mean_exp <- mean(df$Expanded_Knowledge_Score)
sd_exp <- sd(df$Expanded_Knowledge_Score)
df$Expanded_Knowledge_Score_Z_Score <- (df$Expanded_Knowledge_Score - mean_exp) / sd_exp

cat("Expanded Knowledge Scores summary:\n")
cat("  Mean Score: ", round(mean_exp, 4), "\n")
cat("  SD Score:   ", round(sd_exp, 4), "\n\n")


# --- Compute (1-p) Difficulty-Weighted Knowledge Score ---
# Each item is weighted by (1 - proportion_correct), so hard questions
if (FALSE) {
# (answered correctly by fewer participants) receive more weight.
cat("Computing (1-p) Difficulty-Weighted Knowledge Scores...\n")

# Reconstruct all individual binary item columns
item_matrix <- data.frame(
  Q15 = as.numeric(df[[q15_col]] == q15_correct & !is.na(df[[q15_col]])),
  Q17 = as.numeric(df[[q17_col]] == q17_correct & !is.na(df[[q17_col]])),
  Q19 = as.numeric(df[[q19_col]] == q19_correct & !is.na(df[[q19_col]])),
  Q20 = as.numeric(df[[q20_col]] %in% q20_correct & !is.na(df[[q20_col]])),
  Q21 = as.numeric(df[[q21_col]] == q21_correct & !is.na(df[[q21_col]])),
  Q22 = as.numeric(df[[q22_col]] == q22_correct & !is.na(df[[q22_col]])),
  Q23 = as.numeric(df[[q23_col]] == q23_correct & !is.na(df[[q23_col]])),
  Q24 = as.numeric(df[[q24_col]] == q24_correct & !is.na(df[[q24_col]])),
  Q26 = as.numeric(df[[q26_col]] == q26_correct & !is.na(df[[q26_col]]))
)

# Add Q16 checkbox sub-items
for (col_name in q16_cols) {
  safe_name <- paste0("Q16_", which(q16_cols == col_name))
  item_matrix[[safe_name]] <- as.numeric(df_numeric_scores[[col_name]])
}

# Add Q27 checkbox sub-items
for (col_name in q27_cols) {
  safe_name <- paste0("Q27_", which(q27_cols == col_name))
  item_matrix[[safe_name]] <- as.numeric(df_numeric_scores[[col_name]])
}

n_items <- ncol(item_matrix)
cat("  Total binary knowledge items:", n_items, "\n")

# Compute (1-p) weights for each item
item_proportions <- colMeans(item_matrix, na.rm = TRUE)
item_weights <- 1 - item_proportions

cat("\n  Item Difficulty Weights:\n")
cat(sprintf("  %-15s %8s %10s %10s\n", "Item", "% Correct", "Difficulty", "Weight"))
cat("  ", strrep("-", 50), "\n")
for (i in seq_along(item_weights)) {
  item_name <- names(item_weights)[i]
  pct <- item_proportions[i] * 100
  difficulty <- ifelse(pct > 60, "EASY", ifelse(pct > 30, "MEDIUM", "HARD"))
  cat(sprintf("  %-15s %7.1f%%   %-10s %8.4f\n", item_name, pct, difficulty, item_weights[i]))
}

max_possible_weight <- sum(item_weights)
cat("\n  Max possible weighted score:", round(max_possible_weight, 4), "\n")

# Compute difficulty-weighted score: sum of (item_value * weight)
df$DiffW_Knowledge_Score <- as.numeric(as.matrix(item_matrix) %*% item_weights)

# Compute Z-score for difficulty-weighted score
mean_dw <- mean(df$DiffW_Knowledge_Score)
sd_dw <- sd(df$DiffW_Knowledge_Score)
if (sd_dw > 0) {
  df$DiffW_Knowledge_Score_Z_Score <- (df$DiffW_Knowledge_Score - mean_dw) / sd_dw
} else {
  df$DiffW_Knowledge_Score_Z_Score <- 0
}

cat("\nDifficulty-Weighted Knowledge Scores summary:\n")
cat("  Mean Score: ", round(mean_dw, 4), "\n")
cat("  SD Score:   ", round(sd_dw, 4), "\n")
cat("  Median:     ", round(median(df$DiffW_Knowledge_Score), 4), "\n")
cat("  Min:        ", round(min(df$DiffW_Knowledge_Score), 4), "\n")
cat("  Max:        ", round(max(df$DiffW_Knowledge_Score), 4), "\n")

# Correlation between raw and difficulty-weighted scores
r_pearson <- cor(df$Expanded_Knowledge_Score, df$DiffW_Knowledge_Score)
r_spearman <- cor(df$Expanded_Knowledge_Score, df$DiffW_Knowledge_Score, method = "spearman")
cat("  Correlation with Raw Score:\n")
cat("    Pearson:  r =", round(r_pearson, 4), "\n")
cat("    Spearman: ρ =", round(r_spearman, 4), "\n\n")
}

# --- Compute Attitude & Practice Scores ---
cat("Computing Attitude and Practice Scores...\n")

# Partner Attitude Score
q28_cols <- grep("^28\\. What should a thalassemia carrier do after diagnosis\\? \\(Tick all that apply\\)/", colnames(df), value = TRUE)
q30_col <- grep("^30\\.", colnames(df), value = TRUE)[1]
q31_col <- grep("^31\\.", colnames(df), value = TRUE)[1]
q32_col <- grep("^32\\.", colnames(df), value = TRUE)[1]
q34_col <- grep("^34\\.", colnames(df), value = TRUE)[1]

df$Partner_Attitude <- 0
# Q28
for (col in q28_cols) {
  opt <- tolower(stringr::str_split(col, "/", simplify=TRUE)[,2])
  if (length(opt) == 0) next
  val <- df[[col]]
  val[is.na(val)] <- 0
  if (grepl("get the partner tested", opt)) df$Partner_Attitude <- df$Partner_Attitude + ifelse(val == 1, 1, 0)
  if (grepl("get family members tested", opt)) df$Partner_Attitude <- df$Partner_Attitude + ifelse(val == 1, 1, 0)
  if (grepl("ignore it", opt)) df$Partner_Attitude <- df$Partner_Attitude + ifelse(val == 1, -2, 0)
}
# Q30
df$Partner_Attitude <- df$Partner_Attitude + dplyr::case_when(
  grepl("definitely not", tolower(df[[q30_col]])) ~ 1,
  grepl("not sure", tolower(df[[q30_col]])) ~ -1,
  grepl("yes i am willing|yes i have", tolower(df[[q30_col]])) ~ -2,
  TRUE ~ 0
)
# Q31
df$Partner_Attitude <- df$Partner_Attitude + dplyr::case_when(
  grepl("^no$", tolower(df[[q31_col]])) ~ 1,
  grepl("yes", tolower(df[[q31_col]])) ~ -1,
  TRUE ~ 0
)
# Q32
df$Partner_Attitude <- df$Partner_Attitude + dplyr::case_when(
  grepl("very important", tolower(df[[q32_col]])) ~ 2,
  grepl("^important", tolower(df[[q32_col]])) ~ 1,
  grepl("not important", tolower(df[[q32_col]])) ~ -1,
  TRUE ~ 0
)
# Q34
df$Partner_Attitude <- df$Partner_Attitude + dplyr::case_when(
  grepl("lack of understanding|did not think it was necessary|concern about causing worry", tolower(df[[q34_col]])) ~ -1,
  TRUE ~ 0
)

# Cascade Attitude Score
q35_col <- grep("^35\\.", colnames(df), value = TRUE)[1]
q36_col <- grep("^36\\.", colnames(df), value = TRUE)[1]
q40_col <- grep("^40\\.", colnames(df), value = TRUE)[1]

df$Cascade_Attitude <- 0
df$Cascade_Attitude <- df$Cascade_Attitude + dplyr::case_when(
  grepl("agree", tolower(df[[q35_col]])) & !grepl("disagree", tolower(df[[q35_col]])) ~ 1,
  grepl("disagree", tolower(df[[q35_col]])) ~ -1,
  TRUE ~ 0
)
df$Cascade_Attitude <- df$Cascade_Attitude + dplyr::case_when(
  grepl("^yes$", tolower(df[[q36_col]])) ~ 1,
  grepl("^no$", tolower(df[[q36_col]])) ~ -1,
  TRUE ~ 0
)
df$Cascade_Attitude <- df$Cascade_Attitude + dplyr::case_when(
  grepl("very important", tolower(df[[q40_col]])) ~ 2,
  grepl("^important", tolower(df[[q40_col]])) ~ 1,
  grepl("not important", tolower(df[[q40_col]])) ~ -1,
  TRUE ~ 0
)

# Partner Practice
q33_col <- grep("^33\\.", colnames(df), value = TRUE)[1]
map_partner_practice <- function(x) {
  v <- tolower(as.character(x))
  if (grepl("before marriage", v)) return("Safe")
  if (grepl("after marriage|pregnancy", v)) return("Delayed")
  if (grepl("did not screen|did not disclose", v)) return("Unsafe")
  return(NA_character_)
}
df$Partner_Practice_Raw <- sapply(df[[q33_col]], map_partner_practice)

# Cascade Practice
col_1st <- grep("first-degree", colnames(df), ignore.case=TRUE, value=TRUE)[1]
col_2nd <- grep("second-degree", colnames(df), ignore.case=TRUE, value=TRUE)[1]
col_3rd <- grep("third-degree", colnames(df), ignore.case=TRUE, value=TRUE)[1]

score_relative <- function(x) {
  v <- tolower(as.character(x))
  ifelse(grepl("all", v), 2, ifelse(grepl("some", v), 1, 0))
}
df$Cascade_Practice_Score <- as.numeric(sapply(df[[col_1st]], score_relative)) +
                             as.numeric(sapply(df[[col_2nd]], score_relative)) +
                             as.numeric(sapply(df[[col_3rd]], score_relative))

cat("Attitude and Practice Scores computed successfully.\n\n")

# --- Verification ---
cat("Verification metrics:\n")
cat("  Mean of Basic Z-Scores:   ", round(mean(df$Knowledge_Score_Z_Score), 6), "\n")
cat("  SD of Basic Z-Scores:     ", round(sd(df$Knowledge_Score_Z_Score), 6), "\n")
cat("  Mean of Expanded Z-Scores:", round(mean(df$Expanded_Knowledge_Score_Z_Score), 6), "\n")
cat("  SD of Expanded Z-Scores:  ", round(sd(df$Expanded_Knowledge_Score_Z_Score), 6), "\n")
# cat("  Mean of DiffW Z-Scores:   ", round(mean(df$DiffW_Knowledge_Score_Z_Score), 6), "\n")
# cat("  SD of DiffW Z-Scores:     ", round(sd(df$DiffW_Knowledge_Score_Z_Score), 6), "\n")

cat("Stage 2 completed. Scores added to 'df'.\n\n")

