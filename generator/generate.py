import os
import subprocess
from generator.config import api_key
import pandas as pd
from generator.utils import generate_evaluation
import openai
# Read the task list
task_list = pd.read_csv("llm_task_list.csv")

# Define the output directory
output_dir = "results/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Define the evaluation prompt for ChatGPT-4

ll_agi_model_list = ["gpt-3.5-turbo"] #"gpt-4",
babyagi_script = os.path.join(os.getcwd(), "agents/babyagi/babyagi.py")
# For each task
for index, row in task_list.iterrows():
    # For each repetition
    for model in ll_agi_model_list:
        for repetition_index in range(3):
            # Define the prompt
            eu_prompt = row['Prompt*']

            system_prompt = "You are a medical advisor."
            input_text = eu_prompt
            generated_text = generate_evaluation(api_key, model, system_prompt, input_text)
            print("working on", model, row['index'], repetition_index)
            # Write the generated text to a .txt file
            txt_filename = f"{model}/{model}_trunc-0_{row['index']}_{repetition_index}.txt"
            with open(os.path.join(output_dir, txt_filename), 'w') as file:
                file.write(generated_text)

            # call python generator/babyagi/babyagi.py
            # TODO: put gpt4 into babyagi, but this would be expensive
            subprocess.run(["python", babyagi_script, "--task_index", str(row['index']), "--repetition_index", str(repetition_index)])#, "--model", model

