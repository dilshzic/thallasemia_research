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

# ------------------------------------------------------------------------------
# Data Preparation: Binarize Demographics & Scores
# ------------------------------------------------------------------------------

# Helper function to find column names safely
find_col <- function(df, pattern) {
  col <- grep(pattern, colnames(df), value = TRUE)
  if (length(col) == 0) return(NA)
  return(col[1])
}

# Get columns
gender_col <- find_col(df, "^2\\. Gender")
marital_col <- find_col(df, "^9\\. Marital Status")
age_col <- find_col(df, "^1\\. Age")
prov_col <- find_col(df, "Province")
edu_col <- find_col(df, "^7\\. Education Level")
inc_col <- find_col(df, "^6\\. Monthly Income")

# --- Binarize Demographics ---
# Gender (already binary: Female/Male)
df$B_Gender <- as.character(df[[gender_col]])

# Marital Status (Single vs Married)
df$B_Marital <- ifelse(grepl("Single|Married", as.character(df[[marital_col]])), as.character(df[[marital_col]]), NA)

# Age Group (< 35 vs >= 35)
df$B_Age <- ifelse(as.numeric(df[[age_col]]) < 35, "<35", ">=35")

# Province (Western vs North Western)
df$B_Province <- ifelse(grepl("Western", as.character(df[[prov_col]])) & !grepl("North", as.character(df[[prov_col]])), "Western", 
                 ifelse(grepl("North Western", as.character(df[[prov_col]])), "North Western", NA))

# Education (Up to A/L vs Degree and Above)
df$B_Education <- ifelse(grepl("O/L|A/L", as.character(df[[edu_col]])), "Up to A/L", 
                  ifelse(grepl("Degree|Undergraduate|Graduate", as.character(df[[edu_col]])), "Degree/Above", NA))

# Income (Below Median vs Above Median)
inc_numeric <- dplyr::case_when(
  grepl("< 25,000", as.character(df[[inc_col]])) ~ 1,
  grepl("25,000 – 50,000", as.character(df[[inc_col]])) ~ 2,
  grepl("51,000 – 100,000", as.character(df[[inc_col]])) ~ 3,
  grepl("> 100,000", as.character(df[[inc_col]])) ~ 4,
  TRUE ~ NA_real_
)
med_inc <- median(inc_numeric, na.rm=TRUE)
df$B_Income <- ifelse(inc_numeric <= med_inc, "Below/Equal Median", "Above Median")

# Partner Practice (Safe vs Unsafe/Delayed)
df$B_Partner_Practice <- ifelse(df$Partner_Practice_Raw == "Safe", "Safe", 
                         ifelse(df$Partner_Practice_Raw %in% c("Delayed", "Unsafe"), "Unsafe/Delayed", NA))

# --- Binarize Scores (Median Splits) ---
med_k <- median(df$Expanded_Knowledge_Score, na.rm=TRUE)
med_pa <- median(df$Partner_Attitude, na.rm=TRUE)
med_ca <- median(df$Cascade_Attitude, na.rm=TRUE)
med_cp <- median(df$Cascade_Practice_Score, na.rm=TRUE)

df$Cat_Knowledge <- ifelse(df$Expanded_Knowledge_Score > med_k, "High", "Low")
df$Cat_Partner_Att <- ifelse(df$Partner_Attitude > med_pa, "Good", "Poor")
df$Cat_Cascade_Att <- ifelse(df$Cascade_Attitude > med_ca, "Good", "Poor")
df$Cat_Cascade_Prac <- ifelse(df$Cascade_Practice_Score > med_cp, "Good", "Poor")

# ------------------------------------------------------------------------------
# Run T-Tests
# ------------------------------------------------------------------------------
cat("\nRunning all T-Tests...\n")
t_test_results <- list()

run_ttest <- function(indep, dep, label) {
  sub_df <- df[!is.na(df[[indep]]) & !is.na(df[[dep]]), ]
  groups <- unique(sub_df[[indep]])
  if(length(groups) != 2) return(NULL)
  
  f <- reformulate(paste0("`", indep, "`"), response = paste0("`", dep, "`"))
  res <- tryCatch(t.test(f, data = sub_df, var.equal = FALSE), error = function(e) NULL)
  
  if(!is.null(res)) {
    return(data.frame(
      Test_Label = label,
      Independent_Variable = indep,
      Dependent_Variable = dep,
      t_statistic = res$statistic,
      df = res$parameter,
      p_value = res$p.value,
      Significant = ifelse(res$p.value < 0.05, "Yes", "No")
    ))
  }
  return(NULL)
}

scores <- c("Expanded_Knowledge_Score", "Partner_Attitude", "Cascade_Attitude", "Cascade_Practice_Score")
indeps <- c("B_Gender", "B_Marital", "B_Age", "B_Province", "B_Education", "B_Income")

