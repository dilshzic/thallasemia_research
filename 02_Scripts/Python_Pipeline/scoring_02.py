# ==============================================================================
# Pipeline Stage 2: Knowledge Scores & Z-Scores Calculation Module
# ==============================================================================

import pandas as pd
import numpy as np

def calculate_scores(df):
    print("Calculating scoring metrics...")
    
    # --- 1. Identify columns for Basic Knowledge Score (Q16 & Q27 sub-columns) ---
    q16_cols = [c for c in df.columns if c.startswith("16. What are the clinical forms of thalassemia? (Tick all that apply)/")]
    # Exclude "I don't know" from positive scoring
    q16_cols = [c for c in q16_cols if "I don’t know" not in c]
    
    q27_cols = [c for c in df.columns if c.startswith("27. Problems faced by thalassemia major patients (Tick all that apply):/")]
    
    print(f"Found {len(q16_cols)} columns for Q16 (forms) and {len(q27_cols)} columns for Q27 (complications).")
    
    # Copy data to calculate score, replacing NA with 0
    temp_df = df[q16_cols + q27_cols].apply(pd.to_numeric, errors='coerce').fillna(0)
    
    # Basic raw score
    df['Knowledge_Score'] = temp_df.sum(axis=1)
    
    # Calculate Basic Z-score
    mean_basic = df['Knowledge_Score'].mean()
    sd_basic = df['Knowledge_Score'].std(ddof=1) # sample standard deviation
    
    if sd_basic > 0:
        df['Knowledge_Score_Z_Score'] = (df['Knowledge_Score'] - mean_basic) / sd_basic
    else:
        df['Knowledge_Score_Z_Score'] = 0.0
        
    print("Basic Knowledge Scores summary:")
    print(f"  Mean Score: {mean_basic:.4f}")
    print(f"  SD Score:   {sd_basic:.4f}\n")
    
    
    # --- 2. Compute Expanded Knowledge Score (All 11 knowledge questions, max 20 points) ---
    # Correct answers definitions:
    q15_correct = "Yes"
    q17_correct = "Thalassemia major (severe form)"
    q19_correct = "Yes"
    q20_correct = "Very difficult (e.g., bone marrow transplant)"
    q21_correct = "Can be prevented"
    q22_correct = "From generation to generation (hereditary)"
    q23_correct = "Healthy"
    q24_correct = "Has a chance to be affected (e.g., 25%)"
    q26_correct = "40–100"
    
    print("Computing Expanded Knowledge Scores (max 20 points)...")
    expanded_scores = pd.Series([0.0] * len(df))
    
    # Q15
    q15_col = "15. Is thalassemia a blood-related disease?"
    expanded_scores += (df[q15_col] == q15_correct).astype(float)
    
    # Q16
    for col in q16_cols:
        expanded_scores += pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    # Q17
    q17_col = "17. What is the most severe form of thalassemia?"
    expanded_scores += df[q17_col].astype(str).str.contains("Thalassemia major").astype(float)
    
    # Q19
    q19_col = "19. Does thalassemia major require lifelong treatment?"
    expanded_scores += (df[q19_col] == q19_correct).astype(float)
    
    # Q20
    q20_col = "20. Can thalassemia major be cured?"
    expanded_scores += df[q20_col].astype(str).str.contains("bone marrow transplant|Cannot be cured").astype(float)
    
    # Q21
    q21_col = "21. Can the spread of thalassemia be prevented?"
    expanded_scores += df[q21_col].astype(str).str.contains("Can be prevented").astype(float)
    
    # Q22
    q22_col = "22. How is thalassemia transmitted?"
    expanded_scores += df[q22_col].astype(str).str.contains("generation to generation").astype(float)
    
    # Q23
    q23_col = "23. Is a thalassemia carrier usually sick or healthy?"
    expanded_scores += (df[q23_col] == q23_correct).astype(float)
    
    # Q24
    q24_col = "24. A child born from two thalassemia carriers will be:"
    expanded_scores += df[q24_col].astype(str).str.contains("chance").astype(float)
    
    # Q26
    q26_col = "26. How many thalassemia births occur in Sri Lanka per year?"
    expanded_scores += df[q26_col].astype(str).str.contains("40").astype(float)
    
    # Q27
    for col in q27_cols:
        expanded_scores += pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    df['Expanded_Knowledge_Score'] = expanded_scores
    
    # Calculate Expanded Z-score
    mean_exp = df['Expanded_Knowledge_Score'].mean()
    sd_exp = df['Expanded_Knowledge_Score'].std(ddof=1)
    
    if sd_exp > 0:
        df['Expanded_Knowledge_Score_Z_Score'] = (df['Expanded_Knowledge_Score'] - mean_exp) / sd_exp
    else:
        df['Expanded_Knowledge_Score_Z_Score'] = 0.0
        
    print("Expanded Knowledge Scores summary:")
    print(f"  Mean Score: {mean_exp:.4f}")
    print(f"  SD Score:   {sd_exp:.4f}\n")
    
    
    # --- 3. Compute (1-p) Difficulty-Weighted Knowledge Score ---
    if False:
        pass
        
    print("\nComputing Attitude and Practice Scores...")
    # Partner Attitude
    q28_cols = [c for c in df.columns if c.startswith('28.') and '/' in c]
    q30_col = [c for c in df.columns if c.startswith('30.')][0]
    q31_col = [c for c in df.columns if c.startswith('31.')][0]
    q32_col = [c for c in df.columns if c.startswith('32.')][0]
    q34_col = [c for c in df.columns if c.startswith('34.')][0]

    def get_q28_score(row):
        s = 0
        for col in q28_cols:
            if row[col] == 1.0:
                opt = col.split('/', 1)[1].strip().lower()
                if 'get the partner tested' in opt or 'get family members tested' in opt: s += 1
                if 'ignore it' in opt: s -= 2
        return s
    
    def get_partner_attitude(row):
        s = get_q28_score(row)
        # Q30
        v30 = str(row[q30_col]).lower()
        if 'definitely not' in v30: s += 1
        elif 'not sure' in v30: s -= 1
        elif 'yes i am willing' in v30 or 'yes i have' in v30: s -= 2
        # Q31
        v31 = str(row[q31_col]).lower().strip()
        if v31 == 'no': s += 1
        elif 'yes' in v31: s -= 1
        # Q32
        v32 = str(row[q32_col]).lower()
        if 'very important' in v32: s += 2
        elif v32.startswith('important'): s += 1
        elif 'not important' in v32: s -= 1
        # Q34
        v34 = str(row[q34_col]).lower()
        if 'lack of understanding' in v34 or 'did not think it was necessary' in v34 or 'concern about causing worry' in v34: s -= 1
        return s

    df['Partner_Attitude'] = df.apply(get_partner_attitude, axis=1)

    # Cascade Attitude
    q35_col = [c for c in df.columns if c.startswith('35.')][0]
    q36_col = [c for c in df.columns if c.startswith('36.')][0]
    q40_col = [c for c in df.columns if c.startswith('40.')][0]
    
    def get_cascade_attitude(row):
        s = 0
        v35 = str(row[q35_col]).lower()
        if 'agree' in v35 and 'disagree' not in v35: s += 1
        elif 'disagree' in v35: s -= 1
        v36 = str(row[q36_col]).lower().strip()
        if v36 == 'yes': s += 1
        elif v36 == 'no': s -= 1
        v40 = str(row[q40_col]).lower()
        if 'very important' in v40: s += 2
        elif v40.startswith('important'): s += 1
        elif 'not important' in v40: s -= 1
        return s

    df['Cascade_Attitude'] = df.apply(get_cascade_attitude, axis=1)

    # Practices
    q33_col = [c for c in df.columns if c.startswith('33.')][0]
    def map_partner_practice(v):
        v = str(v).lower()
        if 'before marriage' in v: return 'Safe'
        if 'after marriage' in v or 'pregnancy' in v: return 'Delayed'
        if 'did not screen' in v or 'did not disclose' in v: return 'Unsafe'
        return np.nan
    df['Partner_Practice_Raw'] = df[q33_col].apply(map_partner_practice)

    col_1st = [c for c in df.columns if 'first-degree' in c.lower()][0]
    col_2nd = [c for c in df.columns if 'second-degree' in c.lower()][0]
    col_3rd = [c for c in df.columns if 'third-degree' in c.lower()][0]
    def score_rel(v):
        v = str(v).lower()
        if 'all' in v: return 2
        if 'some' in v: return 1
        return 0
    df['Cascade_Practice_Score'] = df[col_1st].apply(score_rel) + df[col_2nd].apply(score_rel) + df[col_3rd].apply(score_rel)
    print("Scores computed successfully.")
    
    # Verification checks
    print("Verification metrics:")
    print(f"  Mean of Basic Z-Scores:    {df['Knowledge_Score_Z_Score'].mean():.6f}")
    print(f"  SD of Basic Z-Scores:      {df['Knowledge_Score_Z_Score'].std(ddof=1):.6f}")
    print(f"  Mean of Expanded Z-Scores: {df['Expanded_Knowledge_Score_Z_Score'].mean():.6f}")
    print(f"  SD of Expanded Z-Scores:   {df['Expanded_Knowledge_Score_Z_Score'].std(ddof=1):.6f}")
    # print(f"  Mean of DiffW Z-Scores:    {df['DiffW_Knowledge_Score_Z_Score'].mean():.6f}")
    # print(f"  SD of DiffW Z-Scores:      {df['DiffW_Knowledge_Score_Z_Score'].std(ddof=1):.6f}")
    
    return df

