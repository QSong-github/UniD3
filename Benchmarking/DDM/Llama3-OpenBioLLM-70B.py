import transformers
import torch
import re
import pandas as pd
from tqdm import tqdm
import csv



model_id = "aaditya/OpenBioLLM-Llama3-70B"


tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)

model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map=0 if torch.cuda.is_available() else -1,  
    load_in_8bit=True, 
)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
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
        messages = [{"role": "user", "content":input}]

        prompt = pipeline.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
        )
        outputs = pipeline(
            prompt,
            max_new_tokens=32,
            do_sample=True,
            temperature=0.1,
            top_p=0.9,
        )

        answer = outputs[0]["generated_text"]
        output_rows.append([row[0], answer])
        

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease"])
    output_df.to_csv("DDM_OpenBioLLM_pred.csv", index=False)
    print("Saved.csv")

