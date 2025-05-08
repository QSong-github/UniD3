from datasets import load_dataset, concatenate_datasets
import pandas as pd
from fuzzywuzzy import fuzz


splits = {'train': 'data/train-00000-of-00001.parquet', 'validation': 'data/validation-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet', 'test_oneshot': 'data/test_oneshot-00000-of-00001.parquet', 'test_twoshot': 'data/test_twoshot-00000-of-00001.parquet'}
df_train = pd.read_parquet("hf://datasets/YufeiHFUT/CDR_with_all_info/" + splits["train"])
df_test = pd.read_parquet("hf://datasets/YufeiHFUT/CDR_with_all_info/" + splits["test"])
df_val = pd.read_parquet("hf://datasets/YufeiHFUT/CDR_with_all_info/" + splits["validation"])
merged_dataset = pd.concat([df_train, df_test, df_val], ignore_index=True)

df_CDR = merged_dataset[merged_dataset["label"] == "Yes"]

df_CDR["drug_upper"] = df_CDR["head_chemical_entName"].str.upper()
df_CDR["tail_disease_entName_upper"] = df_CDR["tail_disease_entName"].str.upper()


df_ddm = pd.read_csv('/UniD3/Dataset_generation/DDM.csv')
df_ddm["drug_upper"] = df_ddm["drug"].str.upper()
df_ddm["disease_upper"] = df_ddm["disease"].str.upper()


common_drugs = set(df_ddm["drug_upper"]) & set(df_CDR["drug_upper"])
df_p3ps_filtered = df_CDR[df_CDR["drug_upper"].isin(common_drugs)]
df_ddm_filtered = df_ddm[df_ddm["drug_upper"].isin(common_drugs)]


merged = pd.merge(df_p3ps_filtered, df_ddm_filtered, on="drug_upper", how="inner")


def is_similar(row, threshold=60):
    return fuzz.token_set_ratio(row['disease_upper'], row['tail_disease_entName_upper']) >= threshold


filtered_merged = merged[merged.apply(is_similar, axis=1)]


final_df = filtered_merged[["drug", "disease", "head_chemical_entName", "tail_disease_entName"]]

final_df = final_df.drop_duplicates()
final_df.to_csv("CDR_fuzzy.csv", index=False)
print(f"keep {len(final_df)} records")
print(final_df.head())
