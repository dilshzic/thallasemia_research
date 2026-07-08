# ==============================================================================
# Pipeline Stage 3: Descriptive Statistics Summaries Module
# ==============================================================================

import pandas as pd
import numpy as np
import re
import os

# --- Helper Function: Dynamic Column Finder ---
def find_col(df, pattern):
    matched = [c for c in df.columns if re.search(pattern, c, re.IGNORECASE)]
    if matched:
        return matched[0]
    else:
        raise KeyError(f"CRITICAL ERROR: Could not locate column matching pattern: {pattern}")

# --- Helper Function: Single Select Frequency Table ---
def calc_freq(df, column_name, question_id=""):
    series = df[column_name]
    # Handle pandas Categorical columns to prevent category set errors when filling NA
    if isinstance(series.dtype, pd.CategoricalDtype):
        if series.isna().any() and "Missing/No Response" not in series.cat.categories:
            series = series.cat.add_categories("Missing/No Response")
            
    # Group by cell values, filling NaN with missing response string
    counts = series.fillna("Missing/No Response").value_counts()
    total = len(df)
    
    records = []
    for val, count in counts.items():
        records.append({
            "Question_ID": question_id,
            "Question": column_name,
            "Response": str(val).strip(),
            "Frequency": int(count),
            "Percentage": float((count / total) * 100)
        })
        
    res_df = pd.DataFrame(records)
    # Sort by frequency descending (ties by response)
    if not res_df.empty:
        res_df = res_df.sort_values(by=["Frequency", "Response"], ascending=[False, True])
    return res_df

# --- Helper Function: Multi-Select Frequency Table ---
def calc_multi_freq(df, prefix, question_id="", question_name=""):
    cols = [c for c in df.columns if c.startswith(prefix)]
    if not cols:
        return pd.DataFrame()
        
    records = []
    total = len(df)
    for c in cols:
        option_name = c[len(prefix):].strip()
        # Sum binary values
        checked_count = int(pd.to_numeric(df[c], errors='coerce').fillna(0).sum())
        records.append({
            "Question_ID": question_id,
            "Question": question_name,
            "Response": option_name,
            "Frequency": checked_count,
            "Percentage": float((checked_count / total) * 100)
        })
        
    res_df = pd.DataFrame(records)
    if not res_df.empty:
        res_df = res_df.sort_values(by=["Frequency", "Response"], ascending=[False, True])
    return res_df


