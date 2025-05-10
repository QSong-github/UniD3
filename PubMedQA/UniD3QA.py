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

WORKING_DIR = "/blue/qsong1/wang.qing/LightRAG-main/KG_building_level2/level2_T1_70B"

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
    output_rows = []
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    print("\nStarting Mix Search:")

    with open('/blue/qsong1/wang.qing/LightRAG-main/PubMedQA/matched_questionsDDM.csv', mode='r', encoding='utf-8-sig') as infile:
        csvreader = csv.reader(infile)
        
        for row in tqdm(csvreader, desc="Processing"):
            conentent = 'Question: ' + row[1] + " Context " + row[2] 
            prompt =  conentent + 'Just answer YES or NO.'
            # print("conentent:", conentent)
            input = conentent + prompt
            answer = rag.query(input, param=QueryParam(mode="mix"))

            output_rows.append([row[1], row[4], answer])

    output_df = pd.DataFrame(output_rows, columns=["question", 'gt',"answer"])
    output_df.to_csv("UniD3QA_output_DDM.csv", index=False)
    print("Saved.csv")




if __name__ == "__main__":
    main()