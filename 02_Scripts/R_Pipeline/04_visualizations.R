# ==============================================================================
# Pipeline Stage 4: Visualizations
# ==============================================================================

if (!exists("df")) {
  stop("CRITICAL ERROR: Dataframe 'df' is not available in environment. Run Stage 1, 2, and 3 first.")
}

cat("Generating visual plots...\n")

# Setup themes and output directories
if (!exists("plot_dir")) {
  plot_dir <- "./outputs/plots"
}

# --- 1. Age Distribution Plot ---
cat("  Plotting Age Distribution...\n")
age_col <- find_col(df, "^1\\. Age")
mean_age <- mean(as.numeric(df[[age_col]]), na.rm = TRUE)

p1 <- ggplot2::ggplot(df, ggplot2::aes(x = as.numeric(.data[[age_col]]))) +
  ggplot2::geom_histogram(bins = 15, fill = "#4A90E2", color = "white", alpha = 0.8) +
  ggplot2::geom_vline(xintercept = mean_age, color = "#D0021B", linetype = "dashed", size = 1.1) +
  ggplot2::annotate("text", x = mean_age + 4, y = 30, label = paste("Mean:", round(mean_age, 1)), color = "#D0021B", fontface = "bold") +
  ggplot2::theme_minimal() +
  ggplot2::labs(
    title = "Participant Age Distribution",
    subtitle = paste("Sample cohort N =", nrow(df)),
    x = "Age (Years)",
    y = "Count"
  ) +
  ggplot2::theme(
    plot.title = ggplot2::element_text(face = "bold", size = 14, color = "#2C3E50"),
    plot.subtitle = ggplot2::element_text(size = 10, color = "#7F8C8D"),
    axis.title = ggplot2::element_text(face = "bold")
  )

ggplot2::ggsave(file.path(plot_dir, "age_distribution.png"), plot = p1, width = 7, height = 5, dpi = 300)


# --- 2. Gender Distribution Bar Plot ---
cat("  Plotting Gender Frequencies...\n")
gender_col <- find_col(df, "^2\\. Gender")
gender_df <- df %>% 
  dplyr::mutate(Gender = ifelse(is.na(.data[[gender_col]]), "Missing/No Response", as.character(.data[[gender_col]]))) %>%
  dplyr::group_by(Gender) %>%
  dplyr::summarise(Count = n(), .groups = 'drop')

p2 <- ggplot2::ggplot(gender_df, ggplot2::aes(x = Gender, y = Count, fill = Gender)) +
  ggplot2::geom_bar(stat = "identity", width = 0.5, show.legend = FALSE) +
  ggplot2::scale_fill_manual(values = c("Female" = "#E15759", "Male" = "#4E79A7", "Missing/No Response" = "#76B7B2")) +
  ggplot2::geom_text(ggplot2::aes(label = paste0(Count, "\n(", round(Count/sum(Count)*100, 1), "%)")), vjust = -0.2, fontface = "bold", size = 3.5) +
  ggplot2::ylim(0, max(gender_df$Count) * 1.15) +
  ggplot2::theme_minimal() +
  ggplot2::labs(
    title = "Cohort Gender Distribution",
    x = "Gender Category",
    y = "Number of Participants"
  ) +
  ggplot2::theme(
    plot.title = ggplot2::element_text(face = "bold", size = 14, color = "#2C3E50"),
    axis.title = ggplot2::element_text(face = "bold")
  )

ggplot2::ggsave(file.path(plot_dir, "gender_distribution.png"), plot = p2, width = 6, height = 5, dpi = 300)


# --- 3. Knowledge Score Distribution Plot ---
cat("  Plotting Knowledge Score Density...\n")
mean_exp_score <- mean(df$Expanded_Knowledge_Score, na.rm = TRUE)

p3 <- ggplot2::ggplot(df, ggplot2::aes(x = Expanded_Knowledge_Score)) +
  ggplot2::geom_histogram(binwidth = 1, fill = "#76B7B2", color = "white", alpha = 0.8) +
  ggplot2::geom_vline(xintercept = mean_exp_score, color = "#E15759", linetype = "dashed", size = 1.1) +
  ggplot2::annotate("text", x = mean_exp_score + 1.8, y = 22, label = paste("Mean:", round(mean_exp_score, 2)), color = "#E15759", fontface = "bold") +
  ggplot2::theme_minimal() +
  ggplot2::labs(
    title = "Expanded Knowledge Score Distribution",
    subtitle = "Calculated across all 11 knowledge questions (Max possible: 20)",
    x = "Raw Expanded Knowledge Score",
    y = "Number of Participants"
  ) +
  ggplot2::theme(
    plot.title = ggplot2::element_text(face = "bold", size = 14, color = "#2C3E50"),
    plot.subtitle = ggplot2::element_text(size = 10, color = "#7F8C8D"),
    axis.title = ggplot2::element_text(face = "bold")
  )

ggplot2::ggsave(file.path(plot_dir, "knowledge_score_distribution.png"), plot = p3, width = 7, height = 5, dpi = 300)


# --- 4. Relative/Cascade Screening Rates Plot ---
cat("  Plotting Genetic Relative Screening Rates...\n")
r1_col <- find_col(df, "^First-degree relatives")
r2_col <- find_col(df, "^Second-degree relatives")
r3_col <- find_col(df, "^Third-degree relatives")

rel_data <- df %>%
  dplyr::select(First = all_of(r1_col), Second = all_of(r2_col), Third = all_of(r3_col)) %>%
  tidyr::pivot_longer(cols = dplyr::everything(), names_to = "Relationship", values_to = "Screened_Extent") %>%
  dplyr::mutate(
    Screened_Extent = ifelse(is.na(Screened_Extent), "Missing/No Response", Screened_Extent),
    Relationship = factor(Relationship, levels = c("First", "Second", "Third"), 
                          labels = c("1st Degree\n(Parents/Siblings/Kids)", "2nd Degree\n(Aunts/Uncles/Grandparents)", "3rd Degree\n(Cousins/etc.)"))
  ) %>%
  dplyr::group_by(Relationship, Screened_Extent) %>%
  dplyr::summarise(Count = n(), .groups = 'drop')

# Set factor levels for Extent to sort legend nicely
rel_data$Screened_Extent <- factor(rel_data$Screened_Extent, levels = c("All", "Some", "Don't know", "Missing/No Response"))

p4 <- ggplot2::ggplot(rel_data, ggplot2::aes(x = Relationship, y = Count, fill = Screened_Extent)) +
  ggplot2::geom_bar(stat = "identity", position = ggplot2::position_dodge(width = 0.85), width = 0.8) +
  ggplot2::scale_fill_brewer(palette = "Set2", name = "Screening Penetration") +
  ggplot2::theme_minimal() +
  ggplot2::labs(
    title = "Cascade Screening Extent by Relationship Degree",
    subtitle = "Comparison of family screening penetration",
    x = "Degree of Genetic Relationship",
    y = "Number of Responses"
  ) +
  ggplot2::theme(
    plot.title = ggplot2::element_text(face = "bold", size = 14, color = "#2C3E50"),
    plot.subtitle = ggplot2::element_text(size = 10, color = "#7F8C8D"),
    axis.title = ggplot2::element_text(face = "bold")
  )

ggplot2::ggsave(file.path(plot_dir, "relative_screening_rates.png"), plot = p4, width = 8, height = 5, dpi = 300)

cat("Stage 4 completed. All plots saved as high-res PNGs under '", plot_dir, "'.\n\n", sep = "")
