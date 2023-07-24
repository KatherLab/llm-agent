import os
import subprocess
import openai
import pandas as pd
from utils import generate_evaluation
from config import api_key, csv_path, output_dir
scoring_model = "gpt-4"
# Get the directory that the current script is in
script_dir = os.path.dirname(os.path.realpath(__file__))

# Read the task list
task_list = pd.read_csv(csv_path)

# Define the output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# recursively get all the txt files under output_dir
txt_files = []
for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file.endswith(".txt"):
             txt_files.append(os.path.join(root, file))
# Define the evaluation prompt for ChatGPT-4


for file in txt_files:
    print(file)
    model = file.split("/")[-1].split("_")[0]
    truncation_index = file.split("/")[-1].split("_")[1].split("-")[-1]
    task_index = file.split("/")[-1].split("_")[2]
    repetition_index = file.split("/")[-1].split("_")[-1].split(".")[-2]
    with open(file, 'r') as file:
        generated_text = file.read()

    # Generate the .md file (this could be replaced with an actual function call or API request)
    md_filename = f"{model}_trunc-{truncation_index}_{task_index}_{repetition_index}.md"

    row = task_list.loc[task_list['index'] == int(task_index)].iloc[0]
    eu_prompt = row['Prompt*']
    discription = row['Description']
    print(eu_prompt)
    print(discription)
    evaluation_prompt = f"""
    I will give you the output of an AI model that was prompted to provide a hypothetical approach to solve a complex question. 
    The objective objective it to {discription}. The initial prompt assigned to the AI model is {eu_prompt}.
    Please summarize this output in a table with the following columns: 
    summary (content should be three concise sentences), 
    main ideas (content should be three very short bullet points), 
    main finding (content should be three very short bullet points), 
    novelty (rate the novelty of this approach from 1 to 10), 
    feasibility (rate the feasibility of this approach from 1 to 10), 
    correctness (rate the factual correctness of the output from 1 to 10). 
    Remember that the approach was hypothetical, i.e. the AI model did not actually perform any study. 
    Do not suggest in your output that actual research was done, rather, emphasize the hypothetical idea. OK?
    """

    evaluation = generate_evaluation(openai.api_key, scoring_model, evaluation_prompt, generated_text)
    file_foldername = os.path.join(output_dir, model)
    if not os.path.exists(file_foldername):
        os.makedirs(file_foldername)
    with open(os.path.join(file_foldername, md_filename), 'w') as file:
        file.write(f"## Summary table by {scoring_model}\n")
        file.write(evaluation)