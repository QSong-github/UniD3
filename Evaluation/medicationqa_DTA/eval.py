import pandas as pd
from bert_score import score


df1 = pd.read_csv("/UniD3/Evaluation/medicationqa_DTA/matched_drugs.csv")  
df2 = pd.read_csv("/UniD3/Evaluation/medicationqa_DTA/DTAeval2.csv") 


df1['Focus (Drug)'] = df1['Focus (Drug)'].str.upper().str.strip()
df2['drug'] = df2['drug'].str.upper().str.strip()

merged = pd.merge(df1, df2, left_on='Focus (Drug)', right_on='drug', how='inner')


merged = merged.dropna(subset=['Answer', 'answer'])
merged = merged[(merged['Answer'].str.strip() != "") & (merged['answer'].str.strip() != "")]


references = merged['Answer'].tolist()
candidates = merged['answer'].tolist()

P, R, F1 = score(candidates, references, lang="en", verbose=True)



print(f"Precision: {P.mean().item():.4f}")
print(f"Recall:    {R.mean().item():.4f}")
print(f"F1:        {F1.mean().item():.4f}")
