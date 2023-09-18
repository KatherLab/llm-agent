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
merged_df.drop(columns=['eu_prompt', 'repetition_index', 'truncation_index', 'table_index', 'file_path', 'summary', 'main_ideas', 'timestamp'], inplace=True)

# Display the first few rows of the merged dataframe
#print(merged_df.head())

# List of rating categories to adjust
rating_categories = ['accuracy', 'relevance', 'creativity', 'specificity', 'feasibility', 'red_flags']

# For each rating category, adjust the score by subtracting the mean score for each subgroup
for category in rating_categories:
    # Calculate the mean for each subgroup
    means = merged_df.groupby(['model', 'author'])[category].transform('mean')

    # Adjust the score
    merged_df[f'{category}_adjusted'] = merged_df[category] - means

print(merged_df.head(100))
print(gpt4_df['task_index'].values)
def get_df_task(desired_task_index):
    # Filtering gpt4_df to get ids with the desired task index
    filtered_ids = gpt4_df[gpt4_df['task_index'] == desired_task_index]['id']
    print(filtered_ids.values)
    # Filtering merged_df based on these ids
    result_df = merged_df[merged_df['summary_id'].isin(filtered_ids)]
    print(result_df)
    return result_df

def generate_heatmap(df, score_column, title):
    """Generate a heatmap for the given score column."""
    # Create a pivot table with authors as rows, rating_categories as columns, and the average adjusted score as values
    table = df.pivot_table(index='author', columns='accuracy_adjusted', values=score_column, aggfunc='mean')
    # pivot_table = df.pivot_table(index='rating_categories', columns='author', values=score_column, aggfunc='mean')
    # print(pivot_table)
    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(table, annot=True, cmap="coolwarm", center=0, linewidths=.5, cbar_kws={"shrink": 0.75})
    plt.title(title)
    plt.tight_layout()
    plt.show()
import seaborn as sns
import matplotlib.pyplot as plt
for index in range(1, 11):
    new_merged_df = get_df_task(str(index))

    #save the dataframe to a csv file
    new_merged_df.to_csv(str(index)+'task.csv')
    data = pd.read_csv(str(index)+'task.csv')
    # Selecting columns with '_adjusted' in their names
    adjusted_cols = [col for col in data.columns if '_adjusted' in col]
    cols_of_interest = ['author'] + adjusted_cols

    # Group by author and compute the mean for the selected columns
    heatmap_data_adjusted = data[cols_of_interest].groupby('author').mean()

    # Plot the heatmap
    plt.figure(figsize=(14, 10))
    sns.heatmap(heatmap_data_adjusted, cmap='viridis', annot=True, vmin=-2, vmax=3)
    plt.title("Mean Adjusted Ratings by Author for task "+str(index))
    #save the heatmap to a svg file
    plt.savefig('adjusted_score_heatmap/'+str(index)+'task_adjusted_score_heatmap.svg')

    plt.show()
#for key in merged_df.keys():
    #if "_adjusted" in key:
        #print(key)
        ## Generate the heatmap for accuracy_adjusted scores
        #generate_heatmap(merged_df, key, key+'  Scores by Model and Reader')
