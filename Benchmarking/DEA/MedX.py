
import pandas as pd
from tqdm import tqdm
import csv
import re
import torch
import transformers

model_id = "skumar9/Llama-medx_v3.2"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)

gen_kwargs = {
    "return_full_text": False,
    "max_new_tokens": 32,
}


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
    
        answer = pipeline(input, **gen_kwargs)[0]["generated_text"]
        output_rows.append([row[0], row[1], answer])
        
    output_df = pd.DataFrame(output_rows, columns=["drug", "disease", "answer"])
    output_df.to_csv("DEA_MedX_pred.csv", index=False)
    print("Saved.csv")
