# ==============================================================================
# Thalassemia Research: R Pipeline for Inferential Statistics
# Topic: Independent T-Tests for Knowledge Scores vs Demographics
# ==============================================================================

# 1. Load Required Libraries
# Ensure you have installed these via install.packages(c("readxl", "dplyr", "ggplot2"))
library(readxl)
library(dplyr)
library(ggplot2)

# 2. Define File Paths
# Update these paths if running on a different machine
raw_data_path <- "../../01_Data/Raw_Data/Thalassemia_Research.xlsx"
weighted_v3_path <- "../../01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"
standard_v3_path <- "../../01_Data/Processed_Data/Participant_V3_Knowledge.csv"

# 3. Data Ingestion
cat("\n--- Loading Data ---\n")
df_raw <- read_excel(raw_data_path, sheet = 1)
df_wv3 <- read.csv(weighted_v3_path)
df_v3 <- read.csv(standard_v3_path)

# 4. Data Preparation & Merging
# Extracting exact demographic columns
gender_col <- grep("gender", tolower(names(df_raw)), value=TRUE)[1]
marital_col <- grep("marital", tolower(names(df_raw)), value=TRUE)[1]

# Creating a clean merged dataframe
# Assuming row order hasn't changed across CSV exports (1-to-1 mapping)
df_clean <- data.frame(
  Gender = trimws(df_raw[[gender_col]]),
  Marital_Status = trimws(df_raw[[marital_col]]),
  V3_Score = df_v3$V3_Knowledge_Score,
  Weighted_V3_Score = df_wv3$Weighted_V3_Knowledge_Score
)

# Standardize capitalization
df_clean$Gender <- tools::toTitleCase(tolower(df_clean$Gender))
df_clean$Marital_Status <- tools::toTitleCase(tolower(df_clean$Marital_Status))

# Filter out NA rows
df_clean <- df_clean %>% filter(!is.na(Gender) & !is.na(Marital_Status))

# Filter specifically for the binary comparisons
df_clean_marital <- df_clean %>% filter(Marital_Status %in% c("Married", "Single"))

# ==============================================================================
# 5. Statistical Analysis: T-Tests (Welch's Two Sample t-test)
# ==============================================================================

cat("\n========================================================\n")
cat("TEST 1: Knowledge Score vs Gender (Male vs Female)\n")
cat("========================================================\n")

# T-Test for Weighted V3
ttest_gender_wv3 <- t.test(Weighted_V3_Score ~ Gender, data = df_clean)
print(ttest_gender_wv3)

# T-Test for Standard V3
ttest_gender_v3 <- t.test(V3_Score ~ Gender, data = df_clean)
print(ttest_gender_v3)


cat("\n========================================================\n")
cat("TEST 2: Knowledge Score vs Marital Status (Married vs Single)\n")
cat("========================================================\n")

# T-Test for Weighted V3
ttest_marital_wv3 <- t.test(Weighted_V3_Score ~ Marital_Status, data = df_clean_marital)
print(ttest_marital_wv3)

# T-Test for Standard V3
ttest_marital_v3 <- t.test(V3_Score ~ Marital_Status, data = df_clean_marital)
print(ttest_marital_v3)

# ==============================================================================
# 6. Optional: Generate Publication-Ready Plots using ggplot2
# ==============================================================================

cat("\n--- Generating ggplot2 Visualizations ---\n")

# Gender Plot
p_gender <- ggplot(df_clean, aes(x = Gender, y = Weighted_V3_Score, fill = Gender)) +
  geom_violin(trim = FALSE, alpha = 0.6) +
  geom_boxplot(width = 0.1, fill = "white", outlier.shape = NA) +
  theme_minimal() +
  labs(title = "Weighted V3 Knowledge Score by Gender",
       subtitle = paste("Welch Two Sample t-test p-value:", format(ttest_gender_wv3$p.value, digits=4)),
       y = "Weighted V3 Score",
       x = "Gender") +
  theme(legend.position = "none", plot.title = element_text(face="bold"))

# Marital Status Plot
p_marital <- ggplot(df_clean_marital, aes(x = Marital_Status, y = Weighted_V3_Score, fill = Marital_Status)) +
  geom_violin(trim = FALSE, alpha = 0.6) +
  geom_boxplot(width = 0.1, fill = "white", outlier.shape = NA) +
  scale_fill_manual(values = c("Married" = "coral", "Single" = "steelblue")) +
  theme_minimal() +
  labs(title = "Weighted V3 Knowledge Score by Marital Status",
       subtitle = paste("Welch Two Sample t-test p-value:", format(ttest_marital_wv3$p.value, digits=4)),
       y = "Weighted V3 Score",
       x = "Marital Status") +
  theme(legend.position = "none", plot.title = element_text(face="bold"))

# Save plots to current directory
ggsave("R_Plot_Knowledge_vs_Gender.png", plot = p_gender, width = 7, height = 5)
ggsave("R_Plot_Knowledge_vs_Marital.png", plot = p_marital, width = 7, height = 5)

cat("Visualizations saved as PNG files in the script directory.\n")
cat("Pipeline Execution Complete.\n")
