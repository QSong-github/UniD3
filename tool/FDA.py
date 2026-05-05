import pandas as pd


df = pd.read_csv('/UniD3/tool/Products.csv')

drug_names = set(df['DrugName'].str.upper())


unique_drug_names_df = pd.DataFrame(list(drug_names), columns=['drug'])


unique_drug_names_df.to_csv('FDA_list.csv', index=False)

