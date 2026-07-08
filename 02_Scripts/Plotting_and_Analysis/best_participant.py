import pandas as pd
excel_file = '/home/dilshan/Desktop/Thallasemia research/Thalassemia_Research.xlsx'
df = pd.read_excel(excel_file, sheet_name=0)
csv_file = '/home/dilshan/Desktop/Thallasemia research/Participant_Weighted_Scores.csv'
scores_df = pd.read_csv(csv_file)

df = df.merge(scores_df, on='_id')
best_participant = df.loc[df['Weighted_Knowledge_Score'].idxmax()]

print(f"Best Participant ID: {best_participant['_id']}")
print(f"Max Score: {best_participant['Weighted_Knowledge_Score']:.4f}")
print("\\n--- Knowledge Answers ---")

single_choice = {
    '15. Is thalassemia a blood-related disease?': 'Yes',
    ' 17. What is the most severe form of thalassemia?': 'Thalassemia major (severe form)  ',
    '19. Does thalassemia major require lifelong treatment?': 'Yes',
    '20. Can thalassemia major be cured?': 'Very difficult (e.g., bone marrow transplant)    ',
    '21. Can the spread of thalassemia be prevented?': 'Can be prevented       ',
    '22. How is thalassemia transmitted?': 'From generation to generation (hereditary)  ',
    '23. Is a thalassemia carrier usually sick or healthy?': 'Healthy ',
    '24. A child born from two thalassemia carriers will be:': 'Has a chance to be affected (e.g., 25%) ',
    '26. How many thalassemia births occur in Sri Lanka per year?': '40–100  '
}

for col in df.columns:
    for q in single_choice.keys():
        if q in col and '/' not in col:
            print(f"{q} -> {best_participant[col]}")

print("\\n--- Multiple Choice Options Selected ---")
mc_prefixes = [
    '16. What are the clinical forms of thalassemia? (Tick all that apply)',
    '27. Problems faced by thalassemia major patients (Tick all that apply)',
    '28. What should a thalassemia carrier do after diagnosis? (Tick all that apply)'
]

for prefix in mc_prefixes:
    print(f"\\n{prefix}:")
    for col in df.columns:
        if col.startswith(prefix) and '/' in col:
            if best_participant[col] == 1.0:
                print(f" - {col.split('/', 1)[1].strip()}")
