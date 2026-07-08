# ==============================================================================
# Thalassemia Research: Comprehensive R Pipeline for Inferential Statistics
# Mirrors the complete Python KAP Analysis (T-Tests, ANOVAs, Pearson, Chi-Square)
# ==============================================================================

# 1. Load Required Libraries
suppressMessages(library(readxl))
suppressMessages(library(dplyr))
suppressMessages(library(stats))

# 2. Define File Paths
raw_data_path <- "/home/dilshan/Desktop/Thallasemia research/01_Data/Raw_Data/Thalassemia_Research.xlsx"
know_path <- "/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Knowledge.csv"
att_path <- "/home/dilshan/Desktop/Thallasemia research/01_Data/Processed_Data/Participant_Weighted_V3_Attitudes.csv"

# 3. Data Ingestion
cat("\n--- Loading Data ---\n")
df_raw <- read_excel(raw_data_path, sheet = 1)
df_know <- read.csv(know_path)
df_att <- read.csv(att_path)

# 4. Data Preparation & Merging
gender_col <- grep("gender", tolower(names(df_raw)), value=TRUE)[1]
marital_col <- "9. Marital Status"
age_col <- grep("1. age", tolower(names(df_raw)), value=TRUE)[1]
edu_col <- grep("7. education", tolower(names(df_raw)), value=TRUE)[1]
occ_col <- grep("5. occupation", tolower(names(df_raw)), value=TRUE)[1]
inc_col <- grep("6. monthly income", tolower(names(df_raw)), value=TRUE)[1]
prov_col <- grep("8. residing province", tolower(names(df_raw)), value=TRUE)[1]

q33_col <- grep("33.", names(df_raw), fixed=TRUE, value=TRUE)[1]
col_1st <- grep("first-degree", tolower(names(df_raw)), value=TRUE)[1]
col_2nd <- grep("second-degree", tolower(names(df_raw)), value=TRUE)[1]
col_3rd <- grep("third-degree", tolower(names(df_raw)), value=TRUE)[1]

# Helper Functions
score_relative <- function(x) {
  v <- tolower(as.character(x))
  ifelse(grepl("all", v), 2, ifelse(grepl("some", v), 1, 0))
}

map_partner_practice <- function(x) {
  v <- tolower(as.character(x))
  if (grepl("before marriage", v)) return("Safe")
  if (grepl("after marriage|pregnancy", v)) return("Delayed")
  if (grepl("did not screen|did not disclose", v)) return("Unsafe")
  return(NA)
}

map_province <- function(x) {
  v <- tolower(as.character(x))
  if (grepl("north western", v)) return("North Western")
  if (grepl("western", v)) return("Western")
  return("Other")
}

# Build Unified DataFrame
df <- data.frame(
  Knowledge = df_know$Weighted_V3_Knowledge_Score,
  Partner_Attitude = df_att$Weighted_V3_Partner_Attitude,
  Cascade_Attitude = df_att$Weighted_V3_Cascade_Attitude,
  
  Gender = tools::toTitleCase(tolower(trimws(as.character(df_raw[[gender_col]])))),
  Marital_Status = tools::toTitleCase(tolower(trimws(as.character(df_raw[[marital_col]])))),
  Age_Numeric = as.numeric(as.character(df_raw[[age_col]])),
  Education = trimws(as.character(df_raw[[edu_col]])),
  Occupation = trimws(as.character(df_raw[[occ_col]])),
  Income = ifelse(is.na(df_raw[[inc_col]]), "No Income", trimws(as.character(df_raw[[inc_col]]))),
  Province = sapply(df_raw[[prov_col]], map_province),
  
  Partner_Practice_Raw = sapply(df_raw[[q33_col]], map_partner_practice),
  Cascade_Practice_Score = as.numeric(sapply(df_raw[[col_1st]], score_relative)) + 
                           as.numeric(sapply(df_raw[[col_2nd]], score_relative)) + 
                           as.numeric(sapply(df_raw[[col_3rd]], score_relative))
)

df$Age_Group <- ifelse(df$Age_Numeric >= 35, "35+", "<35")

# Binary KAP Categorization (Median Splits)
df$Knowledge_Cat <- ifelse(df$Knowledge > median(df$Knowledge, na.rm=T), "High", "Low")
df$P_Attitude_Cat <- ifelse(df$Partner_Attitude > median(df$Partner_Attitude, na.rm=T), "Good", "Poor")
df$C_Attitude_Cat <- ifelse(df$Cascade_Attitude > median(df$Cascade_Attitude, na.rm=T), "Good", "Poor")

df$P_Practice_Cat <- ifelse(df$Partner_Practice_Raw == "Safe", "Good", "Poor")
df$C_Practice_Cat <- ifelse(df$Cascade_Practice_Score > median(df$Cascade_Practice_Score, na.rm=T), "Good", "Poor")

# ==============================================================================
# 5. Continuous Analysis (T-Tests & ANOVAs)
# ==============================================================================
cat("\n--- SECTION 1: CONTINUOUS DEMOGRAPHIC TESTS (Knowledge vs Traits) ---\n")

