# $\text{Uni}D^3$: Open Knowledge Graphs and QA Benchmarks for Drug–Disease Discovery and Reasoning


### Overview

Drug--disease knowledge underpins drug discovery and precision medicine, yet most of it is locked in unstructured PubMed articles and only partially captured by curated databases. We release UniD3
-KG, a suite of six knowledge graphs spanning three tasks (Drug--Disease Matching, DDM; Drug Effectiveness Assessment, DEA; and Drug--Target Analysis, DTA), and UniD3
-data, three open QA datasets (
 DDM, 
 DEA and 
 DTA pairs), distilled from 
 PubMed articles with Llama-3.3-70B by the UniD3
 KG-RAG pipeline, which couples task-specific prompting with a dual-stage entity extraction that re-extracts over the consolidated graph to recover cross-chunk and cross-document evidence. External validation on CDR, DrugReviews, P3ps and MedicationQA and a benchmark across seven LLM baselines and three retrieval variants show that UniD3
-data is faithful to curated sources and that retrieval over UniD3
-KG consistently improves biomedical QA; a blinded clinician review of 
 FDA-approved, US-marketed drugs further confirms strong agreement with the UniD3
-data DDM split (accuracy 
, F1 
, AUROC 
). All artefacts---UniD3
-KG, UniD3
-data, benchmark scripts and the UniD3
-QA explainable chatbot---are released as shared infrastructure for biomedical NLP and drug repurposing. The generated KGs, vector database, and the interactive UniD3 web chatbot will be released upon paper acceptance.

![The workflow of Uni$D^3$](unid3.png)


### UniD3 QA （under [LightRAG](https://github.com/HKUDS/LightRAG) framework（required lightrag-hku==1.1.0））
   ```bash
   # Please download the generated knowledge graph from the release archive (link to be released upon acceptance) before using UniD3 QA. 
   # Please specify the specific working path, large language model and RAG mode.
   $ conda env create -f UniD3_environment.yaml
   # run ollama before here
   $ python QA_launcher.py --working_dir "/UniD3/KG_building_level2/level2_T2_70B" --model "myllama3.3_70B" --mode "mix"
   ```



### Dataset Usage

The three QA datasets (DDM, DEA, DTA) will be released on a public dataset hub upon paper acceptance. Once available, they will be loadable via standard `pandas.read_csv` or `datasets.load_dataset` interfaces.

### Citation

### License
MIT License (anonymized for review; copyright information will be added upon paper acceptance).
