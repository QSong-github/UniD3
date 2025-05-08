
import pandas as pd
from tqdm import tqdm
import csv
import ollama


model_name = 'llama3.3:70b'

prompt = """In a task named Drug Effectiveness Assessment (Evaluate the effectiveness of [specific drug] for treating [specific disease]. 
I will give you a drug name and a disease name, and you need to judge whether this drug is effective for this disease.
To keep it simple, please just answer 'effective' or 'ineffective', nothing else.

Here is an example:
The drug name is ELTANEXOR and the disease name is Acute Myeloid Leukemia (AML).

Answer: effective

Now, please answer the following question:

"""

output_rows = []
with open('/UniD3/Benchmarking/data/DEA.csv', mode='r', encoding='utf-8-sig') as infile:
    csvreader = csv.reader(infile)
    header = next(csvreader)

    infile.seek(0)
    total_lines = sum(1 for line in infile) - 1  
    infile.seek(0)
    next(csvreader)  
    for row in tqdm(csvreader, total=total_lines, desc="Processing"):
        conentent = 'The drug name is ' + row[0] + " and the disease name is " + row[1] + "."
        # print("conentent:", conentent)
        input = prompt + conentent
    
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': input}]
        )
        answer = response['message']['content']
        output_rows.append([row[0], row[1], answer])
        

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease", "pred_label"])
    output_df.to_csv("DEA_Llama33_70B_pred.csv", index=False)
    print("Saved.csv")
