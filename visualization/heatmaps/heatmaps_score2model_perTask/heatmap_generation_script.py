
import sqlite3
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Define the path to scores.db
scores_db_path = "/home/jeff/PycharmProjects/llm-agent/webui/scores.db"
gpt4_db_path = "/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db"

# Fetch the data from scores.db
conn = sqlite3.connect(scores_db_path)
cursor = conn.cursor()
cursor.execute("SELECT summary_id, author, accuracy, relevance, creativity, specificity, feasibility FROM score")
scores_data = cursor.fetchall()
conn.close()

# Fetch the model names and task indices from GPT4_summaries.db
conn = sqlite3.connect(gpt4_db_path)
cursor = conn.cursor()
cursor.execute("SELECT id, model, task_index FROM Summaries")
gpt4_data = cursor.fetchall()
conn.close()

# Convert fetched data into dictionaries for easy lookup
gpt4_dict = {entry[0]: {"model": entry[1], "task_index": int(entry[2])} for entry in gpt4_data}
scores_dict = {}
for entry in scores_data:
    summary_id = entry[0]
    if summary_id not in scores_dict:
        scores_dict[summary_id] = []
    scores_dict[summary_id].append({
        "author": entry[1],
        "accuracy": entry[2],
        "relevance": entry[3],
        "creativity": entry[4],
        "specificity": entry[5],
        "feasibility": entry[6]
    })

# Extract unique model names for the x-axis
model_names = sorted(list(set([data['model'] for data in gpt4_dict.values()])))

# Extract unique author names for the y-axis
author_labels = sorted(list(set([score['author'] for scores in scores_dict.values() for score in scores])))

score_labels = ["accuracy", "relevance", "creativity", "specificity", "feasibility"]

# Function to calculate the median score for all the authors for a given model on a given task
def calculate_median_score_for_model(model, task_index, score_label):
    # Filter scores by model and task index
    filtered_scores = {k: v for k, v in scores_dict.items() if gpt4_dict[k]["model"] == model and gpt4_dict[k]["task_index"] == task_index}

    # Extract the accuracy scores for all the authors
    score = [score[score_label] for scores in filtered_scores.values() for score in scores]

    # Return the median accuracy score
    return np.median(score)

# Function to generate a DataFrame for heatmap plotting
def generate_dataframe_for_heatmap(task_index):
    # Filter scores by task index

    # Initialize an empty DataFrame with score_label as rows and models as columns
    df = pd.DataFrame(0, index=score_labels, columns=model_names)
    
    # Populate the DataFrame with median scores for each score-model combination
    for model in model_names:
        for score_label in score_labels:
            df.at[score_label, model] = calculate_median_score_for_model(model, task_index, score_label)

    '''
    for summary_id, scores in filtered_scores.items():
        model = gpt4_dict[summary_id]["model"]
        for score in scores:
            author = score["author"]
            accuracy = score["accuracy"]
            # Update the DataFrame
            df.at[author, model] = accuracy
    '''
    print(df.head(10))

    return df
# Function to plot the heatmap for a given task,
# Function to plot the heatmap for a given task
def plot_individual_heatmap(task_index):
    df = generate_dataframe_for_heatmap(task_index)
    plt.figure(figsize=(12, 8))
    sns.heatmap(df, annot=True, cmap='coolwarm', cbar_kws={'label': 'Median Score'}, vmin=2, vmax=10)
    plt.title(f'Median Scores for Task {task_index}')
    plt.ylabel('Score Label')
    plt.xlabel('Model Name')
    plt.tight_layout()
    plot_path = f'task_{task_index}_heatmap.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# Generate and save heatmaps for each task
heatmap_paths = [plot_individual_heatmap(i) for i in range(1, 11)]

# Open the heatmaps and combine them into a single image
imgs = [Image.open(path) for path in heatmap_paths]
min_img_width = min(img.width for img in imgs)
total_height = sum(img.height for img in imgs)
combined_img = Image.new('RGB', (min_img_width, total_height))
y_offset = 0
for img in imgs:
    combined_img.paste(img, (0, y_offset))
    y_offset += img.height
combined_img.save('combined_heatmap.png')
