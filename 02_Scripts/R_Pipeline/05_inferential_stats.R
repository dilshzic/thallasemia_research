# ==============================================================================
# Pipeline Stage 5: Inferential Statistical Analysis
# ==============================================================================

if (!exists("df")) {
  stop("CRITICAL ERROR: Dataframe 'df' is not available in environment. Run Stage 1, 2, 3, and 4 first.")
}

cat("Executing Stage 5: Inferential Statistical Analysis...\n")

# Setup output CSV directory
if (!exists("csv_dir")) {
  csv_dir <- "./outputs/csv"
}

# --- 1. Chi-Square: Education vs. Knowledge Level ---
cat("\nRunning Chi-Square Test: Education Level vs. Knowledge Level...\n")
edu_col <- find_col(df, "^7\\. Education Level")
median_exp_score <- median(df$Expanded_Knowledge_Score, na.rm = TRUE)
df$Knowledge_Level <- ifelse(df$Expanded_Knowledge_Score > median_exp_score, "High", "Low")

# Exclude Missing/No Response
sub_edu <- df %>% 
  dplyr::filter(!is.na(.data[[edu_col]]) & .data[[edu_col]] != "Missing/No Response")

edu_table <- table(sub_edu[[edu_col]], sub_edu$Knowledge_Level)
print(edu_table)

chi_edu <- chisq.test(edu_table)
print(chi_edu)

# Save results to df
chi_edu_df <- data.frame(
  Test = "Chi-Square: Education vs Knowledge Level",
  Statistic = chi_edu$statistic,
  df = chi_edu$parameter,
  p_value = chi_edu$p.value,
  Significant = ifelse(chi_edu$p.value < 0.05, "Yes", "No")
)


# --- 2. Chi-Square: Family History vs. Family Disclosure ---
cat("\nRunning Chi-Square Test: Family History vs. Family Disclosure...\n")
hist_col <- find_col(df, "^11\\. Do you have a family history")
disc_col <- find_col(df, "^36\\. Do your family members")

sub_hist <- df %>%
  dplyr::filter(.data[[hist_col]] %in% c("Yes", "No") & .data[[disc_col]] %in% c("Yes", "No"))

hist_table <- table(sub_hist[[hist_col]], sub_hist[[disc_col]])
print(hist_table)

chi_hist <- chisq.test(hist_table, correct = TRUE) # Yates continuity correction
print(chi_hist)

chi_hist_df <- data.frame(
  Test = "Chi-Square: Family History vs Family Disclosure",
  Statistic = chi_hist$statistic,
  df = chi_hist$parameter,
  p_value = chi_hist$p.value,
  Significant = ifelse(chi_hist$p.value < 0.05, "Yes", "No")
)


# --- 3. Chi-Square: Marital Status vs. Partner Screening ---
cat("\nRunning Chi-Square Test: Marital Status vs. Partner Screening...\n")
status_col <- find_col(df, "^9\\. Marital Status")
practice_col <- find_col(df, "^33\\. What was your practice")

screened_categories <- c("Partner was screened before marriage", "Partner was screened after marriage", "Partner was screened during pregnancy")
unscreened_categories <- c("Did not screen partner", "Did not disclose thalassemia carrier state to partner")

df$Partner_Screened_Recoded <- NA_character_
df$Partner_Screened_Recoded[df[[practice_col]] %in% screened_categories] <- "Screened"
df$Partner_Screened_Recoded[df[[practice_col]] %in% unscreened_categories] <- "Unscreened"

sub_marital <- df %>%
  dplyr::filter(.data[[status_col]] %in% c("Single", "Married") & !is.na(Partner_Screened_Recoded))

marital_table <- table(sub_marital[[status_col]], sub_marital$Partner_Screened_Recoded)
print(marital_table)

chi_mar <- chisq.test(marital_table, correct = TRUE)
print(chi_mar)

chi_mar_df <- data.frame(
  Test = "Chi-Square: Marital Status vs Partner Screening Practice",
  Statistic = chi_mar$statistic,
  df = chi_mar$parameter,
  p_value = chi_mar$p.value,
  Significant = ifelse(chi_mar$p.value < 0.05, "Yes", "No")
)

# Combine and save all Chi-Squares
chisq_all <- rbind(chi_edu_df, chi_hist_df, chi_mar_df)
write.csv(chisq_all, file.path(csv_dir, "inferential_chisq.csv"), row.names = FALSE)


