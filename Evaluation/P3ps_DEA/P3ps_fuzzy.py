from datasets import load_dataset, concatenate_datasets
import pandas as pd
from fuzzywuzzy import fuzz


ds = load_dataset("P3ps/condition_to_drug")
merged_dataset = concatenate_datasets([ds["train"], ds["validation"], ds["test"]])
df_p3ps = pd.DataFrame(merged_dataset)
df_p3ps["drug_upper"] = df_p3ps["drugName"].str.upper()
df_p3ps["condition_upper"] = df_p3ps["condition"].str.upper()

df_dea = pd.read_csv('/UniD3/Dataset_generation/DEA.csv')
df_dea = df_dea[df_dea["label"].str.lower() == "effective"]
df_dea["drug_upper"] = df_dea["drug"].str.upper()
df_dea["disease_upper"] = df_dea["disease"].str.upper()


common_drugs = set(df_dea["drug_upper"]) & set(df_p3ps["drug_upper"])
df_p3ps_filtered = df_p3ps[df_p3ps["drug_upper"].isin(common_drugs)]
df_dea_filtered = df_dea[df_dea["drug_upper"].isin(common_drugs)]


merged = pd.merge(df_p3ps_filtered, df_dea_filtered, on="drug_upper", how="inner")

def is_similar(row, threshold=60):
    return fuzz.token_set_ratio(row['disease_upper'], row['condition_upper']) >= threshold

filtered_merged = merged[merged.apply(is_similar, axis=1)]


final_df = filtered_merged[["drug", "disease", "drugName", "condition"]]

final_df = final_df.drop_duplicates()
final_df.to_csv("P3ps_fuzzy.csv", index=False)

