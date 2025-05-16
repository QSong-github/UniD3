# $\text{Uni}D^3$: LLM-driven Drug-Disease Dataset Construction via KG-RAG


### Overview
With the rapid advancement of large language models (LLMs) in biomedicine, constructing high-quality and scalable drug-disease datasets ($D^3$) remains a significant challenge due to high annotation costs and the limited availability of structured data. To address these limitations, we propose Uni$D^3$, a unified generative framework based on Knowledge Graph Retrieval-Augmented Generation (KG-RAG) for automated $D^3$ construction.
$\text{Uni}D^3$ supports three core biomedical tasks: Drug-Disease Matching (DDM), Drug Effectiveness Assessment (DEA), and Drug-Target Analysis (DTA). Leveraging over 150,000 drug-related publications from PubMed, $\text{Uni}D^3$ employs Llama3.3-70B with carefully designed prompts to extract relational triplets.
To enhance precision and reduce noisy nodes in the KG, the $\text{Uni}D^3$ framework introduces a dual-stage entity extraction strategy that progressively builds both paper-level and KG-level entity information. This hierarchical approach improves the accuracy and consistency of the Uni$D^3$-generated datasets.
We evaluated the quality of the Uni$D^3$-generated datasets using both external datasets and expert clinical reviews. The Uni$D^3$-generated datasets achieved F1 scores exceeding 0.80 across all three tasks and a high expert validation score of 0.9005 F1 in the DDM task.
Uni$D^3$ offers significant advantages in reducing manual labor while maintaining scalability, enabling continuous dataset refinement through iterative KG updates. The code and datasets are publicly available at \url{https://github.com/QSong-github/UniD3}. The genertared KGs and vector database are stored in [zenodo](https://zenodo.org/records/15368180).

![The workflow of Uni$D^3$](unid3.png)


### UniD3 QA （under [LightRAG](https://github.com/HKUDS/LightRAG) framework）
   ```bash
   # Please download the generated knowledge graph from zenodo before using UniD3 QA. 
   # Please specify the specific working path, large language model and RAG mode.
   $ python QA_launcher.py --working_dir "/UniD3/KG_building_level2/level2_T2_70B" --model "myllama3.3_70B" --mode "mix"
   ```



### Dataset Usage  
   (1) [DDM](https://huggingface.co/datasets/Mike2481/UniD3_DDM)
   
   #### Pandas  <img src="https://pandas.pydata.org/static/img/pandas_mark.svg" alt="Pandas" width="20" />
   ```
   import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   df = pd.read_csv("hf://datasets/Mike2481/UniD3_DDM/DDM.csv")
   ```
   #### HuggingFace <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="Hugging Face" width="20" />
   ```
   from datasets import load_dataset
   # Login using e.g. `huggingface-cli login` to access this dataset
   ds = load_dataset("Mike2481/UniD3_DDM")
   ```

   (2) [DEA](https://huggingface.co/datasets/Mike2481/UniD3_DEA)

   #### Pandas  <img src="https://pandas.pydata.org/static/img/pandas_mark.svg" alt="Pandas" width="20" />
   ```
   import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   df = pd.read_csv("hf://datasets/Mike2481/UniD3_DEA/DEA.csv")
   ```
   #### HuggingFace <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="Hugging Face" width="20" />
   ```
   from datasets import load_dataset
   # Login using e.g. `huggingface-cli login` to access this dataset
   ds = load_dataset("Mike2481/UniD3_DEA")
   ```
   
   (3) [DTA](https://huggingface.co/datasets/Mike2481/UniD3_DTA)

   #### Pandas  <img src="https://pandas.pydata.org/static/img/pandas_mark.svg" alt="Pandas" width="20" />
   ```
   import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   df = pd.read_csv("hf://datasets/Mike2481/UniD3_DTA/DTA.csv")
   ```
   #### HuggingFace <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="Hugging Face" width="20" />
   ```
   from datasets import load_dataset
   # Login using e.g. `huggingface-cli login` to access this dataset
   ds = load_dataset("Mike2481/UniD3_DTA")
   ```
### Citation

### License
MIT License © Qianqian Song Lab
