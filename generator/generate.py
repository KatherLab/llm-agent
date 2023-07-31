import os
import subprocess
import sys
sys.path.append('..')
script_dir = os.path.dirname(os.path.realpath(__file__))

from config import api_key, csv_path, output_dir, num_iterations
import pandas as pd
from utils import generate_evaluation
import openai

# Read the task list
task_list = pd.read_csv(csv_path)


if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Define the evaluation prompt for ChatGPT-4

ll_agi_model_list = ["gpt-3.5-turbo", "gpt-4"] #"gpt-4",
babyagi_script = os.path.join(script_dir, "agents/babyagi/babyagi.py")
camel_script = os.path.join(script_dir, "agents/camel-master/examples/code/main.py")
cot_script = os.path.join(script_dir, "agents/auto-cot-main/cot_main.py")
bard_script = os.path.join(script_dir, "agents/bard.py")

task_list = task_list[4:6]
# For each task
for index, row in task_list.iterrows():
    # For each repetition

    for repetition_index in range(3):

        for model in ll_agi_model_list:
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
        subprocess.run(["python", babyagi_script, "--task_index", str(row['index']), "--repetition_index", str(repetition_index), "--num_iterations", str(num_iterations)])#, "--model", model
        print('working on babyagi ', row['index'], repetition_index, 'done')

        subprocess.run(["python", camel_script, "--task_index", str(row['index']), "--repetition_index", str(repetition_index), "--num_iterations", str(num_iterations)])#, "--model", model
        print('working on camel ', row['index'], repetition_index, 'done')

        #print("python", cot_script, "--task_index", str(row['index']), "--repetition_index", str(repetition_index), "--num_iterations", str(num_iterations))
        subprocess.run(["python", cot_script, "--task_index", str(row['index']), "--repetition_index", str(repetition_index)])#, "--model", model
        print('working on cot ', row['index'], repetition_index, 'done')

        subprocess.run(["python", bard_script, "--task_index", str(row['index']), "--repetition_index", str(repetition_index)])#, "--model", model
        print('working on bard ', row['index'], repetition_index, 'done')

        # llama2 7b chat model enabled, dependent on another repo
        # TODO: integrate llama2 7b chat model, potentially llama2 13b and 70b
