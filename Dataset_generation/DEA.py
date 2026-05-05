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





def clean_node_ids(df, column='node'):
    return set(df[column].str.replace('"', '', regex=False).str.upper())


def extract_info_from_answer(answer):
    try:
        effective = re.findall(r"Effectively treated diseases: \[(.*?)\]", answer)
        ineffective = re.findall(r"Diseases with ineffective treatment.*?: \[(.*?)\]", answer)
        explanation = re.findall(r"Explanation:\s*(.*)", answer, re.DOTALL)

        effective_list = [d.strip() for d in effective[0].split(',')] if effective else []
        ineffective_list = [d.strip() for d in ineffective[0].split(',')] if ineffective else []
        explanation_text = explanation[0].strip() if explanation else ""

        return effective_list, ineffective_list, explanation_text
    except Exception as e:
        print("Parsing failed:", e)
        return [], [], ""

def main():
    prompt = """In a task named Drug Effectiveness Assessment (Evaluate the effectiveness of [specific drug] for treating [specific disease]. 
    Now I give you a drug name, and you answer what disease it can treat or cannot treat. Then give brief explanations.
    Include an analysis of clinical or preclinical data, the strength of the drug’s interaction with its target genes or pathways, and any evidence of therapeutic outcomes.
    To keep it simple, please make sure your response contains only three parts: the list of Effectively treated diseases, list of Diseases with ineffective treatment or unclear efficacy and a brief Explanation.

    Here is an example:
    The drug name is OMADACYCLINE

    Effectively treated diseases: [Community-Acquired Bacterial Pneumonia, CABP, Acute Bacterial Skin and Skin Structure Infections (ABSSSI)]
    Diseases with ineffective treatment or unclear efficacy: [Urinary Tract Infections (UTIs), Bacterial Meningitis]
    Explanation: The drug is effective against CABP and ABSSSI due to its strong binding affinity to bacterial ribosomes, inhibiting protein synthesis. Clinical trials have shown significant improvement in patients with these infections. However, its efficacy in treating UTIs and bacterial meningitis is unclear due to limited data and potential resistance mechanisms.

    Now, please answer the following question:
    The drug name is """

    df = pd.read_csv('/UniD3/tool/DRAG_T2_70B_output/drug_entities.csv')
    drug_list = clean_node_ids(df, 'id')
    print("Drug list length:", len(drug_list))

    output_rows = []
    # Initialize RAG instance
    rag = asyncio.run(initialize_rag())
    print("\nStarting Mix Search:")

    for drug in tqdm(drug_list):
        input = prompt + drug
        answer = rag.query(input, param=QueryParam(mode="mix"))

        effective_list, ineffective_list, explanation = extract_info_from_answer(answer)

        for disease in effective_list:
            output_rows.append([drug, disease, "effective", explanation])

        for disease in ineffective_list:
            output_rows.append([drug, disease, "ineffective", explanation])

    output_df = pd.DataFrame(output_rows, columns=["drug", "disease", "label", "explanation"])
    output_df.to_csv("DEA.csv", index=False)
    print("Saved.csv")




if __name__ == "__main__":
    main()