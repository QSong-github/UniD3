from datasets import load_dataset, concatenate_datasets
import pandas as pd




splits = {'train': 'data/train-00000-of-00001.parquet', 'validation': 'data/validation-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet', 'test_oneshot': 'data/test_oneshot-00000-of-00001.parquet', 'test_twoshot': 'data/test_twoshot-00000-of-00001.parquet'}
df_train = pd.read_parquet("hf://datasets/YufeiHFUT/CDR_with_all_info/" + splits["train"])
df_test = pd.read_parquet("hf://datasets/YufeiHFUT/CDR_with_all_info/" + splits["test"])
df_val = pd.read_parquet("hf://datasets/YufeiHFUT/CDR_with_all_info/" + splits["validation"])
merged_dataset = pd.concat([df_train, df_test, df_val], ignore_index=True)


df_CDR_effective = merged_dataset[merged_dataset["label"] == "Yes"]

CDR_list = set(df_CDR_effective['head_chemical_entName'].str.upper())



df_DEA = pd.read_csv('/UniD3/Dataset_generation/DEA.csv')
df_DEA_effective = df_DEA[df_DEA["label"].str.lower() == "ineffective"]


DEA_list = set(df_DEA_effective['drug'].str.upper())


intersection = CDR_list & DEA_list

filtered_cdr = merged_dataset[
    merged_dataset["head_chemical_entName"].str.upper().isin(intersection)
]
filtered_dea = df_DEA_effective[
    df_DEA_effective["drug"].str.upper().isin(intersection)
]


df_CDR = pd.DataFrame(filtered_cdr)


df_CDR["drug_upper"] = df_CDR["head_chemical_entName"].str.upper()
filtered_dea["drug_upper"] = filtered_dea["drug"].str.upper()


merged = pd.merge(df_CDR, filtered_dea, on="drug_upper", how="inner")


final_df = merged[["drug", "disease", "head_chemical_entName", "tail_disease_entName"]]

final_df = final_df.drop_duplicates()

final_df.to_csv("CDR_all.csv", index=False)

