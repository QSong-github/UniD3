import pandas as pd
from bert_score import score
import torch


df = pd.read_csv('/blue/qsong1/wang.qing/LightRAG-main/Evaluation/drug_reviews_DEA/DR_fuzzy_ineff.csv')


disease_list = df['disease'].tolist()
tail_disease_list = df['condition'].tolist()


device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")


def compute_bertscore_average(disease_list, tail_disease_list, device):
    precision, recall, f1 = score(disease_list, tail_disease_list, lang="en", device=device, verbose=True)
    avg_precision = precision.mean().item()
    avg_recall = recall.mean().item()
    avg_f1 = f1.mean().item()
    return avg_precision, avg_recall, avg_f1

avg_precision, avg_recall, avg_f1 = compute_bertscore_average(disease_list, tail_disease_list, device)
print(f"ineff Average Precision: {avg_precision}")
print(f"ineff Average Recall: {avg_recall}")
print(f"ineff Average F1 Score: {avg_f1}")




df = pd.read_csv('/UniD3/Evaluation/drug_reviews_DEA/DR_fuzzy_eff.csv')


disease_list = df['disease'].tolist()
tail_disease_list = df['condition'].tolist()


device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")


def compute_bertscore_average(disease_list, tail_disease_list, device):
    precision, recall, f1 = score(disease_list, tail_disease_list, lang="en", device=device, verbose=True)
    avg_precision = precision.mean().item()
    avg_recall = recall.mean().item()
    avg_f1 = f1.mean().item()
    return avg_precision, avg_recall, avg_f1

avg_precision, avg_recall, avg_f1 = compute_bertscore_average(disease_list, tail_disease_list, device)
print(f"eff Average Precision: {avg_precision}")
print(f"eff Average Recall: {avg_recall}")
print(f"eff Average F1 Score: {avg_f1}")