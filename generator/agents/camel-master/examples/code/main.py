# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
import pandas as pd
from colorama import Fore

from camel.societies import RolePlaying
from camel.typing import TaskType
from camel.utils import print_text_animated
import sys
sys.path.append('generator/')
from config import api_key, output_dir, csv_path, num_iterations, truncate_interval
# insert api key into os environment
import os
LLM_MODEL = "gpt4"
if api_key:
    os.environ['OPENAI_API_KEY'] = api_key

def main(num_iterations, task_index, repetition_index, model_type=None) -> None:
    task_list = pd.read_csv(csv_path)
    row = task_list.loc[task_list['index'] == int(task_index)].iloc[0]
    eu_prompt = row['Prompt*']
    task_prompt = eu_prompt
    #language = "JavaScript"
    domain = "evaluating EU health policy"
    meta_dict = {"domain": domain}
    role_play_session = RolePlaying(
        assistant_role_name=f"Medical advisor.",
        assistant_agent_kwargs=dict(model=model_type),
        user_role_name=f"Person working in {domain}",
        user_agent_kwargs=dict(model=model_type),
        task_prompt=task_prompt,
        with_task_specify=True,
        task_specify_agent_kwargs=dict(model=model_type),
        task_type=TaskType.CODE,
        extend_sys_msg_meta_dicts=[meta_dict, meta_dict],
        extend_task_specify_meta_dict=meta_dict,
    )

    print(
        Fore.GREEN +
        f"AI Assistant sys message:\n{role_play_session.assistant_sys_msg}\n")
    print(Fore.BLUE +
          f"AI User sys message:\n{role_play_session.user_sys_msg}\n")

    print(Fore.YELLOW + f"Original task prompt:\n{task_prompt}\n")
    print(
        Fore.CYAN +
        f"Specified task prompt:\n{role_play_session.specified_task_prompt}\n")
    print(Fore.RED + f"Final task prompt:\n{role_play_session.task_prompt}\n")

    chat_turn_limit, n = num_iterations, 0
    input_assistant_msg, _ = role_play_session.init_chat()
    count = 0
    txt_path = os.path.join(output_dir, f"camel-{LLM_MODEL}/camel-{LLM_MODEL}_trunc-0_{task_index}_{repetition_index}.txt")
    txt_filename = txt_path
    sys.stdout = open(txt_filename, 'a', encoding='utf-8')
    while n < chat_turn_limit:
        if count !=0 and count % truncate_interval == 0:
            sys.stdout.close()
            txt_path = os.path.join(output_dir, f"camel-{LLM_MODEL}/camel-{LLM_MODEL}_trunc-{int(count/truncate_interval)}_{task_index}_{repetition_index}.txt")
            txt_filename = txt_path
            sys.stdout = open(txt_filename, 'a', encoding='utf-8')
        n += 1
        assistant_response, user_response = role_play_session.step(
            input_assistant_msg)

        input_assistant_msg = assistant_response.msg

        if assistant_response.terminated:
            print(Fore.GREEN +
                  ("AI Assistant terminated. Reason: "
                   f"{assistant_response.info['termination_reasons']}."))
            break
        if user_response.terminated:
            print(Fore.GREEN +
                  ("AI User terminated. "
                   f"Reason: {user_response.info['termination_reasons']}."))
            break

        print_text_animated(Fore.BLUE +
                            f"AI User:\n\n{user_response.msg.content}\n")
        print_text_animated(Fore.GREEN + "AI Assistant:\n\n"
                            f"{assistant_response.msg.content}\n")

        if "CAMEL_TASK_DONE" in user_response.msg.content:
            break


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
    # Call main function
    main(num_iterations, task_index, repetition_index)
