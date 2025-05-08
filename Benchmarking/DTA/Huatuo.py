
import pandas as pd
from tqdm import tqdm
import csv
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re

model = AutoModelForCausalLM.from_pretrained("FreedomIntelligence/HuatuoGPT-o1-7B",torch_dtype=torch.bfloat16,device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("FreedomIntelligence/HuatuoGPT-o1-7B")

prompt = """In a task named Drug-Target Analysis (Identify potential diseases that could be treated by [specific Drug]. For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism.). 
I will give you a drug name and the drug-related Question, and you need to give an Answer of this Question.
To keep it simple, please just give the Answer, nothing else.

Here is an example:
The drug name is OMADACYCLINE and the Question is "What are the primary gene targets of Omadacycline in treating community-acquired bacterial pneumonia (CABP), and how do these targets relate to the disease's underlying biology?".

Answer: "The primary gene targets of Omadacycline in treating CABP are the bacterial ribosomal subunits, specifically the 30S and 50S subunits. By binding to these subunits, Omadacycline inhibits protein synthesis in bacteria, ultimately leading to their death. This mechanism is consistent with the underlying biology of CABP, as it targets the fundamental process of bacterial growth and replication, which is essential for the progression of the disease. Additionally, Omadacycline's broad-spectrum activity against various bacterial pathogens, including those resistant to other antibiotics, makes it an effective treatment option for CABP, where timely and effective treatment is crucial to prevent severe outcomes."

Now, please answer the following question:

"""

output_rows = []
with open('/UniD3/Benchmarking/DTA/DTA.csv', mode='r', encoding='utf-8-sig') as infile:
    csvreader = csv.reader(infile)

    header = next(csvreader)

    infile.seek(0)
    total_lines = sum(1 for line in infile) - 1 
    infile.seek(0)
    next(csvreader)  

    for row in tqdm(csvreader, total=total_lines, desc="Processing"):
        conentent = 'The drug name is ' + row[0] + " and the Question is " + row[1] + "."
        # print("conentent:", conentent)
        input = prompt + conentent
    
        messages = [{"role": "user", "content": input}]
        inputs = tokenizer(tokenizer.apply_chat_template(messages, tokenize=False,add_generation_prompt=True), return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=32)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        output_rows.append([row[0], row[1], answer])

    output_df = pd.DataFrame(output_rows, columns=["drug", "question", "answer"])
    output_df.to_csv("DTA_Huatuo_pred.csv", index=False)
    print("Saved.csv")
