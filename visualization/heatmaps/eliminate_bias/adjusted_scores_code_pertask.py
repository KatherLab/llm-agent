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

import sqlite3
import pandas as pd

# Fetch the data from scores.db again
conn_scores = sqlite3.connect(scores_db_path)
scores_df = pd.read_sql_query("SELECT * FROM score", conn_scores)
conn_scores.close()

# Fetch the data from GPT4_summaries.db again
conn_gpt4 = sqlite3.connect(gpt4_db_path)
gpt4_df = pd.read_sql_query("SELECT * FROM Summaries", conn_gpt4)
conn_gpt4.close()

#print("!!!!!!!!!!")


# Display the first few rows of each dataframe for an overview
#print(scores_df.head())
#print(gpt4_df.head())
# Merge the scores dataframe with the GPT4 dataframe on the summary_id column
merged_df = pd.merge(scores_df, gpt4_df, left_on='summary_id', right_on='id', suffixes=('', '_summary'))

# Drop unnecessary columns from the merged dataframe
merged_df.drop(columns=['id_summary', 'eu_prompt', 'repetition_index', 'truncation_index', 'table_index', 'file_path', 'summary', 'main_ideas', 'timestamp', 'red_flags'], inplace=True)

# Display the first few rows of the merged dataframe
#print(merged_df.head())

# List of rating categories to adjust
rating_categories = ['accuracy', 'relevance', 'creativity', 'specificity', 'feasibility']

# For each rating category, adjust the score by subtracting the mean score for each subgroup
for category in rating_categories:
    # Calculate the mean for each subgroup
    means = merged_df.groupby(['model', 'author'])[category].transform('mean')

    # Adjust the score
    merged_df[f'{category}_adjusted'] = merged_df[category] - means

# Display the first few rows of the dataframe after adjustment
print(merged_df.head(100))
# print accuracy_adjusted
#print(merged_df['feasibility_adjusted'])
import seaborn as sns
import matplotlib.pyplot as plt


# Convert fetched data into dictionaries for easy lookup
gpt4_dict = {entry[0]: {"model": entry[1], "task_index": int(entry[2])} for entry in gpt4_df}
scores_dict = {}
for entry in scores_df:
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
# Function to generate a DataFrame for heatmap plotting
def generate_dataframe_for_heatmap(task_index):
    # Filter scores by task index
    filtered_scores = {k: v for k, v in scores_dict.items() if gpt4_dict[k]["task_index"] == task_index}

    # Initialize an empty DataFrame with authors as rows and models as columns
    df = pd.DataFrame(0, index=author_labels, columns=model_names)

    # Populate the DataFrame with median scores for each author-model combination
    for summary_id, scores in filtered_scores.items():
        model = gpt4_dict[summary_id]["model"]
        for score in scores:
            author = score["author"]
            accuracy = score["accuracy"]
            # Update the DataFrame
            df.at[author, model] = accuracy

    return df

print("+_+_+_+")
print(generate_dataframe_for_heatmap(0))
def generate_heatmap(df, task_index, title):
    """Generate a heatmap for the given score column."""
    # Create a pivot table with models as rows, authors as columns, and the average adjusted score as values
    pivot_table = df.pivot_table(index='author', columns='author', values=score_column)
    #print(pivot_table)
    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, annot=True, cmap="coolwarm", center=0, linewidths=.5, cbar_kws={"shrink": 0.75})
    plt.title(title)
    plt.tight_layout()
    plt.show()

for key in merged_df.keys():
    if "_adjusted" in key:
        print(key)
        # Generate the heatmap for accuracy_adjusted scores
        generate_heatmap(merged_df, key, key+'  Scores by Model and Reader')
