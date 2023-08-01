import openai
import os





# Get the directory that the current script is in
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to the CSV file
csv_path = os.path.join(script_dir, "llm_task_list.csv")

key_file = os.path.join(script_dir, "API_KEY")

# Define the output directory
output_dir = os.path.join(script_dir, "results/")

def read_openai_api_key():
    try:
        with open(key_file, 'r') as f:
            api_key = f.read().splitlines()[0]
            return api_key
    except FileNotFoundError:
        print("API_KEY file not found.")
        return None
def read_bard_token():
    try:
        with open(key_file, 'r') as f:
            # read second line
            token = f.read().splitlines()[1]
            return token
    except FileNotFoundError:
        print("API_KEY file not found.")
        return None
api_key = openai.api_key = read_openai_api_key()
bard_token = read_bard_token()
#print("API_KEY:", api_key)
#print("BARD_TOKEN:", bard_token)
num_iterations = 6
truncate_interval = 2