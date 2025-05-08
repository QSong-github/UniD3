
import pandas as pd
from tqdm import tqdm
import csv
import ollama


model_name = 'llama3.3:70b'

prompt = """In a task named Drug-Disease Matching (Identify potential diseases that could be treated by [specific Drug]). 
I will give you a drug name, and you need to list several diseases that have a positive association with this drug.
To keep it simple, please just answer with the disease names, nothing else.

Here is an example:
The drug name is CEFTAZIDIME-AVIBACTAM.

Answer: [Complicated Urinary Tract Infections (cUTI),Complicated Intra-Abdominal Infections (cIAI),Hospital-Acquired Bacterial Pneumonia (HABP)]

Now, please answer the following question:

"""

output_rows = []
with open('/UniD3/Benchmarking/DDM/DDM.csv', mode='r', encoding='utf-8-sig') as infile:
    csvreader = csv.reader(infile)
    
    header = next(csvreader)

    infile.seek(0)
    total_lines = sum(1 for line in infile) - 1  
    infile.seek(0)
    next(csvreader)  

    for row in tqdm(csvreader, total=total_lines, desc="Processing"):
        conentent = 'The drug name is ' + row[0] + "."
        # print("conentent:", conentent)
        input = prompt + conentent
    
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': input}]
        )
        answer = response['message']['content']
        output_rows.append([row[0], answer])
        

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease"])
    output_df.to_csv("DDM_Llama33_70B_pred.csv", index=False)
    print("Saved.csv")
