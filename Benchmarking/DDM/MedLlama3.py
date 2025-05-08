
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
        messages = [{"role": "user", "content": input}]
        user_message = messages[0]["content"]
        inputs = user_message
        outputs = generator(inputs, max_new_tokens=64, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        answer = outputs[0]["generated_text"]
        output_rows.append([row[0], answer])
        

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease"])
    output_df.to_csv("DDM_MedLlama3_pred.csv", index=False)
    print("Saved.csv")