def run_descriptive_stats(df, csv_dir):
    print("Calculating descriptive statistics tables...")
    
    # ==================== 1. DEMOGRAPHICS (PART A: Q1-Q14) ====================
    print("  Processing Part A: Demographics...")
    demographics_dfs = []
    
    # Age numeric summary
    age_col = find_col(df, r"^1\. Age")
    age_vals = pd.to_numeric(df[age_col], errors='coerce')
    age_summary = pd.DataFrame([
        {"Question_ID": "Q1_Summary", "Question": "1. Age (Numerical Stats)", "Response": "Mean Age", "Frequency": np.nan, "Percentage": float(age_vals.mean())},
        {"Question_ID": "Q1_Summary", "Question": "1. Age (Numerical Stats)", "Response": "Standard Deviation", "Frequency": np.nan, "Percentage": float(age_vals.std(ddof=1))},
        {"Question_ID": "Q1_Summary", "Question": "1. Age (Numerical Stats)", "Response": "Median Age", "Frequency": np.nan, "Percentage": float(age_vals.median())},
        {"Question_ID": "Q1_Summary", "Question": "1. Age (Numerical Stats)", "Response": "Min Age", "Frequency": np.nan, "Percentage": float(age_vals.min())},
        {"Question_ID": "Q1_Summary", "Question": "1. Age (Numerical Stats)", "Response": "Max Age", "Frequency": np.nan, "Percentage": float(age_vals.max())}
    ])
    demographics_dfs.append(age_summary)
    
    # Age group categories
    bins = [15, 24, 34, 44, 54, 100]
    labels = ["18-24", "25-34", "35-44", "45-54", "55+"]
    df['Age_Group'] = pd.cut(age_vals, bins=bins, labels=labels)
    demographics_dfs.append(calc_freq(df, "Age_Group", "Q1_Groups"))
    
    # Categorical demographics Q2 to Q11
    q2_to_q11 = [
        {"p": r"^2\. Gender", "id": "Q2"},
        {"p": r"^3\. Ethnicity", "id": "Q3"},
        {"p": r"^4\. Religion", "id": "Q4"},
        {"p": r"^5\. Occupation", "id": "Q5"},
        {"p": r"^6\. Monthly Income", "id": "Q6"},
        {"p": r"^7\. Education Level", "id": "Q7"},
        {"p": r"^8\. Residing Province", "id": "Q8"},
        {"p": r"^9\. Marital Status", "id": "Q9"},
        {"p": r"^10\. Do you have children", "id": "Q10"},
        {"p": r"^11\. Do you have a family history", "id": "Q11"}
    ]
    
    for item in q2_to_q11:
        matched_col = find_col(df, item["p"])
        demographics_dfs.append(calc_freq(df, matched_col, item["id"]))
        
    # Q12: Specifics of family history
    q12_col = find_col(df, r"^12\. If yes")
    demographics_dfs.append(calc_freq(df, q12_col, "Q12"))
    
    # Q13 & Q14
    q13_col = find_col(df, r"^13\. When were you diagnosed")
    # Clean datetime format to year string
    df['Diagnosis_Year'] = pd.to_datetime(df[q13_col], errors='coerce').dt.strftime('%Y')
    # Fallback for numerical/string years already in cells
    df.loc[df['Diagnosis_Year'].isna(), 'Diagnosis_Year'] = df.loc[df['Diagnosis_Year'].isna(), q13_col].astype(str)
    df['Diagnosis_Year'] = df['Diagnosis_Year'].replace({'nan': np.nan, 'NaT': np.nan})
    demographics_dfs.append(calc_freq(df, "Diagnosis_Year", "Q13"))
    
    q14_col = find_col(df, r"^14\. Where were you diagnosed")
    demographics_dfs.append(calc_freq(df, q14_col, "Q14"))
    
    # Concatenate and save demographics
    demographics_all = pd.concat(demographics_dfs, ignore_index=True)
    demographics_all.to_csv(os.path.join(csv_dir, "demographics.csv"), index=False)
    
    
    # ==================== 2. KNOWLEDGE QUESTIONS (PART B: Q15-Q29) ====================
    print("  Processing Part B: Knowledge Questions...")
    knowledge_dfs = []
    
    single_knowledge = [
        {"p": r"^15\. Is thalassemia", "id": "Q15"},
        {"p": r"^17\. What is the most severe", "id": "Q17"},
        {"p": r"^18\. What form of thalassemia do you have", "id": "Q18"},
        {"p": r"^19\. Does thalassemia major require", "id": "Q19"},
        {"p": r"^20\. Can thalassemia major be cured", "id": "Q20"},
        {"p": r"^21\. Can the spread", "id": "Q21"},
        {"p": r"^22\. How is thalassemia transmitted", "id": "Q22"},
        {"p": r"^23\. Is a thalassemia carrier", "id": "Q23"},
        {"p": r"^24\. A child born from two", "id": "Q24"},
        {"p": r"^25\. After diagnosis, was counseling", "id": "Q25"},
        {"p": r"^26\. How many thalassemia births", "id": "Q26"},
        {"p": r"^29\. How did you learn", "id": "Q29"}
    ]
    
    for item in single_knowledge:
        matched_col = find_col(df, item["p"])
        knowledge_dfs.append(calc_freq(df, matched_col, item["id"]))
        
    # Multi-select Q16, Q27, Q28
    q16_multi = calc_multi_freq(df, "16. What are the clinical forms of thalassemia? (Tick all that apply)/", "Q16", "What are the clinical forms of thalassemia?")
    if not q16_multi.empty:
        knowledge_dfs.append(q16_multi)
        
    q27_multi = calc_multi_freq(df, "27. Problems faced by thalassemia major patients (Tick all that apply):/", "Q27", "Problems faced by thalassemia major patients")
    if not q27_multi.empty:
        knowledge_dfs.append(q27_multi)
        
    q28_multi = calc_multi_freq(df, "28. What should a thalassemia carrier do after diagnosis? (Tick all that apply) /", "Q28", "What should a thalassemia carrier do after diagnosis?")
    if not q28_multi.empty:
        knowledge_dfs.append(q28_multi)
        
    # Concatenate and save knowledge
    knowledge_all = pd.concat(knowledge_dfs, ignore_index=True)
    knowledge_all.to_csv(os.path.join(csv_dir, "knowledge.csv"), index=False)
    
    
    # ==================== 3. MARRIAGE & PARTNER SCREENING (PART C: Q30-Q34) ====================
    print("  Processing Part C: Marriage & Partner attitudes...")
    marriage_dfs = []
    
    q30_col = find_col(df, r"^30\. Are you willing")
    q31_col = find_col(df, r"^31\. Do you accept")
    q32_col = find_col(df, r"^32\. How important")
    q33_col = find_col(df, r"^33\. What was your practice")
    q34_col = find_col(df, r"^34\. If you did not disclose")
    
    # Locate write-in Columns by index relative to Q33 and Q34 columns
    q33_idx = list(df.columns).index(q33_col)
    q33_other_col = df.columns[q33_idx + 1]
    
    q34_idx = list(df.columns).index(q34_col)
    q34_other_col = df.columns[q34_idx + 1]
    
    marriage_dfs.append(calc_freq(df, q30_col, "Q30"))
    marriage_dfs.append(calc_freq(df, q31_col, "Q31"))
    marriage_dfs.append(calc_freq(df, q32_col, "Q32"))
    marriage_dfs.append(calc_freq(df, q33_col, "Q33"))
    marriage_dfs.append(calc_freq(df, q33_other_col, "Q33_Other"))
    marriage_dfs.append(calc_freq(df, q34_col, "Q34"))
    marriage_dfs.append(calc_freq(df, q34_other_col, "Q34_Other"))
    
    marriage_all = pd.concat(marriage_dfs, ignore_index=True)
    marriage_all.to_csv(os.path.join(csv_dir, "marriage_partner.csv"), index=False)
    
    
    # ==================== 4. FAMILY SCREENING (PART D: Q35-Q40) ====================
    print("  Processing Part D: Family Screening...")
    family_dfs = []
    
    q35_col = find_col(df, r"^35\. Do you think")
    q36_col = find_col(df, r"^36\. Do your family members")
    q37_1_col = find_col(df, r"^First-degree relatives")
    q37_2_col = find_col(df, r"^Second-degree relatives")
    q37_3_col = find_col(df, r"^Third-degree relatives")
    
    # Q38 prefix and columns
    q38_prefix = "38. If not screened, what were the reasons? (Tick all that apply)/"
    q38_cols = [c for c in df.columns if c.startswith(q38_prefix)]
    q38_last_idx = list(df.columns).index(q38_cols[-1])
    q38_other_col = df.columns[q38_last_idx + 1]
    
    q39_col = find_col(df, r"^39\. How easy")
    q40_col = find_col(df, r"^40\. How important")
    
    family_dfs.append(calc_freq(df, q35_col, "Q35"))
    family_dfs.append(calc_freq(df, q36_col, "Q36"))
    family_dfs.append(calc_freq(df, q37_1_col, "Q37_FirstDegree"))
    family_dfs.append(calc_freq(df, q37_2_col, "Q37_SecondDegree"))
    family_dfs.append(calc_freq(df, q37_3_col, "Q37_ThirdDegree"))
    
    q38_multi = calc_multi_freq(df, q38_prefix, "Q38_Barriers", "If not screened, what were the reasons?")
    if not q38_multi.empty:
        family_dfs.append(q38_multi)
        
    family_dfs.append(calc_freq(df, q38_other_col, "Q38_Other"))
    family_dfs.append(calc_freq(df, q39_col, "Q39"))
    family_dfs.append(calc_freq(df, q40_col, "Q40"))
    
    family_all = pd.concat(family_dfs, ignore_index=True)
    family_all.to_csv(os.path.join(csv_dir, "family_screening.csv"), index=False)
