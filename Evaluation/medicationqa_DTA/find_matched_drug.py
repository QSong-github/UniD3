import pandas as pd


df1 = pd.read_parquet("hf://datasets/truehealth/medicationqa/data/train-00000-of-00001-7427a10e891759be.parquet")

df1['Focus_cleaned'] = df1['Focus (Drug)'].dropna().astype(str).str.upper().str.replace('"', '', regex=False).str.strip()


df2 = pd.read_csv('/UniD3/tool/DRAG_T3_70B_output/drug_entities.csv')
drug = df2['id'].dropna().astype(str).str.upper().str.replace('"', '', regex=False).str.strip().unique().tolist()


intersection = set(df1['Focus_cleaned'].dropna().unique()) & set(drug)



df1_filtered = df1[df1['Focus_cleaned'].isin(intersection)]


df1_filtered.to_csv('matched_drugs.csv', index=False)

