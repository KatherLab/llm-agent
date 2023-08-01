import os
import sys
sys.path.append('generator/')
from config import api_key, output_dir, csv_path, truncate_interval
from api import cot
import pandas as pd

def cot_main(output_dir, repetition_index, task_index):
    task_list = pd.read_csv(csv_path)
    row = task_list.loc[task_list['index'] == int(task_index)].iloc[0]
    eu_prompt = row['Prompt*']
    print("working on cot ", row['index'], repetition_index, 'done')
    cot(method="zero_shot_cot", question=eu_prompt, output_dir = output_dir, task_index = task_index, repetition_index = repetition_index)
    cot(method="manual_cot", question=eu_prompt, output_dir = output_dir, task_index = task_index, repetition_index = repetition_index)
    cot(method="auto_cot", question=eu_prompt, output_dir = output_dir, task_index = task_index, repetition_index = repetition_index)

if __name__ == "__main__":
    # Extract command line arguments. Skip the first one because it's the script name.
    args = sys.argv[1:]
    print(args)
    # Parse arguments
    task_index = args[args.index("--task_index") + 1] if "--task_index" in args else 1
    repetition_index = args[args.index("--repetition_index") + 1] if "--repetition_index" in args else 1
    num_iterations = args[args.index("--num_iterations") + 1] if "--num_iterations" in args else 1
    num_iterations = int(num_iterations)

    # Convert strings to integers
    task_index = int(task_index)
    repetition_index = int(repetition_index)

    # Call main function
    cot_main(output_dir, repetition_index = repetition_index, task_index=task_index)