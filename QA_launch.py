import argparse
import asyncio
import nest_asyncio
nest_asyncio.apply()
import os
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description="Run LightRAG with specified parameters.")
    parser.add_argument("--working_dir", type=str, required=True, help="Working directory path.")
    parser.add_argument("--model", type=str, required=True, help="Model name.")
    parser.add_argument("--mode", type=str, required=True, help="Query mode (e.g., mix).")
    return parser.parse_args()

async def initialize_rag(working_dir, model, mode):
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    rag = LightRAG(
        chunk_token_size=8000,
        working_dir=working_dir,
        llm_model_func=ollama_model_complete,
        llm_model_name=model,
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
    args = parse_args()
    rag = asyncio.run(initialize_rag(args.working_dir, args.model, args.mode))
    print("\nStarting Search:")
    input_text = input("Enter query: ")
    answer = rag.query(input_text, param=QueryParam(mode=args.mode))
    print(answer)

if __name__ == "__main__":
    main()
