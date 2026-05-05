
import pandas as pd
from tqdm import tqdm
import csv
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re

model = AutoModelForCausalLM.from_pretrained("FreedomIntelligence/HuatuoGPT-o1-7B",torch_dtype=torch.bfloat16,device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("FreedomIntelligence/HuatuoGPT-o1-7B")

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
    
        messages = [{"role": "user", "content": input}]
        inputs = tokenizer(tokenizer.apply_chat_template(messages, tokenize=False,add_generation_prompt=True), return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=128)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        output_rows.append([row[0], row[1], answer])
        

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease", "answer"])
    output_df.to_csv("DEA_Huatuo_pred.csv", index=False)
    print("Saved.csv")
