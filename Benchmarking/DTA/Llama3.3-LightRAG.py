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

WORKING_DIR = "/blue/qsong1/wang.qing/LightRAG-main/KG_building_level2/level2_T2_70B"

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
    prompt = """In a task named Drug-Target Analysis (Identify potential diseases that could be treated by [specific Drug]. For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism.). 
    I will give you a drug name and the drug-related Question, and you need to give an Answer of this Question.
    To keep it simple, please just give the Answer, nothing else.

    Here is an example:
    The drug name is OMADACYCLINE and the Question is "What are the primary gene targets of Omadacycline in treating community-acquired bacterial pneumonia (CABP), and how do these targets relate to the disease's underlying biology?".

    Answer: "The primary gene targets of Omadacycline in treating CABP are the bacterial ribosomal subunits, specifically the 30S and 50S subunits. By binding to these subunits, Omadacycline inhibits protein synthesis in bacteria, ultimately leading to their death. This mechanism is consistent with the underlying biology of CABP, as it targets the fundamental process of bacterial growth and replication, which is essential for the progression of the disease. Additionally, Omadacycline's broad-spectrum activity against various bacterial pathogens, including those resistant to other antibiotics, makes it an effective treatment option for CABP, where timely and effective treatment is crucial to prevent severe outcomes."

    Now, please answer the following question:

    """

    output_rows = []
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    print("\nStarting Mix Search:")

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
            answer = rag.query(input, param=QueryParam(mode="local"))

            output_rows.append([row[0], row[1], answer])

    output_df = pd.DataFrame(output_rows, columns=["drug", "question", "answer"])
    output_df.to_csv("DTA_LlamaLightRAG_pred.csv", index=False)
    print("Saved.csv")




if __name__ == "__main__":
    main()