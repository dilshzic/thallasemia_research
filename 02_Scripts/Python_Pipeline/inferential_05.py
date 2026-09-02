# ==============================================================================
# Pipeline Stage 5: Inferential Statistical Analysis Module
# ==============================================================================

import pandas as pd
import numpy as np
import os
import re
import scipy.stats as stats

def find_col(df, pattern):
    matched = [c for c in df.columns if re.search(pattern, c, re.IGNORECASE)]
    if matched:
        return matched[0]
    else:
        raise KeyError(f"CRITICAL ERROR: Could not locate column matching pattern: {pattern}")

def run_inferential_stats(df, csv_dir):
    print("Executing Stage 5: Inferential Statistical Analysis...")
    
    gender_col = find_col(df, r"^2\. Gender")
    marital_col = find_col(df, r"^9\. Marital Status")
    age_col = find_col(df, r"^1\. Age")
    prov_col = find_col(df, r"Province")
    edu_col = find_col(df, r"^7\. Education Level")
    inc_col = find_col(df, r"^6\. Monthly Income")

    # --- Binarize Demographics ---
    df['B_Gender'] = df[gender_col].astype(str).str.strip()
    
    def map_marital(x):
        s = str(x).strip()
        if s in ["Single", "Married"]: return s
        return np.nan
    df['B_Marital'] = df[marital_col].apply(map_marital)
    
    df['B_Age'] = np.where(pd.to_numeric(df[age_col], errors='coerce') < 35, "<35", ">=35")
    
    def map_prov(x):
        s = str(x)
        if 'Western' in s and 'North' not in s: return 'Western'
        if 'North Western' in s: return 'North Western'
        return np.nan
    df['B_Province'] = df[prov_col].apply(map_prov)
    
    def map_edu(x):
        s = str(x)
        if 'O/L' in s or 'A/L' in s: return 'Up to A/L'
        if 'Degree' in s or 'Undergraduate' in s or 'Graduate' in s: return 'Degree/Above'
        return np.nan
    df['B_Education'] = df[edu_col].apply(map_edu)
    
    def map_inc(x):
        s = str(x)
        if '< 25,000' in s: return 1
        if '25,000 – 50,000' in s: return 2
        if '51,000 – 100,000' in s: return 3
        if '> 100,000' in s: return 4
        return np.nan
    inc_numeric = df[inc_col].apply(map_inc)
    med_inc = inc_numeric.median()
    df['B_Income'] = np.where(inc_numeric.isna(), np.nan, np.where(inc_numeric <= med_inc, 'Below/Equal Median', 'Above Median'))
    
    def map_pp(x):
        if x == 'Safe': return 'Safe'
        if x in ['Delayed', 'Unsafe']: return 'Unsafe/Delayed'
        return np.nan
    df['B_Partner_Practice'] = df['Partner_Practice_Raw'].apply(map_pp)

    # --- Binarize Scores ---
    med_k = df['Expanded_Knowledge_Score'].median()
    med_pa = df['Partner_Attitude'].median()
    med_ca = df['Cascade_Attitude'].median()
    med_cp = df['Cascade_Practice_Score'].median()

    df['Cat_Knowledge'] = np.where(df['Expanded_Knowledge_Score'] > med_k, 'High', 'Low')
    df['Cat_Partner_Att'] = np.where(df['Partner_Attitude'] > med_pa, 'Good', 'Poor')
    df['Cat_Cascade_Att'] = np.where(df['Cascade_Attitude'] > med_ca, 'Good', 'Poor')
    df['Cat_Cascade_Prac'] = np.where(df['Cascade_Practice_Score'] > med_cp, 'Good', 'Poor')

    # --- 1. T-Tests ---
    print("\nRunning all T-Tests...")
    t_test_results = []
    
    def run_ttest(indep, dep, label):
        sub_df = df.dropna(subset=[indep, dep])
        groups = sub_df[indep].unique()
        if len(groups) != 2: return
        g1 = sub_df[sub_df[indep] == groups[0]][dep]
        g2 = sub_df[sub_df[indep] == groups[1]][dep]
        if len(g1) < 2 or len(g2) < 2: return
        t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
        try:
            v1, v2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
            n1, n2 = len(g1), len(g2)
            dof = ((v1/n1 + v2/n2)**2) / ((v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1))
        except:
            dof = np.nan
        t_test_results.append({
            "Test_Label": label,
            "Independent_Variable": indep,
            "Dependent_Variable": dep,
            "t_statistic": t_stat,
            "df": dof,
            "p_value": p_val,
            "Significant": "Yes" if p_val < 0.05 else "No"
        })

    scores = ["Expanded_Knowledge_Score", "Partner_Attitude", "Cascade_Attitude", "Cascade_Practice_Score"]
    indeps = ["B_Gender", "B_Marital", "B_Age", "B_Province", "B_Education", "B_Income"]
    
    idx = 1
    for indep in indeps:
        for score in scores:
            run_ttest(indep, score, f"T-Test {idx}")
            idx += 1
            
    cross_tests = [
        ("B_Partner_Practice", "Expanded_Knowledge_Score"),
        ("B_Partner_Practice", "Partner_Attitude"),
        ("Cat_Cascade_Prac", "Expanded_Knowledge_Score"),
        ("Cat_Cascade_Prac", "Cascade_Attitude")
    ]
    for ct in cross_tests:
        run_ttest(ct[0], ct[1], f"T-Test {idx}")
        idx += 1

    t_df_all = pd.DataFrame(t_test_results)
    t_df_all.to_csv(os.path.join(csv_dir, "inferential_ttest.csv"), index=False)

    # --- 2. Chi-Square Tests ---
    print("Running all Chi-Square Tests...")
    chisq_results = []
    
    def run_chisq(var1, var2, label):
        sub_df = df.dropna(subset=[var1, var2])
        if len(sub_df) == 0: return
        contingency = pd.crosstab(sub_df[var1], sub_df[var2])
        if contingency.shape[0] < 2 or contingency.shape[1] < 2: return
        chi2, p, dof, _ = stats.chi2_contingency(contingency, correction=True)
        chisq_results.append({
            "Test_Label": label,
            "Variable_1": var1,
            "Variable_2": var2,
            "Statistic": chi2,
            "df": dof,
            "p_value": p,
            "Significant": "Yes" if p < 0.05 else "No"
        })

    idx = 1
    for indep in indeps:
        run_chisq(indep, "Cat_Knowledge", f"ChiSq {idx}"); idx += 1
        
    for indep in ["B_Gender", "B_Marital", "B_Education"]:
        run_chisq(indep, "Cat_Partner_Att", f"ChiSq {idx}"); idx += 1
    for indep in ["B_Gender", "B_Education"]:
        run_chisq(indep, "Cat_Cascade_Att", f"ChiSq {idx}"); idx += 1
        
    for indep in ["B_Gender", "B_Marital", "B_Education", "B_Income"]:
        run_chisq(indep, "B_Partner_Practice", f"ChiSq {idx}"); idx += 1
    for indep in ["B_Gender", "B_Education"]:
        run_chisq(indep, "Cat_Cascade_Prac", f"ChiSq {idx}"); idx += 1

    cross_chisq = [
        ("Cat_Knowledge", "Cat_Partner_Att"),
        ("Cat_Knowledge", "Cat_Cascade_Att"),
        ("Cat_Knowledge", "B_Partner_Practice"),
        ("Cat_Knowledge", "Cat_Cascade_Prac"),
        ("Cat_Partner_Att", "B_Partner_Practice"),
        ("Cat_Cascade_Att", "Cat_Cascade_Prac")
    ]
    for cc in cross_chisq:
        run_chisq(cc[0], cc[1], f"ChiSq {idx}"); idx += 1

    chisq_df_all = pd.DataFrame(chisq_results)
    chisq_df_all.to_csv(os.path.join(csv_dir, "inferential_chisq.csv"), index=False)
    
    # --- 3. Z-Tests for Proportions ---
    print("Running Z-Tests (Proportions)...")
    from statsmodels.stats.proportion import proportions_ztest
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    
    ztest_results = []
    
    def run_ztest(indep, dep, success_val, label):
        sub_df = df.dropna(subset=[indep, dep])
        groups = sub_df[indep].unique()
        if len(groups) != 2: return
        
        count = np.array([
            sum(sub_df[sub_df[indep] == groups[0]][dep] == success_val),
            sum(sub_df[sub_df[indep] == groups[1]][dep] == success_val)
        ])
        nobs = np.array([
            sum(sub_df[indep] == groups[0]),
            sum(sub_df[indep] == groups[1])
        ])
        if any(nobs == 0): return
        
        stat, pval = proportions_ztest(count, nobs)
        ztest_results.append({
            "Test_Label": label,
            "Independent_Variable": indep,
            "Dependent_Variable": dep,
            "Statistic": stat,
            "p_value": pval,
            "Significant": "Yes" if pval < 0.05 else "No"
        })

    idx = 1
    for indep in ["B_Gender", "B_Marital", "B_Education", "B_Income"]:
        run_ztest(indep, "B_Partner_Practice", "Safe", f"Z-Test {idx}"); idx += 1
        
    if ztest_results:
        z_df_all = pd.DataFrame(ztest_results)
        z_df_all.to_csv(os.path.join(csv_dir, "inferential_ztest.csv"), index=False)

    # --- 4. Multiple Linear Regression ---
    print("Running Multiple Linear Regression...")
    reg_df = df.dropna(subset=["Expanded_Knowledge_Score", "B_Gender", "B_Marital", "B_Education", "B_Income"]).copy()
    if len(reg_df) > 0:
        reg_model = smf.ols("Expanded_Knowledge_Score ~ C(B_Gender) + C(B_Marital) + C(B_Education) + C(B_Income)", data=reg_df).fit()
        
        coef_df = pd.DataFrame({
            'Term': reg_model.params.index,
            'Estimate': reg_model.params.values,
            'Std.Error': reg_model.bse.values,
            't_value': reg_model.tvalues.values,
            'p_value': reg_model.pvalues.values,
            'Significant': ["Yes" if p < 0.05 else "No" for p in reg_model.pvalues.values]
        })
        coef_df.to_csv(os.path.join(csv_dir, "inferential_regression.csv"), index=False)

    print(f"Stage 5 completed. Inferential outputs saved under '{csv_dir}'.\n")
