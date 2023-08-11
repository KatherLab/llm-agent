
import sqlite3
import os
import re
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append('generator/')
from config import csv_path
import pandas as pd

# Initialization
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append('generator/')
task_list = pd.read_csv(csv_path)
conn = sqlite3.connect(os.path.join(script_dir, "GPT4_summaries.db"))
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Summaries (
        id INTEGER PRIMARY KEY,
        model TEXT,
        task_index TEXT,
        eu_prompt TEXT,
        repetition_index INTEGER,
        truncation_index INTEGER,
        table_index INTEGER,
        file_path TEXT,
        summary TEXT UNIQUE,
        main_ideas TEXT,
        accuracy INTEGER,
        relevance INTEGER,
        novelty INTEGER,
        specificity INTEGER,
        feasibility INTEGER
    )
''')
conn.commit()

def parse_md_file(file_path):
    print(file_path)
    with open(file_path, 'r') as file:
        file_content = file.read()
    section_pattern = re.compile(r"(?<=## Summary table by gpt-4)(.*?)(?=##|$)", re.DOTALL)
    match = section_pattern.search(file_content)
    if match:
        summary_data = re.split(r'\n\n|\n(?=[A-Z])', match.group().strip())
        summary = summary_data[1].strip()
        main_ideas = summary_data[2].replace('Main Ideas: ', '').strip()
        def process_score(score_str):
            score_str = score_str.strip()
            return float(re.search(r"\d+(\.\d+)?", score_str).group())
        accuracy = process_score(summary_data[3])
        relevance = process_score(summary_data[4])
        novelty = process_score(summary_data[5])
        specificity = process_score(summary_data[6])
        feasibility = process_score(summary_data[7])
        return [summary, main_ideas, accuracy, relevance, novelty, specificity, feasibility]
    return None

def populate_db(folder_path, model, conn):
    #files = [f for f in os.listdir(folder_path) if f.endswith(".md")] # include all files
    files = [f for f in os.listdir(folder_path) if f.endswith(".md") and f.rsplit('_', 1)[-1] == '0.md'] # only include 0.md files, discard repititions

    for file in files:
        file_path = os.path.join(folder_path, file)
        summary_data = parse_md_file(file_path)
        if summary_data:
            model = file.split("/")[-1].split("_")[0]
            truncation_index = file.split("/")[-1].split("_")[1].split("-")[-1]
            task_index = file.split("/")[-1].split("_")[2]
            row = task_list.loc[task_list['index'] == int(task_index)].iloc[0]
            eu_prompt = row['Prompt*']
            repetition_index = file.split("/")[-1].split("_")[-1].split(".")[-2]
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO Summaries (
                        model, task_index, eu_prompt, repetition_index, truncation_index, table_index, file_path, summary, main_ideas, accuracy, relevance, novelty, specificity, feasibility
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (model, task_index, eu_prompt, repetition_index, truncation_index, 0, file_path, *summary_data))
                conn.commit()
            except sqlite3.IntegrityError:
                pass

def update_db(base_path, conn):
    models = os.listdir(base_path)
    for model in models:
        folder_path = os.path.join(base_path, model)
        populate_db(folder_path, model, conn)

base_path = os.path.join(script_dir, "../generator/results")
assert os.path.exists(base_path), "Directory does not exist"
update_db(base_path, conn)