# ==============================================================================
# Pipeline Stage 3: Descriptive Statistics Summaries
# ==============================================================================

if (!exists("df")) {
  stop("CRITICAL ERROR: Dataframe 'df' is not available in environment. Run Stage 1 and 2 first.")
}

cat("Calculating descriptive statistics tables...\n")

# --- Helper Function: Dynamic Column Finder ---
find_col <- function(dataframe, pattern) {
  cols <- colnames(dataframe)
  matched <- cols[grepl(pattern, cols, ignore.case = TRUE)]
  if (length(matched) > 0) {
    return(matched[1])
  } else {
    stop(paste("CRITICAL ERROR: Could not locate column matching pattern:", pattern))
  }
}

# --- Helper Function: Single Select Frequency Table ---
calc_freq <- function(dataframe, column_name, question_id = "") {
  dataframe %>%
    dplyr::mutate(Response = ifelse(is.na(.data[[column_name]]), "Missing/No Response", as.character(.data[[column_name]]))) %>%
    dplyr::group_by(Response) %>%
    dplyr::summarise(Frequency = n(), .groups = 'drop') %>%
    dplyr::mutate(
      Percentage = (Frequency / sum(Frequency)) * 100,
      Question_ID = question_id,
      Question = column_name
    ) %>%
    dplyr::select(Question_ID, Question, Response, Frequency, Percentage) %>%
    dplyr::arrange(desc(Frequency))
}

# --- Helper Function: Multi-Select Frequency Table ---
calc_multi_freq <- function(dataframe, prefix, question_id = "", question_name = "") {
  # Find columns starting with prefix
  cols <- colnames(dataframe)[startsWith(colnames(dataframe), prefix)]
  if (length(cols) == 0) return(NULL)
  
  results <- lapply(cols, function(c) {
    option_name <- substring(c, nchar(prefix) + 1)
    option_name <- stringr::str_trim(option_name)
    
    val <- as.numeric(dataframe[[c]])
    val[is.na(val)] <- 0
    checked_count <- sum(val)
    
    data.frame(
      Question_ID = question_id,
      Question = question_name,
      Response = option_name,
      Frequency = checked_count,
      Percentage = (checked_count / nrow(dataframe)) * 100,
      stringsAsFactors = FALSE
    )
  })
  
  do.call(rbind, results) %>% dplyr::arrange(desc(Frequency))
}


# ==================== 1. DEMOGRAPHICS (PART A: Q1-Q14) ====================
cat("  Processing Part A: Demographics...\n")

# Age numeric summary
age_col <- find_col(df, "^1\\. Age")
age_vals <- as.numeric(df[[age_col]])
age_summary <- data.frame(
  Question_ID = "Q1_Summary",
  Question = "1. Age (Numerical Stats)",
  Response = c("Mean Age", "Standard Deviation", "Median Age", "Min Age", "Max Age"),
  Frequency = c(NA_integer_, NA_integer_, NA_integer_, NA_integer_, NA_integer_),
  Percentage = c(mean(age_vals, na.rm=TRUE), sd(age_vals, na.rm=TRUE), median(age_vals, na.rm=TRUE), min(age_vals, na.rm=TRUE), max(age_vals, na.rm=TRUE))
)

# Age group categories
age_bins <- c(15, 24, 34, 44, 54, 100)
age_labels <- c("18-24", "25-34", "35-44", "45-54", "55+")
df$Age_Group <- cut(age_vals, breaks = age_bins, labels = age_labels)
q1_freq <- calc_freq(df, "Age_Group", "Q1_Groups")

# Categorical demographics Q2 to Q11
q2_to_q11 <- list(
  list(p = "^2\\. Gender", id = "Q2"),
  list(p = "^3\\. Ethnicity", id = "Q3"),
  list(p = "^4\\. Religion", id = "Q4"),
  list(p = "^5\\. Occupation", id = "Q5"),
  list(p = "^6\\. Monthly Income", id = "Q6"),
  list(p = "^7\\. Education Level", id = "Q7"),
  list(p = "^8\\. Residing Province", id = "Q8"),
  list(p = "^9\\. Marital Status", id = "Q9"),
  list(p = "^10\\. Do you have children", id = "Q10"),
  list(p = "^11\\. Do you have a family history", id = "Q11")
)

demographics_list <- list(age_summary, q1_freq)

for (item in q2_to_q11) {
  matched_col <- find_col(df, item$p)
  demographics_list[[length(demographics_list) + 1]] <- calc_freq(df, matched_col, item$id)
}

# Q12: Specifics of family history
q12_col <- find_col(df, "^12\\. If yes")
demographics_list[[length(demographics_list) + 1]] <- calc_freq(df, q12_col, "Q12")

# Q13 & Q14
q13_col <- find_col(df, "^13\\. When were you diagnosed")
df$Diagnosis_Year <- format(as.Date(df[[q13_col]], format="%Y-%m-%d"), "%Y")
# Fallback if already numerical or string year
if (all(is.na(df$Diagnosis_Year))) {
  df$Diagnosis_Year <- as.character(df[[q13_col]])
}
demographics_list[[length(demographics_list) + 1]] <- calc_freq(df, "Diagnosis_Year", "Q13")

q14_col <- find_col(df, "^14\\. Where were you diagnosed")
demographics_list[[length(demographics_list) + 1]] <- calc_freq(df, q14_col, "Q14")

# Save Demographics CSV
demographics_all <- do.call(rbind, demographics_list)
write.csv(demographics_all, file.path(csv_dir, "demographics.csv"), row.names = FALSE)


