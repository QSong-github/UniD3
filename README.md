# $\text{Uni}D^3$: Open Knowledge Graphs and QA Benchmarks for Drug–Disease Discovery and Reasoning


### Overview

Drug--disease knowledge underpins drug discovery and precision medicine, yet most of it is locked in unstructured PubMed articles and only partially captured by curated databases. We release UniD
-KG, a suite of six knowledge graphs spanning three tasks (Drug--Disease Matching, DDM; Drug Effectiveness Assessment, DEA; and Drug--Target Analysis, DTA), and UniD
-data, three open QA datasets (
 DDM, 
 DEA and 
 DTA pairs), distilled from 
 PubMed articles with Llama-3.3-70B by the UniD
 KG-RAG pipeline, which couples task-specific prompting with a dual-stage entity extraction that re-extracts over the consolidated graph to recover cross-chunk and cross-document evidence. External validation on CDR, DrugReviews, P3ps and MedicationQA and a benchmark across seven LLM baselines and three retrieval variants show that UniD
-data is faithful to curated sources and that retrieval over UniD
-KG consistently improves biomedical QA; a blinded clinician review of 
 FDA-approved, US-marketed drugs further confirms strong agreement with the UniD
-data DDM split (accuracy 
, F1 
, AUROC 
). All artefacts---UniD
-KG, UniD
-data, benchmark scripts and the UniD
-QA explainable chatbot---are released as shared infrastructure for biomedical NLP and drug repurposing. The generated KGs and vector database are stored in [zenodo](https://zenodo.org/records/15368180). In addition, the UniD3 web [chatbot](https://unid3.site/) provides interactive access to the UniD3-generated datasets, enabling users to explore and query the resources.

![The workflow of Uni$D^3$](unid3.png)


### UniD3 QA （under [LightRAG](https://github.com/HKUDS/LightRAG) framework（required lightrag-hku==1.1.0））
   ```bash
   # Please download the generated knowledge graph from zenodo before using UniD3 QA. 
   # Please specify the specific working path, large language model and RAG mode.
   $ conda env create -f UniD3_environment.yaml
   # run ollama before here
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
