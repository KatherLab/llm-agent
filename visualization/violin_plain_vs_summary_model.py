import os
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
def extract_model_name_from_filename(filename):
    """Extract the model name from the filename using a regular expression."""
    match = re.search(r"onlyscore_(.*?)_", filename)
    if match:
        return match.group(1)
    else:
        return None

def updated_aggregate_scores(directory):
    """Aggregate scores with model names extracted from filenames."""
    files = find_md_files(directory)
    all_scores = []
    for file in files:
        scores = extract_scores_from_md(file)
        model_name = extract_model_name_from_filename(os.path.basename(file))
        scores["model"] = model_name
        all_scores.append(scores)
    return pd.DataFrame(all_scores)


# Step 1: Recursively find all markdown files
def find_md_files(directory):
    return [os.path.join(root, file) for root, dirs, files in os.walk(directory) for file in files if
            file.endswith('.md') and file.startswith('onlyscore')]


# Step 2: Parse each markdown file to extract scores
def extract_scores_from_md(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        content = content.split("\n", 2)[2]  # Skip the first and second lines
        lines = content.split("\n")
        scores = {}
        mapping = {
            "Factual accuracy": "accuracy",
            "Problem Solving / Relevance": "relevance",
            "Novelty / Creativity": "novelty",
            "Specificity": "specificity",
            "Feasibility": "feasibility"
        }
        for line in lines:
            if ':' in line:
                key, value = line.split(':')
                mapped_key = mapping.get(key.strip(), key.strip())
                scores[mapped_key] = float(value)
    return scores


# Step 3: Aggregate scores into a DataFrame
def aggregate_scores(directory):
    files = find_md_files(directory)
    all_scores = []
    for file in files:
        scores = extract_scores_from_md(file)
        all_scores.append(scores)
    return pd.DataFrame(all_scores)


# Connect to the Summaries database
conn_summaries = sqlite3.connect('/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db')
summaries_data = pd.read_sql_query("SELECT * FROM Summaries", conn_summaries)


# Plotting scores side-by-side in a combined plot
def combined_plot_side_by_side(directory):
    md_scores = aggregate_scores(directory)
    categories = ['accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']

    # Initialize a single figure with 5 subplots
    fig, axes = plt.subplots(1, 5, figsize=(25, 6), sharey=True)
    print()


    for i, category in enumerate(categories):
        sns.kdeplot(data=md_scores, x=category, ax=axes[i], label="MD Files", shade=True)
        sns.kdeplot(data=summaries_data, x=category, ax=axes[i], label="Summaries Table", shade=True)

        axes[i].set_title(f"{category.capitalize()} Scores")
        axes[i].set_xlabel(category.capitalize())
        if i == 0:  # Only set the ylabel for the first subplot to avoid repetition
            axes[i].set_ylabel("Density")
        axes[i].legend()

    plt.tight_layout()
    plt.show()

categories = ['accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']

def combined_violin_plot(directory):
    # Get scores from markdown files
    md_scores = aggregate_scores(directory)
    print(md_scores)
    md_scores["source"] = "llm-agents plain output"

    # Select relevant columns from summaries_data and rename them to match md_scores
    summaries_scores = summaries_data[
        ['model', 'accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']].copy()
    summaries_scores["source"] = "GPT4 generated Summaries"

    # Combine the scores
    combined_scores = pd.concat([md_scores, summaries_scores], ignore_index=True)
    combined_melted = combined_scores.melt(id_vars=['source', 'model'], value_vars=categories,
                                           var_name='category', value_name='score')

    # Plot
    plt.figure(figsize=(18, 8))
    sns.violinplot(data=combined_melted, x="model", y="score", hue="source", split=True, inner="quartile", cut=0)
    plt.title("Comparison of Scores: llm-agents plain output vs. GPT4 generated Summaries")
    plt.ylabel("Score")
    plt.xlabel("Model/llm-agent Name")
    plt.xticks(rotation=45)
    plt.legend(title="Score Source")
    plt.tight_layout()
    plt.show()


def combined_violin_plot(directory):
    # Use the updated_aggregate_scores function
    md_scores = updated_aggregate_scores(directory)
    md_scores["source"] = "llm-agents plain output"

    summaries_scores = summaries_data[
        ['model', 'accuracy', 'relevance', 'novelty', 'specificity', 'feasibility']].copy()
    summaries_scores["source"] = "GPT4 generated Summaries"
    # print the difference between md_scores and summaries_data with statistics
    print(md_scores.describe())
    #save the difference between md_scores and summaries_data with statistics
    md_scores.describe().to_csv('md_scores.csv')
    print(summaries_scores.describe())
    summaries_scores.describe().to_csv('summaries_scores.csv')
    combined_scores = pd.concat([md_scores, summaries_scores], ignore_index=True)
    combined_melted = combined_scores.melt(id_vars=['source', 'model'], value_vars=categories,
                                           var_name='category', value_name='score')

    plt.figure(figsize=(18, 8))
    sns.violinplot(data=combined_melted, x="model", y="score", hue="source", split=True, inner="quartile", cut=0)
    plt.title("Comparison of Scores: llm-agents plain output vs. GPT4 generated Summaries")
    plt.ylabel("Score")
    plt.xlabel("Model/llm-agent Name")
    plt.xticks(rotation=45)
    plt.legend(title="Score Source")
    plt.tight_layout()
    plt.show()


# Call the combined violin plot function
combined_violin_plot('/home/jeff/PycharmProjects/llm-agent/generator/results')

