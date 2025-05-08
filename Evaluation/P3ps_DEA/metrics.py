import pandas as pd
from bert_score import score
import torch

# 读取CSV文件
df = pd.read_csv('/blue/qsong1/wang.qing/LightRAG-main/Evaluation/P3ps_DEA/P3ps_fuzzy.csv')

# 提取'disease'和'tail_disease_entName'列
disease_list = df['disease'].tolist()
tail_disease_list = df['condition'].tolist()

# 检查是否有可用的GPU
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# 计算BERTScore并求平均
def compute_bertscore_average(disease_list, tail_disease_list, device):
    precision, recall, f1 = score(disease_list, tail_disease_list, lang="en", device=device, verbose=True)
    avg_precision = precision.mean().item()
    avg_recall = recall.mean().item()
    avg_f1 = f1.mean().item()
    return avg_precision, avg_recall, avg_f1

avg_precision, avg_recall, avg_f1 = compute_bertscore_average(disease_list, tail_disease_list, device)
print(f"Average Precision: {avg_precision}")
print(f"Average Recall: {avg_recall}")
print(f"Average F1 Score: {avg_f1}")
