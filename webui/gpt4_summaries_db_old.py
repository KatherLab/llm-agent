import sqlite3
import os
import re

# Connect to SQLite database
conn = sqlite3.connect("GPT4_summaries.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Summaries_old (
        id INTEGER PRIMARY KEY,
        model TEXT,
        task TEXT,
        run INTEGER,
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

def parse_md_file(file_path):
    """Parse a markdown file and extract the summary table data."""
    with open(file_path, 'r') as file:
        file_content = file.read()
    sections = section_pattern.split(file_content)
    summary_tables = []
    for i in range(len(sections)):
        if sections[i].strip() == "Summary table by gpt-4":
            matches = table_pattern.findall(sections[i+1])
            if matches:
                for match in matches:
                    summary_table = [group.strip() for group in match.split("|")[1:-1]]
                    summary_tables.append(summary_table)
    return summary_tables

def populate_db(folder_path, model, conn):
    """Populate the database with data from the markdown files in a folder."""
    task_pattern = re.compile(r"^.*?_(.*?)_.*$")
    run_pattern = re.compile(r".*[_-](\d{1,2})\.md$")
    files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
    for file in files:
        file_path = os.path.join(folder_path, file)
        summary_tables = parse_md_file(file_path)
        if summary_tables:
            task = task_pattern.match(file).groups()[0]
            run = int(run_pattern.match(file).groups()[0])
            for i, summary_table in enumerate(summary_tables):
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        INSERT INTO Summaries_old (
                            model, task, run, table_index, file_path, summary, main_ideas, main_finding, novelty, feasibility, correctness
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (model, task, run, i, file_path, *summary_table))
                    conn.commit()
                except sqlite3.IntegrityError:
                    pass  # Skip if summary is already in the database

def update_db(base_path, conn):
    """Update the database with new files from the base directory."""
    models = os.listdir(base_path)
    for model in models:
        folder_path = os.path.join(base_path, model)
        populate_db(folder_path, model, conn)


# Replace with your directory path
os.path.join(os.getcwd(), 'GPT4_summaries.db')
#base_path = os.path.join(os.getcwd(), "GPT4generated_summaries")
base_path = "/home/jeff/PycharmProjects/llm-agent/GPT4generated_summaries"
assert os.path.exists(base_path), "Directory does not exist"
update_db(base_path, conn)
