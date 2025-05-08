import asyncio
import nest_asyncio
import pandas as pd
nest_asyncio.apply()
import os
import re
import csv
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc
from tqdm import tqdm

WORKING_DIR = "/UniD3/KG_building_level2/level2_T2_70B"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    rag = LightRAG(
        chunk_token_size=8000,
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="myllama3.3_70B",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8000,
            func=lambda texts: ollama_embedding(
                texts, embed_model="nomic-embed-text", host="http://localhost:11434"
            ),
        ),
    )


    return rag






def main():
    prompt = """In a task named Drug-Disease Matching (Identify potential diseases that could be treated by [specific Drug]). 
    I will give you a drug name, and you need to list several diseases that have a positive association with this drug.
    To keep it simple, please just answer with the disease names, nothing else.

    Here is an example:
    The drug name is CEFTAZIDIME-AVIBACTAM.

    Answer: [Complicated Urinary Tract Infections (cUTI),Complicated Intra-Abdominal Infections (cIAI),Hospital-Acquired Bacterial Pneumonia (HABP)]

    Now, please answer the following question:

    """

    output_rows = []
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    print("\nStarting Mix Search:")

    with open('/UniD3/Benchmarking/DDM/DDM.csv', mode='r', encoding='utf-8-sig') as infile:
        csvreader = csv.reader(infile)

        header = next(csvreader)
        infile.seek(0)
        total_lines = sum(1 for line in infile) - 1 
        infile.seek(0)
        next(csvreader)  

        for row in tqdm(csvreader, total=total_lines, desc="Processing"):
            conentent = 'The drug name is ' + row[0] + "."

            input = prompt + conentent
            answer = rag.query(input, param=QueryParam(mode="local"))

            output_rows.append([row[0], answer])


    output_df = pd.DataFrame(output_rows, columns=["drug", "disease"])
    output_df.to_csv("DDM_LlamaLightRAG_pred.csv", index=False)
    print("Saved.csv")




if __name__ == "__main__":
    main()