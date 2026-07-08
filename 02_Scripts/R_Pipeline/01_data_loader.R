# ==============================================================================
# Pipeline Stage 1: Data Loader & Cleaning
# ==============================================================================

# Verify we have the xlsx_path variable from the orchestrator
if (!exists("xlsx_path")) {
  xlsx_path <- "/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx"
}

cat("Reading sheet 1 from Thalassemia_Research.xlsx...\n")

# Load the dataset
# Sheet 1 has the raw participant response data
df_raw <- readxl::read_excel(xlsx_path, sheet = 1)

cat("Original dimensions:", nrow(df_raw), "rows and", ncol(df_raw), "columns.\n")

# Clean column headers (trim leading/trailing spaces, standardizing headers)
clean_headers <- stringr::str_trim(colnames(df_raw))

# Some columns might have newlines or other weird spacing in them
# Clean up whitespace inside headers to prevent matching issues
clean_headers <- stringr::str_replace_all(clean_headers, "\\s+", " ")
colnames(df_raw) <- clean_headers

cat("Standardized all column headers.\n")

# Clean cell character strings
# Trimming leading/trailing spaces of all character columns to ensure robust matches
df_cleaned <- df_raw %>%
  dplyr::mutate(across(where(is.character), ~ {
    val <- stringr::str_trim(.x)
    val <- stringr::str_replace_all(val, "\\s+", " ") # replace multiple spaces with single space
    # Convert empty strings to NA
    ifelse(val == "", NA_character_, val)
  }))

cat("Cleaned text cell values (trimmed trailing spaces and normalized whitespace).\n")

# Keep track of cleaned dataset globally
df <- df_cleaned
cat("Stage 1 completed. Dataframe 'df' is loaded in the global environment.\n\n")
