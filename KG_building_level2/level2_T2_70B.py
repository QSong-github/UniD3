import asyncio
import os
import inspect
import logging
import csv
import pandas as pd
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc


def combine_content(node_file, edge_file, output_file):
    node_df = pd.read_csv(node_file)
    

    edge_df = pd.read_csv(edge_file)
    

    node_content = {}
    
    for _, row in node_df.iterrows():
        node_id = row['node_id']
        content = f"entity: {node_id} "
        content += f"entity_type: {row['entity_type']} "
        content += f"entity description: {row['description']} "
        node_content[node_id] = content
    

    for _, row in edge_df.iterrows():
        source, target = row['source'], row['target']
        edge_info = f"relation weight: {row['weight']} relation: {row['description']} keywords: {row['keywords']} "
        
        if source in node_content:
            node_content[source] += edge_info + f"connected to: {target} "
        if target in node_content:
            node_content[target] += edge_info + f"connected to: {source} "
    

    for key in node_content:
        node_content[key] = node_content[key].replace('\t', ' ')
    
  
    result_df = pd.DataFrame(list(node_content.items()), columns=['node', 'content'])
    result_df.to_csv(output_file, index=False)
    return node_content


def load_processed_ids(processed_ids_file):
    if not os.path.exists(processed_ids_file):
        return set()
    
    processed_ids = set()
    with open(processed_ids_file, 'r') as f:
        reader = csv.reader(f)
        next(reader, None) 
        for row in reader:
            processed_ids.add(row[0])  
    return processed_ids


def save_processed_id(processed_ids_file, node_id):
    with open(processed_ids_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([node_id])


def D_Rag():
    WORKING_DIR = "level2_T2_70B"
    nodes_file = '/UniD3/tool/DRAG_T2_70B_output/filtered_nodes.csv'
    edges_file = '/UniD3/tool/DRAG_T2_70B_output/filtered_edges.csv'
    output_file = '/UniD3/tool/DRAG_T2_70B_output/contents.csv'
    processed_ids_file = "/UniD3/tool/DRAG_T2_70B_output/processed_ids.csv"

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

    if not os.path.exists(WORKING_DIR):
        os.mkdir(WORKING_DIR)

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
    

    processed_ids = load_processed_ids(processed_ids_file)

    batch_content = combine_content(nodes_file, edges_file, output_file)
    
    for node_id in batch_content:
        if node_id in processed_ids:
            logging.info(f"Skipping already processed node: {node_id}")
            continue  
        
        rag.insert(batch_content[node_id])

 
        save_processed_id(processed_ids_file, node_id)


if __name__ == '__main__':
    processed_ids_file = "/UniD3/tool/DRAG_T2_70B_output/processed_ids.csv"
    if not os.path.exists(processed_ids_file):
        with open(processed_ids_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["node_id"])  

    D_Rag()
