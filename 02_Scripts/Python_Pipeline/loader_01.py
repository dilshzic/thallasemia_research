# ==============================================================================
# Pipeline Stage 1: Data Loader & Cleaning Module
# ==============================================================================

import pandas as pd
import numpy as np

def load_and_clean_data(xlsx_path):
    print("Reading sheet 1 from Thalassemia_Research.xlsx...")
    df = pd.read_excel(xlsx_path, sheet_name=0)
    
    print(f"Original dimensions: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    # Deduplicate and normalize column headers
    # Standardizes whitespace, removes newlines, and appends suffixes for duplicate headers
    new_cols = []
    seen = {}
    for col in df.columns:
        if pd.isna(col):
            cleaned = "Unnamed"
        else:
            cleaned = str(col).strip().replace('\n', ' ')
            cleaned = ' '.join(cleaned.split())
        
        if cleaned in seen:
            seen[cleaned] += 1
            new_cols.append(f"{cleaned}_{seen[cleaned]}")
        else:
            seen[cleaned] = 0
            new_cols.append(cleaned)
            
    df.columns = new_cols
    print("Standardized and deduplicated all column headers.")
    
    # Clean text cell values
    # Trims leading/trailing whitespace, collapses internal spaces, and sets blanks to NaN
    for col in df.columns:
        # Check if the column contains object/string types
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True)
            # Replace string nan, None, empty strings with numpy NaN
            df[col] = df[col].replace({'nan': np.nan, 'None': np.nan, '': np.nan})
            
    print("Cleaned text cell values (trimmed trailing spaces and normalized whitespace).")
    return df