test_idx <- 1
for(indep in indeps) {
  for(score in scores) {
    res <- run_ttest(indep, score, paste("T-Test", test_idx))
    if(!is.null(res)) t_test_results[[test_idx]] <- res
    test_idx <- test_idx + 1
  }
}

# Cross-KAP T-tests
cross_tests <- list(
  c("B_Partner_Practice", "Expanded_Knowledge_Score"),
  c("B_Partner_Practice", "Partner_Attitude"),
  c("Cat_Cascade_Prac", "Expanded_Knowledge_Score"),
  c("Cat_Cascade_Prac", "Cascade_Attitude")
)
for(ct in cross_tests) {
  res <- run_ttest(ct[1], ct[2], paste("T-Test", test_idx))
  if(!is.null(res)) t_test_results[[test_idx]] <- res
  test_idx <- test_idx + 1
}

t_df_all <- do.call(rbind, t_test_results)
write.csv(t_df_all, file.path(csv_dir, "inferential_ttest.csv"), row.names = FALSE)


# ------------------------------------------------------------------------------
# Run Chi-Square Tests
# ------------------------------------------------------------------------------
cat("Running all Chi-Square Tests...\n")
chisq_results <- list()

run_chisq <- function(var1, var2, label) {
  sub_df <- df[!is.na(df[[var1]]) & !is.na(df[[var2]]), ]
  if(nrow(sub_df) == 0) return(NULL)
  
  tbl <- table(sub_df[[var1]], sub_df[[var2]])
  if(nrow(tbl) < 2 | ncol(tbl) < 2) return(NULL)
  
  res <- tryCatch(chisq.test(tbl, correct = TRUE), error = function(e) NULL)
  
  if(!is.null(res)) {
    return(data.frame(
      Test_Label = label,
      Variable_1 = var1,
      Variable_2 = var2,
      Statistic = res$statistic,
      df = res$parameter,
      p_value = res$p.value,
      Significant = ifelse(res$p.value < 0.05, "Yes", "No")
    ))
  }
  return(NULL)
}

test_idx <- 1
# 1. Demographics vs Knowledge Cat
for(indep in indeps) {
  res <- run_chisq(indep, "Cat_Knowledge", paste("ChiSq", test_idx))
  if(!is.null(res)) chisq_results[[test_idx]] <- res
  test_idx <- test_idx + 1
}

# 2. Demographics vs Attitude Cats
for(indep in c("B_Gender", "B_Marital", "B_Education")) {
  res <- run_chisq(indep, "Cat_Partner_Att", paste("ChiSq", test_idx)); test_idx <- test_idx + 1
  if(!is.null(res)) chisq_results[[test_idx-1]] <- res
}
for(indep in c("B_Gender", "B_Education")) {
  res <- run_chisq(indep, "Cat_Cascade_Att", paste("ChiSq", test_idx)); test_idx <- test_idx + 1
  if(!is.null(res)) chisq_results[[test_idx-1]] <- res
}

# 3. Demographics vs Practice
for(indep in c("B_Gender", "B_Marital", "B_Education", "B_Income")) {
  res <- run_chisq(indep, "B_Partner_Practice", paste("ChiSq", test_idx)); test_idx <- test_idx + 1
  if(!is.null(res)) chisq_results[[test_idx-1]] <- res
}
for(indep in c("B_Gender", "B_Education")) {
  res <- run_chisq(indep, "Cat_Cascade_Prac", paste("ChiSq", test_idx)); test_idx <- test_idx + 1
  if(!is.null(res)) chisq_results[[test_idx-1]] <- res
}

# 4. Cross-KAP Assocs
cross_chisq <- list(
  c("Cat_Knowledge", "Cat_Partner_Att"),
  c("Cat_Knowledge", "Cat_Cascade_Att"),
  c("Cat_Knowledge", "B_Partner_Practice"),
  c("Cat_Knowledge", "Cat_Cascade_Prac"),
  c("Cat_Partner_Att", "B_Partner_Practice"),
  c("Cat_Cascade_Att", "Cat_Cascade_Prac")
)
for(cc in cross_chisq) {
  res <- run_chisq(cc[1], cc[2], paste("ChiSq", test_idx)); test_idx <- test_idx + 1
  if(!is.null(res)) chisq_results[[test_idx-1]] <- res
}

chisq_df_all <- do.call(rbind, chisq_results)
write.csv(chisq_df_all, file.path(csv_dir, "inferential_chisq.csv"), row.names = FALSE)

cat("Stage 5 completed. Inferential outputs saved under '", csv_dir, "'.\n\n", sep = "")
