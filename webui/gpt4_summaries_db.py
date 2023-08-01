import sqlite3
import os
import re
import sys
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append('generator/')
from config import csv_path
import pandas as pd

# Read the task list
task_list = pd.read_csv(csv_path)
# Connect to SQLite database
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
        main_finding TEXT,
        novelty INTEGER,
        feasibility INTEGER,
        correctness INTEGER
    )
''')

conn.commit()

# Regular expression patterns for parsing markdown files
section_pattern = re.compile(r"^## (.*?)$", re.MULTILINE)
table_pattern = re.compile(r"\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n(\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|\n)+", re.MULTILINE)

import re


def parse_md_file(file_path):
    """Parse a markdown file and extract the summary table data."""
    with open(file_path, 'r') as file:
        file_content = file.read()

    print("parsing ", file_path)
    section_pattern = re.compile(r"(?<=## Summary table by gpt-4)(.*?)(?=##|$)", re.DOTALL)
    match = section_pattern.search(file_content)
    if match:
        summary_data = re.split(r'\n\n|\n(?=[A-Z])', match.group().strip())
        # Extract each component of the summary
        summary = summary_data[1].replace('Summary: ', '').strip()
        main_ideas = summary_data[2].replace('Main Ideas: ', '').strip()
        main_finding = summary_data[3].replace('Main Finding: ', '').strip()

        # Processing the scores
        def process_score(score_str):
            score_str = score_str.strip()
            if '/' in score_str:  # score is a fraction
                return float(score_str.split('/')[0])  # numerator of the fraction
            if len(score_str) > 15:
                return float(score_str[0])
            if '\n' in score_str:  # score is a fraction
                return float(score_str.split('\n')[-1])
            else:  # score is a whole number
                return float(score_str)

        print(summary_data[4])
        novelty = process_score(summary_data[4].replace('Novelty: ', ''))
        feasibility = process_score(summary_data[5].replace('Feasibility: ', ''))
        correctness = process_score(summary_data[6].replace('Correctness: ', ''))

        return [summary, main_ideas, main_finding, novelty, feasibility, correctness]

    return None


def populate_db(folder_path, model, conn):
    """Populate the database with data from the markdown files in a folder."""
    files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
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
            for i in range(len(summary_data)//6):  # each summary data set contains 6 fields
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        INSERT INTO Summaries (
                            model, task_index, eu_prompt, repetition_index, truncation_index, table_index, file_path, summary, main_ideas, main_finding, novelty, feasibility, correctness
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (model, task_index, eu_prompt, repetition_index, truncation_index, i, file_path, *summary_data[i*6:i*6+6]))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass  # Skip if summary is already in the database


def update_db(base_path, conn):
    """Update the database with new files from the base directory."""
    models = os.listdir(base_path)
    print(models)
    for model in models:
        folder_path = os.path.join(base_path, model)
        populate_db(folder_path, model, conn)


# Replace with your directory path
os.path.join(script_dir, 'GPT4_summaries.db')
#base_path = os.path.join(os.getcwd(), "GPT4generated_summaries")
base_path = os.path.join(script_dir, "../generator/results")
assert os.path.exists(base_path), "Directory does not exist"
update_db(base_path, conn)
