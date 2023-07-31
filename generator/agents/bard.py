import pandas as pd
from bardapi import Bard

import sys
sys.path.append('generator/')
from config import bard_token, output_dir, csv_path, truncate_interval


def main(task_index, repetition_index):
    task_list = pd.read_csv(csv_path)
    row = task_list.loc[task_list['index'] == int(task_index)].iloc[0]
    eu_prompt = row['Prompt*']
    bard = Bard(token=bard_token)
    answer = bard.get_answer(eu_prompt)['content']
    with open(f"{output_dir}/bard/bard_trunc-0_{task_index}_{repetition_index}.txt", 'w') as file:
        file.write(answer)
    print(answer)




if __name__ == "__main__":
    # Extract command line arguments. Skip the first one because it's the script name.
    args = sys.argv[1:]

    # Parse arguments
    task_index = args[args.index("--task_index") + 1] if "--task_index" in args else 1
    repetition_index = args[args.index("--repetition_index") + 1] if "--repetition_index" in args else 1
    num_iterations = args[args.index("--num_iterations") + 1] if "--num_iterations" in args else 1

    # Convert strings to integers
    task_index = int(task_index)
    repetition_index = int(repetition_index)
    num_iterations = int(num_iterations)
    # Call main function
    main(task_index=task_index, repetition_index=repetition_index)
