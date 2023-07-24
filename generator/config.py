import openai
import os


def read_api_key():
    try:
        with open('API_KEY', 'r') as f:
            api_key = f.read().strip()
            return api_key
    except FileNotFoundError:
        print("API_KEY file not found.")
        return None

api_key = openai.api_key = read_api_key()

# Get the directory that the current script is in
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the CSV file
csv_path = os.path.join(script_dir, "llm_task_list.csv")

# Define the output directory
output_dir = os.path.join(script_dir, "results/")