# ==================== 2. KNOWLEDGE QUESTIONS (PART B: Q15-Q29) ====================
cat("  Processing Part B: Knowledge Questions...\n")

knowledge_list <- list()

# Single select knowledge questions
single_knowledge <- list(
  list(p = "^15\\. Is thalassemia", id = "Q15"),
  list(p = "^17\\. What is the most severe", id = "Q17"),
  list(p = "^18\\. What form of thalassemia do you have", id = "Q18"),
  list(p = "^19\\. Does thalassemia major require", id = "Q19"),
  list(p = "^20\\. Can thalassemia major be cured", id = "Q20"),
  list(p = "^21\\. Can the spread", id = "Q21"),
  list(p = "^22\\. How is thalassemia transmitted", id = "Q22"),
  list(p = "^23\\. Is a thalassemia carrier", id = "Q23"),
  list(p = "^24\\. A child born from two", id = "Q24"),
  list(p = "^25\\. After diagnosis, was counseling", id = "Q25"),
  list(p = "^26\\. How many thalassemia births", id = "Q26"),
  list(p = "^29\\. How did you learn", id = "Q29")
)

for (item in single_knowledge) {
  matched_col <- find_col(df, item$p)
  knowledge_list[[length(knowledge_list) + 1]] <- calc_freq(df, matched_col, item$id)
}

# Multi-select knowledge questions Q16, Q27, Q28
q16_multi <- calc_multi_freq(df, "16. What are the clinical forms of thalassemia? (Tick all that apply)/", "Q16", "What are the clinical forms of thalassemia?")
if (!is.null(q16_multi)) knowledge_list[[length(knowledge_list) + 1]] <- q16_multi

q27_multi <- calc_multi_freq(df, "27. Problems faced by thalassemia major patients (Tick all that apply):/", "Q27", "Problems faced by thalassemia major patients")
if (!is.null(q27_multi)) knowledge_list[[length(knowledge_list) + 1]] <- q27_multi

q28_multi <- calc_multi_freq(df, "28. What should a thalassemia carrier do after diagnosis? (Tick all that apply) /", "Q28", "What should a thalassemia carrier do after diagnosis?")
if (!is.null(q28_multi)) knowledge_list[[length(knowledge_list) + 1]] <- q28_multi

# Save Knowledge CSV
knowledge_all <- do.call(rbind, knowledge_list)
write.csv(knowledge_all, file.path(csv_dir, "knowledge.csv"), row.names = FALSE)


# ==================== 3. MARRIAGE & PARTNER SCREENING (PART C: Q30-Q34) ====================
cat("  Processing Part C: Marriage & Partner attitudes...\n")

q30_col <- find_col(df, "^30\\. Are you willing")
q31_col <- find_col(df, "^31\\. Do you accept")
q32_col <- find_col(df, "^32\\. How important")
q33_col <- find_col(df, "^33\\. What was your practice")
q34_col <- find_col(df, "^34\\. If you did not disclose")

# Robustly find write-in cols relative to Q33 and Q34
q33_idx <- which(colnames(df) == q33_col)
q33_other_col <- colnames(df)[q33_idx + 1]

q34_idx <- which(colnames(df) == q34_col)
q34_other_col <- colnames(df)[q34_idx + 1]

marriage_list <- list(
  calc_freq(df, q30_col, "Q30"),
  calc_freq(df, q31_col, "Q31"),
  calc_freq(df, q32_col, "Q32"),
  calc_freq(df, q33_col, "Q33"),
  calc_freq(df, q33_other_col, "Q33_Other"),
  calc_freq(df, q34_col, "Q34"),
  calc_freq(df, q34_other_col, "Q34_Other")
)

marriage_all <- do.call(rbind, marriage_list)
write.csv(marriage_all, file.path(csv_dir, "marriage_partner.csv"), row.names = FALSE)


# ==================== 4. FAMILY SCREENING (PART D: Q35-Q40) ====================
cat("  Processing Part D: Family Screening...\n")

q35_col <- find_col(df, "^35\\. Do you think")
q36_col <- find_col(df, "^36\\. Do your family members")
q37_1_col <- find_col(df, "^First-degree relatives")
q37_2_col <- find_col(df, "^Second-degree relatives")
q37_3_col <- find_col(df, "^Third-degree relatives")

# Q38 barriers and write-in
q38_prefix <- "38. If not screened, what were the reasons? (Tick all that apply)/"
q38_cols <- colnames(df)[startsWith(colnames(df), q38_prefix)]
# Write-in sits right after the last Q38 barrier column
q38_last_idx <- which(colnames(df) == q38_cols[length(q38_cols)])
q38_other_col <- colnames(df)[q38_last_idx + 1]

q39_col <- find_col(df, "^39\\. How easy")
q40_col <- find_col(df, "^40\\. How important")

family_list <- list(
  calc_freq(df, q35_col, "Q35"),
  calc_freq(df, q36_col, "Q36"),
  calc_freq(df, q37_1_col, "Q37_FirstDegree"),
  calc_freq(df, q37_2_col, "Q37_SecondDegree"),
  calc_freq(df, q37_3_col, "Q37_ThirdDegree"),
  calc_multi_freq(df, q38_prefix, "Q38_Barriers", "If not screened, what were the reasons?"),
  calc_freq(df, q38_other_col, "Q38_Other"),
  calc_freq(df, q39_col, "Q39"),
  calc_freq(df, q40_col, "Q40")
)

family_all <- do.call(rbind, family_list)
write.csv(family_all, file.path(csv_dir, "family_screening.csv"), row.names = FALSE)

cat("Stage 3 completed. All CSV files saved under '", csv_dir, "'.\n\n", sep = "")
