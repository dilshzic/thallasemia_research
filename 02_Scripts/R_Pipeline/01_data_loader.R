# ==============================================================================
# Pipeline Stage 1: Data Loader & Cleaning
# ==============================================================================
# This script takes a raw, messy spreadsheet and organizes it for R to analyze.
# Think of it like organizing scattered medical records into a neat electronic health record.

# 1. Setting Up the File Path
# If R doesn't already know where the file is (!exists), we point it to the file on the desktop.
if (!exists("xlsx_path")) {
  xlsx_path <- "/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx"
}

# 2. Loading the Data
# cat() prints messages to your screen so you can track progress.
cat("Reading sheet 1 from Thalassemia_Research.xlsx...\n")

# df_raw <- ... assigns the data from Sheet 1 to a new object called df_raw.
# read_excel() opens the Excel file, and nrow()/ncol() check the number of rows and columns.
df_raw <- readxl::read_excel(xlsx_path, sheet = 1)

cat("Original dimensions:", nrow(df_raw), "rows and", ncol(df_raw), "columns.\n")

# 3. Cleaning the Column Names (Headers)
# We fix accidental spaces in headers (like "Age " instead of "Age") so R doesn't get confused.
# str_trim() removes invisible spaces at the edges of column names.
clean_headers <- stringr::str_trim(colnames(df_raw))

# str_replace_all() squashes accidental double/triple spaces between words into a single space.
clean_headers <- stringr::str_replace_all(clean_headers, "\\s+", " ")
# Save the cleaned headers back to the dataframe.
colnames(df_raw) <- clean_headers

cat("Standardized all column headers.\n")

# 4. Cleaning the Data Inside the Cells
# %>% (The Pipe) means "and then". It takes df_raw and passes it to the next step.
df_cleaned <- df_raw %>%
  # mutate(across(where(is.character)...) looks at every text column to clean it.
  dplyr::mutate(across(where(is.character), ~ {
    # Like headers, we remove edge spaces and squash middle spaces.
    val <- stringr::str_trim(.x)
    val <- stringr::str_replace_all(val, "\\s+", " ") # replace multiple spaces with single space
    # Missing data should be NA (Not Available), not a blank space "".
    # This safely replaces completely empty cells with NA.
    ifelse(val == "", NA_character_, val)
  }))

cat("Cleaned text cell values (trimmed trailing spaces and normalized whitespace).\n")

# 5. Finalizing
# Save the perfectly cleaned data as a simple variable named df, ready for analysis!
df <- df_cleaned
cat("Stage 1 completed. Dataframe 'df' is loaded in the global environment.\n\n")
