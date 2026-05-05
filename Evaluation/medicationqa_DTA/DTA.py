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
    prompt = """ Now I give you a drug name and a question of this drug. You need to rephrase the question and then give the corresponding answer.
    To keep it simple, please make sure your response contains only two parts: Paraphrased Question and Answer.

    Here is an example:
    The drug name is VALIUM and the question is How does valium affect the brain?

    Paraphrased Question: What effects does Valium have on the brain?
    Answer: Valium (diazepam) affects the brain by enhancing the activity of gamma-aminobutyric acid (GABA), a major inhibitory neurotransmitter. It binds to GABA-A receptors and increases their sensitivity to GABA, which leads to a calming effect on brain activity. This results in reduced anxiety, sedation, muscle relaxation, and anticonvulsant effects. Essentially, Valium slows down excessive neural activity in the brain, making it useful for treating anxiety, seizures, muscle spasms, and insomnia.

    Now, please answer the following question:
    """
    with open('/blue/qsong1/wang.qing/LightRAG-main/Evaluation/medicationqa_DTA/matched_drugs_from_df1.csv', mode='r', encoding='utf-8-sig') as infile:
        csvreader = csv.reader(infile)

        csv_file = "DTAeval2.csv"

        header = next(csvreader)
        output_rows = []

        rag = asyncio.run(initialize_rag())
        print("\nStarting Mix Search:")
        
        for row in tqdm(csvreader, desc="Processing"):
            conentent = 'The drug name is ' + row[1].upper() + " and the Question is " + row[0] + "."
            print("conentent:", conentent)
            input = prompt + conentent
            output = rag.query(input, param=QueryParam(mode="mix"))
            print(output)

            question, answer = extract_qa(output)
            output_rows.append([row[1].upper(), question, answer])

            pd.DataFrame([[row[1].upper(), question, answer]], columns=["drug", "question", "answer"]).to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False, encoding='utf-8-sig')





if __name__ == "__main__":
    main()