# UniD3: LLM-driven Drug-Disease Dataset Construction via KG-RAG


### QA with UniD3
   (1) [Geneformer](https://huggingface.co/ctheodoris/Geneformer)
   ```bash
   # entering the code directory
   $ cd ./benchmark/Geneformer-finetuing-lora-prompt_cell_cls/
   ```



### Dataset Usage  
   (1) [DDM](https://huggingface.co/datasets/Mike2481/UniD3_DDM)
   
   #### Pandas  <img src="https://pandas.pydata.org/static/img/pandas_mark.svg" alt="Pandas" width="16" />
   ```
   import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   df = pd.read_csv("hf://datasets/Mike2481/UniD3_DDM/DDM.csv")
   ```
   #### HuggingFace <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="Hugging Face" width="16" />
   ```
   from datasets import load_dataset
   # Login using e.g. `huggingface-cli login` to access this dataset
   ds = load_dataset("Mike2481/UniD3_DDM")
   ```

   #### HuggingFace <img src="https://huggingface.co/front/assets/huggingface_logo.svg" alt="Hugging Face" width="16" />
   ```
   import requests
   # Login using e.g. `huggingface-cli login` to access this dataset
   headers = build_hf_headers()  # handles authentication
   jsonld = requests.get("https://huggingface.co/api/datasets/Mike2481/UniD3_DEA/croissant", headers=headers).json()
   ds = Dataset(jsonld=jsonld)
   records = ds.records("default")
   ```






   (3) [DEA](https://huggingface.co/datasets/Mike2481/UniD3_DEA)
   ```bash
   $ import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ ds = load_dataset("Mike2481/UniD3_DEA")
   ```
   ```bash
   $ from datasets import load_dataset
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ ds = load_dataset("Mike2481/UniD3_DEA")
   ```
   
   (4) [DTA](https://huggingface.co/datasets/Mike2481/UniD3_DTA)
   ```bash
   $ import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ df = pd.read_csv("hf://datasets/Mike2481/UniD3_DTA/DTA.csv")
   ```
   ```bash
   $ from datasets import load_dataset
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ ds = load_dataset("Mike2481/UniD3_DTA")
   ```
### Citation

### License
MIT License © Qianqian Song Lab
