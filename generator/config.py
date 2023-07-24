import openai
import os

api_key = openai.api_key = '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'
# Get the directory that the current script is in
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the CSV file
csv_path = os.path.join(script_dir, "llm_task_list.csv")

# Define the output directory
output_dir = os.path.join(script_dir, "results/")