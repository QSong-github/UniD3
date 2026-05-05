
import pandas as pd
from tqdm import tqdm
import csv
import re
from transformers import AutoTokenizer, pipeline
import torch

model = "johnsnowlabs/JSL-MedLlama-3-8B-v2.0"


tokenizer = AutoTokenizer.from_pretrained(model)
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",
)





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
    next(csvreader)  

    for row in tqdm(csvreader, total=total_lines, desc="Processing"):
        conentent = 'The drug name is ' + row[0] + " and the disease name is " + row[1] + "."
        # print("conentent:", conentent)
        input = prompt + conentent
        messages = [{"role": "user", "content": input}]
        user_message = messages[0]["content"]
        inputs = user_message
        outputs = generator(inputs, max_new_tokens=64, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        answer = outputs[0]["generated_text"]
        output_rows.append([row[0], row[1], answer])
        

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease", "answer"])
    output_df.to_csv("DEA_MedLlama3_pred.csv", index=False)
    print("Saved.csv")
