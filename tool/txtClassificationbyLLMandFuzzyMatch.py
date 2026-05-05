import os
import csv
import ollama
import re
import pandas as pd
from rapidfuzz import process, fuzz
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def extract_titles(text):

    patterns = {
        'Drug Disease Matching': r"Drug Disease Matching: \[(.*?)\]",
        'Drug Effectiveness Assessment': r"Drug Effectiveness Assessment: \[(.*?)\]",
        'Drug Target Analysis': r"Drug Target Analysis: \[(.*?)\]"
    }
    

    extracted_titles = {}
    

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        titles = matches[0].split(',') if matches else []
        extracted_titles[key] = titles
    
    return extracted_titles

def append_to_csv(file_path, titles_dict, column_order):

    max_length = max(len(titles_dict.get(column, [])) for column in column_order)
    
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        with open(file_path, 'r+', newline='', encoding='utf-8') as check_file:
            if check_file.read() == "":
                writer.writerow(column_order)

        for i in range(max_length):
            row = [titles_dict.get(column, [''])[i] if i < len(titles_dict.get(column, [])) else '' for column in column_order]
            writer.writerow(row)


def classify():
    # The prompt for filtering paper content
    prompt4paperClass = """
    You should think as an expert in the medical field, I will give you a bunch of research paper titles. Please select the appropriate papers for the three tasks I set. You need to classify each paper title. Of course, if you think a paper does not belong to any task, you can classify it as "irrelevant". The following are the specific descriptions of the three tasks:

    Task1:
    Drug Disease Matching
    Identify potential drugs that could treat [specific disease]. For each drug, provide an analysis of its target genes and pathways and explain their relevance to the disease mechanism.

    Task2:
    Drug Effectiveness Assessment
    Evaluate the effectiveness of [specific drug] for treating [specific disease]. Include an analysis of clinical or preclinical data, the strength of the drug's interaction with its target genes or pathways, and any evidence of therapeutic outcomes.

    Task3:
    Drug Target Analysis
    Map the genes and pathways targeted by [specific drug]. Explain how these targets are implicated in [specific disease] and assess whether the drug's mechanism of action aligns with the disease's underlying biology.

    You must give the result in the following format:
    Drug Disease Matching:[title1,title2,title3,title4,...]

    Drug Effectiveness Assessment:[title1,title2,title4,title4,...]

    Drug Target Analysis:[title1,title2,title3,title4,...]

    Now think carefully and categorize these titles carefully. 
    The following are the titles that need to be categorized:

    """

    # Directory path
    dir = "/UniD3/txt_files/"
    csv_file_path = "llm4classification.csv"



    # Get all files in the directory
    paper_list = os.listdir(dir)



    batch_size = 100

    for i in tqdm(range(0, len(paper_list), batch_size), desc="Topic classification for papers"):
        batch_titles = paper_list[i:i + batch_size]

        # Get the classification results
        response = ollama.chat(
            model='myllama3.3',
            messages=[
                {
                    'role': 'user',
                    'content': f"{prompt4paperClass}\n{batch_titles}",
                },
            ]
        )
            
        msg = response['message']['content']
 

        titles = extract_titles(msg)


        column_order = ['Drug Disease Matching', 'Drug Effectiveness Assessment', 'Drug Target Analysis']

        append_to_csv(csv_file_path, titles, column_order)

    print(f"Titles have been appended to {csv_file_path}")
    
#################################################################
# classify()
#################################################################

def process_item(item, paper_list):
    if pd.isna(item) or item.strip() == '':
        return None
    else:
        result = process.extractOne(item.strip(), paper_list, scorer=fuzz.token_sort_ratio, score_cutoff=0.5)
        if result:
            closest_match = result[0]  
            return closest_match
        return None




def filter():
    dir_path = "/UniD3/txt_files/" 
    csv_file_path = "llm4classification.csv"
    output_csv_file_path = 'fuzzy_match_llm4classification.csv'  

    paper_list = os.listdir(dir_path)

    df = pd.read_csv(csv_file_path)

    columns_to_check = ['Drug Disease Matching', 'Drug Effectiveness Assessment', 'Drug Target Analysis']

    for column in columns_to_check:
        if column in df.columns:
            df[column + '_Closest'] = None

    for column in columns_to_check:
        if column in df.columns:
            items = df[column].tolist()
            with ThreadPoolExecutor() as executor:
                closest_titles = list(tqdm(executor.map(lambda item: process_item(item, paper_list), items), total=len(items), desc=f'Processing {column}'))
            df[column + '_Closest'] = closest_titles
            
    
            df = df[df[column + '_Closest'].notna()]

    df.to_csv(output_csv_file_path, index=False)

    print("Saved:", output_csv_file_path)

filter()

