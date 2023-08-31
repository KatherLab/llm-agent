
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define functions for computing scores and plotting heatmaps (already defined above)

# Connect to scores.db and fetch scores from it
conn = sqlite3.connect('scores.db')
cursor = conn.cursor()
cursor.execute("SELECT summary_id, accuracy, relevance, creativity, specificity, feasibility FROM Scores")
scores_data = cursor.fetchall()
cursor.execute("SELECT id, model, task_index FROM Summaries")
gpt4_data = cursor.fetchall()
conn.close()

# Convert the fetched data to dictionaries for easier processing
scores_dict = {}
for entry in scores_data:
    summary_id = entry[0]
    scores = {
        'accuracy': entry[1],
        'relevance': entry[2],
        'creativity': entry[3],
        'specificity': entry[4],
        'feasibility': entry[5]
    }
    if summary_id not in scores_dict:
        scores_dict[summary_id] = [scores]
    else:
        scores_dict[summary_id].append(scores)

gpt4_dict = {entry[0]: {'model': entry[1], 'task_index': entry[2]} for entry in gpt4_data}

# Compute median scores and plot heatmaps using scores from scores.db
median_task_scores, median_model_scores = compute_scores(scores_dict, gpt4_dict, metric=np.median)
plot_heatmap_with_scaling(median_task_scores, sorted(median_task_scores.keys()), 'Median Scores by Task (from scores.db)', 'Task Index', 'median_heatmap_by_task.png')
plot_heatmap_with_scaling(median_model_scores, sorted(median_model_scores.keys()), 'Median Scores by Model (from scores.db)', 'Model Name', 'median_heatmap_by_model.png')
