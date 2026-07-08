# ==============================================================================
# Pipeline Stage 4: Visualizations Module
# ==============================================================================

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re

def find_col(df, pattern):
    matched = [c for c in df.columns if re.search(pattern, c, re.IGNORECASE)]
    if matched:
        return matched[0]
    else:
        raise KeyError(f"CRITICAL ERROR: Could not locate column matching pattern: {pattern}")

def generate_plots(df, plot_dir):
    print("Generating visual plots...")
    
    # Set modern plotting theme
    sns.set_theme(style="whitegrid")
    
    # --- 1. Age Distribution Plot ---
    print("  Plotting Age Distribution...")
    age_col = find_col(df, r"^1\. Age")
    age_vals = pd.to_numeric(df[age_col], errors='coerce').dropna()
    mean_age = age_vals.mean()
    
    plt.figure(figsize=(7, 5))
    ax = sns.histplot(age_vals, bins=15, color="#4A90E2", edgecolor="white", alpha=0.8)
    plt.axvline(mean_age, color="#D0021B", linestyle="--", linewidth=2)
    plt.text(mean_age + 2, ax.get_ylim()[1] * 0.8, f"Mean: {mean_age:.1f}", color="#D0021B", weight="bold")
    
    plt.title("Participant Age Distribution", fontsize=14, weight="bold", pad=15, color="#2C3E50")
    plt.xlabel("Age (Years)", fontsize=11, weight="bold")
    plt.ylabel("Count", fontsize=11, weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "age_distribution.png"), dpi=300)
    plt.close()
    
    
    # --- 2. Gender Distribution Bar Plot ---
    print("  Plotting Gender Frequencies...")
    gender_col = find_col(df, r"^2\. Gender")
    gender_series = df[gender_col].fillna("Missing/No Response")
    gender_counts = gender_series.value_counts()
    
    plt.figure(figsize=(6, 5))
    colors = {"Female": "#E15759", "Male": "#4E79A7", "Missing/No Response": "#76B7B2"}
    palette = [colors.get(x, "#7F8C8D") for x in gender_counts.index]
    
    ax = sns.barplot(x=gender_counts.index, y=gender_counts.values, palette=palette, hue=gender_counts.index, legend=False)
    
    # Add count and percentage labels above the bars
    total = len(df)
    for p in ax.patches:
        val = int(p.get_height())
        pct = (val / total) * 100
        ax.annotate(f"{val}\n({pct:.1f}%)", (p.get_x() + p.get_width() / 2., val),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', weight='bold', size=10)
                    
    plt.ylim(0, max(gender_counts.values) * 1.15)
    plt.title("Cohort Gender Distribution", fontsize=14, weight="bold", pad=15, color="#2C3E50")
    plt.xlabel("Gender Category", fontsize=11, weight="bold")
    plt.ylabel("Number of Participants", fontsize=11, weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "gender_distribution.png"), dpi=300)
    plt.close()
    
    
    # --- 3. Knowledge Score Distribution Plot ---
    print("  Plotting Knowledge Score Density...")
    score_vals = df['Expanded_Knowledge_Score'].dropna()
    mean_exp_score = score_vals.mean()
    
    plt.figure(figsize=(7, 5))
    ax = sns.histplot(score_vals, binwidth=1, color="#76B7B2", edgecolor="white", alpha=0.8)
    plt.axvline(mean_exp_score, color="#E15759", linestyle="--", linewidth=2)
    plt.text(mean_exp_score + 1.2, ax.get_ylim()[1] * 0.8, f"Mean: {mean_exp_score:.2f}", color="#E15759", weight="bold")
    
    plt.title("Expanded Knowledge Score Distribution", fontsize=14, weight="bold", pad=15, color="#2C3E50")
    plt.xlabel("Raw Expanded Knowledge Score (Max: 20)", fontsize=11, weight="bold")
    plt.ylabel("Number of Participants", fontsize=11, weight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "knowledge_score_distribution.png"), dpi=300)
    plt.close()
    
    
    # --- 4. Relative/Cascade Screening Rates Plot ---
    print("  Plotting Genetic Relative Screening Rates...")
    r1_col = find_col(df, r"^First-degree relatives")
    r2_col = find_col(df, r"^Second-degree relatives")
    r3_col = find_col(df, r"^Third-degree relatives")
    
    # Reshape from wide to long format
    rel_df = df[[r1_col, r2_col, r3_col]].copy()
    rel_df.columns = ["1st Degree\n(Parents/Siblings/Kids)", "2nd Degree\n(Aunts/Uncles/Grandparents)", "3rd Degree\n(Cousins/etc.)"]
    
    long_df = rel_df.melt(var_name="Relationship", value_name="Screened_Extent")
    long_df["Screened_Extent"] = long_df["Screened_Extent"].fillna("Missing/No Response")
    
    # Aggregate counts
    agg_df = long_df.groupby(["Relationship", "Screened_Extent"]).size().reset_name="Count"
    agg_df = long_df.groupby(["Relationship", "Screened_Extent"]).size().reset_index(name="Count")
    
    # Custom ordering of Extent Screened
    extent_order = ["All", "Some", "Don't know", "Missing/No Response"]
    agg_df["Screened_Extent"] = pd.Categorical(agg_df["Screened_Extent"], categories=extent_order, ordered=True)
    agg_df = agg_df.sort_values(by="Screened_Extent")
    
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(data=agg_df, x="Relationship", y="Count", hue="Screened_Extent", palette="Set2")
    
    plt.title("Cascade Screening Extent by Relationship Degree", fontsize=14, weight="bold", pad=15, color="#2C3E50")
    plt.xlabel("Degree of Genetic Relationship", fontsize=11, weight="bold")
    plt.ylabel("Number of Responses", fontsize=11, weight="bold")
    plt.legend(title="Screening Penetration", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, "relative_screening_rates.png"), dpi=300)
    plt.close()
