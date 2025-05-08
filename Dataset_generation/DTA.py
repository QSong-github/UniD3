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

WORKING_DIR = "/UniD3/KG_building_level2/level2_T3_70B"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def initialize_rag():
    rag = LightRAG(
        chunk_token_size=8000,
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="llama3.3:70B",
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




def clean_node_ids(df, column='node'):
    return set(df[column].str.replace('"', '', regex=False).str.upper())


def extract_qa(text):
    q_match = re.search(r'Question:\s*(.+?)(?=\n|Answer:|$)', text, re.DOTALL | re.IGNORECASE)
    a_match = re.search(r'Answer:\s*(.+)', text, re.DOTALL | re.IGNORECASE)

    question = q_match.group(1).strip() if q_match else ""
    answer = a_match.group(1).strip() if a_match else ""

    return question, answer


def main():
    prompt = """In a task named Drug-Target Analysis (Map the genes and pathways targeted by [specific drug]). 
    Now I give you a drug name, and you give a pair of questions and answers about this drug in the current task.
    The questions and answers need to include how these targets relate to [specific disease] and evaluate whether the drug's mechanism of action is consistent with the underlying biology of the disease.
    To keep it simple, please make sure your response contains only two parts: Question and Answer.

    Here is an example:
    The drug name is OMADACYCLINE

    Question: How effective is Omadacycline for treating acute bacterial skin and skin structure infections (ABSSSI)?
    Answer: Omadacycline is highly effective for treating ABSSSI. Clinical trials (OASIS-1 and OASIS-2) demonstrated its efficacy, showing similar success rates to linezolid in both early clinical response and overall outcomes. It interacts strongly with bacterial ribosomal subunits to inhibit protein synthesis, and is effective against drug-resistant bacteria like MRSA. Omadacycline has a comparable safety profile to linezolid, with common side effects being mild gastrointestinal issues.

    Now, please answer the following question:
    The drug name is """

    df = pd.read_csv('/UniD3/tool/DRAG_T3_70B_output/drug_entities.csv')
    drug_list = clean_node_ids(df, 'id')
    print("Drug list length:", len(drug_list))
    processed_drugs = set()
    csv_file = "DTA4.csv"
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        processed_drugs = set(existing_df['drug'].tolist())
    output_rows = []
    write_header = not os.path.exists(csv_file)
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    print("\nStarting Mix Search:")
    
    for drug in tqdm(drug_list):
        if drug in processed_drugs:
            continue  

        try:
            input = prompt + drug
            output = rag.query(input, param=QueryParam(mode="mix"))
            print(output)

            question, answer = extract_qa(output)
            output_rows.append([drug, question, answer])

            pd.DataFrame([[drug, question, answer]], columns=["drug", "question", "answer"]).to_csv(
                csv_file, mode='a', index=False, header=write_header
            )
            write_header = False  
        except Exception as e:
            print(f"Error processing {drug}: {e}")




if __name__ == "__main__":
    main()