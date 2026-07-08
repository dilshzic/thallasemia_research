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
    expanded_scores += df[q20_col].astype(str).str.contains("bone marrow transplant").astype(float)
    
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
    # Each item is weighted by (1 - proportion_correct), so hard questions
    # (answered correctly by fewer participants) receive more weight.
    print("Computing (1-p) Difficulty-Weighted Knowledge Scores...")
    
    # Reconstruct all individual binary item columns
    items = {}
    items['Q15'] = (df[q15_col] == q15_correct).astype(float)
    
    for i, col in enumerate(q16_cols):
        items[f'Q16_{i+1}'] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    items['Q17'] = df[q17_col].astype(str).str.contains("Thalassemia major").astype(float)
    items['Q19'] = (df[q19_col] == q19_correct).astype(float)
    items['Q20'] = df[q20_col].astype(str).str.contains("bone marrow transplant").astype(float)
    items['Q21'] = df[q21_col].astype(str).str.contains("Can be prevented").astype(float)
    items['Q22'] = df[q22_col].astype(str).str.contains("generation to generation").astype(float)
    items['Q23'] = (df[q23_col] == q23_correct).astype(float)
    items['Q24'] = df[q24_col].astype(str).str.contains("chance").astype(float)
    items['Q26'] = df[q26_col].astype(str).str.contains("40").astype(float)
    
    for i, col in enumerate(q27_cols):
        items[f'Q27_{i+1}'] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    item_df = pd.DataFrame(items)
    n_items = len(item_df.columns)
    print(f"  Total binary knowledge items: {n_items}")
    
    # Compute (1-p) weights for each item
    item_proportions = item_df.mean()
    item_weights = 1 - item_proportions
    
    print("\n  Item Difficulty Weights:")
    print(f"  {'Item':<15} {'% Correct':>10} {'Difficulty':>12} {'Weight':>10}")
    print(f"  {'-'*50}")
    for col_name in item_df.columns:
        pct = item_proportions[col_name] * 100
        difficulty = "EASY" if pct > 60 else ("MEDIUM" if pct > 30 else "HARD")
        print(f"  {col_name:<15} {pct:>9.1f}%   {difficulty:<10} {item_weights[col_name]:>8.4f}")
    
    max_possible = item_weights.sum()
    print(f"\n  Max possible weighted score: {max_possible:.4f}")
    
    # Compute difficulty-weighted score: sum of (item_value * weight)
    weights_array = np.array([item_weights[c] for c in item_df.columns])
    df['DiffW_Knowledge_Score'] = item_df.values @ weights_array
    
    # Compute Z-score for difficulty-weighted score
    mean_dw = df['DiffW_Knowledge_Score'].mean()
    sd_dw = df['DiffW_Knowledge_Score'].std(ddof=1)
    
    if sd_dw > 0:
        df['DiffW_Knowledge_Score_Z_Score'] = (df['DiffW_Knowledge_Score'] - mean_dw) / sd_dw
    else:
        df['DiffW_Knowledge_Score_Z_Score'] = 0.0
    
    print(f"\nDifficulty-Weighted Knowledge Scores summary:")
    print(f"  Mean Score: {mean_dw:.4f}")
    print(f"  SD Score:   {sd_dw:.4f}")
    print(f"  Median:     {df['DiffW_Knowledge_Score'].median():.4f}")
    print(f"  Min:        {df['DiffW_Knowledge_Score'].min():.4f}")
    print(f"  Max:        {df['DiffW_Knowledge_Score'].max():.4f}")
    
    # Correlation between raw and difficulty-weighted scores
    r_pearson = np.corrcoef(df['Expanded_Knowledge_Score'], df['DiffW_Knowledge_Score'])[0, 1]
    print(f"  Correlation with Raw Score:")
    print(f"    Pearson:  r = {r_pearson:.4f}\n")
    
    
    # Verification checks
    print("Verification metrics:")
    print(f"  Mean of Basic Z-Scores:    {df['Knowledge_Score_Z_Score'].mean():.6f}")
    print(f"  SD of Basic Z-Scores:      {df['Knowledge_Score_Z_Score'].std(ddof=1):.6f}")
    print(f"  Mean of Expanded Z-Scores: {df['Expanded_Knowledge_Score_Z_Score'].mean():.6f}")
    print(f"  SD of Expanded Z-Scores:   {df['Expanded_Knowledge_Score_Z_Score'].std(ddof=1):.6f}")
    print(f"  Mean of DiffW Z-Scores:    {df['DiffW_Knowledge_Score_Z_Score'].mean():.6f}")
    print(f"  SD of DiffW Z-Scores:      {df['DiffW_Knowledge_Score_Z_Score'].std(ddof=1):.6f}")
    
    return df

