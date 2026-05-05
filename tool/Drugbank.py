import pandas as pd


df = pd.read_csv('/UniD3/tool/drugbank vocabulary.csv')

drug_names = set(df['Common name'].str.upper())


unique_drug_names_df = pd.DataFrame(list(drug_names), columns=['drug'])


unique_drug_names_df.to_csv('Drugbank_list.csv', index=False)

