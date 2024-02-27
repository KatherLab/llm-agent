import sqlite3

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the databases
conn_summaries = sqlite3.connect('/home/jeff/PycharmProjects/llm-agent/webui/GPT4_summaries.db')
conn_scores = sqlite3.connect('/home/jeff/PycharmProjects/llm-agent/webui/scores.db')

# Fetch the data from the 'Summaries' table
summaries_data = pd.read_sql_query("SELECT * FROM Summaries", conn_summaries)

# Fetch the data from the 'score' table
scores_data = pd.read_sql_query("SELECT * FROM score", conn_scores)

# Merge the tables on 'id' from Summaries and 'summary_id' from score
merged_data = pd.merge(summaries_data, scores_data, left_on='id', right_on='summary_id')

# Model renaming
model_renames = {
    "gpt-3.5-turbo": "gpt-3.5",
    "cot-gpt-4-zero-shot-cot": "cot-zero",
    "cot-gpt-4-manual-cot": "cot-manual",
    "llama-2-7b-chat": "llama2",
    "camel-gpt4": "camel",
    "babyagi-gpt-4": "babyagi"
}
merged_data['model'] = merged_data['model'].replace(model_renames)

# Subtract the human expert score from the GPT-4 score for each category
merged_data['accuracy_diff'] = merged_data['accuracy_x'] - merged_data['accuracy_y']
merged_data['relevance_diff'] = merged_data['relevance_x'] - merged_data['relevance_y']
merged_data['creativity_diff'] = merged_data['novelty'] - merged_data['creativity']
merged_data['specificity_diff'] = merged_data['specificity_x'] - merged_data['specificity_y']
merged_data['feasibility_diff'] = merged_data['feasibility_x'] - merged_data['feasibility_y']

# Selecting only the necessary columns for the heatmap
heatmap_data = merged_data[['model', 'accuracy_diff', 'relevance_diff', 'creativity_diff', 'specificity_diff', 'feasibility_diff']]

# Aggregate the data by taking the mean of the score differences for each model
heatmap_agg = heatmap_data.groupby('model').mean().reset_index()

# Melt the aggregated data to prepare for pivoting
pivot_data = heatmap_agg.melt(id_vars=['model'], var_name='category', value_name='score_difference')

# Pivot the melted data for the heatmap
pivot_table_agg = pivot_data.pivot(index='model', columns='category', values='score_difference')
pivot_table_agg = pivot_table_agg[['accuracy_diff', 'relevance_diff', 'creativity_diff', 'specificity_diff', 'feasibility_diff']]  # ordering

# Create a heatmap from the pivot table
plt.figure(figsize=(12, 8))
heatmap = sns.heatmap(pivot_table_agg, annot=True, fmt=".2f", cmap='Blues', vmin=0, vmax=5, linewidths=.5)
# Set an explicit and descriptive title
plt.title('Differences in GPT-4 vs. Human Expert Ratings Across Models', fontsize=18, pad=20)

# Set more descriptive axis labels
plt.xlabel('Rating Categories', fontsize=15, color='black', labelpad=15, fontweight='normal', fontname='DejaVu Sans')
plt.ylabel('LLM Model', fontsize=15, color='black', labelpad=15, fontweight='normal', fontname='DejaVu Sans')

# Set x-axis labels directly with the names of the categories, ensuring clarity about what the scores represent
categories = ['Accuracy ', 'Relevance ', 'Creativity ', 'Specificity ', 'Feasibility ']
#plt.xticks(ticks=np.arange(len(categories)), labels=categories, ha="left")
plt.xlabel('Score Difference', fontsize=15, color='black', labelpad=15, fontweight='normal', fontname='DejaVu Sans')


# Add a legend or a color bar label to clarify what the numbers mean
heatmap.figure.colorbar(heatmap.collections[0]).set_label('Score Difference (GPT-4 - Human Expert)', rotation=270, labelpad=20)


plt.show()

# Close database connections
conn_summaries.close()
conn_scores.close()
