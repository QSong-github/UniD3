import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def calculate_metrics(csv_file):
    df = pd.read_excel(csv_file)

    df = df[df['Clinical use'].isin(['y', 'n'])]

    label_mapping = {'effective': 1, 'ineffective': 0}
    df['Effectiveness Label'] = df['Effectiveness Label'].map(label_mapping)

    df = df.dropna(subset=['Effectiveness Label', 'Clinical use'])

    clinical_use_mapping = {'y': 1, 'n': 0}
    y_true = df['Effectiveness Label'].tolist()
    y_pred = df['Clinical use'].map(clinical_use_mapping).tolist()


    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    auroc = roc_auc_score(y_true, y_pred)


    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"AUROC: {auroc:.4f}")


calculate_metrics('/UniD3/ClinicianEval/fda_drug_effect_by_clinician.xlsx')
