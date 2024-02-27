import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

from scipy.stats import stats


def extract_model_and_task_from_filename(filename):
    """Extract the model name and task name from the filename using regular expressions."""
    model_match = re.search(r"onlyscore_(.*?)_", filename)
    task_match = re.search(r"_trunc-\d+_(\d+)_\d+\.md", filename)

    model_name = model_match.group(1) if model_match else None
    task_name = task_match.group(1) if task_match else None

    return model_name, task_name


def find_md_files(directory):
    return [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files if
            file.endswith('.md') and file.startswith('onlyscore')]


def extract_scores_from_md(file_path):
    with open(file_path, 'r') as file:
        content = file.read().split("\n", 2)[2]
        lines = content.split("\n")
        scores = {}
        mapping = {"Factual accuracy": "accuracy", "Problem Solving / Relevance": "relevance",
                   "Novelty / Creativity": "novelty", "Specificity": "specificity", "Feasibility": "feasibility"}
        for line in lines:
            if ':' in line:
                key, value = line.split(':')
                scores[mapping[key.strip()]] = float(value)
    return scores


def updated_aggregate_scores(directory):
    files = find_md_files(directory)
    all_scores = []
    for file in files:
        model_name, task_name = extract_model_and_task_from_filename(os.path.basename(file))
        scores = extract_scores_from_md(file)
        scores["model"] = model_name
        scores["task_index"] = int(task_name)  # Convert task name to integer
        all_scores.append(scores)
    return pd.DataFrame(all_scores)


# Connect to the Summaries database
conn_summaries = sqlite3.connect('/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db')
summaries_data = pd.read_sql_query("SELECT * FROM Summaries", conn_summaries)

categories = ['accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']


def combined_violin_plot_by_taskindex(directory):
    md_scores = updated_aggregate_scores(directory)
    md_scores["source"] = "LLM-agents plain output"

    summaries_scores = summaries_data[
        ['task_index', 'model', 'accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']].copy()
    summaries_scores["source"] = "GPT-4 generated Summaries"
    summaries_scores["task_index"] = summaries_scores["task_index"].astype(int)

    combined_scores = pd.concat([md_scores, summaries_scores], ignore_index=True)
    combined_scores = combined_scores.sort_values(by='task_index')  # Sort by task_index
    combined_melted = combined_scores.melt(id_vars=['source', 'task_index'], value_vars=categories, var_name='category',
                                           value_name='score')

    plt.figure(figsize=(18, 8))
    sns.set(style="whitegrid", font_scale=2)  # Increase font scale

    # Define color palette
    colorblind_palette = sns.color_palette("colorblind")
    palette = {"LLM-agents plain output": colorblind_palette[0], "GPT-4 generated Summaries": colorblind_palette[1]}

    ax = sns.violinplot(data=combined_melted, x="task_index", y="score", hue="source", split=True, inner="quartile",
                        cut=0, palette=palette)  # Use custom palette

    # Customize plot elements
    ax.set_xlabel("Task Index", fontsize=28, color='black', labelpad=20, fontweight='normal', fontname='Arial')
    ax.set_ylabel("Score", fontsize=28, color='black', labelpad=10, fontweight='normal', fontname='Arial')
    ax.set_xticklabels(sorted(combined_melted['task_index'].unique()))  # Order Task Index labels

    # Move legend to bottom right and fix the order of the legend
    handles, labels = ax.get_legend_handles_labels()
    order = ['LLM-agents plain output', 'GPT-4 generated Summaries']
    plt.legend([handles[labels.index(i)] for i in order], order, title="Score Source", loc='lower right', bbox_to_anchor=(1.0, 0.0))
    plt.tight_layout()
    plt.show()


def combined_violin_plot_by_metric(directory):
    md_scores = updated_aggregate_scores(directory)
    md_scores["source"] = "LLM-agents plain output"

    summaries_scores = summaries_data[
        ['task_index', 'model', 'accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']].copy()
    summaries_scores["source"] = "GPT-4 generated Summaries"
    summaries_scores["task_index"] = summaries_scores["task_index"].astype(int)

    combined_scores = pd.concat([md_scores, summaries_scores], ignore_index=True)
    combined_melted = combined_scores.melt(id_vars=['source', 'task_index'], value_vars=categories, var_name='category',
                                           value_name='score')

    plt.figure(figsize=(18, 8))
    sns.set(style="whitegrid", font_scale=2)  # Increase font scale
    ax = sns.violinplot(data=combined_melted, x="category", y="score", hue="source", split=True, inner="quartile",
                        cut=0, palette="colorblind")  # Colorblind-friendly palette

    # Customize plot elements
    #ax.set_title("Comparison of Scores by Metric")
    ax.set_xlabel("Metric", fontsize=28, color='black', labelpad=20, fontweight='normal', fontname='Arial')
    ax.set_ylabel("Score", fontsize=28, color='black', labelpad=10, fontweight='normal', fontname='Arial')
    ax.set_xticklabels(
        [label.capitalize() for label in combined_melted['category'].unique()])  # Capitalize first letter
    # Move legend to bottom right and fix the order of the legend
    handles, labels = ax.get_legend_handles_labels()
    order = ['LLM-agents plain output', 'GPT-4 generated Summaries']
    plt.legend([handles[labels.index(i)] for i in order], order, title="Score Source", loc='lower right', bbox_to_anchor=(1.0, 0.0))
    # print the scores for gp4 and llm-agents
    print("GPT4 generated Summaries")
    #print(summaries_scores)
    print("llm-agents plain output")
    #print(md_scores)
    # calculate the p value for each metric
    for metric in combined_melted['category'].unique():
        print("Metric: " + metric)
        print("p value: " + str(stats.ttest_ind(combined_melted.loc[(combined_melted['source'] == 'GPT4 generated Summaries') & (combined_melted['category'] == metric), 'score'],
                                                 combined_melted.loc[(combined_melted['source'] == 'llm-agents plain output') & (combined_melted['category'] == metric), 'score'])[1]))
    # calculate a overall p value
    print("Overall p value: " + str(stats.ttest_ind(combined_melted.loc[(combined_melted['source'] == 'GPT4 generated Summaries'), 'score'],
                                                 combined_melted.loc[(combined_melted['source'] == 'llm-agents plain output'), 'score'])[1]))


    plt.tight_layout()
    plt.show()


# Call the function
combined_violin_plot_by_metric('/home/jeff/PycharmProjects/llm-agent/generator/results')
