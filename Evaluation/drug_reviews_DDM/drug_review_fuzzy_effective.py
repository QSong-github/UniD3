from datasets import load_dataset, concatenate_datasets
import pandas as pd
from fuzzywuzzy import fuzz


df_dr = pd.read_json("hf://datasets/flxclxc/encoded_drug_reviews/encoded_drug_reviews.jsonl", lines=True)

df_dr_effective = df_dr[df_dr["rating"] >= 7]

df_dr_effective["drug_upper"] = df_dr_effective["drugName"].str.upper()
df_dr_effective["condition_upper"] = df_dr_effective["condition"].str.upper()


df_ddm = pd.read_csv('/UniD3/Dataset_generation/DDM.csv')
df_ddm["drug_upper"] = df_ddm["drug"].str.upper()
df_ddm["disease_upper"] = df_ddm["disease"].str.upper()


common_drugs = set(df_ddm["drug_upper"]) & set(df_dr_effective["drug_upper"])
df_dr_filtered = df_dr_effective[df_dr_effective["drug_upper"].isin(common_drugs)]
df_ddm_filtered = df_ddm[df_ddm["drug_upper"].isin(common_drugs)]


merged = pd.merge(df_dr_filtered, df_ddm_filtered, on="drug_upper", how="inner")


def is_similar(row, threshold=60):
    return fuzz.token_set_ratio(row['disease_upper'], row['condition_upper']) >= threshold


filtered_merged = merged[merged.apply(is_similar, axis=1)]


final_df = filtered_merged[["drug", "disease", "drugName", "condition"]]

final_df = final_df.drop_duplicates()
final_df.to_csv("DR_fuzzy_eff.csv", index=False)

