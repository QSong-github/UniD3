# UniD3: LLM-driven Drug-Disease Dataset Construction via KG-RAG


### QA with UniD3
   (1) [Geneformer](https://huggingface.co/ctheodoris/Geneformer)
   ```bash
   # entering the code directory
   $ cd ./benchmark/Geneformer-finetuing-lora-prompt_cell_cls/
   ```

### Dataset Usage
   (1) [Geneformer](https://huggingface.co/ctheodoris/Geneformer)
   ```bash
   # entering the code directory
   $ cd ./benchmark/Geneformer-finetuing-lora-prompt_cell_cls/
   # creating dataset
   $ python dataset_making.py
   # generating fixed embedding
   $ python get_ebd.py
   # train and test by fixed embedding
   $ python benchmarking_main_EBD.py
   # train and test by fine-tuning with LORA
   $ python benchmarking_main_FT.py
   ```
   
   (2) [DDM](https://github.com/deeplearningplus/tGPT)
   ```bash
   $ import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ df = pd.read_csv("hf://datasets/Mike2481/UniD3_DDM/DDM.csv")
   ```

   (3) [DEA](https://github.com/snap-stanford/uce)
   ```bash
   $ import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ df = pd.read_csv("hf://datasets/Mike2481/UniD3_DDM/DDM.csv")
   ```
   
   (4) [DTA](https://github.com/TencentAILabHealthcare/scBERT)
   ```bash
   $ import pandas as pd
   # Login using e.g. `huggingface-cli login` to access this dataset
   $ df = pd.read_csv("hf://datasets/Mike2481/UniD3_DDM/DDM.csv")
   ```
