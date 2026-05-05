import asyncio
import os
import inspect
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc
import csv
from tqdm import tqdm
import pandas as pd
import re

def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text).strip()

    reference_regex = re.compile(r'(References|Reference)', re.IGNORECASE)
    match = reference_regex.search(cleaned_text)
    if match:
        cleaned_text = cleaned_text[:match.start()]

    return cleaned_text


def D_Rag():
    WORKING_DIR = "level1_T1_70B"
    done_records_path = 'DRAG_T1_70B_done_records.csv'  

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

    if not os.path.exists(WORKING_DIR):
        os.mkdir(WORKING_DIR)

    BATCH_SIZE = 20
    rag = LightRAG(
        chunk_token_size=8000,
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="myllama3.3:latest",
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
        addon_params={
            "param_name": BATCH_SIZE,
        },
    )


    batch_content = []
    batch_files = []
    processed_files = set()


    if os.path.exists(done_records_path):
        df_done = pd.read_csv(done_records_path)
        processed_files.update(df_done.iloc[:, 0].tolist())


    csv_file_path = 'fuzzy_match_llm4classification.csv' 


    df = pd.read_csv(csv_file_path)


    for drug in tqdm(df['Drug Disease Matching_Closest'], desc="LightRAG indexing"):
        paper_path = f'/UniD3/txt_files/{drug}'  

        if paper_path in processed_files:
            print(f"File {paper_path} already processed. Skipping...")
            continue

        try:
            with open(paper_path, "r", encoding="utf-8") as f:
                content = f.read()
                cleaned_content = clean_text(content)
                batch_content.append(cleaned_content)
                batch_files.append(paper_path)

  
            if len(batch_content) >= BATCH_SIZE:
                rag.insert(batch_content)

                with open(done_records_path, "a", encoding="utf-8", newline='') as done_f:
                    writer = csv.writer(done_f)
                    for file in batch_files:
                        writer.writerow([file])
                        processed_files.add(file)

                batch_content = []
                batch_files = []

        except FileNotFoundError:
            print(f"File {paper_path} not found. Skipping...")
        except Exception as e:
            print(f"An error occurred with file {paper_path}: {e}")

    if batch_content:
        rag.insert(batch_content)
        with open(done_records_path, "a", encoding="utf-8", newline='') as done_f:
            writer = csv.writer(done_f)
            for file in batch_files:
                writer.writerow([file])
                processed_files.add(file)


if __name__ == '__main__':
    D_Rag()