# --- 4. T-Test: Gender vs. Expanded Knowledge Score ---
cat("\nRunning Welch's Independent t-test: Gender vs. Knowledge Score...\n")
gender_col <- find_col(df, "^2\\. Gender")

sub_gen <- df %>% dplyr::filter(.data[[gender_col]] %in% c("Female", "Male"))
formula_t <- reformulate(paste0("`", gender_col, "`"), response = "Expanded_Knowledge_Score")
t_res <- t.test(formula_t, data = sub_gen, var.equal = FALSE)
print(t_res)

# Save t-test summary
t_df <- data.frame(
  Test = "Welch t-test: Gender vs Expanded Knowledge Score",
  t_statistic = t_res$statistic,
  df = t_res$parameter,
  p_value = t_res$p.value,
  Mean_Female = mean(df$Expanded_Knowledge_Score[df[[gender_col]] == "Female"], na.rm=TRUE),
  Mean_Male = mean(df$Expanded_Knowledge_Score[df[[gender_col]] == "Male"], na.rm=TRUE),
  Significant = ifelse(t_res$p.value < 0.05, "Yes", "No")
)
write.csv(t_df, file.path(csv_dir, "inferential_ttest.csv"), row.names = FALSE)


# --- 5. ANOVA: Education Level vs. Expanded Knowledge Score ---
cat("\nRunning One-Way ANOVA: Education Level vs. Knowledge Score...\n")
formula_anova <- reformulate(paste0("`", edu_col, "`"), response = "Expanded_Knowledge_Score")
anova_res <- aov(formula_anova, data = sub_edu)
print(summary(anova_res))

# Save ANOVA summary table
anova_sum <- summary(anova_res)[[1]]
anova_df <- data.frame(
  Source = row.names(anova_sum),
  Df = anova_sum$Df,
  Sum_Sq = anova_sum$`Sum Sq`,
  Mean_Sq = anova_sum$`Mean Sq`,
  F_value = anova_sum$`F value`,
  Pr_F = anova_sum$`Pr(>F)`
)
write.csv(anova_df, file.path(csv_dir, "inferential_anova.csv"), row.names = FALSE)


# --- 6. Linear Regression: Predict Expanded Knowledge Score ---
cat("\nFitting Multiple Linear Regression Model...\n")
income_col <- find_col(df, "^6\\. Monthly Income")
age_col <- find_col(df, "^1\\. Age")

# Prepare regression dataframe (remove Missing/No Response categories)
reg_df <- df %>%
  dplyr::mutate(
    Age = as.numeric(.data[[age_col]]),
    Gender = .data[[gender_col]],
    Education = .data[[edu_col]],
    Income = .data[[income_col]]
  ) %>%
  dplyr::filter(
    !is.na(Age) & 
    Gender %in% c("Female", "Male") &
    !is.na(Education) & Education != "Missing/No Response" &
    !is.na(Income) & Income != "Missing/No Response"
  )

# Set baselines matching Python statsmodels analysis
reg_df$Gender <- factor(reg_df$Gender, levels = c("Female", "Male"))
reg_df$Education <- factor(reg_df$Education, levels = c("Up to O/L", "Up to A/L", "Undergraduate", "Graduate"))
reg_df$Income <- factor(reg_df$Income, levels = c("< 25,000", "25,000 – 50,000", "51,000 – 100,000", "> 100,000"))

lm_res <- lm(Expanded_Knowledge_Score ~ Age + Gender + Education + Income, data = reg_df)
print(summary(lm_res))

# Save regression coefficients table
lm_sum <- summary(lm_res)$coefficients
lm_df <- data.frame(
  Term = row.names(lm_sum),
  Estimate = lm_sum[, "Estimate"],
  Std_Error = lm_sum[, "Std. Error"],
  t_value = lm_sum[, "t value"],
  p_value = lm_sum[, "Pr(>|t|)"],
  Significant = ifelse(lm_sum[, "Pr(>|t|)"] < 0.05, "Yes", "No")
)
write.csv(lm_df, file.path(csv_dir, "inferential_regression.csv"), row.names = FALSE)

cat("Stage 5 completed. Inferential outputs saved under '", csv_dir, "'.\n\n", sep = "")
