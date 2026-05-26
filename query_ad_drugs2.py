import argparse
import asyncio
import nest_asyncio
nest_asyncio.apply()
import os
import logging
import numpy as np
from openai import AsyncOpenAI
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

API_KEY = "**********************************"
BASE_URL = "******************"

async_client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, timeout=600)


async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
    model_name = kwargs.get("model", None)
    if model_name is None:
        try:
            model_name = kwargs["hashing_kv"].global_config["llm_model_name"]
        except:
            model_name = "llama-3.1-70b-instruct"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    response = await async_client.chat.completions.create(
        model=model_name,
        messages=messages,
    )
    return response.choices[0].message.content


async def embedding_func(texts):
    response = await async_client.embeddings.create(
        model="nomic-embed-text-v1.5",
        input=texts,
    )
    return np.array([dp.embedding for dp in response.data], dtype=np.float32)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--working_dir", type=str, required=True)
    parser.add_argument("--model", type=str, default="llama-3.1-70b-instruct")
    parser.add_argument("--mode", type=str, default="mix")
    return parser.parse_args()


async def initialize_rag(working_dir, model):
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)

    rag = LightRAG(
        chunk_token_size=8000,
        working_dir=working_dir,
        llm_model_func=llm_model_func,
        llm_model_name=model,
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8000,
            func=embedding_func,
        ),
    )
    return rag


QUERY = """For Alzheimer's disease, provide a comprehensive list of top 30 to 50 drugs that are currently approved, in clinical trials, or under active investigation. For each drug, include: drug name, generic name, drug class, mechanism of action, development stage (FDA Approved / Phase 3 / Phase 2 / Phase 1), biological target, indication, manufacturer, and supporting references or evidence."""


def main():
    args = parse_args()

    print("Initializing UniD3 RAG system...")
    rag = asyncio.run(initialize_rag(args.working_dir, args.model))

    print("Querying...")
    answer = rag.query(QUERY, param=QueryParam(mode=args.mode))

    print("\n" + "=" * 80)
    print("RAW ANSWER:")
    print("=" * 80)
    print(answer)

    output_file = "raw_answer.txt"
    with open(output_file, "w") as f:
        f.write(answer)
    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    main()
