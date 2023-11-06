import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connect to the databases
conn_summaries = sqlite3.connect('GPT4_summaries.db')
conn_scores = sqlite3.connect('scores.db')

# Fetch the data from the 'Summaries' table
summaries_data = pd.read_sql_query("SELECT * FROM Summaries", conn_summaries)

# Fetch the data from the 'score' table
scores_data = pd.read_sql_query("SELECT * FROM score", conn_scores)

# Merge the tables on 'id' from Summaries and 'summary_id' from score
merged_data = pd.merge(summaries_data, scores_data, left_on='id', right_on='summary_id')

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

# Pivot the aggregated data for the heatmap
pivot_table_agg = heatmap_agg.melt(id_vars=['model'], var_name='category', value_name='score_difference')
pivot_table_agg = pivot_table_agg.pivot("model", "category", "score_difference")
pivot_table_agg = pivot_table_agg[['accuracy_diff', 'relevance_diff', 'creativity_diff', 'specificity_diff', 'feasibility_diff']]  # ordering

# Create a heatmap from the pivot table
plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(pivot_table_agg, annot=True, fmt=".2f", cmap='vlag', linewidths=.5)
plt.title('Heatmap of Score Differences (GPT-4 Score - Human Expert Score)')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()

# Close database connections
conn_summaries.close()
conn_scores.close()
