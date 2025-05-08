from datasets import load_dataset, concatenate_datasets
import pandas as pd



df_dr = pd.read_json("hf://datasets/flxclxc/encoded_drug_reviews/encoded_drug_reviews.jsonl", lines=True)


df_dr_effective = df_dr[df_dr["rating"] <= 3]
df_dr_list = set(df_dr_effective['drugName'].str.upper())

df_DEA = pd.read_csv('/UniD3/Dataset_generation/DEA.csv')
df_DEA_effective = df_DEA[df_DEA["label"].str.lower() == "ineffective"]


DEA_list = set(df_DEA_effective['drug'].str.upper())

intersection = df_dr_list & DEA_list


filtered_dr = df_dr_effective[df_dr_effective['drugName'].str.upper().isin(intersection)]
filtered_dea = df_DEA_effective[df_DEA_effective['drug'].str.upper().isin(intersection)]

df_p3ps = pd.DataFrame(filtered_dr)

df_p3ps["drug_upper"] = df_p3ps["drugName"].str.upper()
filtered_dea["drug_upper"] = filtered_dea["drug"].str.upper()


merged = pd.merge(df_p3ps, filtered_dea, on="drug_upper", how="inner")


final_df = merged[["drug", "disease", "drugName", "condition"]]

final_df = final_df.drop_duplicates()

final_df.to_csv("DR_all_ineff.csv", index=False)
