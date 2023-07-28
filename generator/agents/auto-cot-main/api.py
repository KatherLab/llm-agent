import argparse
import sys

from utils import *

def cot(method, question, output_dir, task_index, repetition_index):
    global method_name
    LLM_MODEL = "gpt3"
    args = parse_arguments()
    decoder = Decoder()

    args.method = method
    args.model = LLM_MODEL
    if args.method != "zero_shot_cot":
        if args.method == "auto_cot":
            args.demo_path = "generator/agents/auto-cot-main/demos/multiarith_auto"
        else:
            args.demo_path = "generator/agents/auto-cot-main/demos/multiarith_manual"
        demo = create_demo_text(args, cot_flag=True)
    else:
        demo = None
    if method == "zero_shot":
        method_name = "zero-shot"
    elif method == "zero_shot_cot":
        method_name = "zero-shot-cot"
    elif method == "manual_cot":
        method_name = "manual-cot"

    txt_path = os.path.join(output_dir, f"cot-{LLM_MODEL}-{method_name}/cot-{LLM_MODEL}-{method_name}_trunc-0_{task_index}_{repetition_index}.txt")
    txt_filename = txt_path
    sys.stdout = open(txt_filename, 'a', encoding='utf-8')

    x = "Q: " + question + "\n" + "A:"
    print('*****************************')
    print("Test Question:")
    print(question)
    print('*****************************')

    if args.method == "zero_shot":
        x = x + " " + args.direct_answer_trigger_for_zeroshot
    elif args.method == "zero_shot_cot":
        x = x + " " + args.cot_trigger
    elif args.method == "manual_cot":
        x = demo + x
    elif args.method == "auto_cot":
        x = demo + x + " " + args.cot_trigger
    else:
        raise ValueError("method is not properly defined ...")

    print("Prompted Input:")
    print(x.replace("\n\n", "\n").strip())
    print('*****************************')

    max_length = args.max_length_cot if "cot" in args.method else args.max_length_direct
    print(args)
    z = decoder.decode(args, x, max_length)
    z = z.replace("\n\n", "\n").replace("\n", "").strip()
    if args.method == "zero_shot_cot":
        z2 = x + z + " " + args.direct_answer_trigger_for_zeroshot_cot
        max_length = args.max_length_direct
        pred = decoder.decode(args, z2, max_length)
        print("Output:")
        print(z + " " + args.direct_answer_trigger_for_zeroshot_cot + " " + pred)
        print('*****************************')
    else:
        pred = z
        print("Output:")
        print(pred)
        print('*****************************')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Zero-shot-CoT")

    parser.add_argument("--max_num_worker", type=int, default=0, help="maximum number of workers for dataloader")
    parser.add_argument(
        "--model", type=str, default="gpt4", help="model used for decoding. Note that 'gpt3' are the smallest models."
    )
    parser.add_argument(
        "--method", type=str, default="auto_cot", choices=["zero_shot", "zero_shot_cot", "few_shot", "few_shot_cot", "auto_cot"], help="method"
    )
    parser.add_argument(
        "--cot_trigger_no", type=int, default=1, help="A trigger sentence that elicits a model to execute chain of thought"
    )
    parser.add_argument(
        "--max_length_cot", type=int, default=256, help="maximum length of output tokens by model for reasoning extraction"
    )
    parser.add_argument(
        "--max_length_direct", type=int, default=32, help="maximum length of output tokens by model for answer extraction"
    )
    parser.add_argument(
        "--limit_dataset_size", type=int, default=0, help="whether to limit test dataset size. if 0, the dataset size is unlimited and we use all the samples in the dataset for testing."
    )
    parser.add_argument(
        "--api_time_interval", type=float, default=1.0, help=""
    )
    parser.add_argument(
        "--temperature", type=float, default=0, help=""
    )
    parser.add_argument(
        "--log_dir", type=str, default="./log/", help="log directory"
    )
    parser.add_argument("--repetition_index", type=int, default=0, help="repetition index")
    parser.add_argument("--task_index", type=int, default=0, help="task index")
    parser.add_argument("--output_dir", type=str, default="./output/", help="output directory")
    args = parser.parse_args()

    args.direct_answer_trigger_for_fewshot = "The answer is"
    args.direct_answer_trigger_for_zeroshot = "The answer is"
    args.direct_answer_trigger_for_zeroshot_cot = "The answer is"
    args.cot_trigger = "Let's think step by step."

    return args