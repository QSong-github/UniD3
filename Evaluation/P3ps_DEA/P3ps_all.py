from datasets import load_dataset, concatenate_datasets
import pandas as pd

ds = load_dataset("P3ps/condition_to_drug")
merged_dataset = concatenate_datasets([ds["train"], ds["validation"], ds["test"]])

P3ps_list = set([name.upper() for name in merged_dataset['drugName']])


df_DEA = pd.read_csv('/UniD3/Dataset_generation/DEA.csv')
df_DEA_effective = df_DEA[df_DEA["label"].str.lower() == "effective"]


DEA_list = set(df_DEA_effective['drug'].str.upper())


intersection = P3ps_list & DEA_list


filtered_p3ps = merged_dataset.filter(lambda x: x['drugName'].upper() in intersection)
filtered_dea = df_DEA_effective[df_DEA_effective['drug'].str.upper().isin(intersection)]


df_p3ps = pd.DataFrame(filtered_p3ps)

df_p3ps["drug_upper"] = df_p3ps["drugName"].str.upper()
filtered_dea["drug_upper"] = filtered_dea["drug"].str.upper()


merged = pd.merge(df_p3ps, filtered_dea, on="drug_upper", how="inner")


final_df = merged[["drug", "disease", "drugName", "condition"]]

final_df = final_df.drop_duplicates()

final_df.to_csv("P3ps_all.csv", index=False)

