import pandas as pd
from tqdm import tqdm

def find_matches(question_file, drug_file, output_file):
    questions_df = pd.read_parquet(question_file)
    drugs_df = pd.read_csv(drug_file)
    

    questions_df['question'] = questions_df['question'].astype(str).str.upper()
    drugs_df['drug'] = drugs_df['drug'].astype(str).str.upper()
    drugs_df['disease'] = drugs_df['disease'].astype(str).str.upper()


    matched_rows = []

    for _, question_row in tqdm(questions_df.iterrows(), total=len(questions_df), desc="Processing questions"):
        question = question_row['question']
        
        for _, drug_row in drugs_df.iterrows():
            drug = drug_row['drug']
            disease = drug_row['disease']
            
      
            if drug in question and disease in question:
                matched_rows.append(question_row)
                break  

    if matched_rows:
        pd.DataFrame(matched_rows).to_csv(output_file, index=False)
        print(f"saved to {output_file}")
    else:
        print("not find any matches.")


find_matches("hf://datasets/qiaojin/PubMedQA/pqa_artificial/train-00000-of-00001.parquet", 
             '/UniD3/Dataset_generation/DEA.csv', 
             'matched_questionsDEA.csv')
