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

WORKING_DIR = "/UniD3/KG_building_level2/level2_T1_70B"

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



def clean_node_ids(df, column='node'):
    return set(df[column].str.replace('"', '', regex=False).str.upper())


def extract_info_from_answer(text):
    summary_match = re.search(r'Drug summary:\s*(.+?)(?=\n[A-Z]|$)', text, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""

    disease_pattern = re.compile(
        r'Name:\s*(.+?)\s*Explanation:\s*(.+?)(?=\nName:|\Z)', re.DOTALL)
    
    diseases = []
    for match in disease_pattern.findall(text):
        name = match[0].strip()
        explanation = match[1].strip().rstrip("]")
        diseases.append((name, explanation))

    return summary, diseases

def main():
    prompt = """In a task named Drug-Disease Matching. Identify potential diseases that could be treated by a [specific Drug]. 
    Now I give you the name of a drug and you respond by giving some diseases that the drug can treat or relieve. Then give brief explanations.
    For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism in the explanation.
    To keep it simple, please make sure your response contains only two parts: the first is the drug summary, followed by a list of some drugs (those with proven efficacy and some under investigation) and their corresponding explanations.

    Here is an example:
    The drug name is OMADACYCLINE

    Drug summary: Omadacycline is a novel aminomethylcycline antibiotic used to treat several bacterial infections. Its primary mechanism involves binding to the 30S ribosomal subunit of bacteria, inhibiting protein synthesis and preventing bacterial growth.
    Diseases 1 
    Name: Community-Acquired Bacterial Pneumonia, CABP
    Explanation: Omadacycline inhibits protein synthesis in Streptococcus pneumoniae, limiting bacterial proliferation in the lungs.
    Diseases 2
    Name: Acute Bacterial Skin and Skin Structure Infections (ABSSSI)]
    Explanation: It targets Staphylococcus aureus (including MRSA), stopping bacterial growth in skin and soft tissues.
    Diseases 3
    Name: Urinary Tract Infections (UTI) (under investigation)
    Explanation: It suppresses Escherichia coli protein production, reducing bacterial colonization in the urinary tract.

    
    Now, please answer the following question:
    The drug name is """

    df = pd.read_csv('/UniD3/tool/DRAG_T1_70B_output/drug_entities.csv')
    drug_list = clean_node_ids(df, 'id')
    print("Drug list length:", len(drug_list))

    processed_drugs = set()
    csv_file = "DDM.csv"
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
        input_text = prompt + drug
        answer = rag.query(input_text, param=QueryParam(mode="mix"))

        summary, diseases = extract_info_from_answer(answer)

        for disease_name, explanation in diseases:
            output_rows.append([drug, disease_name, explanation, summary])
            pd.DataFrame([[drug, disease_name, explanation, summary]], columns=["drug", "disease", "explanation", "summary"]).to_csv(
                csv_file, mode='a', index=False, header=write_header
            )
            write_header = False  




if __name__ == "__main__":
    main()