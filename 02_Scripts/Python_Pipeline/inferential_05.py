# ==============================================================================
# Pipeline Stage 5: Inferential Statistical Analysis Module
# ==============================================================================

import pandas as pd
import numpy as np
import os
import re
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

def find_col(df, pattern):
    matched = [c for c in df.columns if re.search(pattern, c, re.IGNORECASE)]
    if matched:
        return matched[0]
    else:
        raise KeyError(f"CRITICAL ERROR: Could not locate column matching pattern: {pattern}")

def run_inferential_stats(df, csv_dir):
    print("Executing Stage 5: Inferential Statistical Analysis...")
    
    # --- 1. Chi-Square: Education vs. Knowledge Level ---
    print("\nRunning Chi-Square Test: Education Level vs. Knowledge Level...")
    edu_col = find_col(df, r"^7\. Education Level")
    median_exp_score = df['Expanded_Knowledge_Score'].median()
    df['Knowledge_Level'] = np.where(df['Expanded_Knowledge_Score'] > median_exp_score, 'High', 'Low')
    
    # Exclude Missing/No Response
    sub_edu = df[df[edu_col].notna() & (df[edu_col] != "Missing/No Response")]
    contingency_edu = pd.crosstab(sub_edu[edu_col], sub_edu['Knowledge_Level'])
    print(contingency_edu)
    
    chi2_edu, p_edu, dof_edu, expected_edu = stats.chi2_contingency(contingency_edu)
    print(f"Chi2: {chi2_edu:.4f}, p-val: {p_edu:.4e}, df: {dof_edu}")
    
    chi_edu_df = pd.DataFrame([{
        "Test": "Chi-Square: Education vs Knowledge Level",
        "Statistic": chi2_edu,
        "df": dof_edu,
        "p_value": p_edu,
        "Significant": "Yes" if p_edu < 0.05 else "No"
    }])
    
    
    # --- 2. Chi-Square: Family History vs. Family Disclosure ---
    print("\nRunning Chi-Square Test: Family History vs. Family Disclosure...")
    hist_col = find_col(df, r"^11\. Do you have a family history")
    disc_col = find_col(df, r"^36\. Do your family members")
    
    sub_hist = df[df[hist_col].isin(["Yes", "No"]) & df[disc_col].isin(["Yes", "No"])]
    contingency_hist = pd.crosstab(sub_hist[hist_col], sub_hist[disc_col])
    print(contingency_hist)
    
    chi2_hist, p_hist, dof_hist, expected_hist = stats.chi2_contingency(contingency_hist, correction=True)
    print(f"Chi2: {chi2_hist:.4f}, p-val: {p_hist:.4e}, df: {dof_hist}")
    
    chi_hist_df = pd.DataFrame([{
        "Test": "Chi-Square: Family History vs Family Disclosure",
        "Statistic": chi2_hist,
        "df": dof_hist,
        "p_value": p_hist,
        "Significant": "Yes" if p_hist < 0.05 else "No"
    }])
    
    
    # --- 3. Chi-Square: Marital Status vs. Partner Screening ---
    print("\nRunning Chi-Square Test: Marital Status vs. Partner Screening...")
    status_col = find_col(df, r"^9\. Marital Status")
    practice_col = find_col(df, r"^33\. What was your practice")
    
    screened_categories = ["Partner was screened before marriage", "Partner was screened after marriage", "Partner was screened during pregnancy"]
    unscreened_categories = ["Did not screen partner", "Did not disclose thalassemia carrier state to partner"]
    
    df['Partner_Screened_Recoded'] = pd.Series([np.nan] * len(df), dtype=object)
    df.loc[df[practice_col].isin(screened_categories), 'Partner_Screened_Recoded'] = 'Screened'
    df.loc[df[practice_col].isin(unscreened_categories), 'Partner_Screened_Recoded'] = 'Unscreened'
    
    sub_marital = df[df[status_col].isin(["Single", "Married"]) & df['Partner_Screened_Recoded'].notna()]
    contingency_marital = pd.crosstab(sub_marital[status_col], sub_marital['Partner_Screened_Recoded'])
    print(contingency_marital)
    
    chi2_mar, p_mar, dof_mar, expected_mar = stats.chi2_contingency(contingency_marital, correction=True)
    print(f"Chi2: {chi2_mar:.4f}, p-val: {p_mar:.4e}, df: {dof_mar}")
    
    chi_mar_df = pd.DataFrame([{
        "Test": "Chi-Square: Marital Status vs Partner Screening Practice",
        "Statistic": chi2_mar,
        "df": dof_mar,
        "p_value": p_mar,
        "Significant": "Yes" if p_mar < 0.05 else "No"
    }])
    
    # Save Chi-Squares CSV
    chisq_all = pd.concat([chi_edu_df, chi_hist_df, chi_mar_df], ignore_index=True)
    chisq_all.to_csv(os.path.join(csv_dir, "inferential_chisq.csv"), index=False)
    
    
    # --- 4. T-Test: Gender vs. Expanded Knowledge Score ---
    print("\nRunning Welch's Independent t-test: Gender vs. Knowledge Score...")
    gender_col = find_col(df, r"^2\. Gender")
    sub_gen = df[df[gender_col].isin(["Female", "Male"])]
    
    females = sub_gen[sub_gen[gender_col] == "Female"]['Expanded_Knowledge_Score']
    males = sub_gen[sub_gen[gender_col] == "Male"]['Expanded_Knowledge_Score']
    
    t_stat, p_t = stats.ttest_ind(females, males, equal_var=False)
    print(f"T-statistic: {t_stat:.4f}, p-val: {p_t:.4e}")
    
    t_df = pd.DataFrame([{
        "Test": "Welch t-test: Gender vs Expanded Knowledge Score",
        "t_statistic": t_stat,
        "df": float(stats.ttest_ind(females, males, equal_var=False).df), # stats.ttest_ind returns df in newer scipy versions
        "p_value": p_t,
        "Mean_Female": females.mean(),
        "Mean_Male": males.mean(),
        "Significant": "Yes" if p_t < 0.05 else "No"
    }])
    # Handle older scipy where df is not returned directly by modifying df if it fails
    if t_df["df"].isna().any():
        # Approximation of Welch df
        v1 = females.var() / len(females)
        v2 = males.var() / len(males)
        welch_df = ((v1 + v2)**2) / ((v1**2)/(len(females)-1) + (v2**2)/(len(males)-1))
        t_df["df"] = welch_df
        
    t_df.to_csv(os.path.join(csv_dir, "inferential_ttest.csv"), index=False)
    
    
    # --- 5. ANOVA: Education Level vs. Expanded Knowledge Score ---
    print("\nRunning One-Way ANOVA: Education Level vs. Knowledge Score...")
    anova_groups = [group['Expanded_Knowledge_Score'].values for name, group in sub_edu.groupby(edu_col)]
    f_stat, p_f = stats.f_oneway(*anova_groups)
    print(f"F-statistic: {f_stat:.4f}, p-val: {p_f:.4e}")
    
    # Save ANOVA summary table (Compute standard ANOVA details manually for CSV output)
    n_groups = len(anova_groups)
    n_total = len(sub_edu)
    df_between = n_groups - 1
    df_within = n_total - n_groups
    
    overall_mean = sub_edu['Expanded_Knowledge_Score'].mean()
    ss_between = sum(len(g) * (g.mean() - overall_mean)**2 for g in anova_groups)
    ss_total = sum((sub_edu['Expanded_Knowledge_Score'] - overall_mean)**2)
    ss_within = ss_total - ss_between
    
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within
    
    anova_df = pd.DataFrame([
        {"Source": edu_col, "Df": df_between, "Sum_Sq": ss_between, "Mean_Sq": ms_between, "F_value": f_stat, "Pr_F": p_f},
        {"Source": "Residuals", "Df": df_within, "Sum_Sq": ss_within, "Mean_Sq": ms_within, "F_value": np.nan, "Pr_F": np.nan}
    ])
    anova_df.to_csv(os.path.join(csv_dir, "inferential_anova.csv"), index=False)
    
    
    # --- 6. Linear Regression: Predict Expanded Knowledge Score ---
    print("\nFitting Multiple Linear Regression Model...")
    income_col = find_col(df, r"^6\. Monthly Income")
    age_col = find_col(df, r"^1\. Age")
    
    reg_df = df.copy()
    reg_df['Age'] = pd.to_numeric(reg_df[age_col], errors='coerce')
    reg_df['Gender'] = reg_df[gender_col]
    reg_df['Education'] = reg_df[edu_col]
    reg_df['Income'] = reg_df[income_col]
    
    reg_df = reg_df.dropna(subset=['Age', 'Gender', 'Education', 'Income'])
    reg_df = reg_df[reg_df['Education'] != "Missing/No Response"]
    reg_df = reg_df[reg_df['Income'] != "Missing/No Response"]
    reg_df = reg_df[reg_df['Gender'] != "Missing/No Response"]
    
    print(f"Regression cohort size: {len(reg_df)}")
    
    # Baseline constraints matching R's lm
    model = smf.ols("Expanded_Knowledge_Score ~ Age + C(Gender, Treatment(reference='Female')) + C(Education, Treatment(reference='Up to O/L')) + C(Income, Treatment(reference='< 25,000'))", data=reg_df)
    results = model.fit()
    print(results.summary())
    
    # Save regression coefficients table
    coef_df = pd.DataFrame({
        "Term": results.params.index,
        "Estimate": results.params.values,
        "Std_Error": results.bse.values,
        "t_value": results.tvalues.values,
        "p_value": results.pvalues.values,
        "Significant": ["Yes" if p < 0.05 else "No" for p in results.pvalues.values]
    })
    coef_df.to_csv(os.path.join(csv_dir, "inferential_regression.csv"), index=False)