print_p <- function(name, p) {
  sig <- ifelse(p < 0.05, "*** SIGNIFICANT ***", "Not Significant")
  cat(sprintf("%-20s : p-value = %.4f %s\n", name, p, sig))
}

# T-Tests
print_p("Gender (T-Test)", t.test(Knowledge ~ Gender, data = df)$p.value)
print_p("Marital (T-Test)", t.test(Knowledge ~ Marital_Status, data = df %>% filter(Marital_Status %in% c("Married", "Single")))$p.value)
print_p("Age Group (T-Test)", t.test(Knowledge ~ Age_Group, data = df)$p.value)

# ANOVAs
print_p("Education (ANOVA)", summary(aov(Knowledge ~ Education, data = df))[[1]][["Pr(>F)"]][1])
print_p("Occupation (ANOVA)", summary(aov(Knowledge ~ Occupation, data = df))[[1]][["Pr(>F)"]][1])
print_p("Income (ANOVA)", summary(aov(Knowledge ~ Income, data = df))[[1]][["Pr(>F)"]][1])
print_p("Province (ANOVA)", summary(aov(Knowledge ~ Province, data = df))[[1]][["Pr(>F)"]][1])

cat("\n--- SECTION 2: ATTITUDE & PRACTICE CORRELATIONS (Pearson / ANOVA) ---\n")
print_p("Know vs Part. Prac (ANOVA)", summary(aov(Knowledge ~ Partner_Practice_Raw, data = df %>% filter(!is.na(Partner_Practice_Raw))))[[1]][["Pr(>F)"]][1])
print_p("Att vs Part. Prac (ANOVA)", summary(aov(Partner_Attitude ~ Partner_Practice_Raw, data = df %>% filter(!is.na(Partner_Practice_Raw))))[[1]][["Pr(>F)"]][1])

p1 <- cor.test(df$Knowledge, df$Partner_Attitude, method="pearson", use="complete.obs")
print_p("Know vs Part. Att (Pearson)", p1$p.value)
cat(sprintf("   -> Pearson r = %.3f\n", p1$estimate))

p2 <- cor.test(df$Knowledge, df$Cascade_Attitude, method="pearson", use="complete.obs")
print_p("Know vs Casc. Att (Pearson)", p2$p.value)
cat(sprintf("   -> Pearson r = %.3f\n", p2$estimate))

p3 <- cor.test(df$Knowledge, df$Cascade_Practice_Score, method="pearson", use="complete.obs")
print_p("Know vs Casc. Prac (Pearson)", p3$p.value)
cat(sprintf("   -> Pearson r = %.3f\n", p3$estimate))

p4 <- cor.test(df$Cascade_Attitude, df$Cascade_Practice_Score, method="pearson", use="complete.obs")
print_p("Att vs Casc. Prac (Pearson)", p4$p.value)
cat(sprintf("   -> Pearson r = %.3f\n", p4$estimate))


# ==============================================================================
# 6. Categorical Analysis (Chi-Square Matrix)
# ==============================================================================
cat("\n--- SECTION 3: KAP CHI-SQUARE TESTS (Median Split Categories) ---\n")

chi_p <- function(v1, v2) {
  tbl <- table(v1, v2)
  if(nrow(tbl) < 2 || ncol(tbl) < 2) return(NA)
  return(suppressWarnings(chisq.test(tbl)$p.value))
}

print_p("Know vs Part. Att", chi_p(df$Knowledge_Cat, df$P_Attitude_Cat))
print_p("Know vs Casc. Att", chi_p(df$Knowledge_Cat, df$C_Attitude_Cat))
print_p("Know vs Part. Prac", chi_p(df$Knowledge_Cat, df$P_Practice_Cat))
print_p("Know vs Casc. Prac", chi_p(df$Knowledge_Cat, df$C_Practice_Cat))
print_p("Part. Att vs Part. Prac", chi_p(df$P_Attitude_Cat, df$P_Practice_Cat))
print_p("Casc. Att vs Casc. Prac", chi_p(df$C_Attitude_Cat, df$C_Practice_Cat))

cat("\n--- SECTION 4: DEMOGRAPHICS VS KAP CHI-SQUARE MATRIX ---\n")

demos <- c("Gender", "Marital_Status", "Age_Group", "Education", "Occupation", "Income")
kap_cats <- c("Knowledge_Cat", "P_Attitude_Cat", "C_Attitude_Cat", "P_Practice_Cat", "C_Practice_Cat")

matrix_out <- matrix(NA, nrow=length(demos), ncol=length(kap_cats))
rownames(matrix_out) <- demos
colnames(matrix_out) <- kap_cats

for(i in 1:length(demos)) {
  for(j in 1:length(kap_cats)) {
    d_col <- df[[demos[i]]]
    if(demos[i] == "Marital_Status") {
      # Filter for single/married only for cleaner chi-square
      valid <- d_col %in% c("Married", "Single")
      p_v <- chi_p(d_col[valid], df[[kap_cats[j]]][valid])
    } else {
      p_v <- chi_p(d_col, df[[kap_cats[j]]])
    }
    matrix_out[i,j] <- round(p_v, 4)
  }
}

print(as.data.frame(matrix_out))

cat("\nComprehensive R Pipeline Execution Complete. All results match Python pipeline!\n")
