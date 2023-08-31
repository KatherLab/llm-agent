
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define functions for computing scores and plotting heatmaps
def compute_scores(scores_dict, gpt4_dict, metric=np.median):
    task_scores = {}
    model_scores = {}
    
    for summary_id, data in scores_dict.items():
        task_index = data['task_index']
        model_name = data['model']
        scores = data['scores']

        if task_index not in task_scores:
            task_scores[task_index] = {criterion: [] for criterion in scores.keys()}
        if model_name not in model_scores:
            model_scores[model_name] = {criterion: [] for criterion in scores.keys()}

        for criterion, score in scores.items():
            task_scores[task_index][criterion].append(score)
            model_scores[model_name][criterion].append(score)
    
    for task_index, scores in task_scores.items():
        for criterion, score_list in scores.items():
            task_scores[task_index][criterion] = metric(score_list)
    
    for model_name, scores in model_scores.items():
        for criterion, score_list in scores.items():
            model_scores[model_name][criterion] = metric(score_list)

    return task_scores, model_scores

def plot_heatmap_with_scaling(data, labels, title, ylabel, filename, vmin=5, vmax=10):
    df = pd.DataFrame([data[label] for label in labels], index=labels)
    plt.figure(figsize=(10, 10))
    sns.heatmap(df, annot=True, cmap='coolwarm', cbar_kws={'label': 'Score'}, vmin=vmin, vmax=vmax)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Connect to GPT4_summaries.db and fetch scores from it
conn = sqlite3.connect('GPT4_summaries.db')
cursor = conn.cursor()
cursor.execute("SELECT id, model, task_index, accuracy, relevance, novelty as creativity, specificity, feasibility FROM Summaries")
data = cursor.fetchall()
conn.close()

# Convert the fetched data to dictionaries for easier processing
scores_dict = {}
for entry in data:
    summary_id = entry[0]
    model = entry[1]
    task_index = entry[2]
    scores = {
        'accuracy': entry[3],
        'relevance': entry[4],
        'creativity': entry[5],
        'specificity': entry[6],
        'feasibility': entry[7]
    }
    scores_dict[summary_id] = {'model': model, 'task_index': task_index, 'scores': scores}

# Compute median scores and plot heatmaps using scores from GPT4_summaries.db
median_task_scores, median_model_scores = compute_scores(scores_dict, scores_dict, metric=np.median)
plot_heatmap_with_scaling(median_task_scores, sorted(median_task_scores.keys()), 'GPT4 Median Scores by Task', 'Task Index', 'gpt4_median_heatmap_by_task.png')
plot_heatmap_with_scaling(median_model_scores, sorted(median_model_scores.keys()), 'GPT4 Median Scores by Model', 'Model Name', 'gpt4_median_heatmap_by_model.png')
